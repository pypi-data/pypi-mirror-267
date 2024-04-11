import math
import numpy as np
import numba as nb

# collection of cool algorithms compiled with numba

@nb.njit()
def check_1Darrays_equal_numba(a, b):
    """
    Check wether two 1D arrays are equal or not.

    Parameters
    ----------
    a : 1D array
        First array.
    b : 1D array
        Second array.
    
    Returns
    -------
    are_equal : bool
        Whether the arrays are equal or not.
    """

    # check input shape
    if a.ndim != 1 or b.ndim != 1:
        raise ValueError("`a` and `b` must be 1D arrays.")
    if a.size != b.size:
        raise ValueError("`a` and `b` must have same size.")

    for i in range(a.size):
        if a[i] != b[i]:
            return False

    return True





@nb.njit()
def check_2Darrays_equal_numba(a, b):
    """
    Check wether two 2D arrays are equal or not.

    Parameters
    ----------
    a : 2D array
        First array.
    b : 2D array
        Second array.
    
    Returns
    -------
    are_equal : bool
        Whether the arrays are equal or not.
    """

    # check input shape
    if a.ndim != 2 or  b.ndim != 2:
        raise ValueError("`a` and `b` must be 2D arrays.")
    if not a.shape[0] == b.shape[0]:
        raise ValueError("`a` and `b` must have same number of rows.")
    if not a.shape[1] == b.shape[1]:
        raise ValueError("`a` and `b` must have same number of columns.")
    
    n_rows = a.shape[0]
    n_cols = a.shape[1]

    for i in range(n_rows):
        for j in range(n_cols):
            if a[i,j] != b[i,j]:
                return False

    return True





@nb.njit()
def check_3Darrays_equal_numba(a, b):
    """
    Check wether two 3D arrays are equal or not.

    Parameters
    ----------
    a : 2D array
        First array.
    b : 2D array
        Second array.
    
    Returns
    -------
    are_equal : bool
        Whether the arrays are equal or not.
    """

    # check input shape
    if a.ndim != 3 or  b.ndim != 3:
        raise ValueError("`a` and `b` must be 3D arrays.")
    if not a.shape[0] == b.shape[0]:
        raise ValueError("`a` and `b` must have same number of tubes.")
    if not a.shape[1] == b.shape[1]:
        raise ValueError("`a` and `b` must have same number of rows.")
    if not a.shape[2] == b.shape[2]:
        raise ValueError("`a` and `b` must have same number of columns.")
    
    n_tubes = a.shape[0]
    n_rows  = a.shape[1]
    n_cols  = a.shape[2]

    for i in range(n_tubes):
        for j in range(n_rows):
            for k in range(n_cols):
                if a[i,j,k] != b[i,j,k]:
                    return False

    return True





@nb.njit()
def check_2Darray_all_rows_unique_numba(a):
    """
    Check if all rows are unique in a 2D array.
    
    Parameters
    ----------
    a : 2D array
        The array whose rows have to be checked for uniqueness.
    
    Returns
    -------
    all_rows_unique : bool
        Wether all rows are unique or not.
    """
    
    # check shape of input
    if not a.ndim == 2:
        raise ValueError("`a` must be a 2D array.")
    
    # get shape of input array
    n_rows = a.shape[0]
    n_cols = a.shape[1]
    
    # loop over all pairs of rows
    for i in range(n_rows):
        for j in range(i+1, n_rows):
            
            # check if rows are different
            for k in range(n_cols):
                if a[i,k] != a[j,k]:
                    break
            else:
                return False
    
    return True





@nb.njit(parallel=True)
def check_2Darrays_all_rows_unique_numba(arrays):
    """
    Check if all rows are unique for a list of 2D arrays.
    
    Parameters
    ----------
    a : (n_arrays,n_rows,n_cols) 3D array
        The arrays whose rows have to be checked for uniqueness.
    
    Returns
    -------
    all_rows_unique : (n_arrays,) array
        Wether all rows are unique or not for each 2D array.
    """
    
    # check shape of input
    if not arrays.ndim == 3:
        raise ValueError("`a` must be a 3D array.")
    
    # get shape of input array and allocate output array
    n_arrays = arrays.shape[0]
    are_unique = np.zeros(n_arrays, dtype=np.bool_)
        
    # loop over all subarrays
    for idx in nb.prange(n_arrays):
        are_unique[idx] = check_2Darray_all_rows_unique_numba(arrays[idx])
    
    return are_unique





@nb.njit()
def sort_1Darray_numba(a):
    """In place sorting of a 1D array using bottom up mergesort.
    
    Parameters
    ----------
    a : 1D array
        Array to be sorted.
    
    Returns
    -------
    None
    """

    if not a.ndim == 1:
        raise ValueError("`a` must be 1D.")
    
    n = a.size
    working = np.zeros_like(a)
    
    # loop over all widths of subarrays 1, 2, 4, 8, ...
    width = 1
    while width < n:
        
        # loop over every consecutive pair of subarrays
        idx_start = 0
        while idx_start < n:
            
            # merge sorted subarrays to sorted array of twice the width
            idx_middle = min(idx_start+width, n)
            idx_end    = min(idx_start+width+width, n)
            idx_left  = idx_start
            idx_right = idx_middle
            
            k = idx_left
            while k < idx_end:
                if (idx_left < idx_middle 
                    and (idx_right >= idx_end or a[idx_left] <= a[idx_right])):
                    working[k] = a[idx_left]
                    idx_left += 1
                else:
                    working[k] = a[idx_right]
                    idx_right += 1
                k += 1
            
            # next pair of subarrays
            idx_start += width+width
        
        # copy higher sorted working array back to a
        a[:] = working[:]
        
        # double width for next iteration
        width *= 2





@nb.njit(parallel=True)
def arglexsort_3Darray_hslice_numba(a):
    """
    Sort.

    Parameters
    ----------
    a : (n_arrays,n_rows,n_cols) 3D array
        Array of 2D subarrays of shape (n_rows,n_cols) that have to
        be sorted.
    
    Returns
    -------
    argsort : (n_arrays,)
        TODO
    """
    
    # check shape of input
    if not a.ndim == 3:
        raise ValueError("`a` must be a 3D array.")
    
    # Todo
    # get shape of input array
    n_arrays = a.shape[0]
    n_rows   = a.shape[1]
    n_cols   = a.shape[2]
    
    # allocate space for mergesort
    indices = np.zeros(n_arrays, dtype=np.int64)
    for i in range(indices.size):
        indices[i] = i
    working = np.zeros_like(indices)
    
    # loop over all widths of subarrays 1, 2, 4, 8, ...
    width = 1
    while width < n_arrays:
        
        # loop over every consecutive pair of subarrays
        
        for idx in nb.prange((n_arrays-1)//(2*width) + 1):
            
            idx_start = idx*(width+width)
            idx_middle = min(idx_start+width, n_arrays)
            idx_end    = min(idx_start+width+width, n_arrays)
            idx_left  = idx_start
            idx_right = idx_middle
            
            k = idx_left
            while k < idx_end:
                
                # check if we want to copy the left or right part element
                if idx_left < idx_middle:
                    if idx_right >= idx_end:
                        take_left = True
                    else:
                        # need to compare
                        left_not_bigger = True
                        done = False
                        a_idx_left  = indices[idx_left]
                        a_idx_right = indices[idx_right]
                        for idx_row in range(n_rows):
                            for idx_col in range(n_cols):
                                if a[a_idx_left,idx_row,idx_col] > a[a_idx_right,idx_row,idx_col]:
                                    left_not_bigger = False
                                    done = True
                                    break
                                elif a[a_idx_left,idx_row,idx_col] < a[a_idx_right,idx_row,idx_col]:
                                    done = True
                                    break
                            if done: break
                        take_left = left_not_bigger
                else:
                    take_left = False
            
                # copy the correct element
                if take_left:
                    working[k] = indices[idx_left]
                    idx_left += 1
                else:
                    working[k] = indices[idx_right]
                    idx_right += 1
                
                k += 1
        
        indices[:] = working[:]
        
        # double width for next iteration
        width = 2*width
        
    return indices





@nb.njit()
def check_3Darray_unique_hslice_numba(a):
    """
    For an array of 2D arrays, check which are unique and which are not.

    Parameters
    ----------
    a : (n_arrays,n_rows,n_cols) 3D array
        Array of 2D subarrays of shape (n_rows,n_cols) that have to
        be checked for uniqueness.

    Returns
    -------
    is_unique : (n_arrays) array of bool
        For every 2D subarray wether it is unique in `a` or not.
    """
    
    # check shape of input
    if not a.ndim == 3:
        raise ValueError("`a` must be a 3D array.")
    
    # get shape of input array
    n_arrays = a.shape[0]
    n_rows   = a.shape[1]
    n_cols   = a.shape[2]
    
    # argsort array to speed up check for uniqueness
    argsort = arglexsort_3Darray_hslice_numba(a)
    # allocate output array
    is_unique = np.ones(n_arrays, dtype=np.bool_)
    
    # check all consecutive pairs of 2D subarrays
    for i in range(n_arrays-1):
        
        # compare both 2D arrays, if equal not unique
        are_equal = True
        for idx_row in range(n_rows):
            for idx_col in range(n_cols):
                if not a[argsort[i],idx_row,idx_col] == a[argsort[i+1],idx_row,idx_col]:
                    are_equal = False
                    break
            if not are_equal: break
        
        if are_equal:
            is_unique[argsort[i]]   = False
            is_unique[argsort[i+1]] = False
    
    return is_unique





@nb.njit()
def arglexsort_2Darray_rows_numba(a):
    """
    Argsort rows of a 2D array lexicographically. The original array is not 
    altered.

    Parameters
    ----------
    a : (n_rows,n_cols) 2D array
        Array whose columns have to be sorted. For the lexsort, the element in
        the first column of each row has highest priority.
    
    Returns
    -------
    argsort : (n_cols,)
        Indices that indicate the lexicographical order of columns. The sorted
        array is then a[argsort,:].
    """
    
    # check shape of input
    if not a.ndim == 2:
        raise ValueError("`a` must be a 2D array.")
    
    # get shape of input array
    n_rows   = a.shape[0]
    n_cols   = a.shape[1]
    
    # allocate space for mergesort
    indices = np.zeros(n_rows, dtype=np.int64)
    for i in range(indices.size):
        indices[i] = i
    working = np.zeros_like(indices)
    
    # loop over all widths of subarrays 1, 2, 4, 8, ...
    width = 1
    while width < n_rows:
        
        # loop over every consecutive pair of subarrays
        idx_start = 0
        while idx_start < n_rows:
            
            # merge sorted subarrays to sorted array of twice the width
            idx_middle = min(idx_start+width, n_rows)
            idx_end    = min(idx_start+width+width, n_rows)
            idx_left  = idx_start
            idx_right = idx_middle
            
            k = idx_left
            while k < idx_end:
                
                # check if we want to copy the left or right part element
                if idx_left < idx_middle:
                    if idx_right >= idx_end:
                        take_left = True
                    else:
                        # need to compare
                        left_not_bigger = True
                        a_idx_left  = indices[idx_left]
                        a_idx_right = indices[idx_right]
                        for idx_col in range(n_cols):
                            if a[a_idx_left,idx_col] > a[a_idx_right,idx_col]:
                                left_not_bigger = False
                                break
                            elif a[a_idx_left,idx_col] < a[a_idx_right,idx_col]:
                                break
                        take_left = left_not_bigger
                else:
                    take_left = False
            
                # copy the correct element
                if take_left:
                    working[k] = indices[idx_left]
                    idx_left += 1
                else:
                    working[k] = indices[idx_right]
                    idx_right += 1
                
                k += 1
            
            # next pair of subarrays
            idx_start += width+width
        
        indices[:] = working[:]
        
        # double width for next iteration
        width *= 2
        
    return indices





@nb.njit(parallel=True)
def lexsort_2Darrays_rows_numba(a):
    """
    Sort rows of a list of 2D arrays lexicographically in place.
    
    Parameters
    ----------
    a : (n_arrays,n_rows,n_cols) 3D array
        List of `n_arrays` 2D subarrays of shape (n_rows,n_cols) whose have
        to be sorted by columns. For the lexsort, the element in
        the first column of each row has highest priority.
    
    Returns
    -------
    None
    """
    
    # check shape of input
    if not a.ndim == 3:
        raise ValueError("`a` must be a 3D array.")
    
    # get shape of input array
    n_arrays = a.shape[0]
    
    for idx_array in nb.prange(n_arrays):
        argsort = arglexsort_2Darray_rows_numba(a[idx_array])
        a[idx_array,:,:] = a[idx_array,argsort,:]





@nb.njit()
def get_3Darray_unique_hslice_indices_numba(a):
    """
    Get indices of unique 2D horizontal slices of a 3D array.
    
    Parameters
    ----------
    a : (n_tubes,n_rows,n_cols) 3D array
        Array to get the indices of unique slices (cuts along first dimension)
        of.
    
    Returns
    -------
    indices_unique : (<=n_slices,) 1D array
        Indices of the unique slices. The unique and sorted subset of slices is
        then a[indices_unique].
    """
    
    if not a.ndim == 3:
        raise ValueError("`a`must be a 3D array.")
        
    n_tubes = a.shape[0]
    n_rows   = a.shape[1]
    n_cols   = a.shape[2]
    
    
    indices_unique = np.zeros(n_tubes, dtype=np.int64)
    argsort = arglexsort_3Darray_hslice_numba(a)
    
    idx_pivot = argsort[0]
    indices_unique[0] = idx_pivot
    n_unique = 1
    for idx_slice in range(1, n_tubes):
        
        # compare this one with
        are_equal = True
        for idx_row in range(n_rows):
            for idx_col in range(n_cols):
                if not a[idx_pivot,idx_row,idx_col] == a[argsort[idx_slice],idx_row,idx_col]:
                    are_equal = False
                    break
            if not are_equal: break
        
        if not are_equal:
            indices_unique[n_unique] = argsort[idx_slice]
            idx_pivot = argsort[idx_slice]
            n_unique += 1
    
    return indices_unique[:n_unique]





@nb.njit()
def is_lexsorted_3Darray_hslice_numba(a):
    """
    Check wether slices along first dimension of a 3D array are
    lexicographically sorted.
    
    The importance of an entry decrases along a row and then along the columns.
    Hence a[:,0,0] is of highest importance followed by a[:,0,1] and so on.

    Parameters
    ----------
    a : (n_arrays,n_rows,n_cols) 3D array
        Array of 2D subarrays of shape (n_rows,n_cols) that have to be sorted.
    
    Returns
    -------
    is_sorted : bool
        Wether the arrays is lexicographically sorted.
    """
    
    # check shape of input
    if not a.ndim == 3:
        raise ValueError("`a` must be a 3D array.")
    
    # get shape of input array
    n_arrays = a.shape[0]
    n_rows   = a.shape[1]
    n_cols   = a.shape[2]
    
    for i in range(1,n_arrays):
        
        left_not_bigger = False
        for idx_row in range(n_rows):
            for idx_col in range(n_cols):
                if a[i-1,idx_row,idx_col] < a[i,idx_row,idx_col]:
                    left_not_bigger = True
                    break
                elif a[i-1,idx_row,idx_col] > a[i,idx_row,idx_col]:
                    return False
            if left_not_bigger: break
    
    return True





@nb.njit()
def is_lexsorted_and_unique_3Darray_hslice_numba(a):
    """
    Check wether slices along first dimension of a 3D array are
    lexicographically sorted and all elements are unique.
    
    The importance of an entry decrases along a row and then along the columns.
    Hence a[:,0,0] is of highest importance followed by a[:,0,1] and so on.

    Parameters
    ----------
    a : (n_arrays,n_rows,n_cols) 3D array
        Array of 2D subarrays of shape (n_rows,n_cols) that have to be sorted.
    
    Returns
    -------
    is_sorted : bool
        Wether the arrays is lexicographically sorted and all slices are
        unqiue.
    """
    
    # check shape of input
    if not a.ndim == 3:
        raise ValueError("`a` must be a 3D array.")
    
    # get shape of input array
    n_arrays = a.shape[0]
    n_rows   = a.shape[1]
    n_cols   = a.shape[2]
    
    for i in range(1,n_arrays):
        
        left_is_smaller = False
        left_equals_right = True
        for idx_row in range(n_rows):
            for idx_col in range(n_cols):
                if a[i-1,idx_row,idx_col] < a[i,idx_row,idx_col]:
                    left_is_smaller = True
                    left_equals_right = False
                    break
                elif a[i-1,idx_row,idx_col] > a[i,idx_row,idx_col]:
                    return False
            if left_is_smaller: break
        
        if left_equals_right:
            return False
    
    return True





@nb.njit()
def permute_3Darray_hslice_inplace_numba(array, permutation):
    """
    Rearranged the slices of a 3D array according to a permutation.
    
    The rearrangement is performed inplace so no additional memory has to be
    allocated.
    
    Parameters
    ----------
    array : (n,n_rows,n_cols) 3D array
        Array that has to be rearranged along the first dimension. The
        rearrangement will be perfomred inplace.
    permutation : (n,) array of int
        Array defining the permutation. `permutation[i] = j` means, that the
        slice `array[i]` will be where `array[j]` was after rearrangement.
        This array must contain every integer from 0 to n-1 exactly once. This
        array will also be changed inplace.
    
    Returns
    -------
    None
    """
    
    # check shape of input
    if not permutation.ndim == 1:
        raise ValueError("`permutation` must be a 1D array.")
    if not array.ndim == 3:
        raise ValueError("`array` must be a 3D array.")
    if not array.shape[0] == permutation.size:
        raise ValueError("First dimension of `array` must match size of `permutation`.")
    
    # get shape of input array
    n = permutation.size
    n_rows = array.shape[1]
    n_cols = array.shape[2]
    
    # loop over all starting positions
    for i in range(n):
        
        # if element already at correct position go to next position
        if permutation[i] == i:
            continue
        
        # have to do at maximum n-i swaps for this cycle
        for j in range(n-i-1):
            
            if permutation[i] <= i or permutation[i] >= n:
                raise ValueError("Index is out of allowed range. There is something wrong with the `permutation` array.")
            
            new_idx = permutation[i]
            
            # make swap
            for idx_row in range(n_rows):
                for idx_col in range(n_cols):
                    temp = array[new_idx,idx_row,idx_col]
                    array[new_idx,idx_row,idx_col] = array[i,idx_row,idx_col]
                    array[i,idx_row,idx_col] = temp
            permutation[i], permutation[new_idx] = permutation[new_idx], permutation[i]
            
            # if correct element arrived, we are done
            if permutation[i] == i:
                break
        
        else:
            raise ValueError("More swaps than necessary. There is something wrong with the `permutation` array.")





@nb.njit()
def lexsort_3Darray_hslice_numba(a):
    """
    Lexicographically sort the slices along first dimension of a 3D array.
    
    The importance of an entry decrases along a row and then along the columns.
    Hence a[:,0,0] is of highest importance followed by a[:,0,1] and so on.

    Parameters
    ----------
    a : (n_arrays,n_rows,n_cols) 3D array
        Array of 2D subarrays of shape (n_rows,n_cols) that have to be sorted.
    
    Returns
    -------
    None
    """
    
    # check shape of input
    if not a.ndim == 3:
        raise ValueError("`a` must be a 3D array.")
    
    # get shape of input array
    n_arrays = a.shape[0]
    n_rows   = a.shape[1]
    n_cols   = a.shape[2]
    
    # argsort array
    argsort = arglexsort_3Darray_hslice_numba(a)
    permutation = np.zeros(argsort.size, dtype=argsort.dtype)
    for i in range(permutation.size):
        permutation[argsort[i]] = i
    
    # apply permutation
    permute_3Darray_hslice_inplace_numba(a, permutation)





@nb.njit()
def are_hslices_shared_3Darrays_numba(a, b):
    """
    For two 3D arrays, whose slices are sorted and unique, find whether slices
    are shared between to arrays or not.
    
    Parameters
    ----------
    a : (n_a,n_rows,n_cols) 3D array
        First array.
    b : (n_b,n_rows,n_cols) 3D array
        Second array.
        
    Returns
    -------
    a_in_b : (n_a,) array of bool
        Wheter a slice of `a` appears in `b`
    b_in_a : (n_b,) array of bool
        Wheter a slice of `b` appears in `a`.
    """
    
    # check shape and size of input
    if (not a.ndim == 3) or (not b.ndim == 3):
        raise ValueError("`a` and `b` must be 3D.")
    if not a.shape[1] == b.shape[1]:
        raise ValueError("`a` and `b` must have the same number of rows.")
    if not a.shape[2] == b.shape[2]:
        raise ValueError("`a` and `b` must have the same number of columns.")
    
    # get shape of input array
    n_rows = a.shape[1]
    n_cols = a.shape[2]
    n_a    = a.shape[0]
    n_b    = b.shape[0]
    
    # check if elements are sorted and if all slices are unqique
    if not is_lexsorted_and_unique_3Darray_hslice_numba(a):
        raise ValueError("`a` is not sorted or not all slices are unqiue.")
    if not is_lexsorted_and_unique_3Darray_hslice_numba(b):
        raise ValueError("`b` is not sorted or not all slices are unqiue.")
    
    # allocate output arrays    
    a_in_b = np.zeros(shape=(n_a,), dtype=np.bool_)
    b_in_a = np.zeros(shape=(n_b,), dtype=np.bool_)
    
    # loop over all the elements of a and b
    idx_a = 0
    idx_b = 0
    while idx_a < n_a and idx_b < n_b:
        
        # determine wether elements are equal or not
        a_equals_b = True
        for idx_row in range(n_rows):
            for idx_col in range(n_cols):
                if a[idx_a,idx_row,idx_col] < b[idx_b,idx_row,idx_col]:
                    a_is_smaller = True
                    a_equals_b = False
                    break
                elif a[idx_a,idx_row,idx_col] > b[idx_b,idx_row,idx_col]:
                    a_is_smaller = False
                    a_equals_b = False
                    break
            if not a_equals_b: break
        
        if a_equals_b:
            a_in_b[idx_a] = True
            b_in_a[idx_b] = True
            idx_a += 1
            idx_b += 1
        elif a_is_smaller:
            idx_a += 1
        else:
            idx_b += 1
    
    return a_in_b, b_in_a


