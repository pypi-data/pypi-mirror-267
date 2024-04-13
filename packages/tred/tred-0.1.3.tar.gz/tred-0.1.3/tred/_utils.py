"""Miscallaneous utilities"""


from numbers import Real
import numpy as np


class RealNotInt(Real):
    """A type that represents non-integer real numbers.

    [CAN IGNORE]: For internal parameter validation, inspired by sklearn practices.
    [COPIED] From sklearn/utils/_param_validation.py

    Behaves like float, but also works with values extracted from numpy arrays.
    isintance(1, RealNotInt) -> False
    isinstance(1.0, RealNotInt) -> True
    """


RealNotInt.register(float)


def display_tensor_facewise(tens):
    """By default Numpy prints order-3 arrays as vertical stacks of order-2 arrays, in
    line with their broadcasting rules. This function prints a transpose view so the
    print output is a more intuitive sequence of frontal slices. We often use this in
    notebooks. It also prints the rounded values.

    UPDATE: Also works for matrices and vectors now.

    Parameters
    ----------
        tens : ndarray of shape (n, p, t)
            Order-3 tensor representation

    Examples
    --------
    >>> import numpy as np
    >>> from tdim import display_tensor_facewise as disp
    >>> test = np.eye(3)[:, :, None] # a 3x3x1 tensor
    >>> print(test) # Numpy ndarrays default __str__ method is not intuitive here
    [[[1.]
    [0.]
    [0.]]
    [[0.]
    [1.]
    [0.]]
    [[0.]
    [0.]
    [1.]]]
    >>> disp(test)
    Tensor with dimensions (3, 3, 1)
    [[[1. 0. 0.]
    [0. 1. 0.]
    [0. 0. 1.]]]
    """
    assert len(tens.shape) in (
        1,  # vector
        2,  # matrix
        3,  # tensor
    ), "Expecting 1D (vector), 2D (matrix) or 3D (tensor) input"

    if len(tens.shape) == 3:
        print(f"Tensor with shape {tens.shape}")
        print(tens.transpose(2, 0, 1).round(6))
    else:
        if len(tens.shape) == 2:
            print(f"Matrix with shape {tens.shape}")
        else:
            print(f"Vector with length {tens.shape}")
        print(tens.round(5))


def _singular_vals_mat_to_tensor(mat, n, p, t):
    """Decompress $k \times t$ matrix of singular values into $\hat{S}$ from literature.

    NOTE: There's probably a cool numpy way to do this without the for loop...but for now
    it works fine as $t$ is usually modest for the data we work with

    Parameters
    ----------
        mat : ndarray of shape (k, t_)
            $k \times t_$ matrix representation, the function checks if `t_ == t`

        n : int
            first dimension of output tensor

        p : int
            second dimension of output tensor

        t : int
            third dimensions of output tensor

    Returns
    -------
        hatS : ndarray of shape: (n, p, t)
            $n \times p \times t$ tensor representation
    """
    k = min(n, p)
    assert k == mat.shape[0] and t == mat.shape[1], "Ensure conforming dimensions"

    hatS = np.zeros((n, p, t))
    for i in range(t):
        hatS[:k, :k, i] = np.diag(mat[:, i])

    return hatS


def _singular_vals_tensor_to_mat(tensor):
    """Compresses $\hat{S}$, a $n \times p \times t$ f-diagonal tensor of singular values
    into a $k \times t$ matrix. Each row contains the $k$ singular values from that
    longitudinal slice.

    Reverses _singular_vals_mat_to_tensor

    Parameters
    ----------
        tensor : ndarray of shape: (n, p, t)
            $n \times p \times t$ tensor representation

    Returns
    -------
        mat : ndarray of shape: (min(n, p), t)
            $k \times t$ matrix representation of singular values, where
            $k = \min{(n,p)}$

    Reference
    ---------
    For reference, below is a mathematically clearer illustration of this function
    NOTE: It is a code snippet it will not actually run, treat as pseudo-code
    >>> n, p, t = tensor.shape
    >>> k = min(n, p)
    >>> mat = np.zeros((k, t))
    >>> for i in range(t):
    >>>     mat[:, i] = np.diagonal(tensor[:, :, i])
    """
    # implement using one of the various numpy tricks
    return np.diagonal(tensor, axis1=0, axis2=1).transpose()
