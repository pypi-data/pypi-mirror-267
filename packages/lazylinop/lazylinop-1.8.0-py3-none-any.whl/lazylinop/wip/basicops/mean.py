from lazylinop import ones, aslazylinop


def mean(op, axis=0, meth='ones'):
    """
    TODO
    """
    from lazylinop.wip.basicops import average
    lz_op = aslazylinop(op)
    m, n = lz_op.shape
    ve_axis = ValueError("axis must be 0 or 1")
    if meth == 'ones':
        if axis == 0:
            return 1 / m * (ones((1, m)) @ lz_op)
        elif axis == 1:
            return 1 / n * (lz_op @ ones((n, 1)))
        else:
            raise ve_axis
    elif meth == 'avg':
        return average(lz_op, axis=axis)
    else:
        raise ValueError('Unknown meth')
