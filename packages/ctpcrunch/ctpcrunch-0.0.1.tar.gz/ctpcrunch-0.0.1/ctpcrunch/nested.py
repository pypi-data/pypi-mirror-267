import math
import numpy as np
import numba as nb
from .core.array import (_row_in_array_numba, _delete_ones_numba)
from .core.generators import _fill_buffer_permutations_numba
from .core.numbers import (_generate_all_factorizations_numba,
                           _binomcoeff_numba,
                           _multinomcoeff_numba)





#####################################################################
#                                                                   #
#   U   U  TTTTT   III   L       III   TTTTT   III   EEEEE   SSSS   #
#   U   U    T      I    L        I      T      I    E      S       #
#   U   U    T      I    L        I      T      I    EEE     SSS    #
#   U   U    T      I    L        I      T      I    E          S   #
#    UUU     T     III   LLLLL   III     T     III   EEEEE  SSSS    #
#                                                                   #
#####################################################################





def number_of_nested(n_scans, n_blocks):
    """
    Compute the number of nested phase cycles.
    
    Parameters
    ----------
    n_scans : int
        Number of scans for the nested cycle.
    n_blocks : int
        Number of pulse blocks.
    
    Returns
    -------
    n_nest : int
        Number of nested cycles.  
    """

    n_scans  = int(n_scans)
    n_blocks = int(n_blocks)
    
    if n_blocks < 1:
        raise ValueError("`n_blocks` must be at least 1.")
    if n_scans < 2:
        raise ValueError("`n_scans` must be at least 2.")

    # get prime factorizations
    n = n_scans
    primfac = []
    while n%2 == 0:
        n = n//2
        primfac.append(2)
    while n%3 == 0:
        n = n//3
        primfac.append(3)
    i = 5
    while n != 1:
        while n%i == 0:
            primfac.append(i)
            n = n//i
        while n%(i+2) == 0:
            primfac.append(i+2)
            n = n//(i+2)
        i += 6
    
    # test if primfactorization is correct
    n_primfac = len(primfac)
    test = 1
    for i in range(n_primfac):
        test *= primfac[i]
    if not test == n_scans:
        raise ValueError("Prime factorization wrong.")
    del test
    
    # generate all unique factorizations
    factorizations = [primfac]
    reduction = [primfac]
    for i in range(n_primfac-1):
        
        new_reduction = []
        for idx in range(len(reduction)):
            
            for idxl in range(n_primfac-i-1):
                for idxr in range(idxl+1, n_primfac-i):
                    this_red = sorted(reduction[idx])
                    this_red[idxl] *= this_red.pop(idxr)
                    this_red.sort()
                    if not this_red in new_reduction:
                        new_reduction.append(this_red)
                        
        factorizations += new_reduction
        reduction = new_reduction
    
    n_picks = 2 ** n_blocks - 1
    n_cyc = 0
    
    # loop over all factorizations
    for factorization in factorizations:
        
        if len(factorization) > n_picks:
            continue
        
        # count how often certain factors appear
        counts = []
        element = 0
        for val in factorization:
            if val > element:
                counts.append(1)
                element = val
            elif val == element:
                counts[-1] += 1
            else:
                raise ValueError("Factorization is not sorted.")
        if not sum(counts) == len(factorization):
            raise ValueError("Mismatch in number of counts.")
        
        # number of unique permutations
        n_perm = 1
        k = counts[0]
        for i in range(1, len(counts)):
            k += counts[i]
            binom = 1
            for j in range(counts[i]):
                binom = binom * (k-j) // (j+1)
            n_perm *= binom
        
        # number of ways to pick subcycles
        n_comb = 1
        for j in range(len(factorization)):
            n_comb = n_comb * (n_picks-j) // (j+1)
        
        n_cyc += n_perm*n_comb

    return n_cyc







# @numba.njit(['i8[:,:](i8, i8)'], cache=True)
# def _generate_all_factorizations_numba(n, max_n_factors):
#     """
#     Calculate prime factorization of a number with a given list of primes.
#     """
    
#     # number of elements to pre-allocate to avoid appending and copying
#     n_alloc = 64
    
#     # find the prime factorization of n
    
#     # allocate some space for prime factors
#     prime_factorization = np.ones(n_alloc, dtype=np.int64)
    
#     # count the number of prime factors
#     n_prime_factors = 0
#     n_work = n
    
#     # devide out all factors of 2
#     while(n_work % 2 == 0):
#         if n_prime_factors >= n_alloc:
#             prime_factorization = np.append(prime_factorization, 2)
#         else:
#             prime_factorization[n_prime_factors] = 2
#         n_work = n_work//2
#         n_prime_factors += 1
        
#     # devide out all factors of 3
#     while(n_work % 3 == 0):
#         if n_prime_factors >= n_alloc:
#             prime_factorization = np.append(prime_factorization, 3)
#         else:
#             prime_factorization[n_prime_factors] = 3
#         n_work = n_work//3
#         n_prime_factors += 1
    
#     # only check the factors up to sqrt(n_work), 2 and 3 are no factors of n
#     stop = np.int64(np.floor(np.sqrt(n_work)))
    
#     # # loop over remaining possible factors of form 6k+-1, that might be prime
#     # # the smallest next valid factor is always prime, so only real primes are found
#     i = 5
#     while(i <= stop):
        
#         # if n_work = 1, all factors are found
#         if n_work == 1:
#             break
        
#         # check divisibility by possible prime 6k-1
#         while(n_work % i == 0):
#             if n_prime_factors >= n_alloc:
#                 pass
#                 #prime_factorization = np.append(prime_factorization, DTYPE(i))
#             else:
#                 prime_factorization[n_prime_factors] = i
#             n_work = n_work // i
#             n_prime_factors += 1
        
#         # check divisibility by possible prime 6k+1
#         while(n_work % (i+2) == 0):
#             if n_prime_factors >= n_alloc:
#                 prime_factorization = np.append(prime_factorization, i+2)
#             else:
#                 prime_factorization[n_prime_factors] = i+2
#             n_work = n_work // (i+2)
#             n_prime_factors += 1
        
#         # go to next pair of possible primes 6(k+1)+-1
#         i += 6
    
#     # there should be no factors left now, if n_work ist not one, it was prime
#     if not n_work == 1:
#         if n_prime_factors >= n_alloc:
#             prime_factorization = np.append(prime_factorization, n_work)
#         else:
#             prime_factorization[n_prime_factors] = n_work
#         n_prime_factors += 1
        
#     # crop array to number of prime factors
#     prime_factorization = prime_factorization[:n_prime_factors]
    
    
#     # now generate all factorizations from prime factorization
    
#     # handle smaller cases separately
#     if n_prime_factors == 1:
#         factorizations = np.array([[prime_factorization[0]]], dtype=np.int64)
#         cropping_indices = np.array([0], dtype=np.int64)
    
#     elif n_prime_factors == 2:
#         fac1 = prime_factorization.min()
#         fac2 = prime_factorization.max()
#         factorizations = np.array([[fac1,fac2],[fac1*fac2,1]], dtype=np.int64)
#         cropping_indices = np.array([0,1], dtype=np.int64)
    
#     # handle the general case with 3 or more prime factors, allocate some space first
#     else:
#         factorizations = np.ones((n_alloc, n_prime_factors), dtype=np.int64)
#         # total number of factorizations found
#         n_factorizations = 0
#         # stores the borders of the layers
#         cropping_indices = np.zeros(n_prime_factors, dtype=np.int64)
        
#         # initialize first row with all prime factors
#         if n_factorizations >= n_alloc:
#             factorizations = np.append(factorizations, prime_factorization.reshape(1,n_prime_factors), axis=0)
#         else:
#             factorizations[0,:] = prime_factorization[:]
#         n_factorizations += 1
#         cropping_indices[0] = 0
        
#         # allocate space for working array
#         working = np.zeros(n_prime_factors, dtype=prime_factorization.dtype)
        
#         # indices to mark first and last row of the currently to be reduced array
#         idx_red_start = 0
#         idx_red_end = 0
        
#         for idx_layer in range(n_prime_factors-2):
#             # number of relevant factors in this layer
#             n_facs_layer = n_prime_factors - idx_layer
#             # number of new smaller factorizations found for this layer
#             n_new_factorizations = 0
            
#             cropping_indices[idx_layer+1] = n_factorizations
            
#             # loop over all rows to reduce in current layer
#             for idx_red in range(idx_red_start, idx_red_end+1):
                
#                 fac_i = 0
#                 for i in range(n_facs_layer):
#                     # only try this factor, if it differs from previous
#                     if factorizations[idx_red,i] == fac_i:
#                         continue
#                     fac_i = factorizations[idx_red,i]
                    
#                     fac_j = 0
#                     for j in range(i+1, n_facs_layer):
#                         # only try this factor, if it differs from previous
#                         if factorizations[idx_red,j] == fac_j:
#                             continue
#                         fac_j = factorizations[idx_red,j]
                        
#                         # build new factorization
#                         working[:] = factorizations[idx_red,:]
#                         working[i], working[j] = fac_i*fac_j, n+1
                        
#                         # sort the new factorization
#                         working[:n_facs_layer] = np.sort(working[:n_facs_layer])
#                         working[n_facs_layer-1] = 1
                        
#                         # check if this factorization is new
#                         if not _row_in_array_numba(working[:n_facs_layer-1], factorizations[idx_red_end+1:idx_red_end+1+n_new_factorizations,:n_facs_layer-1]):
#                             # append this factorization to all factorizations
#                             if n_factorizations >= n_alloc:
#                                 factorizations = np.append(factorizations, working.reshape(1,n_prime_factors), axis=0)
#                             else:
#                                 factorizations[n_factorizations] = working[:]
#                             n_factorizations += 1
#                             n_new_factorizations += 1
                            
#             # done with this reduction layer, update indices for next iteration
#             idx_red_start = idx_red_end+1
#             idx_red_end = idx_red_end+n_new_factorizations
                
        
#         cropping_indices[-1] = n_factorizations
        
#         # the last layer, reduction to one factor that is just n
#         final_factor = factorizations[n_factorizations-1,0] * factorizations[n_factorizations-1,1]
#         if n_factorizations >= n_alloc:
#             working[:] = 1
#             working[0] = final_factor
#             factorizations = np.append(factorizations, working.reshape(1,n_prime_factors), axis=0)
#         else:
#             factorizations[n_factorizations,0] = final_factor
#         n_factorizations += 1
        
#         # sanity check, if final factor is original number
#         if not factorizations[n_factorizations-1,0] == n:
#             raise ValueError('Final factor does not match initial number.')
        
#         # crop array to number of factorizations
#         factorizations = factorizations[:n_factorizations,:]
    
#     # crop to max_n_factors
#     if max_n_factors > 0:
#         max_n_factors = min(n_prime_factors, max_n_factors)
#         cropping_idx = cropping_indices[n_prime_factors-max_n_factors]
#         factorizations = np.ascontiguousarray(factorizations[cropping_idx:,:max_n_factors])
    
#     return factorizations





@nb.njit(fastmath=True, parallel=True)
def presum_dctps_indices_numba(dctps, indices):
    """
    Presum coherence order changes.

    Parameters
    ----------
    dctps : (n_ctps,n_blocks) 2Darray
        Coherence order changes to presum.
    indices : (n_presum,n_idxs) 2Darray
        Indices to indicate which coherence order changes
        to sum up. Indices that are not between 0 and n_blocks-1 (inclusive)
        are ignored.
    
    Returns
    -------
    dctps0_presum : (n_ctps,n_presum) 2Darray
        Presummed coherence order changes.
    """
    
    # check shape of input
    if not dctps.ndim == 2:
        raise ValueError("`dctps` must be 2D.")
    if not indices.ndim == 2:
        raise ValueError("`indices` must be 2D.")
        
    n_ctps   = dctps.shape[0]
    n_blocks = dctps.shape[1]
    n_presum = indices.shape[0]
    n_idxs   = indices.shape[1]
    
    # allocate space for output
    output = np.zeros(shape=(n_ctps,n_presum), dtype=dctps.dtype)
    
    # loop over all CTPs, do in parallel
    for idx_ctp in nb.prange(n_ctps):
        
        # loop over all sets of indices
        for idx_presum in range(n_presum):
            
            for idx_idx in range(n_idxs):
                index = indices[idx_presum,idx_idx]
                # skip indices out of range
                if index < 0 or index >= n_blocks:
                    continue
                output[idx_ctp,idx_presum] += dctps[idx_ctp,index]
    
    return output







#######################################################
#                                                     #
#    III   N   N  DDDD    III    CCCC  EEEEE   SSSS   #
#     I    NN  N  D   D    I    C      E      S       #
#     I    N N N  D   D    I    C      EEE     SSS    #
#     I    N  NN  D   D    I    C      E          S   #
#    III   N   N  DDDD    III    CCCC  EEEEE  SSSS    #
#                                                     #
#######################################################

# @numba.njit()
# def _init_indices_numba(a):

#     if not a.ndim == 1:
#         raise ValueError("Error in `_next_indices_numba`: "
#                          "`a` must be a 1D array.")
    
#     n = a.size
#     a[:] = -1
#     a[0] = 0



# @numba.njit()
# def _next_indices_numba(a):
    
#     if not a.ndim == 1:
#         raise ValueError("Error in `_next_indices_numba`: "
#                          "`a` must be a 1D array.")

#     n = a.size
    
#     # find first negative entry
#     # the i after the loop breaks is the index of last non-negative entry
#     if a[0] < 0:
#         a[:] = -1
#         return -1
    
#     for imax in range(1,n):
#         if a[imax] < 0:
#             break
#         if (not a[imax] < n) or (not a[imax] > a[imax-1]):
#             a[:] = -1
#             return -1
#     # if loop ran through, only non-negative numbers, set to initial
#     else:
#         a[:] = -1
#         a[0] = 0
#         return 1
    
#     # loop in reverse order over remaining elements
#     max_val = n-1
#     for i in range(imax-1,-1,-1):
        
#         # if entry smaller than max_val, can count this element up
#         if a[i] < max_val:
#             a[i] += 1
#             # count up the following elements
#             for k in range(i+1,imax):
#                 a[k] = a[k-1] + 1
#             return 0
#         # if equal, cannot count this element up, try next one
#         elif a[i] == max_val:
#             max_val -= 1
#         # if greater, then array is not of expected form
#         else:
#             # return error indicator
#             a[:] = -1
#             return -1
            
#     else:
#         # initilaize one more non-negative element
#         for k in range(imax+1):
#             a[k] = k
#         return 0



# @numba.njit()
# def _all_indices_numba(output):
    
#     if not output.ndim == 2:
#         raise ValueError('`output` must be a 2D array.')
        
#     n = output.shape[1]
    
#     output[0,:] = -1
#     output[0,0] = 0
    
#     for i in range(1, output.shape[0]):
#         # copy previous row
#         output[i,:] = output[i-1,:]
#         # count up this line
#         res = _next_indices_numba(output[i,:])
#         if not res == 0:
#             raise ValueError('Internal error in `_all_indices_numba`: ' \
#                              'All combinations used but `output` not filled.')
            
#     # check the last row and make sure it is corrent
#     for j in range(n):
#         if not output[-1,j] == j:
#             raise ValueError('Internal error in `_all_indices_numba`: ' \
#                              'Final row in `output` is not correct.')
            
#     return 0



# @numba.njit()
# def _init_indices2D_numba(a):
    
#     if not a.ndim == 2:
#         raise ValueError("Error in `_init_indices2D_numba`: "
#                          "`a` must be a 2D array.")
    
#     m = a.shape[0]
#     n = a.shape[1]
    
#     # set the first row
#     a[0,:] = -1
#     a[0,0] = 0
    
#     # set all rows after the first one
#     for i in range(1,m):
        
#         # copy previous row
#         a[i,:] = a[i-1,:]
        
#         # find first negative index
#         for jmax in range(n):
#             if a[i,jmax] < 0: break
#         else:
#             raise ValueError("Error in `_init_indices2D_numba`: "
#                              "Cannot increase a row. Too many rows?")
        
#         # try to increase current element
#         max_val = n-1
#         for j in range(jmax-1,-1,-1):
#             if a[i,j] < max_val:
#                 a[i,j] += 1
#                 # increase all the following elements
#                 for k in range(j+1,jmax):
#                     a[i,k] = a[i,k-1] + 1
#                 break
#             elif a[i,j] == max_val:
#                 max_val -= 1
#             else:
#                 raise ValueError("Error in `_init_indices2D_numba`: "
#                                  "Invalid value.")
#         else:
#             # initilaize with one more non-negative element
#             for k in range(jmax+1):
#                 a[i,k] = k



# @numba.njit()
# def _next_indices2D_numba(a):
    
#     if not a.ndim == 2:
#         raise ValueError("`a` must be a 2D array.")
        
#     m = a.shape[0]
#     n = a.shape[1]
    
#     # loop over all cols in reversed order
#     for i in range(m-1, -1, -1):
        
#         res = _next_indices_numba(a[i])
#         if res == 0:
#             for j in range(i+1,m):
#                 a[j,:] = a[j-1,:]
#                 res = _next_indices_numba(a[j])
#                 if res == 0:
#                     continue
#                 elif res == 1:
#                     break
#                 else:
#                     a[:,:] = -1
#                     return -1
#             else:
#                 return 0
#         elif res == 1:
#             continue
#         else:
#             a[:,:] = -1
#             return -1
    
#     # set to initial configuration
#     else:
#         # set the first row
#         a[0,:] = -1
#         a[0,0] = 0
        
#         # set all rows after the first one
#         for i in range(1,m):
            
#             # copy previous row
#             a[i,:] = a[i-1,:]
            
#             # find first negative index
#             for jmax in range(n):
#                 if a[i,jmax] < 0: break
#             else:
#                 raise ValueError("Error in `_init_indices2D_numba`: "
#                                  "Cannot increase a row. Too many rows?")
            
#             # try to increase current element
#             max_val = n-1
#             for j in range(jmax-1,-1,-1):
#                 if a[i,j] < max_val:
#                     a[i,j] += 1
#                     # increase all the following elements
#                     for k in range(j+1,jmax):
#                         a[i,k] = a[i,k-1] + 1
#                     break
#                 elif a[i,j] == max_val:
#                     max_val -= 1
#                 else:
#                     raise ValueError("Error in `_init_indices2D_numba`: "
#                                      "Invalid value.")
#             else:
#                 # initilaize with one more non-negative element
#                 for k in range(jmax+1):
#                     a[i,k] = k
        
#         return 1







# @numba.njit()
# def _next_indices_numba(a):
    
#     n = a.size
    
#     # search for special flags
#     if a[0] < 0:
#         if a[0] == -1:
#             # init flag, initialize array to first configuration
#             a[0] = 0
#             for i in range(1,n):
#                 a[i] = -1
#             return 0
#         elif a[0] == -2:
#             # done flag, nothing to do
#             return 2
#         else:
#             raise ValueError('Internal error in `count_up_indices`.')
    
#     # find first negative entry
#     # the i after the loop breaks is the index of last non-negative entry
#     for i in range(n):
#         if a[i] < 0:
#             break
#     # if loop ran through, only non-negative numbers, set array to done flag
#     else:
#         for i in range(n):
#             a[i] = -2
#         return 1
    
#     # loop in reverse order over remaining elements
#     max_val = n-1
#     for j in range(i-1,-1,-1):
        
#         # if entry smaller than max_val, can count this element up
#         if a[j] < max_val:
#             a[j] += 1
#             # count up the following elements
#             for k in range(j+1,i):
#                 a[k] = a[k-1] + 1
#             return 0
        
#         # if equal, cannot count this element up, try next one
#         elif a[j] == max_val:
#             max_val -= 1
        
#         # if greater, then array is not of expected form
#         else:
#             # return error indicator
#             a[0] = -3
#             return -2
            
#     else:
#         # nothing to count up, so initilaize for iteration with one more
#         # non-negative element
#         for k in range(i+1):
#             a[k] = k
#         return 0
    
#     # we should never be here
#     a[0] = -3
#     return -3












##########################################################################################
#                                                                                        #
#   PPPP   EEEEE  RRRR   M   M  U   U  TTTTT   AAA   TTTTT   III    OOO   N   N   SSSS   #
#   P   P  E      R   R  MM MM  U   U    T    A   A    T      I    O   O  NN  N  S       #
#   PPPP   EEE    RRRR   M M M  U   U    T    AAAAA    T      I    O   O  N N N   SSS    #
#   P      E      R  R   M   M  U   U    T    A   A    T      I    O   O  N  NN      S   #
#   P      EEEEE  R   R  M   M   UUU     T    A   A    T     III    OOO   N   N  SSSS    #
#                                                                                        #
##########################################################################################

# @numba.njit()
# def _init_permutation_numba(a):
#     """Generate the initial permutation of an array inplace.

#     The initial permutation is just the sorted array.
    
#     Parameters
#     ----------
#     a : 1D array_like
#         Array for which to generate the next permutation.

#     Returns
#     -------
#     None
#     """

#     if not a.ndim == 1:
#         raise ValueError("Error in _next_permutation_numba: Only 1D arrays are supported!")
    
#     a.sort()



# @numba.njit()
# def _next_permutation_numba(a):
#     """Generate the next permutation of an array inplace.
    
#     This function mimics the C++ std::next_permutation algorithm and works
#     inplace on an already existing array. The array may have repeating elements
#     in which case only distinguishable permutations are generated.
#     The initial configuration is the array in ascending order, the final one is
#     the array in descending order, which itself will be transformed to the
#     initial configuration again by this function. In that case 1 is returned
#     instead of 0. This means that, starting from an array sorted in ascending
#     order and applying this function again and again, until 1 is returned, all
#     possible permutations have been generated.
    
#     Parameters
#     ----------
#     a : 1D array_like
#         Array for which to generate the next permutation.
    
#     Returns
#     -------
#     indicator : int
#         Indicator for the outcome of the operation. 0 if the next permutation
#         was generared and 1 when the final configuration was given and
#         transformed back to the initial one, sorted in ascending order.
#     """
    
#     if not a.ndim == 1:
#         raise ValueError("Error in _next_permutation_numba: Only 1D arrays are supported!")
    
#     n = a.size
    
#     # get left bound index ldx
#     for ldx in range(n-2,-1,-1):
#         if a[ldx] < a[ldx+1]:
#             break
#     else:
#         # array completely sorted, only reverse
#         for i in range(n//2):
#             a[i], a[-1-i] = a[-1-i], a[i]
#         return 1
    
#     # get right bound index rdx
#     for rdx in range(n-1,ldx,-1):
#         if a[rdx] > a[ldx]:
#             break
    
#     # swap ldx and rdx values
#     a[ldx], a[rdx] = a[rdx], a[ldx]
    
#     # reverse from ldx+1 to end
#     for i in range((n-ldx-1)//2):
#         a[ldx+1+i], a[-1-i] = a[-1-i], a[ldx+1+i]
    
#     return 0



# @numba.njit()
# def _fill_buffer_permutations_numba(buffer, seed):
#     """
#     Given a seed permutation, fill a given buffer with consecutive
#     permutation of an array.
    
#     Parameters
#     ----------
#     buffer : (n_buffered,n_elements) 2D array
#         Buffer array to store the permutations in.
#     seed : (n_elements,) 1D array
#         Initial permutation.
    
#     Returns
#     -------
#     n_filled : int
#         Number of permutations written to the buffer. Equal to the
#         number of rows in buffer if the buffer has been filled or smaller.
#     new_seed : (n_blocks,) 1D array
#         Seed for the next filling of the buffer.
#     all_done : bool
#         Wether the end of the counting has been reached.
#     """
    
#     # check shape of input
#     if not buffer.ndim == 2:
#         raise ValueError("`buffer` must be two dimensional!")
#     if not seed.ndim == 1:
#         raise ValueError("`seed` must be one dimensional!")
#     if not buffer.shape[1] == seed.size:
#         raise ValueError("Shapes of `buffer` and `seed` are not compatible!")
        
#     # copy seed to private working array
#     permutations_working = np.zeros_like(seed)
#     permutations_working[:] = seed[:]
    
#     # initialize the first entry
#     buffer[0,:] = permutations_working[:]
#     n_filled = 1
    
#     # fill the other rows
#     for i in range(1,buffer.shape[0]):
        
#         # try to count up
#         res = _next_permutation_numba(permutations_working)
        
#         if res == 0:
#             buffer[i,:] = permutations_working[:]
#             n_filled += 1
#         else:
#             return n_filled, permutations_working, True
        
#     # check if there is more work to do
#     res = _next_permutation_numba(permutations_working)
#     if res == 0:
#         all_done = False
#     else:
#         all_done = True
    
#     return n_filled, permutations_working, all_done



# @numba.njit()
# def _all_permutations_numba(a, output):
#     """Generate all permutations of an array.
    
#     Parameters
#     ----------
#     a : 1D (n,) array_like
#         Array to which to generate the permutations for.
#     output : 2D (m,n) array_like
#         Pre-allocated output array to store the permutations in.
    
#     Returns
#     -------
#     None    
#     """
    
#     # check dimension of input
#     if not output.ndim == 2:
#         raise ValueError('Error in `_all_permutations_numba`: ...')
#     if not a.ndim == 1:
#         raise ValueError('Error in `_all_permutations_numba`: ...')
#     if not a.size == output.shape[1]:
#         raise ValueError('Error in `_all_permutations_numba`: ...')
    
#     # copy the sorted array to a working array
#     working = np.sort(a)
    
#     # initialize the first row
#     output[0,:] = working[:]
    
#     # loop over all permutations
#     for i in range(1, output.shape[0]):
#         res = _next_permutation_numba(working)
#         if not res == 0:
#             raise ValueError('Error in `_all_permutations_numba`: Iteration not finished but no permutations left.')
#         output[i,:] = working[:]
        
#     # sanity check if really done
#     res = _next_permutation_numba(working)
#     if not res == 1:
#         raise ValueError('Error in `_all_permutations_numba`: Iteration done, but permutations are left.')



@nb.njit()
def _number_of_permutations_numba(a):
    """Find the number of permutations of a given array.
    
    Parameters
    ----------
    a : array_like
        Array to compute the number of permutations for.
    
    Returns
    -------
    n : int
        Number of permutations of the array or 0, if number is too big.
    """
    
    # find number of appearances of unique elements
    a_sorted = np.sort(a)
    counts = np.zeros_like(a_sorted, dtype=np.uint64)
    idx_counts = 0
    counts[0] += 1
    for i in range(1, a_sorted.size):
        if a_sorted[i] > a_sorted[i-1]:
            idx_counts += 1
        counts[idx_counts] += 1
        
    return _multinomcoeff_numba(a_sorted.size, counts[:idx_counts+1])



@nb.njit()
def _log2_number_of_permutations_numba(a):
    """Find the base-2 logarithm of number of permutations of a given array.
    
    Parameters
    ----------
    a : array_like
        Array to compute the number of permutations for.
    
    Returns
    -------
    n : int
        Base-2 logarithm of number of permutations of the array.
    """
    
    # find number of appearances of unique elements
    a_sorted = np.sort(a)
    counts = np.zeros_like(a_sorted, dtype=np.uint64)
    idx_counts = 0
    counts[0] += 1
    for i in range(1, a_sorted.size):
        if a_sorted[i] > a_sorted[i-1]:
            idx_counts += 1
        counts[idx_counts] += 1
        
    # crop array to number of distinguishable elements and sort
    counts = np.sort(counts[:idx_counts+1])
    
    numerator = math.lgamma(counts.sum() + 1.0)
    denominator = 0.0
    for i in range(counts.size):
        denominator += math.lgamma(counts[i] + 1.0)
    
    return ( numerator - denominator ) / np.log(2.0)



@nb.njit()
def _log2_size_all_permutations_array_numba(a):
    """TODO!!! Find the base-2 logarithm of number of permutations of a given array.
    
    Parameters
    ----------
    a : array_like
        Array to compute the number of permutations for.
    
    Returns
    -------
    n : int
        Base-2 logarithm of number of permutations of the array.
    """
    
    # find number of appearances of unique elements
    a_sorted = np.sort(a)
    counts = np.zeros_like(a_sorted, dtype=np.uint64)
    idx_counts = 0
    counts[0] += 1
    for i in range(1, a_sorted.size):
        if a_sorted[i] > a_sorted[i-1]:
            idx_counts += 1
        counts[idx_counts] += 1
        
    # crop array to number of distinguishable elements and sort
    counts = np.sort(counts[:idx_counts+1])
    
    numerator = math.lgamma(counts.sum() + 1.0)
    denominator = 0.0
    for i in range(counts.size):
        denominator += math.lgamma(counts[i] + 1.0)
    
    return ( numerator - denominator + np.log(a_sorted.size) ) / np.log(2.0)







##########################################################################################
#                                                                                        #
#    CCCC   OOO   M   M  BBBB    III   N   N   AAA   TTTTT   III    OOO   N   N   SSSS   #
#   C      O   O  MM MM  B   B    I    NN  N  A   A    T      I    O   O  NN  N  S       #
#   C      O   O  M M M  BBBB     I    N N N  AAAAA    T      I    O   O  N N N   SSS    #
#   C      O   O  M   M  B   B    I    N  NN  A   A    T      I    O   O  N  NN      S   #
#    CCCC   OOO   M   M  BBBB    III   N   N  A   A    T     III    OOO   N   N  SSSS    #
#                                                                                        #
##########################################################################################

@nb.njit()
def _next_picked_indices_numba(a, max_val):
    """
    ToDo

    Parameters
    ----------

    Returns
    -------
    """
    
    if not a.ndim == 1:
        raise ValueError('Internal error in `_next_picked_indices_numba`: '\
                         '`a` must be one dimensional.')
        
    if max_val < a.size:
        raise ValueError('Internal error in `_next_picked_indices_numba`: '\
                         '`max_val` must be at least size of `a`.')
        
    # search for special indices
    if a[0] < 0:
        if a[0] == -1:
            # init flag, initialize array to first configuration
            for i in range(a.size):
                a[i] = i
            return 0
        elif a[0] == -2:
            # done flag, nothing to do
            return 2
        else:
            raise ValueError('Internal error in `_next_picked_indices_numba`: '\
                             'Unrecognized flag.')
    
    # loop in reverse order over remaining elements
    current_max_val = max_val - 1
    for i in range(a.size-1,-1,-1):
        
        # if entry smaller than max_val, can count this element up
        if a[i] < current_max_val:
            a[i] += 1
            # count up the following elements
            for k in range(i+1, a.size):
                a[k] = a[k-1] + 1
            return 0
        
        # if equal, cannot count this element up, try next one
        elif a[i] == current_max_val:
            current_max_val -= 1
        
        # if greater, then array is not of expected form
        else:
            # return error indicator
            a[0] = -3
            return -2
            
    else:
        # nothing to count up, set array to done flag
        for j in range(a.size):
            a[j] = -2
        return 1
    
    # we should never be here
    a[0] = -3
    return -3



@nb.njit()
def _all_picked_indices_numba(max_val, output):
    """
    ToDo

    Parameters
    ----------

    Returns
    -------
    """
    
    if not output.ndim == 2:
        raise ValueError('Error in `_all_picked_indices_numba`: `output` must be 2D.')
        
    # initialize first row
    working = np.zeros(output.shape[1], dtype=output.dtype)
    for i in range(working.size):
        working[i] = i
    output[0,:] = working[:]
    
    # set the other rows
    for i in range(1, output.shape[0]):
        res = _next_picked_indices_numba(working, max_val)
        if not res == 0:
            raise ValueError('Error in `_all_picked_indices_numba`: `output` is full but rows are still left.')
        output[i,:] = working[:]
            
    # check if really done
    res = _next_picked_indices_numba(working, max_val)
    if not res == 1:
        raise ValueError('Error in `_all_picked_indices_numba`: Last row is not the final one.')
    

@nb.njit()
def _count_up_picked_indices_numba(a, max_val):
    """
    Generate the next set of indices that indicate what elements are picked
    from a list with max_val elements (without repetition, order does not
    matter counting from 0).
    
    Parameters
    ----------
    a : (n_picked,) 2D array
        Set of picked indices to increase inplace.
    max_val : int
        Number of elements to pick from.
    
    Returns
    -------
    status : int
        0 if the set of picked indices could be counted up, 1 otherwise. In
        that case the last possible set of picked indices was generated and
        the array should be back to the initial configuration.
    """
    
    if not a.ndim == 1:
        raise ValueError('Internal error in `_count_up_picked_indices_numba`: '\
                         '`a` must be one dimensional.')
    
    if max_val < a.size:
        return -1
        
    # search for special indices
    if a[0] < 0:
        return -1
    
    # loop in reverse order over remaining elements
    current_max_val = max_val - 1
    for i in range(a.size-1,-1,-1):
        
        # if entry smaller than max_val, can count this element up
        if a[i] < current_max_val:
            a[i] += 1
            # count up the following elements
            for k in range(i+1, a.size):
                a[k] = a[k-1] + 1
            return 0
        
        # if equal, cannot count this element up, try next one
        elif a[i] == current_max_val:
            current_max_val -= 1
        
        # if greater, then array is not of expected form
        else:
            # return error indicator
            a[0] = -1
            return -1
            
    else:
        # nothing to count up, set array to initial config
        for j in range(a.size):
            a[j] = j
        return 1
    
    # we should never be here
    a[0] = -1
    return -1



@nb.njit()
def _log2_size_all_picked_indices_array_numba(n, k):
    """TODO!!!! Computes the log2 of the number of elements an array with all
    unique picked indices would have.
    
    If a = [2, 2, 3, 3], then there are 6 unique permutations and the array
    containig them all will have 4*6 = 24 elements, so the function will return
    log2(24) = 4.5849... as the result.
    
    Parameters
    ----------
    n : int
        Array containing the elements.
    k : int
    
    Results
    -------
    result : float
        Log2 of the size, the array containing all permutations written
        explicitly.
    """
    
    result = math.lgamma(n+1.0)
    result -= math.lgamma(k) + math.lgamma(n-k+1.0)
    
    return result / np.log(2.0)




@nb.njit()
def _fill_buffer_picked_indices_numba(buffer, seed, max_val):
    """
    Given some indices that indicate what elements are picked from a list with
    max_val elements, fill a given buffer with consecutive sets of picked
    indices.
    
    Parameters
    ----------
    buffer : (n_buffered,n_picked) 2D array
        Buffer array to store the picked indices in.
    seed : (n_picked,) 1D array
        Initial set of picked indices.
    max_val : int
        Number of elements to pick from.
    
    Returns
    -------
    n_filled : int
        Number of sets of picked indices written to the buffer. Equal to the
        number of rows in buffer if the buffer has been filled or smaller.
    new_seed : (n_blocks,) 1D array
        Seed for the next filling of the buffer.
    all_done : bool
        Wether the end of the counting has been reached.
    """
    
    # check shape of input
    if not buffer.ndim == 2:
        raise ValueError('´buffer´ must be two dimensional!')
    if not seed.ndim == 1:
        raise ValueError('´seed´ must be one dimensional!')
    if not buffer.shape[1] == seed.size:
        raise ValueError('Shapes of ´buffer´ and ´seed´ are not compatible!')
        
    # copy seed to private working array
    picked_working = np.zeros_like(seed)
    picked_working[:] = seed[:]
    
    # initialize the first entry
    buffer[0,:] = picked_working[:]
    n_filled = 1
    
    # fill the other rows
    for i in range(1,buffer.shape[0]):
        
        # try to count up
        res = _count_up_picked_indices_numba(picked_working, max_val)
        
        if res == 0:
            buffer[i,:] = picked_working[:]
            n_filled += 1
        elif res == 1:
            return n_filled, picked_working, True
        else:
            raise ValueError('aaahhh')
            
    # check if there is more work to do
    res = _count_up_picked_indices_numba(picked_working, max_val)
    if res == 0:
        all_done = False
    else:
        all_done = True
    
    return n_filled, picked_working, all_done







#######################################################
#                                                     #
#   V   V   AAA   RRRR    III    OOO   U   U   SSSS   #
#   V   V  A   A  R   R    I    O   O  U   U  S       #
#   V   V  AAAAA  RRRR     I    O   O  U   U   SSS    #
#    V V   A   A  R  R     I    O   O  U   U      S   #
#     V    A   A  R   R   III    OOO    UUU   SSSS    #
#                                                     #
#######################################################

@nb.njit()
def is_valid_nested_numba(lengths, cycled_idxs, dctps0, n_ctps_wanted):
    """
    For a given nestcog phase cycle determine if it passes all wanted CTPs and
    blocks all unwanted CTPs.
    
    Parameters
    ----------
    lengths : ...
        ...
    cycled_idxs : ...
        ...
    dctps0 : (n_ctps, n_blocks) array of int
        Coherence order changes relative to the coherence order changes of
        the reference path. The desired paths must be given first.
    n_ctps_wanted : int
        Number of desired paths. The first n_ctps_wanted rows of dctps0 must
        be the desired paths, the following ones the undesired ones.
    
    Returns
    -------
    is_valid : int
        Wether the phase cycle is valid or not. 0 indicates a valid cycle,
        1 a cycle that filters desired paths and 2 a cycle that does not
        filter desired paths but also not all undesired paths.
    """
    
    # check size and shape of input
    if not lengths.ndim == 1:
        raise ValueError('Internal error: `lengths` must be 1D.')
    if not cycled_idxs.ndim == 2:
        raise ValueError('Internal error: `cycled_idxs` must be 2D.')
    if not dctps0.ndim == 2:
        raise ValueError('Internal error: `dctps0` must be 2D.')
    if not lengths.shape[0] == cycled_idxs.shape[0]:
        raise ValueError('Internal error: First dimensions of `lengths` '
                         'and `cycled_idxs` must have same size.')
    if not cycled_idxs.shape[1] == dctps0.shape[1]:
        raise ValueError('Internal error: Second dimensions of `cycled_idxs` '
                         'and `dctps0` must have same size.')
    if n_ctps_wanted < 0 or n_ctps_wanted > dctps0.shape[0]:
        raise ValueError('Internal error: `n_ctps_wanted` must be between 0 '
                         'and number of given CTPs.')
        
    n_subcyc = lengths.shape[0]
    n_ctps   = dctps0.shape[0]
    n_blocks = dctps0.shape[1]
    
    # loop over all wanted CTPs
    for idx_ctp in range(n_ctps_wanted):
        
        # check if any cycle blocks this CTP
        for idx_cycle in range(n_subcyc):
            if lengths[idx_cycle] <= 1:
                continue
            dcpts0summed = 0
            for idx in range(n_blocks):
                idx_block = cycled_idxs[idx_cycle, idx]
                if idx_block < 0:
                    break
                elif idx_block >= n_blocks:
                    raise ValueError("Error in `are_ctps_passed_cogwheel_numba`: "
                                     "Invalid index.")
                dcpts0summed += dctps0[idx_ctp,idx_block]
            
            # if sum is not zero, current cycle blocks CTP
            if not dcpts0summed % lengths[idx_cycle] == 0:
                return 1
    
    # loop over all unwanted CTPs
    for idx_ctp in range(n_ctps_wanted, n_ctps):
       
        # check if any cycle blocks this CTP
        for idx_cycle in range(n_subcyc):
            if lengths[idx_cycle] <= 1:
                continue
            dcpts0summed = 0
            for idx in range(n_blocks):
                idx_block = cycled_idxs[idx_cycle,idx]
                if idx_block < 0:
                    break
                elif idx_block >= n_blocks:
                    raise ValueError("Error in `are_ctps_passed_cogwheel_numba`: "
                                     "Invalid index.")
                dcpts0summed += dctps0[idx_ctp,idx_block]
            # if sum is not zero, current cycle blocks CTP
            if not dcpts0summed % lengths[idx_cycle] == 0:
                break
        else:
            # if loop does not break, CTP is passed
            return 2
    
    return 0



@nb.njit(parallel=True)
def are_valid_nested_numba(lengths, cycled_idxs, dctps0, n_ctps_wanted, n_check=0):
    """
    For a given nestcog phase cycle determine if it passes all wanted CTPs and
    blocks all unwanted CTPs.
    
    Parameters
    ----------
    lengths : ...
        ...
    cycled_idxs : ...
        ...
    dctps0 : (n_ctps, n_blocks) array of int
        Coherence order changes relative to the coherence order changes of
        the reference path. The desired paths must be given first.
    n_ctps_wanted : int
        Number of desired paths. The first n_ctps_wanted rows of dctps0 must
        be the desired paths, the following ones the undesired ones.
    
    Returns
    -------
    is_valid : int
        Wether the phase cycle is valid or not. 0 indicates a valid cycle,
        1 a cycle that filters desired paths and 2 a cycle that does not
        filter desired paths but also not all undesired paths.
    """
    
    # check size and shape of input
    if not lengths.ndim == 2:
        raise ValueError('Internal error: `lengths` must be 1D.')
    if not cycled_idxs.ndim == 3:
        raise ValueError('Internal error: `cycled_idxs` must be 2D.')
    if not dctps0.ndim == 2:
        raise ValueError('Internal error: `dctps0` must be 2D.')
    
    n_cycles = cycled_idxs.shape[0]
    n_subcyc = cycled_idxs.shape[1]
    n_blocks = cycled_idxs.shape[2]
    n_ctps   = dctps0.shape[0]
    
    if not lengths.shape[0] == n_cycles:
        raise ValueError("")
    if not lengths.shape[1] == n_subcyc:
        raise ValueError("")
    if not dctps0.shape[1] == n_blocks:
        raise ValueError("")
    if n_ctps_wanted < 0 or n_ctps_wanted > n_ctps:
        raise ValueError("")
        
    if n_check <= 0:
        # check every cycle
        n_check = n_cycles
    else:
        n_check = min(n_check, n_cycles)
        
    # allocate output array
    results = np.zeros(n_check, dtype=np.int64)
    results.fill(3)
    
    # parallel loop over all cycles
    for idx_cycle in nb.prange(n_check):
        
        # check validity of current cycle
        res = is_valid_nested_numba(lengths[idx_cycle,:], cycled_idxs[idx_cycle,:,:], 
                                    dctps0, n_ctps_wanted)
        results[idx_cycle] = res
    
    return results




@nb.njit()
def are_ctps_passed_nested_numba(lengths, cycled_idxs, dctps0):
    """
    For a given nestcog phase cycle determine if it passes all wanted CTPs and
    blocks all unwanted CTPs.
    
    Parameters
    ----------
    lengths : ...
        ...
    cycled_idxs : ...
        ...
    dctps0 : (n_ctps, n_blocks) array of int
        Coherence order changes relative to the coherence order changes of
        the reference path. The desired paths must be given first.
    
    Returns
    -------
    is_valid : int
        Wether the phase cycle is valid or not. 0 indicates a valid cycle,
        1 a cycle that filters desired paths and 2 a cycle that does not
        filter desired paths but also not all undesired paths.
    """
    
    # check size and shape of input
    if not lengths.ndim == 1:
        raise ValueError('Internal error: `lengths` must be 1D.')
    if not cycled_idxs.ndim == 2:
        raise ValueError('Internal error: `windings` must be 2D.')
    if not dctps0.ndim == 2:
        raise ValueError('Internal error: `dctps0` must be 2D.')
    if not lengths.shape[0] == cycled_idxs.shape[0]:
        raise ValueError('Internal error: First dimensions of `lengths` '
                         'and `windings` must have same size.')
    if not cycled_idxs.shape[1] == dctps0.shape[1]:
        raise ValueError('Internal error: Second dimensions of `windings` '
                         'and `dctps0` must have same size.')
        
    n_cycles = lengths.shape[0]
    n_ctps   = dctps0.shape[0]
    n_blocks = dctps0.shape[1]
    
    # allocate output array
    is_passed = np.zeros(n_ctps, dtype=np.bool_)
    
    # loop over all CTPs
    for idx_ctp in range(n_ctps):
       
        # check if any subcycle blocks this CTP
        for idx_cycle in range(n_cycles):
            if lengths[idx_cycle] <= 1:
                continue
            dcpts0summed = 0
            for idx in range(n_blocks):
                idx_block = cycled_idxs[idx_cycle,idx]
                if idx_block < 0:
                    break
                elif idx_block >= n_blocks:
                    raise ValueError("Error in `are_ctps_passed_cogwheel_numba`: "
                                     "Invalid index.")
                dcpts0summed += dctps0[idx_ctp,idx_block]
            # if sum is not zero, current cycle blocks CTP
            if not dcpts0summed % lengths[idx_cycle] == 0:
                is_passed[idx_ctp] = False
                break
        else:
            # if loop does not break, CTP is passed
            is_passed[idx_ctp] = True
    
    return is_passed








@nb.njit(fastmath=True)
def nested_check_valid_presum_numba(cycle_lengths, pulse_combi_idx,
                              dctps0_presum, n_ctps_wanted):
    
    # ToDo some sanity checks on input?
    
    n_ctps = dctps0_presum.shape[0]
    # number of different cycles including appended numbers
    n_cycles = cycle_lengths.size
    
    # loop over all wanted cycles
    for i in range(n_ctps_wanted):
        for j in range(n_cycles):
            if cycle_lengths[j] < 0: break
            # check if no cycle blocks this wanted path
            if dctps0_presum[i,pulse_combi_idx[j]] % cycle_lengths[j] != 0:
                return 1
    
    # loop over all unwanted cycles
    for i in range(n_ctps_wanted, n_ctps):
        is_blocked = False
        # check if at least one cycle blocks this unwanted path
        for j in range(n_cycles):
            if cycle_lengths[j] < 0: break
            if dctps0_presum[i,pulse_combi_idx[j]] % cycle_lengths[j] != 0:
                is_blocked = True
                break
        
        # if the last loop did not break, this path is not blocked
        if not is_blocked:
            return 2
    
    # both loops ran through, cycle is valid
    return 0



@nb.njit(fastmath=True)
def nested_check_valid_presum_all_numba(cycle_lengths,
                                        dctps0_presum, n_ctps_wanted):
    """
    ToDo
    """
    
    # some sanity checks on input
    if not cycle_lengths.ndim == 1:
        raise ValueError('kekw')
    if not dctps0_presum.ndim == 2:
        raise ValueError('kekw')
    if not cycle_lengths.size == dctps0_presum.shape[1]:
        raise ValueError('kekw')
    if n_ctps_wanted > dctps0_presum.shape[0]:
        raise ValueError('kekw')
    
    n_ctps = dctps0_presum.shape[0]
    # number of different cycles including appended numbers
    n_cycles = cycle_lengths.size
    
    # loop over all wanted cycles
    for i in range(n_ctps_wanted):
        for j in range(n_cycles):
            if cycle_lengths[j] <= 1: continue
            # check if no cycle blocks this wanted path
            if dctps0_presum[i,j] % cycle_lengths[j] != 0:
                return 1
    
    # loop over all unwanted cycles
    for i in range(n_ctps_wanted, n_ctps):
        is_blocked = False
        # check if at least one cycle blocks this unwanted path
        for j in range(n_cycles):
            if cycle_lengths[j] <= 1: continue
            if dctps0_presum[i,j] % cycle_lengths[j] != 0:
                is_blocked = True
                break
        
        # if the last loop did not break, this path is not blocked
        if not is_blocked:
            return 2
    
    # both loops ran through, cycle is valid
    return 0



@nb.njit(fastmath=True, parallel=True)
def nested_check_valid_presum_all_parallel_numba(cycle_lengths, n_check,
                                        dctps0_presum, n_ctps_wanted):
    """
    ToDo
    """
    
    # check shape and size of input
    if not cycle_lengths.ndim == 2:
        raise ValueError('lol')
    if not dctps0_presum.ndim == 2:
        raise ValueError('lol')
    if not cycle_lengths.shape[1] == dctps0_presum.shape[1]:
        raise ValueError('lol')
    if n_ctps_wanted > dctps0_presum.shape[0]:
        raise ValueError('lol')
    if n_check > cycle_lengths.shape[0]:
        raise ValueError('lol')
    
    # initialize array for output
    results = np.zeros(n_check, dtype=np.int64)
    results.fill(3)
    
    # check all given cycles
    for idx_check in nb.prange(n_check):
        results[idx_check] = nested_check_valid_presum_all_numba(cycle_lengths[idx_check,:], dctps0_presum, n_ctps_wanted)
    return results
    








@nb.njit()
def search_nested_exhaustive_presum1(n_scans_max, cycles_out, dctps0_presum, n_wanted, n_scans_min=2, verbose=0):
    
    # check all input arrays for correct shape
    if not dctps0_presum.ndim == 2:
        raise ValueError('1')
    if  dctps0_presum.shape[0] < n_wanted:
        raise ValueError('2')
    if not cycles_out.ndim == 2:
        raise ValueError('3')
    if not cycles_out.shape[1] == dctps0_presum.shape[1]:
        raise ValueError('4')
    
    n_ctps = dctps0_presum.shape[0]
    n_combinations = dctps0_presum.shape[1]
    
    # number of cycles to find
    n_find = cycles_out.shape[0]
    n_found = 0
    all_found = False
    
    # find the minimum and maximum number of scans checked
    n_scans_min = max(2, n_scans_min)
    n_scans_max = max(n_scans_min, n_scans_max)
    # protect against unreasonably high number of scans
    if np.log2(n_scans_max) > 32.0:
        raise ValueError("Won't search cycles with more than 2^32 scans.")
    
    # show what will happen
    if verbose > 0:
        print('='*80)
        print("Number of pathways:", n_ctps)
        print("Number of wanted pathways:", n_wanted)
        print('Will search number of scans from {n_scans_min} to {n_scans_max}.')
        print('='*80)
    
    # sizes for buffer
    N_BYTES_PERM_BUFFER = 8*1024*1024
    N_BYTES_INT = 8
    
    # allocate space for buffer for maximum number of factors
    size_buffer_perm = N_BYTES_PERM_BUFFER // (N_BYTES_INT * n_combinations)
    buffer_perm = np.zeros(dtype=np.int64, shape=(size_buffer_perm, n_combinations))
    
    
    for n_scans in range(n_scans_min, n_scans_max+1):
        
        if verbose > 1:
            print('\n'+'-'*80)
            print('number of scans:', n_scans)
        
        factorizations = _generate_all_factorizations_numba(n_scans, n_combinations)
        n_factorizations = factorizations.shape[0]
        n_factors = factorizations.shape[1]

        # loop over all factorizations
        for idx_factorization in range(n_factorizations):
            
            if verbose > 2:
                print('factorization:', factorizations[idx_factorization,:])
            
            seed_perm = np.ones(n_combinations, dtype=buffer_perm.dtype)
            seed_perm[:n_factors] = factorizations[idx_factorization,:]
            seed_perm.sort()
            
            while(True):
                
                n_filled_perm, seed_perm, all_done_perm = _fill_buffer_permutations_numba(buffer_perm, seed_perm)
                
                results = nested_check_valid_presum_all_parallel_numba(buffer_perm,
                                                                       n_filled_perm,
                                                                       dctps0_presum,
                                                                       n_wanted)
                
                # check the results
                for idx_res in range(results.size):
                    if results[idx_res] == 0:
                        cycles_out[n_found,:] = buffer_perm[idx_res,:]
                        n_found += 1
                        if n_found >= n_find:
                            all_found = True
                            all_done_perm = True
                            break
                            
                if all_done_perm:
                    break
            
            if all_found:
                break
        
        if n_found > 0:
            break
                               
    return n_found



@nb.njit()
def search_nested_exhaustive_presum2(n_scans_max, cycles_out, dctps0_presum, n_wanted, n_scans_min=2, verbose=0):
    """ToDo"""
    
    # check shape of input
    if not dctps0_presum.ndim == 2:
        raise ValueError('Todo')
    if dctps0_presum.shape[0] < n_wanted:
        raise ValueError('Todo')
    if not cycles_out.ndim == 2:
        raise ValueError('TODO')
    if not cycles_out.shape[1] == dctps0_presum.shape[1]:
        raise ValueError('TODO')   
    
    n_ctps = dctps0_presum.shape[0]
    n_combinations = dctps0_presum.shape[1]
    
    # number of cycles to find
    n_find = cycles_out.shape[0]
    n_found = 0
    all_found = False
    
    # clean up input number of scans
    n_scans_min = max(2, n_scans_min)
    n_scans_max = max(n_scans_min, n_scans_max)
    # protect against unreasonably high number of scans
    if np.log2(n_scans_max) > 32.0:
        raise ValueError("Won't search cycles with more than 2^32 scans.")
    
    # sizes for buffer
    N_BYTES_PERM_BUFFER = 8*1024*1024
    N_BYTES_COMB_BUFFER = 64*1024*1024
    N_BYTES_INT = 8
    N_BYTES_PERM_BUFFER_LOG2 = np.log2(N_BYTES_PERM_BUFFER)
    N_BYTES_COMB_BUFFER_LOG2 = np.log2(N_BYTES_COMB_BUFFER)
    N_BYTES_INT_LOG2 = np.log2(N_BYTES_INT)
    
    # show what will happen
    if verbose > 0:
        print('='*80)
        print("Number of pathways:", n_ctps)
        print("Number of wanted pathways:", n_wanted)
        print('Will search number of scans from {n_scans_min} to {n_scans_max}.')
        print('='*80)
    
    
    for n_scans in range(n_scans_min, n_scans_max+1):
        
        if verbose > 1:
            print('\n'+'-'*80)
            print('number of scans:', n_scans)
        
        # generate all factorizations
        factorizations = _generate_all_factorizations_numba(n_scans, n_combinations)
        n_factorizations = factorizations.shape[0]
        
        # loop over all factorizations
        for idx_factorization in range(n_factorizations):
            
            # clean up the factorization
            factorization = _delete_ones_numba(factorizations[idx_factorization,:])
            n_factors = factorization.shape[0]
            
            if verbose > 2:
                print(n_factors, 'factor(s):', factorization)
            
            
            # build cache for permutations
            log2_size_perm = _log2_size_all_permutations_array_numba(factorization)
            if log2_size_perm > N_BYTES_PERM_BUFFER_LOG2 - N_BYTES_INT:
                size_buffer_perm = N_BYTES_PERM_BUFFER // (n_factors * N_BYTES_INT)
                buffer_perm = np.zeros((size_buffer_perm, n_factors), dtype=factorization.dtype)
                #raise ValueError('MANUELLER ABBRUCH')
            else:
                size_buffer_perm = _number_of_permutations_numba(factorization)
                buffer_perm = np.zeros((size_buffer_perm, n_factors), dtype=factorization.dtype)
            
            # build cache for picked indices
            log2_size_comb = _log2_size_all_picked_indices_array_numba(n_combinations, n_factors)
            if log2_size_comb > N_BYTES_COMB_BUFFER_LOG2 - N_BYTES_INT:
                size_buffer_comb = N_BYTES_COMB_BUFFER // (N_BYTES_INT * n_factors)
                buffer_comb = np.zeros((size_buffer_comb, n_factors), dtype=factorizations.dtype)
                #raise ValueError('MANUELLER ABBRUCH')
            else:
                size_buffer_comb = _binomcoeff_numba(n_combinations, n_factors)
                buffer_comb = np.zeros((size_buffer_comb, n_factors), dtype=factorizations.dtype)
            
                
            # init seeds for buffers
            seed_perm = np.sort(factorization)
            seed_comb = np.zeros(n_factors, dtype=np.int64)
            for i in range(n_factors):
                seed_comb[i] = i
            
            # generate all permutations and combinations of indices
            # loop for permutations
            while(True):
                
                # fill the permutation buffer
                n_filled_perm, seed_perm, all_done_perm = _fill_buffer_permutations_numba(buffer_perm, seed_perm)
                
                # loop for combinations of indices
                while(True):
                    
                    # fill the combination buffer
                    n_filled_comb, seed_comb, all_done_comb = _fill_buffer_picked_indices_numba(buffer_comb, seed_comb, n_combinations)
                                        
                    # loop over all
                    for idx_perm in range(n_filled_perm):
                        for idx_comb in range(n_filled_comb):
                            
                            res = nested_check_valid_presum_numba(buffer_perm[idx_perm],
                                                                  buffer_comb[idx_comb],
                                                                  dctps0_presum,
                                                                  n_wanted)
                            
                            if res == 0:
                                for i in range(n_factors):
                                    cycles_out[n_found, buffer_comb[idx_comb,i]] = buffer_perm[idx_perm,i]
                                n_found += 1
                                if n_found >= n_find:
                                    all_found = True
                                    all_done_comb = True
                                    all_done_perm = True
                                    break
                            
                        if all_found:
                            break
                
                    if all_done_comb:
                        break
                
                if all_done_perm:
                    break
                
            if all_found:
                break
                
        if n_found > 0:
            break
    
    return n_found









# @numba.njit()
# def nested_check_valid_numba(cycle_lengths, pulses_idxs, dctps0, n_ctps_wanted):
#     """
#     ToDo

#     Parameters
#     ----------

#     Returns
#     -------
#     """
    
#     n_ctps = dctps0.shape[0]
#     n_cycles = cycle_lengths.size

#     # loop over all wanted paths
#     for idx_path in range(n_ctps_wanted):
        
#         # loop over all cycles
#         for idx_cycle in range(n_cycles):

#             # skip cylces of length one as they do not filter anything
#             if cycle_lengths[idx_cycle] == 1:
#                 continue
#             # cycle length smaller than one indicates break point
#             if cycle_lengths[idx_cycle] < 1:
#                 break
            
#             # sum up total coherence change
#             dcpts0_summed = 0
#             for idx_pulse in pulses_idxs[idx_cycle]:
#                 if idx_pulse < 0: break
#                 dcpts0_summed += dctps0[idx_path, idx_pulse]
            
#             # if any cycle blocks any desired path then stop
#             if dcpts0_summed % cycle_lengths[idx_cycle] != 0:
#                 return 1
            
#     # loop over all unwanted paths
#     for idx_path in range(n_ctps_wanted, n_ctps):
        
#         # loop over all cycles
#         is_blocked = False
#         for idx_cycle in range(n_cycles):

#             # skip cylces of length one as they do not filter anything
#             if cycle_lengths[idx_cycle] == 1:
#                 continue
#             # cycle length smaller than one indicates break point
#             if cycle_lengths[idx_cycle] < 1:
#                 break
            
#             # sum up total coherence change
#             dcpts0_summed = 0
#             for idx_pulse in pulses_idxs[idx_cycle]:
#                 if idx_pulse < 0: break
#                 dcpts0_summed += dctps0[idx_path, idx_pulse]
            
#             # if this path is blocked by current cycle, we can stop checking it
#             if dcpts0_summed % cycle_lengths[idx_cycle] != 0:
#                 is_blocked = True
#                 break
        
#         # break loop if any unwanted path is passed
#         if not is_blocked:
#             return 2

#     return 0



# @numba.njit()
# def nested_check_valid_presum_numba(cycle_lengths, pulse_combi_idx, dctps0_presum, n_ctps_wanted):
#     """
#     ToDo

#     Parameters
#     ----------

#     Returns
#     -------
#     """
    
#     # ToDo some sanity checks on input?
    
#     n_ctps = dctps0_presum.shape[0]
#     n_cycles = cycle_lengths.size
    
#     # loop over all wanted cycles
#     for idx_path in range(n_ctps_wanted):
#         for idx_cycle in range(n_cycles):
            
#             # skip cylces of length one as they do not filter anything
#             if cycle_lengths[idx_cycle] == 1:
#                 continue
#             # cycle length smaller than one indicates break point
#             if cycle_lengths[idx_cycle] < 1:
#                 break
            
#             # check if no cycle blocks this wanted path
#             if dctps0_presum[idx_path, pulse_combi_idx[idx_cycle]] % cycle_lengths[idx_cycle] != 0:
#                 return 1
    
#     # loop over all unwanted cycles
#     for idx_path in range(n_ctps_wanted, n_ctps):
#         is_blocked = False
#         # check if at least one cycle blocks this unwanted path
#         for idx_cycle in range(n_cycles):
            
#             # skip cylces of length one as they do not filter anything
#             if cycle_lengths[idx_cycle] == 1:
#                 continue
#             # cycle length smaller than one indicates break point
#             if cycle_lengths[idx_cycle] < 1:
#                 break
            
#             if dctps0_presum[idx_path, pulse_combi_idx[idx_cycle]] % cycle_lengths[idx_cycle] != 0:
#                 is_blocked = True
#                 break
        
#         # if the last loop did not break, this path is not blocked
#         if not is_blocked:
#             return 2
    
#     # both loops ran through, cycle is valid
#     return 0


