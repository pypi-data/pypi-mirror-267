from lazylinop import LazyLinOp, aslazylinop
import numpy as np


def average(op, axis=0, weights=None):
    """
    TODO
    """
#    from lazylinop.wip.basicops import mean
    lz_op = aslazylinop(op)
#    if weights is None:
#        return mean(lz_op, axis=axis, meth='ones')
    # TODO: ensure weights is a vector of proper shape

    def _matmat(lz_op, x, adj=False):
        nonlocal weights

        s = (lz_op.shape[1], 1) if axis == 1 else (1, lz_op.shape[0])
        if weights is None:
            weights = np.ones(s)
        else:
            weights = weights.reshape(s)

        sum_w = np.sum(weights)
        m, n = lz_op.shape
        if axis == 0:
            # whatever is lz_op
            # we can compare the costs
            # of going l2r or r2l
            p = x.shape[1] if x.ndim == 2 else x.shape[0]
            l2r_c = n * (m + p)
            r2l_c = m * p * (n + 1)
            if l2r_c < r2l_c:
                return 1 / sum_w * ((weights @ lz_op) @ x)
            else:  # r2l
                return 1 / sum_w * (weights @ (lz_op @ x))
        elif axis == 1:
            # from l2r because
            # weights @ x is an outer product
            # that might blow up
            # the memory space
            return 1 / sum_w * ((lz_op @ weights) @ x)

    if axis == 1:
        out_shape = (lz_op.shape[0], 1)
    elif axis == 0:
        out_shape = (1, lz_op.shape[1])
    else:
        raise ValueError("axis must be 0 or 1")
    return LazyLinOp(out_shape, matmat=lambda x: _matmat(lz_op, x),
                     rmatmat=lambda x: _matmat(lz_op.H, x, adj=True))
