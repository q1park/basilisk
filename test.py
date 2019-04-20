import unittest
from basilisk import Node, BN
import numpy as np
import pandas as pd

class Test_Basilisk(unittest.TestCase):

    def setUp(self):
        """construct a simple bayesian network.
        """
        B = Node("B")
        A = Node("A", [B])
        C = Node("C", [A])
        T = Node("T")
        self.R = Node("R", [C, T])
        S = Node("S", [C])
        self.W = Node("W", [self.R, S])  # leaf node
        ls_nodes = [B, A, C, T, self.R, self.W, S]
        self.model = BN(ls_nodes)

    def test_scheduler(self):
        """a topological sort returns a list of nodes, which represents the 
        order of execution.
        """

        correct_sequence = ['B', 'A', 'T', 'C', 'S', 'R', 'W']
        
        # returns a list of nodes
        computed_sequence = self.model.scheduler(self.W)  
        
        # convert to list of node names
        computed_sequence = list(map(lambda x: x.name, computed_sequence))  

        self.assertEqual(correct_sequence, computed_sequence)

    def test_sample(self):
        """assert distribution from directly sampling nodes matches distribution
        from joint observations.
        """

        # construct a new graph
        C = Node("cloudy")
        R = Node("rain", [C])
        S = Node("sprinkler", [C])
        W = Node("wet", [R, S])
        ls_n = [C, R, S, W]
        model = BN(ls_n)
        obs = pd.read_csv("data/observations.csv").drop("Unnamed: 0", axis=1)
        model.fit(obs)  

        k = 1000
        
        samples = R.sample(parent_states=["cloudy==True"], num_samples=k)
        count = [r is True for r in samples]
        self.assertAlmostEqual(np.sum(count)/k, .78, places=1)

if __name__ == "__main__":
    unittest.main()