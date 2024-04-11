import math
import numpy as np
import numba
from .core.generators import _next_windings_numba
from .core.numbers import _generate_all_factorizations_numba
from .core.array import _copy_by_mask_numba



##########################################################################
#                                                                        #
#   CCCC   OOO   N   N  V   V  EEEEE  N   N   III   EEEEE   CCCC  EEEEE  #
#  C      O   O  NN  N  V   V  E      NN  N    I    E      C      E      #
#  C      O   O  N N N  V   V  EEE    N N N    I    EEE    C      EEE    #
#  C      O   O  N  NN   V V   E      N  NN    I    E      C      E      #
#   CCCC   OOO   N   N    V    EEEEE  N   N   III   EEEEE   CCCC  EEEEE  #
#                                                                        #
##########################################################################



def number_of_nestcogs(sublengths, n_blocks, last_zero, no_inverse):
    """
    Compute the number of nested cogwheel phase cycles.
    
    Parameters
    ----------
    sublengths : (n_subcyc,) array_like
        Number of scans for the cogwheel cycle.
    n_blocks : int
        Number of pulse blocks.
    no_inverse : bool
        Whether to avoid phase inverted counterparts.
    last_zero : bool
        Whether the last winding number shoud be kept zero. This is reasonable
        if all CTPs have the same total coherence order change as the reference
        path because then only the differences between winding numbers do
        really matter.
    
    Returns
    -------
    n_nestcog : int
        Number of nested cogwheel cycles.    
    """
    
    sublengths = np.asarray(sublengths, dtype=int)
    
    if np.any(sublengths < 1):
        raise ValueError("All subcycle lengths must be at least 1.")
    if not np.any(sublengths > 1):
        return 0
    
    if last_zero:
        n_blocks = n_blocks - 1
    
    lengths, counts = np.unique(sublengths, return_counts=True)
    
    n_nestcog = 1
    for i in range(lengths.size):
        
        if lengths[i] == 1:
            continue
        
        if no_inverse:
            n_subcog = (lengths[i]**n_blocks + (2 - lengths[i]%2)**n_blocks)//2 - 1
        else:
            n_subcog = lengths[i]**n_blocks - 1
        
        if n_subcog < counts[i]:
            return 0
        
        acc = n_subcog
        for j in range(1,counts[i]):
            acc = acc*(n_subcog-j) // (j+1)
        n_nestcog *= acc
    
    return n_nestcog





def nestcog_to_phases(windings, lengths, unit='n_scans'):
    """
    Convert a set of nestcog winding numbers to a list of phases.
    
    Parameters
    ----------
    windings : (n_cycles,n_blocks) array_like of int
        Set of winding numbers, one for each cycled block.
    lengths : (n_cycles,) array of int
        Number of scans. Should be at least 2.
    unit : str (optional)
        Unit of the phases. Default is 'n_scans' (full rotation = n_scans).
        Other possible values are 'rad' or 'radiant' for phase in radian 
        (full rotation = 2pi) or 'deg' or 'degree' (full rotation = 360) for
        degree or 'turn' or 'tr' for turns (full rotation = 1).
    
    Returns
    -------
    phases : (n_blocks, n_scans) array
        Phases for every scan and block in specified unit.
    """
    
    # convert windings and lengths and check dimensionality
    windings = np.asarray(windings)
    lengths = np.asarray(lengths)
    if not windings.ndim == 2:
        raise ValueError("`windings` must be a 2D array.")
    if not lengths.ndim == 1:
        raise ValueError("`lengths` must be a 1D array.")
    n_subcyc = windings.shape[0]
    n_blocks = windings.shape[1]
    if not lengths.size == n_subcyc:
        raise ValueError("Size of `lengths` must match first dimension of `windings`.")
        
    if np.any(lengths<1):
        raise ValueError("All subcycle lengths `lengths` should be at least 1.")
    n_scans = np.prod(lengths)
        
    # allocate array
    phases = np.zeros(shape=(n_scans,n_blocks), dtype=windings.dtype)
    
    # set phases using numba routine
    _nestcog_to_phases_numba(windings, lengths, phases)
    
    # convert to specified units
    if unit.lower() in ['n_scans', 'nscnas', 'scans']:
        return phases
    elif unit.lower() in ['rad', 'radian', 'si']:
        return phases * (2.0*np.pi/n_scans)
    elif unit.lower() in ['deg', 'degree', '°']:
        return phases * (360.0/n_scans)
    elif unit.lower() in ['turn', 'tr', 'pla']:
        return phases * (1.0/n_scans)
    else:
        raise ValueError("Unkown unit '{}', try 'n_scans', 'radian' or 'degree'.".format(unit))





def nestcogs_to_phases(windings, lengths, unit='n_scans'):
    """
    Convert a set of nestcog winding numbers to a list of phases.
    
    Parameters
    ----------
    windings : (n_cycles,n_blocks) array_like of int
        Set of winding numbers, one for each cycled block.
    lengths : (n_cycles,) array of int
        Number of scans. Should be at least 2.
    unit : str (optional)
        Unit of the phases. Default is 'n_scans' (full rotation = n_scans).
        Other possible values are 'rad' or 'radiant' for phase in radian 
        (full rotation = 2pi) or 'deg' or 'degree' (full rotation = 360) for
        degree or 'turn' or 'tr' for turns (full rotation = 1).
    
    Returns
    -------
    phases : (n_blocks, n_scans) array
        Phases for every scan and block in specified unit.
    """
    
    # convert windings and lengths and check dimensionality
    windings = np.asarray(windings)
    lengths = np.asarray(lengths)
    if not windings.ndim == 3:
        raise ValueError("`windings` must be a 3D array.")
    if not lengths.ndim == 2:
        raise ValueError("`lengths` must be a 2D array.")
    n_cycles = windings.shape[0]
    n_subcyc = windings.shape[1]
    n_blocks = windings.shape[2]
    if not lengths.shape[1] == n_subcyc:
        raise ValueError("Second dimension of `lengths` must match second dimension of `windings`.")
        
    if np.any(lengths<1):
        raise ValueError("All subcycle lengths `lengths` should be at least 1.")
    n_scans = np.prod(lengths[0])
    for idx_cyc in range(n_cycles):
        if not n_scans == np.prod(lengths[idx_cyc]):
            raise ValueError("All cycles must have the same number of scans.")
        
    # allocate array
    phases = np.zeros(shape=(n_cycles,n_scans,n_blocks), dtype=windings.dtype)
    
    # set phases using numba routine
    _nestcogs_to_phases_numba(windings, lengths, phases)
    
    # convert to specified units
    if unit.lower() in ['n_scans', 'nscnas', 'scans']:
        return phases
    elif unit.lower() in ['rad', 'radian', 'si']:
        return phases * (2.0*np.pi/n_scans)
    elif unit.lower() in ['deg', 'degree', '°']:
        return phases * (360.0/n_scans)
    elif unit.lower() in ['turn', 'tr', 'pla']:
        return phases * (1.0/n_scans)
    else:
        raise ValueError("Unkown unit '{}', try 'n_scans', 'radian' or 'degree'.".format(unit))




#####################################################################
#                                                                   #
#   U   U  TTTTT   III   L       III   TTTTT   III   EEEEE   SSSS   #
#   U   U    T      I    L        I      T      I    E      S       #
#   U   U    T      I    L        I      T      I    EEE     SSS    #
#   U   U    T      I    L        I      T      I    E          S   #
#    UUU     T     III   LLLLL   III     T     III   EEEEE  SSSS    #
#                                                                   #
#####################################################################



@numba.njit(['u1(u1[:])', 'u2(u2[:])', 'u4(u4[:])', 'u8(u8[:])',
             'i1(i1[:])', 'i2(i2[:])', 'i4(i4[:])', 'i8(i8[:])'],
            cache=True)
def _smallest_common_divisor_numba(a):
    """
    Find the smallest common divisor greater than one among a list of integers.
    Numbers smaller than one are ignored.
    
    The smallest number greater than one is found in `a`. Then, all possible
    prime factors (using 6k+-1 filter) are searched in ascending order.
    If all numbers (greater than zero) in `a` share this factor, it is the
    smallest common factor.
    
    Parameters
    ----------
    a : array_like of int
        Numbers to get the smallest common divisor of.
    
    Returns
    -------
    smallest_common : int
        Smallest common divisor greater than one, or one not all numbers share
        a factor (or if all numbers are smaller than or equal to one).
    """
    
    if not a.ndim == 1:
        raise ValueError("`a` must be a 1D array.")
    
    n = a.size
    
    # get minimum value greater than one
    a_min = a[0]
    for i in range(n):
        if a[i] > 1:
            a_min = a[i]
            break
    else:
        return 1
    for j in range(i+1,n):
        if a[j] > 1 and a[j] < a_min:
            a_min = a[j]
    
    # divisibility by 2
    if a_min%2 == 0:
        a_min = a_min//2
        # iterate over array elements greater than 0, see if all are divisible
        for i in range(n):
            if a[i] < 1: continue
            if not a[i]%2 == 0: break
        else:
            return 2
        # divide out this factor
        while a_min%2 == 0:
            a_min = a_min//2
    
    # divisibility by 3
    if a_min%3 == 0:
        a_min = a_min//3
        # iterate over array elements greater than 0, see if all are divisible
        for i in range(n):
            if a[i] < 1: continue
            if not a[i]%3 == 0: break
        else:
            return 3
        # divide out this factor
        while a_min%3 == 0:
            a_min = a_min//3
    
    # divisibility by all other prime factors (6k+-1 filter)
    div = 5
    while a_min > 1:
        
        if a_min%div == 0:
            a_min = a_min//div
            # iterate over array elements greater than 0, see if all are divisible
            for i in range(n):
                if a[i] < 1: continue
                if not a[i]%div == 0: break
            else:
                return div
            # divide out this factor
            while a_min%div == 0:
                a_min = a_min//div
            
        if a_min%(div+2) == 0:
            a_min = a_min//(div+2)
            # iterate over array elements greater than 0, see if all are divisible
            for i in range(n):
                if a[i] < 1: continue
                if not a[i]%(div+2) == 0: break
            else:
                return (div+2)
            # divide out this factor
            while a_min%(div+2) == 0:
                a_min = a_min//(div+2)
        
        div += 6
    
    return 1



# @numba.njit(['u1(u1[:])', 'u2(u2[:])', 'u4(u4[:])', 'u8(u8[:])',
#              'i1(i1[:])', 'i2(i2[:])', 'i4(i4[:])', 'i8(i8[:])'],
#             cache=True)
# def _OLD_smallest_common_divisor_numba(numbers):
#     """
#     Find the smallest common divisor greater than one among a list of integers.
    
#     First the greatest common divisor among all numbers is computed, whose
#     divisors are also divisors of all numbers. Then the smallest prime divisor
#     of the gcd is returned, which also is the smallest common divisor greater
#     than one. One is returned if at least two numbers are coprime and zero if
#     all numbers are zero themselves.
    
#     Parameters
#     ----------
#     numbers : array_like of int
#         Numbers to get the smallest common divisor of.
    
#     Returns
#     -------
#     smallest_common : int
#         Smallest common divisor greater than one, one if not all numbers share
#         a factor or zero if all numbers are zero.
#     """
    
#     numbers = numbers.flatten()
#     DTYPE = type(numbers[0])
    
#     # find common gcd of all numbers
#     gcd = DTYPE(0)
#     for i in range(numbers.size):
#         gcd = np.gcd(gcd, numbers[i])
#         if gcd == 1:
#             return 1
        
#     # handle smaller cases
#     if gcd <= 3:
#         if gcd == 0:
#             # if all numbers are zero
#             return 0
#         elif gcd == 1:
#             # if at least one number is one or at least two numbers are coprime
#             return 1
#         elif gcd == 2:
#             return 2
#         elif gcd == 3:
#             return 3
#         else:
#             raise ValueError('Internal error: gcd has invalid value.')
    
#     # smallest prime factor of gcd, check divisibility by 2 and 3
#     if gcd % 2 == 0:
#         return 2
#     if gcd % 3 == 0:
#         return 3
    
#     # check all possible divisors of form 6*n +- 1 up to sqrt(gcd)
#     stop = int(np.floor(np.sqrt(gcd)))
#     i = 7
#     while i <= stop:
#         if gcd % (i-2) == 0:
#             return i-2
#         if gcd % i == 0:
#             return i
#         i += 6
     
#     # this factor might have been skipped by previous loop
#     if i-2 <= stop:
#         if gcd % (i-2) == 0:
#             return i-2
    
#     # if we are here, gcd is prime, so just return it as smallest common factor
#     return gcd


@numba.njit()
def _nestcog_to_phases_numba(windings, lengths, phases):
    """Utility"""
    
    # check dimensionality and shape of input
    if not windings.ndim == 2:
        raise ValueError("Error in `_nestcog_to_phases_numba`: `windings` must be 2D.")
    if not lengths.ndim == 1:
        raise ValueError("Error in `_nestcog_to_phases_numba`: `lengths` must be 1D.")
    n_subcyc = windings.shape[0]
    n_blocks = windings.shape[1]
    if not lengths.size == n_subcyc:
        raise ValueError("Size of `lengths` must match first dimension of `windings`.")
    
    # check subcycle lengths and compute number of scans
    if np.any(lengths<1):
        raise ValueError("Error in `_nestcog_to_phases_numba`: All subcycle lengths "
                         "`lengths` should be at least 1.")
    n_scans = np.prod(lengths)
    
    # check dimensionality and shape of output array
    if not phases.ndim == 2:
        raise ValueError("Error in `_nestcog_to_phases_numba`: `phases` must be 2D.")
    if (not phases.shape[0] == n_scans) or (not phases.shape[1] == n_blocks):
        raise ValueError("Error in `_nestcog_to_phases_numba`: `phases` must be of "
                         "shape (n_scans,n_blocks).")
    
    cumprod = 1
    for idx_sub in range(n_subcyc):
        
        for i in range(1, lengths[idx_sub]):
            increment = n_scans // lengths[idx_sub]
            
            for j in range(cumprod):
                pivot = i*cumprod+j
            
                for idx_block in range(n_blocks):
                    phases[pivot,idx_block] = (phases[pivot-cumprod,idx_block] 
                                               + windings[idx_sub, idx_block]*increment)%n_scans
        
        cumprod *= lengths[idx_sub]



@numba.njit(parallel=True)
def _nestcogs_to_phases_numba(windings, lengths, phases):
    """Utility"""
    
    # check dimensionality and shape of input
    if not windings.ndim == 3:
        raise ValueError("Error in `_nestcogs_to_phases_numba`: `windings` must be 3D.")
    if not lengths.ndim == 2:
        raise ValueError("Error in `_nestcogs_to_phases_numba`: `lengths` must be 2D.")
    n_cycles = windings.shape[0]
    n_subcyc = windings.shape[1]
    n_blocks = windings.shape[2]
    if not lengths.shape[1] == n_subcyc:
        raise ValueError("Error in `_nestcogs_to_phases_numba`: Second dimension "
                         "`lengths` must match second dimension of `windings`.")
    
    # check subcycle lengths and compute number of scans
    if np.any(lengths<1):
        raise ValueError("Error in `_nestcogs_to_phases_numba`: All subcycle lengths "
                          "`lengths` should be at least 1.")
    n_scans = np.prod(lengths[0,:])
    for idx_cyc in range(n_cycles):
        if not n_scans == np.prod(lengths[idx_cyc,:]):
            raise ValueError("Error in `_nestcog_to_phases_numba`: All cycles must have "
                              "the same number of scans.")
    
    # check dimensionality and shape of output array
    if not phases.ndim == 3:
        raise ValueError("Error in `_nestcog_to_phases_numba`: `phases` must be 3D.")
    if (not phases.shape[1] == n_scans) or (not phases.shape[2] == n_blocks):
        raise ValueError("Error in `_nestcog_to_phases_numba`: `phases` must be of "
                          "shape (n_scans,n_blocks).")
        
    for idx_cyc in numba.prange(n_cycles):
        
        _nestcog_to_phases_numba(
            windings[idx_cyc,:,:],
            lengths[idx_cyc,:],
            phases[idx_cyc,:,:])




############################################################
#                                                          #
#   CCCC   OOO   U   U  N   N  TTTTT   III   N   N   GGGG  #
#  C      O   O  U   U  NN  N    T      I    NN  N  G      #
#  C      O   O  U   U  N N N    T      I    N N N  G  GG  #
#  C      O   O  U   U  N  NN    T      I    N  NN  G   G  #
#   CCCC   OOO    UUU   N   N    T     III   N   N   GGG   #
#                                                          #
############################################################



# @numba.njit(['i8(i8[:,:],i8[:],i8[:,:],b1,b1,b1,b1)',
#              'i8(u8[:,:],u8[:],u8[:,:],b1,b1,b1,b1)',
#              'i4(i4[:,:],i4[:],i4[:,:],b1,b1,b1,b1)',
#              'i4(u4[:,:],u4[:],u4[:,:],b1,b1,b1,b1)'
#              'i2(i2[:,:],i2[:],i2[:,:],b1,b1,b1,b1)',
#              'i2(u2[:,:],u2[:],u2[:,:],b1,b1,b1,b1)'],
#             fastmath=True, cache=False)
@numba.njit(fastmath=True)
def _init_nestwind_numba(windings, lengths, factorizations,
            last_zero, no_inverse, no_cfscan, no_cfwind):
    """
    Generate the first set of nestcog parameters, than includes the next
    set of winding numbers and subcycle lengths.
    
    Parameters
    ----------
    windings : (n_factors,n_blocks) 2D array of int
        Winding numbers. The last rows corresponding the lengths of one are
        ignored and should be zero.
    lengths : (n_factors,) 1D array of int
        Subcycle lengths for each subcycle. The lengths must be sorted but the
        last elements can be one and are ignored.
    factorizations : (n_factorizations,n_factors) 2D array of int
        All possible factorizations to consider. If the set of winding numbers
        cannot be counted up, the next factorization is set for lengths.
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
    status : int
        0 if the set of winding numbers could be initialized. Negative numbers 
        indicate errors.
    """
    
    # check shape and size of input
    if not windings.ndim == 2:
        raise ValueError("Error in `_init_nestwind_numba`: "
                "`windings` must be a 2D array.")
    if not lengths.ndim == 1:
        raise ValueError("Error in `_init_nestwind_numba`: "
                "`lengths` must be a 2D array.")
    if not factorizations.ndim == 2:
        raise ValueError("Error in `_init_nestwind_numba`: "
                "`factorizations` must be a 2D array.")
    if not windings.shape[0] == lengths.size:
        raise ValueError("Error in `_init_nestwind_numba`: "
                "First dimension of `windings` must equal size of `lengths`.")
    if not factorizations.shape[1] == lengths.size:
        raise ValueError("Error in `_init_nestwind_numba`: "
                "Second dimension of `factorizations` must equal size of `lengths`.")
        
    # set some shape parameters
    n_factors        = windings.shape[0]        # maximum number of factors
    n_blocks         = windings.shape[1]        # number of blocks in pulse sequence
    n_factorizations = factorizations.shape[0]  # total number of factorizations 
    
    # try to init windings
    for idx_factorization in range(n_factorizations):
        
        # set the current factorization
        lengths[:] = factorizations[idx_factorization,:]
    
        # try to init for this factorization
        
        # find number of subcycles and check lengths array
        for idx in range(n_factors):
            # check if value 
            if lengths[idx] <= 1:
                # check if value is greater than one
                if lengths[idx] < 1:
                    raise ValueError("Error in `_init_nestwind_numba`: "
                            "All values in `lengths` must be at least 1.")
                # if one, all next numbers must be one as well
                if lengths[idx] == 1:
                    n_subcyc = idx
                    for jdx in range(idx+1, lengths.size):
                        if not lengths[jdx] == 1:
                            raise ValueError("Error in `_init_nestwind_numba`: "
                                    "The last values of `lengths` must all be one.")
                    break
            # check order
            if idx > 0:
                if lengths[idx] < lengths[idx-1]:
                    raise ValueError("Error in `_init_nestwind_numba`: "
                            "`lengths` must be sorted except for the last values equal to 1.")        
        else:
            n_subcyc = n_factors
        
        # init first row
        windings[0,:] = 0
        windings[0,0] = 1
        
        # loop over all other rows and try to init them
        no_overflow = True
        for idx in range(1, n_subcyc):

            # if same cycle lengths, avoid repetition
            if lengths[idx] == lengths[idx-1]:
                # copy previous line and try to count up
                windings[idx,:] = windings[idx-1,:]
                res = _next_windings_numba(windings[idx,:], lengths[idx],
                        last_zero, no_inverse, no_cfscan, no_cfwind)
                if res == 0:
                    continue
                elif res == 1:
                    # overflow happened, try next factorization
                    no_overflow = False
                    break
                else:
                    raise ValueError("Error in `_init_nestwind_numba`: "
                            "Error when counting up winding numbers.")
            
            # if longer cycle, init next row
            elif lengths[idx] > lengths[idx-1]:
                windings[idx,:] = 0
                windings[idx,0] = 1
            
            # cycle lenghts must be ordered
            else:
                raise ValueError("Error in `_init_nestwind_numba`: "
                        "`lengths` must be sorted except for the last values equal to 1.")
        
        if no_overflow:
            windings[n_subcyc:,:] = 0
            return 0
    
    # the loop must break
    else:
        raise ValueError("Error in `_init_nestwind_numba`: "
                "Could not initialize with any factorization.")





# @numba.njit(['i8(i8[:,:],i8[:],i8[:,:],b1,b1,b1,b1)',
#              'i8(u8[:,:],u8[:],u8[:,:],b1,b1,b1,b1)',
#              'i4(i4[:,:],i4[:],i4[:,:],b1,b1,b1,b1)',
#              'i4(u4[:,:],u4[:],u4[:,:],b1,b1,b1,b1)'
#              'i2(i2[:,:],i2[:],i2[:,:],b1,b1,b1,b1)',
#              'i2(u2[:,:],u2[:],u2[:,:],b1,b1,b1,b1)'],
#             fastmath=True, cache=False)
@numba.njit(fastmath=True)
def _next_nestwind_numba(windings, lengths, factorizations,
                    last_zero, no_inverse, no_cfscan, no_cfwind):
    """
    Generate the next set of nestcog parameters, than includes the next
    set of winding numbers and subcycle lengths.
    
    Parameters
    ----------
    windings : (n_factors,n_blocks) 2D array of int
        Winding numbers. The last rows corresponding the lengths of one are
        ignored and should be zero.
    lengths : (n_factors,) 1D array of int
        Subcycle lengths for each subcycle. The lengths must be sorted but the
        last elements can be one and are ignored.
    factorizations : (n_factorizations,n_factors) 2D array of int
        All possible factorizations to consider. If the set of winding numbers
        cannot be counted up, the next factorization is set for lengths.
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
    status : int
        0 if the set of winding numbers could be counted up, 1 otherwise. In
        that case the last possible set of winding numbers was generated and
        the array should be back to initial configuration. Negative numbers 
        indicate errors.
    """
    
    # check shape and size of input
    if not windings.ndim == 2:
        raise ValueError("Error in `_next_nestwind_numba`: "
                "`windings` must be a 2D array.")
    if not lengths.ndim == 1:
        raise ValueError("Error in `_next_nestwind_numba`: "
                "`lengths` must be a 1D array.")
    if not factorizations.ndim == 2:
        raise ValueError("Error in `_next_nestwind_numba`: "
                "`factorizations` must be a 2D array.")
    if not windings.shape[0] == lengths.size:
        raise ValueError("Error in `_next_nestwind_numba`: "
                "First dimension of `windings` must equal size of `lengths`.")
    if not factorizations.shape[1] == lengths.size:
        raise ValueError("Error in `_next_nestwind_numba`: "
                "Second dimension of `factorizations` must equal size of `lengths`.")
        
    # set some shape parameters
    n_factors        = windings.shape[0]        # maximum number of factors
    n_blocks         = windings.shape[1]        # number of blocks in pulse sequence
    n_factorizations = factorizations.shape[0]  # total number of factorizations 
    
    
    # try to count up count up with current factorization as lengths
    
    # find number of subcycles and check lengths array
    # n_subcyc is the number of factors (sublengths) unequal 1
    for idx in range(lengths.size):
        # if value is not bigger than one
        if lengths[idx] <= 1:
            # value must be greater than or equal to one
            if lengths[idx] < 1:
                return -1
            # if one, all next numbers must be one as well
            if lengths[idx] == 1:
                n_subcyc = idx
                for jdx in range(idx+1, lengths.size):
                    if not lengths[jdx] == 1:
                        return -1
                break
        # check if lengths is sorted
        if idx > 0:
            if lengths[idx] < lengths[idx-1]:
                return -1
    # if loop ran through all values in lengths are greater than one
    else:
        n_subcyc = lengths.size
    
    
    # loop over all cols in reversed order
    for idx in range(n_subcyc-1,-1,-1):
        
        # try to count up the current row
        res = _next_windings_numba(windings[idx,:], lengths[idx],
                    last_zero, no_inverse, no_cfscan, no_cfwind)
        
        # count up successfull, now try to init following rows
        if res == 0:
            
            # loop over successive rows
            for jdx in range(idx+1,n_subcyc):    
                
                # if row before has same subcycle length copy it and count up
                if lengths[jdx] == lengths[jdx-1]:
                    windings[jdx,:] = windings[jdx-1,:]
                    res = _next_windings_numba(windings[jdx,:], lengths[jdx],
                                    last_zero, no_inverse, no_cfscan, no_cfwind)
                    if res == 0:
                        continue
                    elif res == 1:
                        break
                    else:
                        return -1
                
                # row before has smaller subcycle length, make initial configuration
                elif lengths[jdx] > lengths[jdx-1]:
                    windings[jdx,:] = 0
                    windings[jdx,0] = 1
                
                # this should not happen
                else:
                    return -1
            
            # row was counted up and all consecutive ones initialized, work is done
            else:
                return 0
        
        # could not count up this row, so try next one
        elif res == 1:
            continue
        
        else:
            return -1
        
    
    # if could not count up with current factorization, try next one
    
    # get index of recent factorization
    for idx_fac_start in range(n_factorizations):
        # compare all cols
        for jdx in range(n_factors):
            if not factorizations[idx_fac_start,jdx] == lengths[jdx]:
                # try next factorization
                break
        else:
            # if loop ran through, we found the correct line, so break loop
            break
    else:
        # loop must break if current factorization is inside factorizations array
        return -1
    
    # loop over all factorizations that come after the recent one
    for idx_fac in range(idx_fac_start+1, n_factorizations):
        
        # set length to current factorization
        lengths[:] = factorizations[idx_fac,:]
        
        # try to init with this factorization
        
        # find number of subcycles and check lengths array
        # n_subcyc is the number of factors (sublengths) unequal 1
        for idx in range(lengths.size):
            # if value is not bigger than one
            if lengths[idx] <= 1:
                # value must be greater than or equal to one
                if lengths[idx] < 1:
                    return -1
                # if one, all next numbers must be one as well
                if lengths[idx] == 1:
                    n_subcyc = idx
                    for jdx in range(idx+1, lengths.size):
                        if not lengths[jdx] == 1:
                            return -1
                    break
            # check if lengths is sorted
            if idx > 0:
                if lengths[idx] < lengths[idx-1]:
                    return -1
        # if loop ran through all values in lengths are greater than one
        else:
            n_subcyc = lengths.size
            
        # init first row
        windings[0,:] = 0
        windings[0,0] = 1
        
        # loop over all other rows and try to init them
        no_overflow = True
        for idx in range(1, n_subcyc):

            # if same cycle lengths, avoid repetition
            if lengths[idx] == lengths[idx-1]:
                # copy previous line and try to count up
                windings[idx,:] = windings[idx-1,:]
                res = _next_windings_numba(windings[idx,:], lengths[idx],
                        last_zero, no_inverse, no_cfscan, no_cfwind)
                if res == 0:
                    continue
                elif res == 1:
                    # overflow happened, try next factorization
                    no_overflow = False
                    break
                else:
                    return -1
            
            # if longer cycle, init next row
            elif lengths[idx] > lengths[idx-1]:
                windings[idx,:] = 0
                windings[idx,0] = 1
            
            # cycle lenghts must be ordered
            else:
                return -1
        
        if no_overflow:
            windings[n_subcyc:,:] = 0
            return 0
            
    
    # if loop run through last factorization was tried, so we are done
    else:
        res = _init_nestwind_numba(windings, lengths, factorizations,
                    last_zero, no_inverse, no_cfscan, no_cfwind)
        if not res == 0:
            return -1
        else:
            return 1





@numba.njit(fastmath=True)
def _fill_buffer_nestcog_numba(buffer_windings, buffer_lengths,
                               seed_windings, seed_lengths, factorizations,
                               last_zero, no_inverse, no_cfscan, no_cfwind):
    """
    ToDo
    
    Parameters
    ----------
    buffer_windings
    buffer_lengths
    seed_windings
    seed_lengths
    factorizations
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
        Number of filled buffer.
    """
    
    # check shape of input
    if not buffer_windings.ndim == 3:
        raise ValueError("`buffer_windings` must be 3D!")
    if not buffer_lengths.ndim == 2:
        raise ValueError("`buffer_windings` must be 2D!")
    if not seed_windings.ndim == 2:
        raise ValueError("`buffer_windings` must be 2D!")
    if not seed_lengths.ndim == 1:
        raise ValueError("`buffer_windings` must be 1D!")
        
    n_buffered = buffer_windings.shape[0]
    n_factors  = buffer_windings.shape[1]
    n_blocks   = buffer_windings.shape[2]
        
    if not buffer_lengths.shape[0] == n_buffered:
        raise ValueError("1")
    if not buffer_lengths.shape[1] == n_factors:
        raise ValueError("2")
    if not seed_windings.shape[0] == n_factors:
        raise ValueError("3")
    if not seed_windings.shape[1] == n_blocks:
        raise ValueError("4")
    if not seed_lengths.size == n_factors:
        raise ValueError("5")
    if not factorizations.shape[1] == n_factors:
        raise ValueError("6")
        
    # copy seeds to private working arrays
    working_windings = np.zeros_like(seed_windings)
    working_lengths = np.zeros_like(seed_lengths)
    new_seed_windings = np.zeros_like(seed_windings)
    new_seed_lengths = np.zeros_like(seed_lengths)
    working_windings[:,:] = seed_windings[:,:]
    working_lengths[:] = seed_lengths[:]
    
    
    # initialize the first entry
    buffer_windings[0,:,:] = working_windings[:,:]
    buffer_lengths[0,:] = working_lengths[:]
    n_filled = 1
    
    for i in range(1,n_buffered):
        
        # try to count up
        res = _next_nestwind_numba(
                    working_windings, working_lengths, factorizations,
                    last_zero, no_inverse, no_cfscan, no_cfwind)
        if res == 0:
            buffer_windings[i,:,:] = working_windings[:,:]
            buffer_lengths[i,:] = working_lengths[:]
            n_filled += 1
        elif res == 1:
            new_seed_windings[:,:] = working_windings[:,:]
            new_seed_lengths[:] = working_lengths[:]
            return n_filled, new_seed_windings, new_seed_lengths, True
        else:
            return -1, new_seed_windings, new_seed_lengths, False
        
    # check if there is more work to do
    res = _next_nestwind_numba(
                working_windings, working_lengths, factorizations,
                last_zero, no_inverse, no_cfscan, no_cfwind)
    if res == 0:
        all_done = False
    elif res == 1:
        all_done = True
    else:
        return -1, new_seed_windings, new_seed_lengths, False
    
    new_seed_windings[:,:] = working_windings[:,:]
    new_seed_lengths[:] = working_lengths[:]
    return n_filled, new_seed_windings, new_seed_lengths, all_done







#######################################################
#                                                     #
#   V   V   AAA   RRRR    III    OOO   U   U   SSSS   #
#   V   V  A   A  R   R    I    O   O  U   U  S       #
#   V   V  AAAAA  RRRR     I    O   O  U   U   SSS    #
#    V V   A   A  R  R     I    O   O  U   U      S   #
#     V    A   A  R   R   III    OOO    UUU   SSSS    #
#                                                     #
#######################################################



@numba.njit()
def are_ctps_passed_nestcog_numba(cycle_lengths, winding_numbers, dctps0):
    """
    For a given nestcog phase cycle determine if it passes a CTP or blocks it
    given its relative coherence order changes.
    
    Parameters
    ----------
    cycle_lengths : (n_cycles,) array of int
        Cycle lengths of each inner cycle. The number of scans is the product
        all numbers in this array.
    winding_numbers : (n_cycles, n_blocks) array of int
        Winding numbers for each cycle.
    dctps0 : (n_ctps, n_blocks) array of int
        Coherence order changes relative to the coherence order changes of
        the reference path. The desired paths must be given first.
    
    Returns
    -------
    is_passed : array of bool
        For each CTP, wether it is passed by the given phase cycle.
    """
    
    # check size and shape of input
    if not cycle_lengths.ndim == 1:
        raise ValueError('Internal error: `cycle_lengths` must be 1D.')
    if not winding_numbers.ndim == 2:
        raise ValueError('Internal error: `winding_numbers` must be 2D.')
    if not dctps0.ndim == 2:
        raise ValueError('Internal error: `dctps0` must be 2D.')
    if not cycle_lengths.shape[0] == winding_numbers.shape[0]:
        raise ValueError('Internal error: First dimensions of `cycle_lengths` '
                         'and `winding_numbers` must have same size.')
    if not winding_numbers.shape[1] == dctps0.shape[1]:
        raise ValueError('Internal error: Second dimensions of `winding_numbers` '
                         'and `dctps0` must have same size.')
        
    n_cycles = cycle_lengths.shape[0]
    n_ctps = dctps0.shape[0]
    n_blocks = dctps0.shape[1]
    
    is_passed = np.zeros(n_ctps, dtype=np.bool_)
    
    # loop over all ctps
    for idx_ctp in range(n_ctps):
        # check if any cycle blocks this ctp
        for idx_cycle in range(n_cycles):
            dcpts0summed = 0
            for idx_block in range(n_blocks):
                dcpts0summed += winding_numbers[idx_cycle, idx_block] * dctps0[idx_ctp, idx_block]
            # if sum is not zero, current cycle blocks ctp
            if not dcpts0summed % cycle_lengths[idx_cycle] == 0:
                is_passed[idx_ctp] = False
                break
        else:
            # if loop does not break, ctp is passed
            is_passed[idx_ctp] = True
    
    return is_passed





@numba.njit()
def is_valid_nestcog_numba(windings, lengths, dctps0, n_ctps_wanted):
    """
    For a given nestcog phase cycle determine if it passes all wanted CTPs and
    blocks all unwanted CTPs.
    
    Parameters
    ----------
    windings : (n_cycles, n_blocks) array of int
        Winding numbers for each cycle.
    lengths : (n_cycles,) array of int
        Cycle lengths of each inner cycle. The number of scans is the product
        all numbers in this array.
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
    if not windings.ndim == 2:
        raise ValueError('Internal error: `windings` must be 2D.')
    if not dctps0.ndim == 2:
        raise ValueError('Internal error: `dctps0` must be 2D.')
    if not lengths.shape[0] == windings.shape[0]:
        raise ValueError('Internal error: First dimensions of `lengths` '
                         'and `windings` must have same size.')
    if not windings.shape[1] == dctps0.shape[1]:
        raise ValueError('Internal error: Second dimensions of `windings` '
                         'and `dctps0` must have same size.')
    if n_ctps_wanted < 0 or n_ctps_wanted > dctps0.shape[0]:
        raise ValueError('Internal error: `n_ctps_wanted` must be between 0 '
                         'and number of given CTPs.')
        
    n_cycles = lengths.shape[0]
    n_ctps = dctps0.shape[0]
    n_blocks = dctps0.shape[1]
    if n_cycles < 1: return 3
    
    # loop over all wanted CTPs
    for idx_ctp in range(n_ctps_wanted):
        # check if any cycle blocks this CTP
        for idx_cycle in range(n_cycles):
            if lengths[idx_cycle] <= 1: continue
            dcpts0summed = 0
            for idx_block in range(n_blocks):
                dcpts0summed += windings[idx_cycle, idx_block] * dctps0[idx_ctp, idx_block]
            # if sum is not zero, current cycle blocks CTP
            if not dcpts0summed % lengths[idx_cycle] == 0:
                return 1
    
    # loop over all unwanted CTPs
    for idx_ctp in range(n_ctps_wanted, n_ctps):
        # check if any cycle blocks this CTP
        for idx_cycle in range(n_cycles):
            if lengths[idx_cycle] <= 1: continue
            dcpts0summed = 0
            for idx_block in range(n_blocks):
                dcpts0summed += windings[idx_cycle, idx_block] * dctps0[idx_ctp, idx_block]
            # if sum is not zero, current cycle blocks CTP
            if not dcpts0summed % lengths[idx_cycle] == 0:
                break
        else:
            # if loop does not break, CTP is passed
            return 2
    
    return 0





@numba.njit(parallel=True)
def are_valid_nestcogs_numba(windings, lengths, dctps0, n_ctps_wanted, n_check=0):
    """
    For several given nestcog phase cycles determine if they pass all wanted
    CTPs and blocks all unwanted CTPs.
    
    Parameters
    ----------
    lengths : (n_nestcogs, n_cycles,) array of int
        Cycle lengths of each inner cycle for every nestcog cycle.
        The number of scans is the product all numbers for a given nestcog
        cycle.
    windings : (n_nestcogs, n_cycles, n_blocks) array of int
        Winding numbers for each inner cycle and for each nestcog cycle.
    dctps0 : (n_ctps, n_blocks) array of int
        Coherence order changes relative to the coherence order changes of
        the reference path. The desired paths must be given first.
    n_ctps_wanted : int
        Number of desired paths. The first n_ctps_wanted rows of dctps0 must
        be the desired paths, the following ones the undesired ones.
    
    Returns
    -------
    is_valid : array of int
        Wether the phase cycle is valid or not for each nestcog cycle.
        0 indicates a valid cycle, 1 a cycle that filters desired paths and 2
        a cycle that does not filter desired paths but also not all undesired
        paths.
    """
    
    # check size and shape of input
    if not lengths.ndim == 2:
        raise ValueError('Internal error: `lengths` must be 2D.')
    if not windings.ndim == 3:
        raise ValueError('Internal error: `windings` must be 3D.')
    if not dctps0.ndim == 2:
        raise ValueError('Internal error: `dctps0` must be 2D.')
    
    n_cycles = windings.shape[0] # number of nestcog cycles
    n_subcyc = windings.shape[1] # number of subcycles per nestcog
    n_blocks = windings.shape[2] # number of pulse blocks


    if not lengths.shape[0] == n_cycles:
        raise ValueError('Internal error: First dimensions of `lengths` '
                         'and `windings` must have same size.')
    if not lengths.shape[1] == n_subcyc:
        raise ValueError('Internal error: First dimensions of `lengths` '
                         'and second of `windings` must have same size.')
    if not dctps0.shape[1] == n_blocks:
        raise ValueError('Internal error: Second dimensions of `dctps0` '
                         'and third of `windings` must have same size.')
    
    if n_ctps_wanted < 0 or n_ctps_wanted > dctps0.shape[0]:
        raise ValueError('Internal error: `n_ctps_wanted` must be between 0 '
                         'and number of given CTPs.')

    if n_check <= 0:
        # check every cycle
        n_check = n_cycles
    else:
        n_check = min(n_check, n_cycles)

    # allocate output array
    results = np.zeros(n_check, dtype=np.int64)
    results.fill(3)
    
    # parallel loop over all cycles
    for idx_cycle in numba.prange(n_check):
        
        # check validity of current cycle
        res = is_valid_nestcog_numba(
                windings[idx_cycle,:,:], lengths[idx_cycle,:],
                dctps0, n_ctps_wanted)
        results[idx_cycle] = res
    
    return results



def search_nestcog_exhaustive(n_scans_max, dctps0, n_ctps_wanted,
                            last_zero=False, no_inverse=True,
                            no_cfscan=True, no_cfwind=True,
                            n_find=1, n_scans_min=2, verbose=1):
    
    # check input
    n_scans_min = max(2, int(n_scans_min))
    n_scans_max = max(n_scans_min, int(n_scans_max))
    
    n_find = max(1, int(n_find))
    
    dctps0 = np.asarray(dctps0)
    if not dctps0.ndim == 2:
        raise ValueError("Must be 2D")
    
    n_ctps   = dctps0.shape[0]
    n_blocks = dctps0.shape[1]
    
    if n_ctps_wanted < 0 or n_ctps_wanted > n_ctps:
        raise ValueError("Must be inbetween")
        
    n_checked = 0
    
    max_MB_buffer = 32
    
    # print some info
    print("SEARCHING NESTCOG CYCLES EXHAUSTIVELY\n")
    print("Number of CTPs ", n_ctps)
    print("Number of pulse blocks: ", n_blocks)
    print("Probing number of scans from {} to {}".format(n_scans_min, n_scans_max))
    
    print("Maximum memory of buffers: {} MB".format(max_MB_buffer))
    
    print("\n  --> Starting the run <--")
    print("-"*30)
    
    for n_scans in range(n_scans_min, n_scans_max+1):
        print('  --> Number of scans: ', n_scans)
        found_solution = False
        
        factorizations = _generate_all_factorizations_numba(n_scans, 0)
        n_factors = factorizations.shape[1]
        
        # allocate buffers
        n_buffered = int(np.floor( max_MB_buffer * (1024**2/((1+n_blocks)*n_factors*factorizations.itemsize)) ))
        #n_buffered = 10000
        if n_buffered < 1:
            raise ValueError("Cannot allocate buffer.")
        buffer_windings = np.empty((n_buffered,n_factors,n_blocks), dtype=factorizations.dtype)
        buffer_lengths  = np.empty((n_buffered,n_factors), dtype=factorizations.dtype)
        buffer_windings[:,:,:] = 0
        buffer_lengths[:,:] = 0
        
        # allocate seeds
        seed_windings = np.empty((n_factors,n_blocks), dtype=factorizations.dtype)
        seed_lengths  = np.empty((n_factors,), dtype=factorizations.dtype)
        seed_windings[:,:] = 0
        seed_lengths[:]    = 0
        
        # allocate output arrays
        output_windings = np.zeros((n_find,n_factors,n_blocks), dtype=factorizations.dtype)
        output_lengths  = np.zeros((n_find,n_factors), dtype=factorizations.dtype)
        
        # initialize the seeds
        res = _init_nestwind_numba(seed_windings, seed_lengths, factorizations,
                        last_zero, no_inverse, no_cfscan, no_cfwind)
        if not res == 0:
            ValueError("Could not init")
            
        all_done = False
        n_found = 0
        while True:
            
            # fill buffer
            n_set, seed_windings, seed_lengths, all_done = _fill_buffer_nestcog_numba(
                buffer_windings, buffer_lengths, seed_windings, seed_lengths,
                factorizations, last_zero, no_inverse, no_cfscan, no_cfwind)
            
            if n_set < 0:
                raise ValueError("Could not fill buffer.")
            
            # check if there are any valid cycles
            results = are_valid_nestcogs_numba(
                buffer_windings, buffer_lengths, dctps0, n_ctps_wanted, n_set)
            
            # copy possible solutions to output array
            _       = _copy_by_mask_numba(buffer_windings, output_windings, results, n_found)
            n_found = _copy_by_mask_numba(buffer_lengths, output_lengths, results, n_found)
            
            # break
            if all_done or n_found == n_find:
                break
            
        if n_found > 0:
            print("FOUND SOLUTION")
            
            return output_windings[:n_found,:,:], output_lengths[:n_found,:]
        
        # free space of buffer
        del buffer_windings, buffer_lengths
        
    return output_windings[:n_found,:,:], output_lengths[:n_found,:]



