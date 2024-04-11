# small script to find phase cycles
import warnings
import numpy as np
import numba as nb






#######################################
#                                     #
#   AAA   RRRR   RRRR    AAA   Y   Y  #
#  A   A  R   R  R   R  A   A   Y Y   #
#  AAAAA  RRRR   RRRR   AAAAA    Y    #
#  A   A  R  R   R  R   A   A    Y    #
#  A   A  R   R  R   R  A   A    Y    #
#                                     #
#######################################



@nb.njit(['b1(i4[:],i4[:,:])', 'b1(i8[:],i8[:,:])',
          'b1(u4[:],u4[:,:])', 'b1(u8[:],u8[:,:])'],
         cache=True)
def _row_in_array_numba(row, array):
    """Check wether a row is in a 2D array.
    
    Parameters
    ----------
    row : (m,) array_like
        The row to search for in the array.
    array : (m,n) array_like
        The array in which the given row is searched.
    
    Returns
    -------
    is_in_array : bool
        Wether the row is in the array or not.
    """
    
    # check shape of input
    if not row.ndim == 1:
        raise ValueError("`row` must be a 1D array.")
    if not array.ndim == 2:
        raise ValueError("`array` must be a 2D array.")
    
    m, n = array.shape[0], array.shape[1]

    if not row.size == n:
        raise ValueError("Number of elements in `row` does not match number of columns in `array`.")

    # loop over all rows in array
    for i in range(m):
        # loop over all entries in current row of array
        for j in range(n):
            if not array[i,j] == row[j]:
                break
        else:
            # if the loop for this row of array runs through, it equals given row
            return True
    else:
        return False





@nb.njit(['b1(i4[:],i4[:,:])', 'b1(i8[:],i8[:,:])',
          'b1(u4[:],u4[:,:])', 'b1(u8[:],u8[:,:])'],
         cache=True)
def _col_in_array_numba(col, array):
    """Check wether a column is in a 2D array.
    
    Parameters
    ----------
    col : (n,) array_like
        The column to search for in the array.
    array : (m,n) array_like
        The array in which the given column is searched.
    
    Returns
    -------
    is_in_array : bool
        Wether the column is in the array or not.
    """
    
    # check shape of input
    if not col.ndim == 1:
        raise ValueError("`col` must be a 1D array.")
    if not array.ndim == 2:
        raise ValueError("`array` must be a 2D array.")
    
    m, n = array.shape[0], array.shape[1]

    if not col.size == m:
        raise ValueError("Number of elements in `col` does not match number of rows in `array`.")
    
    # loop over all first cols in array
    for i in range(n):
        # loop over all entries in current col of array
        for j in range(m):
            if not array[j,i] == col[j]:
                break
        else:
            # if the loop for this col of array runs through, it equals given col
            return True
    else:
        return False





@nb.njit(cache=True)
def _delete_ones_numba(a):
    """Delete ones from a 1D array.
    
    Returns an array with the same elements as the given array except for
    ones, which are omitted.
    
    Parameters
    ----------
    a : 1D array_like
        Input array, which will not be altered by this function.
    
    Returns
    -------
    a_new : 1D array_like
        New array with ones deleted.
    """
    
    if not a.ndim == 1:
        raise ValueError("`a` must be 1D.")
    
    a_new = np.zeros_like(a)
    n_not_ones = 0
    for i in range(a.size):
        if not a[i] == 1:
            a_new[n_not_ones] = a[i]
            n_not_ones += 1
    
    return a_new[:n_not_ones]




@nb.njit(parallel=False)
def _copy_by_mask_numba(a_in, a_out, mask, key, idx_out):
    """Copy slices from an input array to an output array.

    Parameters
    ----------
    a_in : (n_in,...) array
        Input array to copy the slices from.
    a_out : (n_out,...) array
        Output array to copy the slices to.
    mask : (n_in,) array
        Key values that decide what elements are copied form the input array.
        Only if mask[i]==key, the i-th slices is copied.
    key : scalar
        Value that decides if element is copied or not.
    idx_out : int
        Index of the first slice in output array where a slices can be copied.
        This number must be between 0 and n_out.

    Returns
    -------
    idx_out : int
        New final index.
    """
    
    # check shape and size of input parameters
    if not mask.ndim == 1:
        raise ValueError("`mask` must be 1D.")
    if not a_in.ndim == a_out.ndim:
        raise ValueError("`a_in` and `a_out` must have the same number of dimensions.")
    for idx in range(1, a_out.ndim):
        if not a_in.shape[idx] == a_out.shape[idx]:
            raise ValueError("`a_in` and `a_out` must have the same shape (except first dimension).")
            
    size_in  = mask.size
    size_out = a_out.shape[0]
    
    if not a_in.shape[0] >= size_in:
        raise ValueError("Need more input slices.")
    if idx_out < 0 or idx_out > size_out:
        raise ValueError("`idx_out` is out of range.")
    
    # loop over all input slices
    for idx in range(size_in):
        
        # output is full
        if idx_out >= size_out:
            return size_out
        
        # copy input slice in output
        if mask[idx] == key:
            a_out[idx_out,...] = a_in[idx,...]
            idx_out += 1
    
    return idx_out



