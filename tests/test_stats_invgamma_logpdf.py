from __future__ import print_function
import numpy as np
import tensorflow as tf

from edward.stats import invgamma
from scipy import stats

sess = tf.Session()

def _assert_eq(val_ed, val_true):
    with sess.as_default():
        assert np.allclose(val_ed.eval(), val_true)

def _test_logpdf(x, a=0.5, scale=0.5):
    xtf = tf.constant(x)
    val_true = stats.invgamma.logpdf(x, a, scale=scale)
    _assert_eq(invgamma.logpdf(xtf, tf.constant(a), tf.constant(scale)), val_true)
    _assert_eq(invgamma.logpdf(xtf, tf.constant([a]), tf.constant(scale)), val_true)
    _assert_eq(invgamma.logpdf(xtf, tf.constant(a), tf.constant([scale])), val_true)
    _assert_eq(invgamma.logpdf(xtf, tf.constant([a]), tf.constant([scale])), val_true)

def test_logpdf_scalar():
    _test_logpdf(0.3)
    _test_logpdf(0.7)

    _test_logpdf(0.3, a=1.0, scale=1.0)
    _test_logpdf(0.7, a=1.0, scale=1.0)

    _test_logpdf(0.3, a=0.5, scale=5.0)
    _test_logpdf(0.7, a=0.5, scale=5.0)

    _test_logpdf(0.3, a=5.0, scale=0.5)
    _test_logpdf(0.7, a=5.0, scale=0.5)

def test_logpdf_1d():
    _test_logpdf([0.5, 1.2, 5.3, 8.7], a=0.5, scale=0.5)

def test_logpdf_2d():
    _test_logpdf(np.array([[0.5, 1.2, 5.3, 8.7],[0.5, 1.2, 5.3, 8.7]]),
                 a=0.5, scale=0.5)
