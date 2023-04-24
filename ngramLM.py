import numpy as np
import pandas as pd
import unigramLM

class NGramLM(object):
    
    def __init__(self, N, tokens):
        # You don't need to edit the constructor,
        # but you should understand how it works!
        
        self.N = N

        ngrams = self.create_ngrams(tokens)

        self.ngrams = ngrams
        self.mdl = self.train(ngrams)

        if N < 2:
            raise Exception('N must be greater than 1')
        elif N == 2:
            self.prev_mdl = UnigramLM(tokens)
        else:
            self.prev_mdl = NGramLM(N-1, tokens)

    def create_ngrams(self, tokens):
        index = 0
        out_list = []
        while index + self.N <= len(tokens): 
            out_list.append(tuple((tokens[index:index+self.N])))
            index += 1
        return out_list 
        
    def train(self, ngrams):
        df = pd.DataFrame({'ngram': ngrams})
        df = df.assign(n1gram = pd.Series(df['ngram']).str[:self.N - 1])
        ngram_valcounts = pd.Series(df['ngram']).value_counts()
        n1gram_valuecounts = pd.Series(df['ngram']).str[:self.N - 1].value_counts()
        new_ser = ngram_valcounts[df['ngram']].values / n1gram_valuecounts[df['n1gram']].values
        df = df.assign(prob = new_ser)
        return df
    
    def probability(self, words):
        prob = 1
        ngram_strs = []
        left = 0
        for right in range(len(words)):
            if right == 0:
                ngram_strs.append(tuple([words[right]]))
            elif right + 1 <= self.N:
                ngram_strs.append(tuple(words[left:right+1]))
            else:
                left +=1
                ngram_strs.append(tuple(words[left:right+1]))
        
        pr_mdl = self.prev_mdl
        word_group_i = len(ngram_strs) - 1
        try:
            while word_group_i >= 0:
                word_group = ngram_strs[word_group_i]
                if word_group_i == 0:
                    prob *= pr_mdl.mdl.loc[word_group]
                elif word_group_i + 1 < self.N:
                    prob *= pr_mdl.mdl[pr_mdl.mdl['ngram'] == word_group]['prob'].iloc[0]
                    pr_mdl = pr_mdl.prev_mdl
                else:
                    prob *= self.mdl[self.mdl['ngram'] == word_group]['prob'].iloc[0]
                word_group_i -= 1
        except IndexError:
            prob = 0.0
        return prob
    
    
    def sample(self, M):
        result = []
        result.append('\x02')
  
        df = pd.DataFrame(self.mdl)
        pr_mdl = self.prev_mdl
    
        i = self.N
        while not isinstance(pr_mdl, UnigramLM):
            df = df.merge(pr_mdl.mdl, left_index = True, right_index = True, suffixes = (str(i), str(i-1)))
            i -= 1
            pr_mdl = pr_mdl.prev_mdl
            
        df = df[df.columns.drop(list(df.filter(regex = 'n1gram')))]
        df = df.rename(columns = {'ngram':'ngram2', 'prob':'prob2'})
        gram_i = 2
        counter = 0 
        for i in range(M-1):
            if i < self.N - 1:
                last_tokens = result[:]
            else:
                counter += 1
                last_tokens = result[-(self.N-1):]
            
            print('previous tokens:',last_tokens)
            df_with_token = df[df[f'ngram{gram_i}'].apply(lambda t: all([g[0] == g[1] for g in zip(last_tokens, t)]))]
            
            try:
                df_with_token = df_with_token.groupby(f'ngram{gram_i}').mean(f'prob{gram_i}')
                df_with_token = df_with_token.reset_index()
                vals = df_with_token[f'ngram{gram_i}']
                probs = df_with_token[f'prob{gram_i}']
                probs = np.array(probs / probs.sum())

                choice = np.random.choice(vals, p = probs)
            except ValueError:
                choice = '\x03'
            result.append(choice[-1])
            gram_i += 1
            gram_i = min(gram_i, self.N)
        result.append('\x03')
        
        return ' '.join(result)
            
            
            
        