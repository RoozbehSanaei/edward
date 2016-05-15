from __future__ import print_function
import numpy as np
import tensorflow as tf

from edward.stats import multinomial
from scipy.special import gammaln

sess = tf.Session()

def multinomial_logpmf(x, n, p):
    """
    Arguments
    ----------
    x: np.array
        vector of length K, where x[i] is the number of outcomes
        in the ith bucket
    n: int
        number of outcomes equal to sum x[i]
    p: np.array
        vector of probabilities summing to 1
    """
    return gammaln(n + 1.0) - \
           np.sum(gammaln(x + 1.0)) + \
           np.sum(x * np.log(p))

def multinomial_logpmf_vec(x, n, p):
    if len(x.shape) == 1:
        return multinomial_logpmf(x, n, p)
    else:
        n_minibatch = x.shape[0]
        return np.array([multinomial_logpmf(x[i, :], n, p)
                         for i in xrange(n_minibatch)])

def _assert_eq(val_ed, val_true):
    with sess.as_default():
        assert np.allclose(val_ed.eval(), val_true)

def _test_logpmf(x, n, p):
    xtf = tf.constant(x)
    val_true = multinomial_logpmf_vec(x, n, p)
    _assert_eq(multinomial.logpmf(xtf, n, p),
               val_true)
    _assert_eq(multinomial.logpmf(xtf, n, tf.constant(p, dtype=tf.float32)),
               val_true)
    _assert_eq(multinomial.logpmf(xtf, n, p),
               val_true)
    _assert_eq(multinomial.logpmf(xtf, n, tf.constant(p, dtype=tf.float32)),
               val_true)

def test_logpmf_int_1d():
    _test_logpmf(np.array([0, 1]), 1, np.array([0.5, 0.5]))
    _test_logpmf(np.array([1, 0]), 1, np.array([0.75, 0.25]))

def test_logpmf_float_1d():
    _test_logpmf(np.array([0.0, 1.0]), 1, np.array([0.5, 0.5]))
    _test_logpmf(np.array([1.0, 0.0]), 1, np.array([0.75, 0.25]))

def test_logpmf_int_2d():
    _test_logpmf(np.array([[0, 1],[1, 0]]), 1, np.array([0.5, 0.5]))
    _test_logpmf(np.array([[1, 0],[0, 1]]), 1, np.array([0.75, 0.25]))

def test_logpmf_float_2d():
    _test_logpmf(np.array([[0.0, 1.0],[1.0, 0.0]]), 1, np.array([0.5, 0.5]))
    _test_logpmf(np.array([[1.0, 0.0],[0.0, 1.0]]), 1, np.array([0.75, 0.25]))
