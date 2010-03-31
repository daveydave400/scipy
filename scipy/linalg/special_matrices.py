
import math
import numpy as np

#-----------------------------------------------------------------------------
# matrix construction functions
#-----------------------------------------------------------------------------

def tri(N, M=None, k=0, dtype=None):
    """Construct (N, M) matrix filled with ones at and below the k-th diagonal.

    The matrix has A[i,j] == 1 for i <= j + k

    Parameters
    ----------
    N : integer
    M : integer
        Size of the matrix. If M is None, M == N is assumed.
    k : integer
        Number of subdiagonal below which matrix is filled with ones.
        k == 0 is the main diagonal, k < 0 subdiagonal and k > 0 superdiagonal.
    dtype : dtype
        Data type of the matrix.

    Returns
    -------
    A : array, shape (N, M)

    Examples
    --------
    >>> from scipy.linalg import tri
    >>> tri(3, 5, 2, dtype=int)
    array([[1, 1, 1, 0, 0],
           [1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1]])
    >>> tri(3, 5, -1, dtype=int)
    array([[0, 0, 0, 0, 0],
           [1, 0, 0, 0, 0],
           [1, 1, 0, 0, 0]])

    """
    if M is None: M = N
    if type(M) == type('d'):
        #pearu: any objections to remove this feature?
        #       As tri(N,'d') is equivalent to tri(N,dtype='d')
        dtype = M
        M = N
    m = np.greater_equal(np.subtract.outer(np.arange(N), np.arange(M)),-k)
    if dtype is None:
        return m
    else:
        return m.astype(dtype)

def tril(m, k=0):
    """Construct a copy of a matrix with elements above the k-th diagonal zeroed.

    Parameters
    ----------
    m : array
        Matrix whose elements to return
    k : integer
        Diagonal above which to zero elements.
        k == 0 is the main diagonal, k < 0 subdiagonal and k > 0 superdiagonal.

    Returns
    -------
    A : array, shape m.shape, dtype m.dtype

    Examples
    --------
    >>> from scipy.linalg import tril
    >>> tril([[1,2,3],[4,5,6],[7,8,9],[10,11,12]], -1)
    array([[ 0,  0,  0],
           [ 4,  0,  0],
           [ 7,  8,  0],
           [10, 11, 12]])

    """
    m = np.asarray(m)
    out = tri(m.shape[0], m.shape[1], k=k, dtype=m.dtype.char)*m
    return out

def triu(m, k=0):
    """Construct a copy of a matrix with elements below the k-th diagonal zeroed.

    Parameters
    ----------
    m : array
        Matrix whose elements to return
    k : integer
        Diagonal below which to zero elements.
        k == 0 is the main diagonal, k < 0 subdiagonal and k > 0 superdiagonal.

    Returns
    -------
    A : array, shape m.shape, dtype m.dtype

    Examples
    --------
    >>> from scipy.linalg import tril
    >>> triu([[1,2,3],[4,5,6],[7,8,9],[10,11,12]], -1)
    array([[ 1,  2,  3],
           [ 4,  5,  6],
           [ 0,  8,  9],
           [ 0,  0, 12]])

    """
    m = np.asarray(m)
    out = (1-tri(m.shape[0], m.shape[1], k-1, m.dtype.char))*m
    return out


def toeplitz(c, r=None):
    """Construct a Toeplitz matrix.

    The Toepliz matrix has constant diagonals, with c as its first column
    and r as its first row.  If r is not given, r == conjugate(c) is
    assumed.

    Parameters
    ----------
    c : array-like, 1D
        First column of the matrix.  Whatever the actual shape of `c`, it
        will be converted to a 1D array.
    r : array-like, 1D
        First row of the matrix. If None, `r = conjugate(c)` is assumed; in
        this case, if `c[0]` is real, the result is a Hermitian matrix.
        `r[0]` is ignored; the first row of the returned matrix is
        `[c[0], r[1:]]`.  Whatever the actual shape of `r`, it will be
        converted to a 1D array.

    Returns
    -------
    A : array, shape (len(c), len(r))
        The Toeplitz matrix.
        dtype is the same as `(c[0] + r[0]).dtype`.

    Examples
    --------
    >>> from scipy.linalg import toeplitz
    >>> toeplitz([1,2,3], [1,4,5,6])
    array([[1, 4, 5, 6],
           [2, 1, 4, 5],
           [3, 2, 1, 4]])
    >>> toeplitz([1.0, 2+3j, 4-1j])
    array([[ 1.+0.j,  2.-3.j,  4.+1.j],
           [ 2.+3.j,  1.+0.j,  2.-3.j],
           [ 4.-1.j,  2.+3.j,  1.+0.j]])

    See also
    --------
    circulant : circulant matrix
    hankel : Hankel matrix

    Notes
    -----
    The behavior when `c` or `r` is a scalar, or when `c` is complex and
    `r` is None, was changed in version 0.8.0.  The behavior in previous
    versions was undocumented and is no longer supported. 
    """
    c = np.asarray(c).ravel()
    if r is None:
        r = c.conjugate()
    else:
        r = np.asarray(r).ravel()
    # Form a 1D array of values to be used in the matrix, containing a reversed
    # copy of r[1:], followed by c.
    vals = np.concatenate((r[-1:0:-1], c))
    a, b = np.ogrid[0:len(c), len(r)-1:-1:-1]
    indx = a + b
    # `indx` is a 2D array of indices into the 1D array `vals`, arranged so that
    # `vals[indx]` is the Toeplitz matrix.
    return vals[indx]

def circulant(c):
    """Construct a circulant matrix.

    Parameters
    ----------
    c : array-like, 1D
        First column of the matrix.

    Returns
    -------
    A : array, shape (len(c), len(c))
        A circulant matrix whose first column is `c`.

    Examples
    --------
    >>> from scipy.linalg import circulant
    >>> circulant([1, 2, 3])
    array([[1, 3, 2],
           [2, 1, 3],
           [3, 2, 1]])

    See also
    --------
    toeplitz : Toeplitz matrix
    hankel : Hankel matrix
    
    Notes
    -----
    .. versionadded:: 0.8.0

    """
    c = np.asarray(c).ravel()
    a, b = np.ogrid[0:len(c), 0:-len(c):-1]
    indx = a + b
    # `indx` is a 2D array of indices into `c`, arranged so that `c[indx]` is
    # the circulant matrix.
    return c[indx]

def hankel(c, r=None):
    """Construct a Hankel matrix.

    The Hankel matrix has constant anti-diagonals, with `c` as its
    first column and `r` as its last row.  If `r` is not given, then
    `r = zeros_like(c)` is assumed.

    Parameters
    ----------
    c : array-like, 1D
        First column of the matrix.  Whatever the actual shape of `c`, it
        will be converted to a 1D array.
    r : array-like, 1D
        Last row of the matrix. If None, `r` == 0 is assumed.
        `r[0]` is ignored; the last row of the returned matrix is
        `[c[0], r[1:]]`.  Whatever the actual shape of `r`, it will be
        converted to a 1D array.

    Returns
    -------
    A : array, shape (len(c), len(r))
        The Hankel matrix.
        dtype is the same as `(c[0] + r[0]).dtype`.

    Examples
    --------
    >>> from scipy.linalg import hankel
    >>> hankel([1, 17, 99])
    array([[ 1, 17, 99],
           [17, 99,  0],
           [99,  0,  0]])
    >>> hankel([1,2,3,4], [4,7,7,8,9])
    array([[1, 2, 3, 4, 7],
           [2, 3, 4, 7, 7],
           [3, 4, 7, 7, 8],
           [4, 7, 7, 8, 9]])

    See also
    --------
    toeplitz : Toeplitz matrix
    circulant : circulant matrix

    """
    c = np.asarray(c).ravel()
    if r is None:
        r = np.zeros_like(c)
    else:
        r = np.asarray(r).ravel()
    # Form a 1D array of values to be used in the matrix, containing `c`
    # followed by r[1:].
    vals = np.concatenate((c, r[1:]))
    a, b = np.ogrid[0:len(c), 0:len(r)]
    indx = a + b
    # `indx` is a 2D array of indices into the 1D array `vals`, arranged so that
    # `vals[indx]` is the Hankel matrix.
    return vals[indx]

def hadamard(n, dtype=int):
    """Construct a Hadamard matrix.
    
    `hadamard(n)` constructs an n-by-n Hadamard matrix, using Sylvester's
    construction.  `n` must be a power of 2.

    Parameters
    ----------
    n : int
        The order of the matrix.  `n` must be a power of 2.
    dtype : numpy dtype
        The data type of the array to be constructed.
        
    Returns
    -------
    H : ndarray with shape (n, n)
        The Hadamard matrix.

    Examples
    --------
    >>> hadamard(2, dtype=complex)
    array([[ 1.+0.j,  1.+0.j],
           [ 1.+0.j, -1.-0.j]])
    >>> hadamard(4)
    array([[ 1,  1,  1,  1],
           [ 1, -1,  1, -1],
           [ 1,  1, -1, -1],
           [ 1, -1, -1,  1]])

    Notes
    -----
    .. versionadded:: 0.8.0

    """
    
    # This function is a slightly modified version of the
    # function contributed by Ivo in ticket #675.

    if n < 1:
        lg2 = 0
    else:
        lg2 = int(math.log(n, 2))
    if 2 ** lg2 != n:
        raise ValueError("n must be an positive integer, and n must be power of 2")

    H = np.array([[1]], dtype=dtype)

    # Sylvester's construction
    for i in range(0, lg2): 
        H = np.vstack((np.hstack((H, H)), np.hstack((H, -H))))

    return H

def all_mat(*args):
    return map(np.matrix,args)

def kron(a,b):
    """Kronecker product of a and b.

    The result is the block matrix::

        a[0,0]*b    a[0,1]*b  ... a[0,-1]*b
        a[1,0]*b    a[1,1]*b  ... a[1,-1]*b
        ...
        a[-1,0]*b   a[-1,1]*b ... a[-1,-1]*b

    Parameters
    ----------
    a : array, shape (M, N)
    b : array, shape (P, Q)

    Returns
    -------
    A : array, shape (M*P, N*Q)
        Kronecker product of a and b

    Examples
    --------
    >>> from scipy import kron, array
    >>> kron(array([[1,2],[3,4]]), array([[1,1,1]]))
    array([[1, 1, 1, 2, 2, 2],
           [3, 3, 3, 4, 4, 4]])

    """
    if not a.flags['CONTIGUOUS']:
        a = np.reshape(a, a.shape)
    if not b.flags['CONTIGUOUS']:
        b = np.reshape(b, b.shape)
    o = np.outer(a,b)
    o = o.reshape(a.shape + b.shape)
    return np.concatenate(np.concatenate(o, axis=1), axis=1)

def block_diag(*arrs):
    """Create a block diagonal matrix from the provided arrays.

    Given the inputs `A`, `B` and `C`, the output will have these
    arrays arranged on the diagonal::

        [[A, 0, 0],
         [0, B, 0],
         [0, 0, C]]

    If all the input arrays are square, the output is known as a
    block diagonal matrix.

    Parameters
    ----------
    A, B, C, ... : array-like, up to 2D
        Input arrays.  A 1D array or array-like sequence with length n is
        treated as a 2D array with shape (1,n).

    Returns
    -------
    D : ndarray
        Array with `A`, `B`, `C`, ... on the diagonal.  `D` has the
        same dtype as `A`.

    References
    ----------
    .. [1] Wikipedia, "Block matrix",
           http://en.wikipedia.org/wiki/Block_diagonal_matrix

    Examples
    --------
    >>> A = [[1, 0],
    ...      [0, 1]]
    >>> B = [[3, 4, 5],
    ...      [6, 7, 8]]
    >>> C = [[7]]
    >>> print(block_diag(A, B, C))
    [[1 0 0 0 0 0]
     [0 1 0 0 0 0]
     [0 0 3 4 5 0]
     [0 0 6 7 8 0]
     [0 0 0 0 0 7]]
    >>> block_diag(1.0, [2, 3], [[4, 5], [6, 7]])
    array([[ 1.,  0.,  0.,  0.,  0.],
           [ 0.,  2.,  3.,  0.,  0.],
           [ 0.,  0.,  0.,  4.,  5.],
           [ 0.,  0.,  0.,  6.,  7.]])

    """
    if arrs == ():
        arrs = ([],)
    arrs = [np.atleast_2d(a) for a in arrs]

    bad_args = [k for k in range(len(arrs)) if arrs[k].ndim > 2]
    if bad_args:
        raise ValueError("arguments in the following positions have dimension "
                            "greater than 2: %s" % bad_args) 

    shapes = np.array([a.shape for a in arrs])
    out = np.zeros(np.sum(shapes, axis=0), dtype=arrs[0].dtype)

    r, c = 0, 0
    for i, (rr, cc) in enumerate(shapes):
        out[r:r + rr, c:c + cc] = arrs[i]
        r += rr
        c += cc
    return out