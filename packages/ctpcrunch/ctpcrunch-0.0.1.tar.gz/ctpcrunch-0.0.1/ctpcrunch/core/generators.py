# small script to find phase cycles
import numpy as np
import numba as nb

from .numbers import (_smallest_common_divisor_numba, 
                      _smallest_common_divisor_addval_numba)





########################################################################################
#                                                                                      #
#  PPPP   EEEEE  RRRR   M   M  U   U  TTTTT   AAA   TTTTT   III    OOO   N   N   SSSS  #
#  P   P  E      R   R  MM MM  U   U    T    A   A    T      I    O   O  NN  N  S      #
#  PPPP   EEE    RRRR   M M M  U   U    T    AAAAA    T      I    O   O  N N N   SSS   #
#  P      E      R  R   M   M  U   U    T    A   A    T      I    O   O  N  NN      S  #
#  P      EEEEE  R   R  M   M   UUU     T    A   A    T     III    OOO   N   N  SSSS   #
#                                                                                      #
########################################################################################



@nb.njit()
def _init_permutation_numba(a):
    """Generate the initial permutation of an array inplace.

    The initial permutation is just the sorted array.
    
    Parameters
    ----------
    a : 1D array_like
        Array for which to generate the next permutation.

    Returns
    -------
    None
    """

    if not a.ndim == 1:
        raise ValueError("Error in _next_permutation_numba: Only 1D arrays are supported!")
    
    a.sort()



@nb.njit()
def _next_permutation_numba(a):
    """Generate the next permutation of an array inplace.
    
    This function mimics the C++ std::next_permutation algorithm and works
    inplace on an already existing array. The array may have repeating elements
    in which case only distinguishable permutations are generated.
    The initial configuration is the array in ascending order, the final one is
    the array in descending order, which itself will be transformed to the
    initial configuration again by this function. In that case 1 is returned
    instead of 0. This means that, starting from an array sorted in ascending
    order and applying this function again and again, until 1 is returned, all
    possible permutations have been generated.
    
    Parameters
    ----------
    a : 1D array_like
        Array for which to generate the next permutation.
    
    Returns
    -------
    indicator : int
        Indicator for the outcome of the operation. 0 if the next permutation
        was generared and 1 when the final configuration was given and
        transformed back to the initial one, sorted in ascending order.
    """
    
    if not a.ndim == 1:
        raise ValueError("Error in _next_permutation_numba: Only 1D arrays are supported!")
    
    n = a.size
    
    # get left bound index ldx
    for ldx in range(n-2,-1,-1):
        if a[ldx] < a[ldx+1]:
            break
    else:
        # array completely sorted, only reverse
        for i in range(n//2):
            a[i], a[-1-i] = a[-1-i], a[i]
        return 1
    
    # get right bound index rdx
    for rdx in range(n-1,ldx,-1):
        if a[rdx] > a[ldx]:
            break
    
    # swap ldx and rdx values
    a[ldx], a[rdx] = a[rdx], a[ldx]
    
    # reverse from ldx+1 to end
    for i in range((n-ldx-1)//2):
        a[ldx+1+i], a[-1-i] = a[-1-i], a[ldx+1+i]
    
    return 0



@nb.njit()
def _fill_buffer_permutations_numba(buffer, seed):
    """
    Given a seed permutation, fill a given buffer with consecutive
    permutation of an array.
    
    Parameters
    ----------
    buffer : (n_buffered,n_elements) 2D array
        Buffer array to store the permutations in.
    seed : (n_elements,) 1D array
        Initial permutation.
    
    Returns
    -------
    n_filled : int
        Number of permutations written to the buffer. Equal to the
        number of rows in buffer if the buffer has been filled or smaller.
    new_seed : (n_blocks,) 1D array
        Seed for the next filling of the buffer.
    all_done : bool
        Wether the end of the counting has been reached.
    """
    
    # check shape of input
    if not buffer.ndim == 2:
        raise ValueError("`buffer` must be two dimensional!")
    if not seed.ndim == 1:
        raise ValueError("`seed` must be one dimensional!")
    if not buffer.shape[1] == seed.size:
        raise ValueError("Shapes of `buffer` and `seed` are not compatible!")
        
    # copy seed to private working array
    permutations_working = np.zeros_like(seed)
    permutations_working[:] = seed[:]
    
    # initialize the first entry
    buffer[0,:] = permutations_working[:]
    n_filled = 1
    
    # fill the other rows
    for i in range(1,buffer.shape[0]):
        
        # try to count up
        res = _next_permutation_numba(permutations_working)
        
        if res == 0:
            buffer[i,:] = permutations_working[:]
            n_filled += 1
        else:
            return n_filled, permutations_working, True
        
    # check if there is more work to do
    res = _next_permutation_numba(permutations_working)
    if res == 0:
        all_done = False
    else:
        all_done = True
    
    return n_filled, permutations_working, all_done



@nb.njit()
def _init_permutation_final1_numba(a):
    """Generate the initial permutation of an array inplace. Ignore ones.

    The initial permutation is just the sorted array with ones at the end.
    
    Parameters
    ----------
    a : 1D array_like
        Array for which to generate the next permutation.

    Returns
    -------
    None
    """

    if not a.ndim == 1:
        raise ValueError("Error in _next_permutation_numba: Only 1D arrays are supported!")
    
    # shift elements left to ones
    n_ones = 0
    for i in range(a.size):        
        if a[i] == 1:
            n_ones += 1
        else:
            a[i-n_ones] = a[i]
    
    # sort the initial elements unequal to one
    a[:a.size-n_ones].sort()
    
    # set the final elements to one
    for i in range(a.size-n_ones, a.size):
        a[i] = 1



@nb.njit()
def _next_permutation_final1_numba(a):
    """Generate the next permutation of an array inplace. Tailing ones are
    ignored.
    
    This function mimics the C++ std::next_permutation algorithm and works
    inplace on an already existing array. The array may have repeating elements
    in which case only distinguishable permutations are generated.
    The initial configuration is the array in ascending order, the final one is
    the array in descending order, which itself will be transformed to the
    initial configuration again by this function. In that case 1 is returned
    instead of 0. This means that, starting from an array sorted in ascending
    order and applying this function again and again, until 1 is returned, all
    possible permutations have been generated.
    
    Parameters
    ----------
    a : 1D array_like
        Array for which to generate the next permutation.
    
    Returns
    -------
    indicator : int
        Indicator for the outcome of the operation. 0 if the next permutation
        was generared and 1 when the final configuration was given and
        transformed back to the initial one, sorted in ascending order.
    """
    
    if not a.ndim == 1:
        raise ValueError("Error in _next_permutation_final1_numba: "
                         "Only 1D arrays are supported!")
    
    
    # find how many elements are not zero
    n = 0
    for idx in range(a.size):
        if a[idx] == 1:
            for jdx in range(idx+1,a.size):
                if not a[jdx] == 1:
                    raise ValueError("Error in `_next_permutation_final1_numba`: "
                                     "Array is not sorted correctly.")
            break
        n += 1
    else:
        n += 1
    
    # get left bound index ldx
    for ldx in range(n-2,-1,-1):
        if a[ldx] < a[ldx+1]:
            break
    else:
        # array completely sorted, only reverse
        for i in range(n//2):
            a[i], a[n-1-i] = a[n-1-i], a[i]
        return 1
    
    # get right bound index rdx
    for rdx in range(n-1,ldx,-1):
        if a[rdx] > a[ldx]:
            break
    
    # swap ldx and rdx values
    a[ldx], a[rdx] = a[rdx], a[ldx]
    
    # reverse from ldx+1 to end
    for i in range((n-ldx-1)//2):
        a[ldx+1+i], a[n-1-i] = a[n-1-i], a[ldx+1+i]
    
    return 0





############################################################
#                                                          #
#  W   W   III   N   N  DDDD    III   N   N   GGGG   SSSS  #
#  W   W    I    NN  N  D   D    I    NN  N  G      S      #
#  W W W    I    N N N  D   D    I    N N N  G  GG   SSS   #  
#  WW WW    I    N  NN  D   D    I    N  NN  G   G      S  #
#  W   W   III   N   N  DDDD    III   N   N   GGG   SSSS   #
#                                                          #
############################################################



def _init_windings_numba(windings, n_scans, 
                     last_zero, no_inverse, no_cfscan, no_cfwind):
    
    if not windings.ndim == 1:
        return -1
    if n_scans < 2:
        return -1
    
    windings[:] = 0
    windings[0] = 1

    return 0



@nb.njit(fastmath=True)
def _count_up_windings_numba(windings, n_scans, last_zero, no_inverse):
    """
    Generate the next set of winding numbers from a given set.
    
    The operation is performed inplace. This function is compiled by numba.
    
    Parameters
    ----------
    windings : 1D array
        Set of winding numbers to increase inplace.
    n_scans : int
        Number of scans for the cogwheel cycle.
    last_zero : bool
        Whether the last winding number shoud be kept zero. This is reasonable
        if all CTPs have the same total coherence order change as the reference
        path because then only the differences between winding numbers do
        really matter.
    no_inverse : bool
        Whether to avoid generating the phase inverted counterparts of other
        sets of winding numbers. To achieve this, winding numbers, that have
        only the numbers 0 or (n_scans+1)//2 to their right, are counted up 
        only to n_scans//2 rather than n_scans-1.
    
    Returns
    -------
    status : int
        0 if the set of winding numbers could be counted up, 1 otherwise. In
        that case the last possible set of winding numbers was generated and
        the array should be back to all zeroes. Negative numbers indicate
        errors.
    """
    
    # check the input parameters
    if not windings.ndim == 1:
        return -1
    if n_scans <= 1:
        return -1
    
    if last_zero:
        n_blocks = windings.size - 1
        if not windings[-1] == 0: return -2
    else:
        n_blocks = windings.size
    
    # handle cases with and without phase inversion separately
    if no_inverse:
        
        # loop in reversed order over the winding numbers, find the position
        # where all right sided values are 0 or (n_scans+1)//2 (symmetric block)
        idx_left = n_blocks
        for i in range(n_blocks):
            idx_left -= 1
            if not (windings[idx_left] == 0 or windings[idx_left] == (n_scans+1)//2):
                break
        
        # try to count up asymmetric block, winding numbers from 0 up to n_scans-1
        for i in range(idx_left):
            if windings[i] < n_scans-1:
                windings[i] += 1
                return 0
            elif windings[i] == n_scans-1:
                windings[i] = 0
            else:
                return -2
        
        # try to count up asymmetric block, winding numbers from 0 up to n_scans//2 ok
        for i in range(idx_left, n_blocks):
            if windings[i] < n_scans//2:
                windings[i] += 1
                return 0
            elif windings[i] == n_scans//2:
                windings[i] = 0
            else:
                return -2
        
        # if all winding numbers are set to zero, that was the last combination
        windings[0] = 1
        return 1
    
    # if not no_inverse
    else:
        
        # loop over all blocks, try to increase winding number
        for i in range(n_blocks):
           
            # if winding number is small enough, increase it
            if windings[i] < n_scans-1:
                windings[i] += 1
                return 0
            # if winding number is at maximum, set to zero and try next number
            elif windings[i] == n_scans-1:
                windings[i] = 0
            # in any other case, winding number is invalid
            else:
                return -2
        
        # if all winding numbers are set to zero, that was the last combination
        windings[0] = 1
        return 1



@nb.njit(fastmath=True)
def _count_up_windings_nocfscan_numba(windings, n_scans, last_zero, no_inverse):
    """
    Generate the next set of winding numbers from a given set avoiding all
    combinations whose winding numbers and the number of scans share a factor 
    greater than one. This will avoid reducible cycles, i.e. cycles that are
    equivalent to other cycles with a smaller number of scans.
    
    The operation is performed inplace. This function is compiled by numba.
    
    Parameters
    ----------
    windings : 1D array
        Set of winding numbers to increase inplace.
    n_scans : int
        Number of scans for the cogwheel cycle.
    last_zero : bool
        Whether the last winding number shoud be kept zero. This is reasonable
        if all CTPs have the same total coherence order change as the reference
        path because then only the differences between winding numbers do
        really matter.
    no_inverse : bool
        Whether to avoid generating the phase inverted counterparts of other
        sets of winding numbers. To achieve this, winding numbers, that have
        only the numbers 0 or (n_scans+1)//2 to their right, are counted up 
        only to n_scans//2 rather than n_scans-1.
    
    Returns
    -------
    status : int
        0 if the set of winding numbers could be counted up, 1 otherwise. In
        that case the last possible set of winding numbers was generated and
        the array should be back to all zeroes. Negative numbers indicate
        errors.
    """
    
    while True:
        
        res = _count_up_windings_numba(windings, n_scans, last_zero, no_inverse)
        
        # forward all flags except when counting up was successfull
        if not res == 0:
            return res
        
        # check if no common factor, if there is, count up further
        if _smallest_common_divisor_addval_numba(n_scans, windings) == 1:
            return 0



@nb.njit(fastmath=True)
def _count_up_windings_nocfwind_numba(windings, n_scans, last_zero, no_inverse):
    """
    Generate the next set of winding numbers from a given set avoiding all
    combinations whose winding numbers and the number of scans share a factor 
    greater than one. This will avoid cycles that have the same selection
    properties as a cycles, where no factors are shared.
    
    The operation is performed inplace. This function is compiled by numba.
    
    Parameters
    ----------
    windings : 1D array
        Set of winding numbers to increase inplace.
    n_scans : int
        Number of scans for the cogwheel cycle.
    last_zero : bool
        Whether the last winding number shoud be kept zero. This is reasonable
        if all CTPs have the same total coherence order change as the reference
        path because then only the differences between winding numbers do
        really matter.
    no_inverse : bool
        Whether to avoid generating the phase inverted counterparts of other
        sets of winding numbers. To achieve this, winding numbers, that have
        only the numbers 0 or (n_scans+1)//2 to their right, are counted up 
        only to n_scans//2 rather than n_scans-1.
    
    Returns
    -------
    status : int
        0 if the set of winding numbers could be counted up, 1 otherwise. In
        that case the last possible set of winding numbers was generated and
        the array should be back to all zeroes. Negative numbers indicate
        errors.
    """
    
    while True:
        
        res = _count_up_windings_numba(windings, n_scans, last_zero, no_inverse)
        
        # forward all flags except when counting up was successfull
        if not res == 0:
            return res
        
        # check if no common factor, if there is, count up further
        if _smallest_common_divisor_numba(windings) == 1:
            return 0



@nb.njit(fastmath=True)
def _next_windings_numba(windings, n_scans, 
                     last_zero, no_inverse, no_cfscan, no_cfwind):
    """
    Generate the next set of winding numbers.
    
    Parameters
    ----------
    ...

    Returns
    -------
    ...    
    """
    
    # if no common factor wanted among winding numbers, dont even bother with scans
    if no_cfwind:

        while True:
            res = _count_up_windings_numba(windings, n_scans, last_zero, no_inverse)
            
            # forward error flags
            if not res == 0:
                return res
            
            # check if no common factor, if there is, count up further
            if _smallest_common_divisor_numba(windings) == 1:
                return res
    
    # no common factors between the number of scans and all winding numbers
    elif no_cfscan:
        
        while True:
            res = _count_up_windings_numba(windings, n_scans, last_zero, no_inverse)
            
            # forward error flags
            if not res == 0:
                return res
            
            # check if no common factor, if there is, count up further
            if _smallest_common_divisor_addval_numba(n_scans, windings) == 1:
                return res
    
    # common factors are OK
    else:
        
        res = _count_up_windings_numba(windings, n_scans, last_zero, no_inverse)
        return res



@nb.njit(fastmath=True)
def _fill_buffer_windings_numba(buffer, seed, n_scans,
                                last_zero, no_inverse, no_cfscan, no_cfwind):
    """
    Given a seed set of winding numbers, fill a given buffer with consecutive
    sets of winding numbers.
    
    Parameters
    ----------
    buffer : (n_buffered,n_blocks) 2D array
        Buffer array to store the winding numbers in.
    seed : (n_blocks,) 1D array
        Initial set of winding numbers.
    n_scans : int
        Number of scans for the cogwheel cycle.
    last_zero : bool
        Whether the last winding number shoud be kept zero. This is reasonable
        if all CTPs have the same total coherence order change as the reference
        path because then only the differences between winding numbers do
        really matter.
    no_inverse : bool
        Whether the last non-zero winding number is counted up only to
        n_scans//2 and not n_scans-1. This avoids generating the phase inverted
        counterparts of other sets of winding numbers.
    no_cfscan : bool
        Whether to avoid sets of winding numbers, where every winding number and
        the number of scans share a common factor. This would result in an
        redundant cycle, i.e. a cycle that has smaller length but is repeated.
    no_cfwind : bool
        Whether to avoid sets of winding numbers, where the winding numbers 
        share a common factor. Such cycles would be equivalent (selecting the)
        same CTPs as the cycle with winding numbers, where the common factor
        is devided out.
        If this option is set, setting `no_cfscan` has no effect anymore.
    
    Returns
    -------
    n_filled : int
        Number of sets of winding numbers written to the buffer. Equal to the
        number of rows in buffer if the buffer has been filled or smaller.
    new_seed : (n_blocks,) 1D array
        Seed for the next filling of the buffer.
    all_done : bool
        Wether the end of the counting has been reached.
    """
    
    # check shape of input
    if not buffer.ndim == 2:
        raise ValueError("`buffer` must be two dimensional!")
    if not seed.ndim == 1:
        raise ValueError("`seed` must be one dimensional!")
    if not buffer.shape[1] == seed.size:
        raise ValueError("Shapes of `buffer` and `seed` are not compatible!")
    
    # copy seed to private working array
    windings_working = np.zeros_like(seed)
    new_seed = np.zeros_like(seed)
    windings_working[:] = seed[:]
    
    # initialize the first entry
    buffer[0,:] = windings_working[:]
    n_filled = 1
    
    # fill the other rows
    for i in range(1,buffer.shape[0]):
        
        # try to count up
        res = _next_windings_numba(windings_working, n_scans, 
                                   last_zero, no_inverse, no_cfscan, no_cfwind)
        
        if res == 0:
            buffer[i,:] = windings_working[:]
            n_filled += 1
        elif res == 1:
            new_seed[:] = windings_working[:]
            return n_filled, new_seed, True
        else:
            return -1, new_seed, False
        
    # check if there is more work to do
    res = _count_up_windings_numba(windings_working, n_scans, last_zero, no_inverse)
    if res == 0:
        all_done = False
    elif res == 1:
        all_done = True
    else:
        return -1, new_seed, False
    
    new_seed[:] = windings_working[:]
    return n_filled, new_seed, all_done



@nb.njit(parallel=True, fastmath=True)
def _fill_buffer_windings_numbap(buffer, seed, n_scans,
                                 last_zero, no_inverse, no_cfscan, no_cfwind):
    """
    Given a seed set of winding numbers, fill a given buffer with consecutive
    sets of winding numbers.
    
    Parameters
    ----------
    buffer : (n_buffered,n_blocks) 2D array
        Buffer array to store the winding numbers in.
    seed : (n_blocks,) 1D array
        Initial set of winding numbers.
    n_scans : int
        Number of scans for the cogwheel cycle.
    last_zero : bool
        Whether the last winding number shoud be kept zero. This is reasonable
        if all CTPs have the same total coherence order change as the reference
        path because then only the differences between winding numbers do
        really matter.
    no_inverse : bool
        Whether the last non-zero winding number is counted up only to
        n_scans//2 and not n_scans-1. This avoids generating the phase inverted
        counterparts of other sets of winding numbers.
    no_cfscan : bool
        Whether to avoid sets of winding numbers, where every winding number and
        the number of scans share a common factor. This would result in an
        redundant cycle, i.e. a cycle that has smaller length but is repeated.
    no_cfwind : bool
        Whether to avoid sets of winding numbers, where the winding numbers 
        share a common factor. Such cycles would be equivalent (selecting the)
        same CTPs as the cycle with winding numbers, where the common factor
        is devided out.
        If this option is set, setting `no_cfscan` has no effect anymore.
    
    Returns
    -------
    n_filled : int
        Number of sets of winding numbers written to the buffer. Equal to the
        number of rows in buffer if the buffer has been filled or smaller.
    new_seed : (n_blocks,) 1D array
        Seed for the next filling of the buffer.
    all_done : bool
        Whether the end of the counting has been reached.
    """
    
    # check shape of input
    if not buffer.ndim == 2:
        raise ValueError("`buffer` must be two dimensional!")
    if not seed.ndim == 1:
        raise ValueError("`seed` must be one dimensional!")
    if not buffer.shape[1] == seed.size:
        raise ValueError("Shapes of `buffer` and `seed` are not compatible!")
    
    # get some parameters
    n_buffered = buffer.shape[0]
    n_blocks  = seed.size
    n_workers = min(nb.get_num_threads(), n_buffered)
    
    # allocate array for new seed, working array and copy given seed
    new_seed = np.zeros_like(seed)
    windings_working = np.zeros(n_blocks, dtype=seed.dtype)
    windings_working[:] = seed[:]
    
    # allocate some arrays for each worker
    windings_workers   = np.zeros((n_workers, n_blocks), dtype=seed.dtype)
    #windings_workers[:,0] = 1
    overflowed_workers = np.ones((n_workers,), dtype=np.bool_)
    haderror_workers   = np.zeros((n_workers,), dtype=np.bool_)
    n_filled_workers   = np.zeros((n_workers,), dtype=np.int64)
    n_filled = 0
    
    # sequentially fill initial element of workers
    for idx_worker in range(n_workers):
        
        # set winding numbers
        windings_workers[idx_worker,:] = windings_working[:]
        overflowed_workers[idx_worker] = False
        
        # generate next winding numbers
        res = _next_windings_numba(windings_working, n_scans,
                    last_zero, no_inverse, no_cfscan, no_cfwind)
        if res == 0:
            continue
        elif res == 1:
            break
        else:
            return -1, new_seed, False
    
    # parallel loop for each worker
    for idx_worker in nb.prange(n_workers):
        # loop over all rows that have to be set by this worker
        for idx_buffer in range(idx_worker, n_buffered, n_workers):
            
            # only do work if no overflow yet
            if overflowed_workers[idx_worker]:
                break
            
            # set windings to buffer
            buffer[idx_buffer,:] = windings_workers[idx_worker,:]
            n_filled_workers[idx_worker] += 1
            
            # count up the winding numbers of this worker
            for _ in range(n_workers):
                res = _next_windings_numba(
                            windings_workers[idx_worker,:], n_scans,
                            last_zero, no_inverse, no_cfscan, no_cfwind)
                if res == 0:
                    continue
                elif res == 1:
                    overflowed_workers[idx_worker] = True
                    break
                else:
                    haderror_workers[idx_worker] = True
                    break
                
    
    # check if any worker had an error
    if np.any(haderror_workers):
        return -1, new_seed, False
    
    # number of set phases
    n_filled += n_filled_workers.sum()
    
    # get new seed
    new_seed[:] = buffer[n_filled-1,:]
    res = _next_windings_numba(
                new_seed, n_scans,
                last_zero, no_inverse, no_cfscan, no_cfwind)
    
    if res == 0:
        return n_filled, new_seed, False
    elif res == 1:
        return n_filled, new_seed, True
    else:
        return -1, new_seed, False



#####################################################
#                                                   #
#   SSSS  U   U  BBBB    SSSS  EEEEE  TTTTT   SSSS  #
#  S      U   U  B   B  S      E        T    S      #
#   SSS   U   U  BBBB    SSS   EEE      T     SSS   #
#      S  U   U  B   B      S  E        T        S  #
#  SSSS    UUU   BBBB   SSSS   EEEEE    T    SSSS   #
#                                                   #
#####################################################



@nb.njit(fastmath=True)
def _init_subsetidxs_numba(a):
    """TODO

    TODO

    Parameters
    ----------
    a : array
        TODO

    Returns
    -------
    None
    """

    if not a.ndim == 1:
        raise ValueError("Error in `_init_subsetidxs_numba`: "
                         "`a` must be a 1D array.")
    
    a[:] = -1
    a[0] = 0



@nb.njit(fastmath=True)
def _next_subsetidxs_numba(a):
    """TODO

    TODO

    Parameters
    ----------
    a : array
        TODO

    Returns
    -------
    indicator : int
        TODO
    """
    
    if not a.ndim == 1:
        raise ValueError("Error in `_next_subsetidxs_numba`: "
                         "`a` must be a 1D array.")

    n = a.size
    
    # find first negative entry
    # the i after the loop breaks is the index of last non-negative entry
    if a[0] < 0:
        a[:] = -1
        return -1
    
    for imax in range(1,n):
        if a[imax] < 0:
            break
        if (not a[imax] < n) or (not a[imax] > a[imax-1]):
            a[:] = -1
            return -1
    # if loop ran through, only non-negative numbers, set to initial
    else:
        a[:] = -1
        a[0] = 0
        return 1
    
    # loop in reverse order over remaining elements
    max_val = n-1
    for i in range(imax-1,-1,-1):
        
        # if entry smaller than max_val, can count this element up
        if a[i] < max_val:
            a[i] += 1
            # count up the following elements
            for k in range(i+1,imax):
                a[k] = a[k-1] + 1
            return 0
        # if equal, cannot count this element up, try next one
        elif a[i] == max_val:
            max_val -= 1
        # if greater, then array is not of expected form
        else:
            # return error indicator
            a[:] = -1
            return -1
            
    else:
        # initilaize one more non-negative element
        for k in range(imax+1):
            a[k] = k
        return 0



@nb.njit(fastmath=True)
def _fill_buffer_subsetidxs_numba(buffer, seed):
    """
    Given seed subset indices, fill a given buffer with consecutive
    subset indices.
    
    Parameters
    ----------
    buffer : (n_buffered,n_elements) 2D array
        Buffer array to store the subset indices in.
    seed : (n_elements,) 1D array
        Initial subset indices.
    
    Returns
    -------
    n_filled : int
        Number of subset indices written to the buffer. Equal to the
        number of rows in buffer if the buffer has been filled or smaller.
    new_seed : (n_blocks,) 1D array
        Seed for the next filling of the buffer.
    all_done : bool
        Whether the end of the counting has been reached.
    """

    # check shape of input
    if not buffer.ndim == 2:
        raise ValueError("`buffer` must be 2D!")
    if not seed.ndim == 1:
        raise ValueError("`buffer` must be 1D!")
    if not buffer.shape[1] == seed.size:
        raise ValueError("Shapes of `buffer` and `seed` are not compatible!")

    # copy seed to a private working array
    working = np.zeros_like(seed)
    working[:] = seed[:]
    new_seed = np.zeros_like(seed)

    # initialize the first entry
    buffer[0,:] = working[:]
    n_filled = 1

    # fill the other slices of the buffer
    for idx in range(1, buffer.shape[0]):

        # try to generate next set
        res = _next_subsetidxs_numba(working)
        if res == 0:
            buffer[idx,:] = working[:]
            n_filled += 1
        elif res == 1:
            new_seed[:] = working[:]
            return n_filled, new_seed, True
        else:
            return -1, new_seed, False

    # generate the next seed
    res = _next_subsetidxs_numba(working)
    if res == 0:
        all_done = False
    elif res == 1:
        all_done = True
    else:
        return -1, new_seed, False
    
    new_seed[:] = working[:]
    return n_filled, new_seed, all_done



@nb.njit(fastmath=True)
def _init_subset2Didxs_numba(a):
    """
    ToDo

    ToDo
    
    Parameters
    ----------
    a : array of int
        ... ToDo ...

    Returns
    -------
    indicator : int
        ... ToDo ...
    """
    
    if not a.ndim == 2:
        raise ValueError("Error in `_init_indices2D_numba`: "
                         "`a` must be a 2D array.")
    
    m = a.shape[0]
    n = a.shape[1]
    
    # set the first row
    a[0,:] = -1
    a[0,0] = 0
    
    # set all rows after the first one
    for i in range(1,m):
        
        # copy previous row
        a[i,:] = a[i-1,:]
        
        # find first negative index
        for jmax in range(n):
            if a[i,jmax] < 0: break
        else:
            raise ValueError("Error in `_init_indices2D_numba`: "
                             "Cannot increase a row. Too many rows?")
        
        # try to increase current element
        max_val = n-1
        for j in range(jmax-1,-1,-1):
            if a[i,j] < max_val:
                a[i,j] += 1
                # increase all the following elements
                for k in range(j+1,jmax):
                    a[i,k] = a[i,k-1] + 1
                break
            elif a[i,j] == max_val:
                max_val -= 1
            else:
                raise ValueError("Error in `_init_indices2D_numba`: "
                                 "Invalid value.")
        else:
            # initilaize with one more non-negative element
            for k in range(jmax+1):
                a[i,k] = k



@nb.njit(fastmath=True)
def _next_subset2Didxs_numba(a):
    """
    ToDo

    ToDo
    
    Parameters
    ----------
    a : array of int
        ... ToDo ...

    Returns
    -------
    indicator : int
        ... ToDo ...
    """
    
    if not a.ndim == 2:
        return -3
        
    m = a.shape[0]
    n = a.shape[1]
    
    # loop over all cols in reversed order
    for i in range(m-1, -1, -1):
        
        res = _next_subsetidxs_numba(a[i])
        if res == 0:
            for j in range(i+1,m):
                a[j,:] = a[j-1,:]
                res = _next_subsetidxs_numba(a[j])
                if res == 0:
                    continue
                elif res == 1:
                    break
                else:
                    a[:,:] = -1
                    return -1
            else:
                return 0
        elif res == 1:
            continue
        else:
            a[:,:] = -1
            return -1
    
    # set to initial configuration
    else:
        # set the first row
        a[0,:] = -1
        a[0,0] = 0
        
        # set all rows after the first one
        for i in range(1,m):
            
            # copy previous row
            a[i,:] = a[i-1,:]
            
            # find first negative index
            for jmax in range(n):
                if a[i,jmax] < 0: break
            else:
                return -2
            
            # try to increase current element
            max_val = n-1
            for j in range(jmax-1,-1,-1):
                if a[i,j] < max_val:
                    a[i,j] += 1
                    # increase all the following elements
                    for k in range(j+1,jmax):
                        a[i,k] = a[i,k-1] + 1
                    break
                elif a[i,j] == max_val:
                    max_val -= 1
                else:
                    return -2
            else:
                # initilaize with one more non-negative element
                for k in range(jmax+1):
                    a[i,k] = k
        
        return 1



@nb.njit(fastmath=True)
def _fill_buffer_subset2Didxs_numba(buffer, seed):
    """
    
    Parameters
    ----------
    
    Returns
    -------

    """

    # check shape of input
    if not seed.ndim == 2:
        raise ValueError()
    if not buffer.ndim == seed.ndim + 1:
        raise ValueError()
    for i in range(seed.ndim):
        if not buffer.shape[i+1] == seed.shape[i]:
            raise ValueError()

    # copy seed to a private working array
    working = np.zeros_like(seed)
    working[:,:] = seed[:,:]
    new_seed = np.zeros_like(seed)

    # initialize the first entry
    buffer[0,:,:] = working[:,:]
    n_filled = 1

    # fill the other slices of the buffer
    for idx in range(1, buffer.shape[0]):

        # try to generate next set
        res = _next_subset2Didxs_numba(working)
        if res == 0:
            buffer[idx,:,:] = working[:,:]
            n_filled += 1
        elif res == 1:
            new_seed[:,:] = working[:,:]
            return n_filled, new_seed, True
        else:
            return -1, new_seed, False

    # generate the next seed
    res = _next_subset2Didxs_numba(working)
    if res == 0:
        all_done = False
    elif res == 1:
        all_done = True
    else:
        return -1, new_seed, False
    
    new_seed[:,:] = working[:,:]
    return n_filled, new_seed, all_done



