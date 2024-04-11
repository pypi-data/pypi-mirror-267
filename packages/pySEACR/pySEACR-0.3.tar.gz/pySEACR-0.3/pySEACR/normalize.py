"""
Find normalization factors.
"""
import numpy as np
from scipy.stats import gaussian_kde, iqr
from scipy.signal import decimate

from sklearn.neighbors import KernelDensity

from pySEACR.utils import find_farthest, seq


class Normalize(object):
    """
    Find normalization factors.
    """

    def __init__(self, exp, ctrl):
        """
        Create a new Normalize object.

        Parameters:
            exp (BDG): Experimental/treatment data
            ctrl (BDG): Control/IgG data
        """
        self.exp = exp
        self.ctrl = ctrl


    def bw_nrd0(self, x):
        hi = np.std(x)
        lo = min(hi, iqr(x) / 1.34)
        if lo is None:
            if hi:
                lo = hi
            elif abs(x[0]):
                lo = abs(x[0])
            else:
                lo = 1
        return 0.9 * lo * len(x) ** -0.2

    def max_density(self, vec):
        """
        Estimate input for a kernel density function that has the largest output.

        Parameters:
            vec (collection): Data used to create the kde

        Returns:
            float
        """
        cutoff = find_farthest(vec)
        vec_min = min(vec)
        vec_range = cutoff - vec_min
        values = vec[vec <= cutoff]
        #if len(values) > 510:
            #step = len(values) / 510
            #values = values[[round(step * _) for _ in range(510)]]
            #start = values[0] - 300
            #end = values[-1] + 300
            #values = np.random.choice(values[1:-1], 512, replace=False)
            #values[0] = start
            #values[-1] = end
        #values = np.insert(values, 0, min(values) - 300)
        #values = np.append(values, max(values) + 300)
        kde = KernelDensity(kernel='gaussian', bandwidth=self.bw_nrd0(values)).fit(
            np.reshape(values, (-1, 1)),
        )
        inputs = kde.sample(512, random_state=412)
        densities = 10 ** np.reshape(
            kde.score_samples(inputs),
            (1, 512)
        )[0]
        y_max_index = np.argmax(densities)
        x_values = np.reshape(inputs, (1, 512))[0]
        return x_values[y_max_index]

    def constant(self):
        """
        Ratio kernel density inputs with the highest value.

        Creates a kernel density function for each argument, then finds the
        input for each kde with the highest output (estimated).

        Returns:
            float
        """
        return self.max_density(self.exp.vec) / self.max_density(self.ctrl.vec)
