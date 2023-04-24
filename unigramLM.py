import numpy as np
import pandas as pd

class UnigramLM(object):
    def __init__(self, tokens):

        self.mdl = self.train(tokens)
    
    def train(self, tokens):
        counts = pd.Series(tokens).value_counts()
        return pd.Series(tokens).value_counts() / counts.sum()
    
    def probability(self, words):
        total_probability = 1
        for word in words:
            total_probability *= self.mdl.get(word, 0)
        return total_probability
        
    def sample(self, M):
        return ' '.join(list(np.random.choice(self.mdl.index, p = self.mdl.values, size = M)))