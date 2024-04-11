import numpy as np
import numba

from .core.generators import (_init_windings_numba, _fill_buffer_windings_numba, _fill_buffer_windings_numbap)
from .core.array import (_copy_by_mask_numba,)

############################################################
#                                                          #
#   CCCC   OOO    GGGG  W   W  H   H  EEEEE  EEEEE  L      #
#  C      O   O  G      W   W  H   H  E      E      L      #
#  C      O   O  G  GG  W W W  HHHHH  EEE    EEE    L      #
#  C      O   O  G   G  WW WW  H   H  E      E      L      #
#   CCCC   OOO    GGG   W   W  H   H  EEEEE  EEEEE  LLLLL  #
#                                                          #
############################################################





##########################################################################
#                                                                        #
#   CCCC   OOO   N   N  V   V  EEEEE  N   N   III   EEEEE   CCCC  EEEEE  #
#  C      O   O  NN  N  V   V  E      NN  N    I    E      C      E      #
#  C      O   O  N N N  V   V  EEE    N N N    I    EEE    C      EEE    #
#  C      O   O  N  NN   V V   E      N  NN    I    E      C      E      #
#   CCCC   OOO   N   N    V    EEEEE  N   N   III   EEEEE   CCCC  EEEEE  #
#                                                                        #
##########################################################################



def predict_cogwheel(p0, pmax, symmetrical=False):
    """
    Predict the minimum length of a cogwheel phase cycle.
    
    The minimum length of a cogwheel phase cycle is predicted, that selects
    one pathway or two symmetrical pathways where each pathway starts at 0
    and ends at -1. In some cases, the exact minimum length and a set of valid
    winding numbers can be predicted.
    
    Parameters
    ----------
    p0 : array_like
        Coherence of the desired pathway (or one of two desired pathways)
        between each block.
    pmax : int, array_like
        Maximum possible coherence order between each block. If only an integer
        is given, then the same maximum possible coherence order is assumed
        between each block.
    symmetrical : bool, optional
        Wether two symmetrical pathway are to be selected (same coherences 
        between each pulse block but with opposite sign except for the last
        coherence throughout acquisition). Defaults to false.
    
    Returns
    -------
    Npred : int
        Minimum number of scans for the given cycle. Is the except number when
        also the winding numbers are returned.
    zeta : array_like, None
        Differences of the winding numbers for the predicted cycle. Only
        returned when cycle is predictable. If the cycle is not predictable,
        None is returned.
        
    References
    ----------
    [1] Hughes, C. E., Carravetta, M. & Levitt, M. H. Some conjectures for 
    cogwheel phase cycling. J. Magn. Reson. 167, 259–265 (2004).
    DOI: 10.1016/j.jmr.2004.01.001
    """
    
    # convert to arrays
    p0 = np.asarray(p0).flatten()
    if type(pmax) is int: pmax = [pmax]*p0.size
    pmax = np.asarray(pmax).flatten()
    
    q = pmax + 1 - np.abs(p0)
    Q = np.prod(q)
    
    zeta = np.int64( Q * np.where(p0==0, 1, np.sign(p0))/q )
    haveNoCommonDivisor = np.lcm.reduce(zeta) == np.prod(zeta)
    
    # calculate minimum number of scans
    if symmetrical:
        Npred = int(round( 2*Q*np.sum(np.abs(p0)/q) ))
    else:
        Npred = int(round( Q * (1 + 2*np.sum(np.abs(p0)/q)) ))
    
    # return minimum number of scans and winding number differences...
    if haveNoCommonDivisor:
        # ... if they give a valid phase cycle
        return Npred, zeta%Npred
    else:
        return Npred, None





def number_of_cogwheels(n_scans, n_blocks, last_zero, no_inverse):
    """
    Compute the number of cogwheel phase cycles.
    
    Parameters
    ----------
    n_scans : int
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
    n_cog : int
        Number of cogwheel cycles.    
    """
    
    n_scans  = int(n_scans)
    n_blocks = int(n_blocks)
    
    if n_blocks < 1:
        raise ValueError("`n_blocks` must be at least 1.")
    if n_scans < 2:
        raise ValueError("`n_scans` must be at least 2.")
    
    if last_zero:
        n_blocks = n_blocks - 1
        
    if no_inverse:
        n_cog = (n_scans**n_blocks + (2 - n_scans%2)**n_blocks)//2 - 1
    else:
        n_cog = n_scans**n_blocks - 1
    
    return n_cog





def cogwheel_to_phases(windings, n_scans, unit='n_scans'):
    """
    Convert a set of cogwheel winding numbers to a list of phases.
    
    Parameters
    ----------
    windings : (n_blocks,) array_like of int
        Set of winding numbers, one for each cycled block.
    n_scans : int
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
    
    # convert windings to numpy array and check dimensionality
    windings = np.asarray(windings)
    if not windings.ndim == 1:
        raise ValueError('`windings` must be a 1D array.')
    n_blocks = windings.shape[0]
    if n_scans < 2:
        raise ValueError('`n_scans` should be at least 2.')
    
    # allocate array
    phases = np.zeros(shape=(n_scans,n_blocks), dtype=windings.dtype)
    
    # set phases using numba routine
    _cogwheel_to_phases_numba(windings, n_scans, phases)
    
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





def cogwheels_to_phases(windings, n_scans, unit='n_scans'):
    """
    Convert a set of cogwheel winding numbers to a list of phases.
    
    Parameters
    ----------
    windings : (n_cogs,n_blocks) array_like of int
        Set of winding numbers, one for each cycled block.
    n_scans : int
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
    
    # convert windings to numpy array and check dimensionality
    windings = np.asarray(windings)
    if not windings.ndim == 2:
        raise ValueError('`windings` must be a 2D array.')
    n_cogs = windings.shape[0]
    n_blocks = windings.shape[1]
    if n_scans < 2:
        raise ValueError('`n_scans` should be at least 2.')
    
    # allocate array
    phases = np.zeros(shape=(n_cogs,n_scans,n_blocks), dtype=windings.dtype)
    
    # set phases using numba routine
    _cogwheels_to_phases_numba(windings, n_scans, phases)
    
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







###################################################################
#                                                                 #
#  U   U  TTTTT   III   L       III   TTTTT   III   EEEEE   SSSS  #
#  U   U    T      I    L        I      T      I    E      S      #
#  U   U    T      I    L        I      T      I    EEE     SSS   #
#  U   U    T      I    L        I      T      I    E          S  #
#   UUU     T     III   LLLLL   III     T     III   EEEEE  SSSS   #
#                                                                 #
###################################################################



@numba.njit(parallel=False)
def _cogwheel_to_phases_numba(windings, n_scans, phases): 
    """
    Convert a set of cogwheel winding numbers to a list of phases.
    
    Parameters
    ----------
    windings : (n_blocks,) array_like of int
        Set of winding numbers, one for each cycled block.
    n_scans : int
        Number of scans. Should be at least 2.
    phases : (n_blocks, n_scans) array
        Pre-allocated array to store phases in.
    
    Returns
    -------
    None
    """
    
    # check dimensionality and shape of input
    if not windings.ndim == 1:
        raise ValueError("Error in `_cogwheel_to_phases_numba`: `windings` must be 1D.")
    n_blocks = windings.shape[0]
    if not phases.ndim == 2:
        raise ValueError("Error in `_cogwheel_to_phases_numba`: `phases` must be 2D.")
    if (not phases.shape[0] == n_scans) or (not phases.shape[1] == n_blocks):
        raise ValueError("Error in `_cogwheel_to_phases_numba`: `phases` must be of shape (n_scans,n_blocks).")
    
    # set array elements row by row
    for i in range(1, n_scans):
        phases[i] = np.mod(phases[i-1]+windings, n_scans)





@numba.njit(parallel=True)
def _cogwheels_to_phases_numba(windings, n_scans, phases): 
    """
    Convert multiple set of cogwheel winding numbers to a list of phases.
    
    Parameters
    ----------
    windings : (n_cogs,n_blocks) array_like of int
        Set of winding numbers, one for each cycled block.
    n_scans : int
        Number of scans. Should be at least 2.
    phases : (n_cogs,n_blocks,n_scans) array
        Pre-allocated array to store phases in.
    
    Returns
    -------
    None
    """
    
    # check dimensionality and shape of input
    if not windings.ndim == 2:
        raise ValueError('Error in `_cogwheels_to_phases_numba`: `windings` must be 2D.')
    n_cogs = windings.shape[0]
    n_blocks = windings.shape[1]
    if not phases.ndim == 3:
        raise ValueError('Error in `_cogwheels_to_phases_numba`: `phases` must be 3D.')
    if ( (not phases.shape[0] == n_cogs) 
        or (not phases.shape[1] == n_scans) 
        or (not phases.shape[2] == n_blocks) ):
        raise ValueError('Error in `_cogwheels_to_phases_numba`: `phases` must be of shape (n_scans,n_blocks).')
    
    # set array elements row by row
    for i in numba.prange(n_cogs):
        _cogwheel_to_phases_numba(windings[i], n_scans, phases[i])







# ############################################################
# #                                                          #
# #  W   W   III   N   N  DDDD    III   N   N   GGGG   SSSS  #
# #  W   W    I    NN  N  D   D    I    NN  N  G      S      #
# #  W W W    I    N N N  D   D    I    N N N  G  GG   SSS   #  
# #  WW WW    I    N  NN  D   D    I    N  NN  G   G      S  #
# #  W   W   III   N   N  DDDD    III   N   N   GGG   SSSS   #
# #                                                          #
# ############################################################



# @numba.njit()
# def _smallest_common_divisor_numba(a):
#     """
#     Find the smallest common divisor greater than one of an array of integers.

#     The sign of all integers is ignored. All zeros are ignored as zero is
#     considerd to be divisible by everything. Some sample outputs:

#         [0, 0, 0, 0] --> 0
#         [2,-4, 8, 0] --> 2
#         [2, 4, 6,-3] --> 1
#         [1, 0,-1, 0] --> 1

#     This functions works by first finding the smallest absolute value in
#     `a` greater than one. If no value greater in absolute value than one
#     (or zero) exist then one (or zero) is returned. If all elements in
#     `a` share a common factor it must be a prime factor of this smallest
#     value. Divisibility is then checked for all those prime factors.
    
#     Parameters
#     ----------
#     a : array of int
#         Integers to find the smallest common divisor greater than one of.

#     Returns
#     -------
#     val ;. int
#         Smallest common divisor greater than one shared by all integers in a
#         (always positive) or one if all integers are coprime or zero if all
#         integers in a are zero.
#     """
    
#     if not a.ndim == 1:
#         raise ValueError("`windings` must be a 1D array.")
    
#     n = a.size
    
#     # get minimum absolute value greater than zero
#     val_min = 0
#     for i in range(n):
#         if not val_min == 0:
#             if not abs(a[i]) == 0 and abs(a[i]) < val_min:
#                 val_min = abs(a[i])
#         elif abs(a[i]) > val_min:
#             val_min = abs(a[i])
#     # if no element is bigger than one, just return val_min (0 or 1)
#     if val_min < 2:
#         return val_min
    
#     # check divisibility by 2
#     if val_min%2 == 0:
#         val_min = val_min//2
#         # iterate over array elements greater than 0, see if all are divisible
#         for i in range(n):
#             if not a[i]%2 == 0: break
#         else:
#             # if so, this is the smallest common divisor
#             return 2
#         # divide out this factor
#         while val_min%2 == 0:
#             val_min = val_min//2
    
#     # check divisibility by 3
#     if val_min%3 == 0:
#         val_min = val_min//3
#         # iterate over array elements greater than 0, see if all are divisible
#         for i in range(n):
#             if not a[i]%3 == 0: break
#         else:
#             # if so, this is the smallest common divisor
#             return 3
#         # divide out this factor
#         while val_min%3 == 0:
#             val_min = val_min//3
    
#     # check divisibility by all other prime factors (6k+-1 filter)
#     div = 5
#     while val_min > 1:
        
#         # check divisibility by 6k-1
#         if val_min%div == 0:
#             val_min = val_min//div
#             # iterate over array elements greater than 0, see if all are divisible
#             for i in range(n):
#                 if not a[i]%div == 0: break
#             else:
#                 # if so, this is the smallest common divisor
#                 return div
#             # divide out this factor
#             while val_min%div == 0:
#                 val_min = val_min//div
        
#         # check divisibility by 6k+1
#         if val_min%(div+2) == 0:
#             val_min = val_min//(div+2)
#             # iterate over array elements greater than 0, see if all are divisible
#             for i in range(n):
#                 if not a[i]%(div+2) == 0: break
#             else:
#                 # if so, this is the smallest common divisor
#                 return div+2
#             # divide out this factor
#             while val_min%(div+2) == 0:
#                 val_min = val_min//(div+2)
        
#         div += 6
    
#     # if no common factor was found, elements in `a` are coprime
#     return 1





# @numba.njit()
# def _smallest_common_divisor_nscans_numba(n_scans, windings):
#     """
#     Utility function.
    
#     Parameters
#     ----------
#     ToDo

#     Returns
#     -------
#     ToDo
#     """
    
#     if not windings.ndim == 1:
#         raise ValueError("`windings` must be a 1D array.")
    
#     n = windings.size
    
#     # get minimum absolute value greater than zero
#     val_min = 0
#     for i in range(n):
#         if not val_min == 0:
#             if not abs(windings[i]) == 0 and abs(windings[i]) < val_min:
#                 val_min = abs(windings[i])
#         elif abs(windings[i]) > val_min:
#             val_min = abs(windings[i])
                
#     # if no winding is bigger than one, just return val_min
#     if val_min < 2:
#         return val_min
#     # check if n_scans can make val_min smaller
#     if not abs(n_scans) == 0 and abs(n_scans) < val_min:
#         val_min = abs(n_scans)
    
#     # divisibility by 2
#     if val_min%2 == 0:
#         val_min = val_min//2
#         # iterate over array elements greater than 0, see if all are divisible
#         if n_scans%2 == 0:
#             for i in range(n):
#                 if not windings[i]%2 == 0: break
#             else:
#                 return 2
#         # divide out this factor
#         while val_min%2 == 0:
#             val_min = val_min//2
    
#     # divisibility by 3
#     if val_min%3 == 0:
#         val_min = val_min//3
#         # iterate over array elements greater than 0, see if all are divisible
#         if n_scans%3 == 0:
#             for i in range(n):
#                 if not windings[i]%3 == 0: break
#             else:
#                 return 3
#         # divide out this factor
#         while val_min%3 == 0:
#             val_min = val_min//3
    
#     # divisibility by all other prime factors (6k+-1 filter)
#     div = 5
#     while val_min > 1:
        
#         if val_min%div == 0:
#             val_min = val_min//div
#             # iterate over array elements greater than 0, see if all are divisible
#             if n_scans%div == 0:
#                 for i in range(n):
#                     if not windings[i]%div == 0: break
#                 else:
#                     return div
#             # divide out this factor
#             while val_min%div == 0:
#                 val_min = val_min//div
            
#         if val_min%(div+2) == 0:
#             val_min = val_min//(div+2)
#             # iterate over array elements greater than 0, see if all are divisible
#             if n_scans%(div+2) == 0:
#                 for i in range(n):
#                     if not windings[i]%(div+2) == 0: break
#                 else:
#                     return div+2
#             # divide out this factor
#             while val_min%(div+2) == 0:
#                 val_min = val_min//(div+2)
        
#         div += 6
    
#     return 1





# @numba.njit(fastmath=True)
# def _count_up_windings_numba(windings, n_scans, last_zero, no_inverse):
#     """
#     Generate the next set of winding numbers from a given set.
    
#     The operation is performed inplace. This function is compiled by numba.
    
#     Parameters
#     ----------
#     windings : 1D array
#         Set of winding numbers to increase inplace.
#     n_scans : int
#         Number of scans for the cogwheel cycle.
#     last_zero : bool
#         Whether the last winding number shoud be kept zero. This is reasonable
#         if all CTPs have the same total coherence order change as the reference
#         path because then only the differences between winding numbers do
#         really matter.
#     no_inverse : bool
#         Whether to avoid generating the phase inverted counterparts of other
#         sets of winding numbers. To achieve this, winding numbers, that have
#         only the numbers 0 or (n_scans+1)//2 to their right, are counted up 
#         only to n_scans//2 rather than n_scans-1.
    
#     Returns
#     -------
#     status : int
#         0 if the set of winding numbers could be counted up, 1 otherwise. In
#         that case the last possible set of winding numbers was generated and
#         the array should be back to all zeroes. Negative numbers indicate
#         errors.
#     """
    
#     # check the input parameters
#     if not windings.ndim == 1:
#         return -1
#     if n_scans <= 1:
#         return -1
    
#     if last_zero:
#         n_blocks = windings.size - 1
#         if not windings[-1] == 0: return -2
#     else:
#         n_blocks = windings.size
    
#     # handle cases with and without phase inversion separately
#     if no_inverse:
        
#         # loop in reversed order over the winding numbers, find the position
#         # where all right sided values are 0 or (n_scans+1)//2 (symmetric block)
#         idx_left = n_blocks
#         for i in range(n_blocks):
#             idx_left -= 1
#             if not (windings[idx_left] == 0 or windings[idx_left] == (n_scans+1)//2):
#                 break
        
#         # try to count up asymmetric block, winding numbers from 0 up to n_scans-1
#         for i in range(idx_left):
#             if windings[i] < n_scans-1:
#                 windings[i] += 1
#                 return 0
#             elif windings[i] == n_scans-1:
#                 windings[i] = 0
#             else:
#                 return -2
        
#         # try to count up asymmetric block, winding numbers from 0 up to n_scans//2 ok
#         for i in range(idx_left, n_blocks):
#             if windings[i] < n_scans//2:
#                 windings[i] += 1
#                 return 0
#             elif windings[i] == n_scans//2:
#                 windings[i] = 0
#             else:
#                 return -2
        
#         # if all winding numbers are set to zero, that was the last combination
#         windings[0] = 1
#         return 1
    
#     # if not no_inverse
#     else:
        
#         # loop over all blocks, try to increase winding number
#         for i in range(n_blocks):
           
#             # if winding number is small enough, increase it
#             if windings[i] < n_scans-1:
#                 windings[i] += 1
#                 return 0
#             # if winding number is at maximum, set to zero and try next number
#             elif windings[i] == n_scans-1:
#                 windings[i] = 0
#             # in any other case, winding number is invalid
#             else:
#                 return -2
        
#         # if all winding numbers are set to zero, that was the last combination
#         windings[0] = 1
#         return 1





# @numba.njit(fastmath=True)
# def _count_up_windings_nocfscan_numba(windings, n_scans, last_zero, no_inverse):
#     """
#     Generate the next set of winding numbers from a given set avoiding all
#     combinations whose winding numbers and the number of scans share a factor 
#     greater than one. This will avoid reducible cycles, i.e. cycles that are
#     equivalent to other cycles with a smaller number of scans.
    
#     The operation is performed inplace. This function is compiled by numba.
    
#     Parameters
#     ----------
#     windings : 1D array
#         Set of winding numbers to increase inplace.
#     n_scans : int
#         Number of scans for the cogwheel cycle.
#     last_zero : bool
#         Whether the last winding number shoud be kept zero. This is reasonable
#         if all CTPs have the same total coherence order change as the reference
#         path because then only the differences between winding numbers do
#         really matter.
#     no_inverse : bool
#         Whether to avoid generating the phase inverted counterparts of other
#         sets of winding numbers. To achieve this, winding numbers, that have
#         only the numbers 0 or (n_scans+1)//2 to their right, are counted up 
#         only to n_scans//2 rather than n_scans-1.
    
#     Returns
#     -------
#     status : int
#         0 if the set of winding numbers could be counted up, 1 otherwise. In
#         that case the last possible set of winding numbers was generated and
#         the array should be back to all zeroes. Negative numbers indicate
#         errors.
#     """
    
#     while True:
        
#         res = _count_up_windings_numba(windings, n_scans, last_zero, no_inverse)
        
#         # forward all flags except when counting up was successfull
#         if not res == 0:
#             return res
        
#         # check if no common factor, if there is, count up further
#         if _smallest_common_divisor_nscans_numba(n_scans, windings) == 1:
#             return 0





# @numba.njit(fastmath=True)
# def _count_up_windings_nocfwind_numba(windings, n_scans, last_zero, no_inverse):
#     """
#     Generate the next set of winding numbers from a given set avoiding all
#     combinations whose winding numbers and the number of scans share a factor 
#     greater than one. This will avoid cycles that have the same selection
#     properties as a cycles, where no factors are shared.
    
#     The operation is performed inplace. This function is compiled by numba.
    
#     Parameters
#     ----------
#     windings : 1D array
#         Set of winding numbers to increase inplace.
#     n_scans : int
#         Number of scans for the cogwheel cycle.
#     last_zero : bool
#         Whether the last winding number shoud be kept zero. This is reasonable
#         if all CTPs have the same total coherence order change as the reference
#         path because then only the differences between winding numbers do
#         really matter.
#     no_inverse : bool
#         Whether to avoid generating the phase inverted counterparts of other
#         sets of winding numbers. To achieve this, winding numbers, that have
#         only the numbers 0 or (n_scans+1)//2 to their right, are counted up 
#         only to n_scans//2 rather than n_scans-1.
    
#     Returns
#     -------
#     status : int
#         0 if the set of winding numbers could be counted up, 1 otherwise. In
#         that case the last possible set of winding numbers was generated and
#         the array should be back to all zeroes. Negative numbers indicate
#         errors.
#     """
    
#     while True:
        
#         res = _count_up_windings_numba(windings, n_scans, last_zero, no_inverse)
        
#         # forward all flags except when counting up was successfull
#         if not res == 0:
#             return res
        
#         # check if no common factor, if there is, count up further
#         if _smallest_common_divisor_numba(windings) == 1:
#             return 0





# @numba.njit(fastmath=True)
# def _next_windings_numba(windings, n_scans, 
#                      last_zero, no_inverse, no_cfscan, no_cfwind):
#     """
#     Generate the next set of winding numbers.
    
#     Parameters
#     ----------
#     ...

#     Returns
#     -------
#     ...    
#     """
    
#     # if no common factor wanted among winding numbers, dont even bother with scans
#     if no_cfwind:

#         while True:
#             res = _count_up_windings_numba(windings, n_scans, last_zero, no_inverse)
            
#             # forward error flags
#             if not res == 0:
#                 return res
            
#             # check if no common factor, if there is, count up further
#             if _smallest_common_divisor_numba(windings) == 1:
#                 return res
    
#     # no common factors between the number of scans and all winding numbers
#     elif no_cfscan:
        
#         while True:
#             res = _count_up_windings_numba(windings, n_scans, last_zero, no_inverse)
            
#             # forward error flags
#             if not res == 0:
#                 return res
            
#             # check if no common factor, if there is, count up further
#             if _smallest_common_divisor_nscans_numba(n_scans, windings) == 1:
#                 return res
    
#     # common factors are OK
#     else:
        
#         res = _count_up_windings_numba(windings, n_scans, last_zero, no_inverse)
#         return res





# @numba.njit(fastmath=True)
# def _fill_buffer_windings_numba(buffer, seed, n_scans,
#                                 last_zero, no_inverse, no_cfscan, no_cfwind):
#     """
#     Given a seed set of winding numbers, fill a given buffer with consecutive
#     sets of winding numbers.
    
#     Parameters
#     ----------
#     buffer : (n_buffered,n_blocks) 2D array
#         Buffer array to store the winding numbers in.
#     seed : (n_blocks,) 1D array
#         Initial set of winding numbers.
#     n_scans : int
#         Number of scans for the cogwheel cycle.
#     last_zero : bool
#         Whether the last winding number shoud be kept zero. This is reasonable
#         if all CTPs have the same total coherence order change as the reference
#         path because then only the differences between winding numbers do
#         really matter.
#     no_inverse : bool
#         Whether the last non-zero winding number is counted up only to
#         n_scans//2 and not n_scans-1. This avoids generating the phase inverted
#         counterparts of other sets of winding numbers.
#     no_cfscan : bool
#         Whether to avoid sets of winding numbers, where every winding number and
#         the number of scans share a common factor. This would result in an
#         redundant cycle, i.e. a cycle that has smaller length but is repeated.
#     no_cfwind : bool
#         Whether to avoid sets of winding numbers, where the winding numbers 
#         share a common factor. Such cycles would be equivalent (selecting the)
#         same CTPs as the cycle with winding numbers, where the common factor
#         is devided out.
#         If this option is set, setting `no_cfscan` has no effect anymore.
    
#     Returns
#     -------
#     n_filled : int
#         Number of sets of winding numbers written to the buffer. Equal to the
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
#     windings_working = np.zeros_like(seed)
#     new_seed = np.zeros_like(seed)
#     windings_working[:] = seed[:]
    
#     # initialize the first entry
#     buffer[0,:] = windings_working[:]
#     n_filled = 1
    
#     # fill the other rows
#     for i in range(1,buffer.shape[0]):
        
#         # try to count up
#         res = _next_windings_numba(windings_working, n_scans, 
#                                    last_zero, no_inverse, no_cfscan, no_cfwind)
        
#         if res == 0:
#             buffer[i,:] = windings_working[:]
#             n_filled += 1
#         elif res == 1:
#             new_seed[:] = windings_working[:]
#             return n_filled, new_seed, True
#         else:
#             return -1, new_seed, False
        
#     # check if there is more work to do
#     res = _count_up_windings_numba(windings_working, n_scans, last_zero, no_inverse)
#     if res == 0:
#         all_done = False
#     elif res == 1:
#         all_done = True
#     else:
#         return -1, new_seed, False
    
#     new_seed[:] = windings_working[:]
#     return n_filled, new_seed, all_done





# @numba.njit(parallel=True, fastmath=True)
# def _fill_buffer_windings_numbap(buffer, seed, n_scans,
#                                  last_zero, no_inverse, no_cfscan, no_cfwind):
#     """
#     Given a seed set of winding numbers, fill a given buffer with consecutive
#     sets of winding numbers.
    
#     Parameters
#     ----------
#     buffer : (n_buffered,n_blocks) 2D array
#         Buffer array to store the winding numbers in.
#     seed : (n_blocks,) 1D array
#         Initial set of winding numbers.
#     n_scans : int
#         Number of scans for the cogwheel cycle.
#     last_zero : bool
#         Whether the last winding number shoud be kept zero. This is reasonable
#         if all CTPs have the same total coherence order change as the reference
#         path because then only the differences between winding numbers do
#         really matter.
#     no_inverse : bool
#         Whether the last non-zero winding number is counted up only to
#         n_scans//2 and not n_scans-1. This avoids generating the phase inverted
#         counterparts of other sets of winding numbers.
#     no_cfscan : bool
#         Whether to avoid sets of winding numbers, where every winding number and
#         the number of scans share a common factor. This would result in an
#         redundant cycle, i.e. a cycle that has smaller length but is repeated.
#     no_cfwind : bool
#         Whether to avoid sets of winding numbers, where the winding numbers 
#         share a common factor. Such cycles would be equivalent (selecting the)
#         same CTPs as the cycle with winding numbers, where the common factor
#         is devided out.
#         If this option is set, setting `no_cfscan` has no effect anymore.
    
#     Returns
#     -------
#     n_filled : int
#         Number of sets of winding numbers written to the buffer. Equal to the
#         number of rows in buffer if the buffer has been filled or smaller.
#     new_seed : (n_blocks,) 1D array
#         Seed for the next filling of the buffer.
#     all_done : bool
#         Whether the end of the counting has been reached.
#     """
    
#     # check shape of input
#     if not buffer.ndim == 2:
#         raise ValueError("`buffer` must be two dimensional!")
#     if not seed.ndim == 1:
#         raise ValueError("`seed` must be one dimensional!")
#     if not buffer.shape[1] == seed.size:
#         raise ValueError("Shapes of `buffer` and `seed` are not compatible!")
    
#     # get some parameters
#     n_buffered = buffer.shape[0]
#     n_blocks  = seed.size
#     n_workers = min(numba.get_num_threads(), n_buffered)
    
#     # allocate array for new seed, working array and copy given seed
#     new_seed = np.zeros_like(seed)
#     windings_working = np.zeros(n_blocks, dtype=seed.dtype)
#     windings_working[:] = seed[:]
    
#     # allocate some arrays for each worker
#     windings_workers   = np.zeros((n_workers, n_blocks), dtype=seed.dtype)
#     #windings_workers[:,0] = 1
#     overflowed_workers = np.ones((n_workers,), dtype=np.bool_)
#     haderror_workers   = np.zeros((n_workers,), dtype=np.bool_)
#     n_filled_workers   = np.zeros((n_workers,), dtype=np.int64)
#     n_filled = 0
    
#     # sequentially fill initial element of workers
#     for idx_worker in range(n_workers):
        
#         # set winding numbers
#         windings_workers[idx_worker,:] = windings_working[:]
#         overflowed_workers[idx_worker] = False
        
#         # generate next winding numbers
#         res = _next_windings_numba(windings_working, n_scans,
#                     last_zero, no_inverse, no_cfscan, no_cfwind)
#         if res == 0:
#             continue
#         elif res == 1:
#             break
#         else:
#             return -1, new_seed, False
    
#     # parallel loop for each worker
#     for idx_worker in numba.prange(n_workers):
#         # loop over all rows that have to be set by this worker
#         for idx_buffer in range(idx_worker, n_buffered, n_workers):
            
#             # only do work if no overflow yet
#             if overflowed_workers[idx_worker]:
#                 break
            
#             # set windings to buffer
#             buffer[idx_buffer,:] = windings_workers[idx_worker,:]
#             n_filled_workers[idx_worker] += 1
            
#             # count up the winding numbers of this worker
#             for _ in range(n_workers):
#                 res = _next_windings_numba(
#                             windings_workers[idx_worker,:], n_scans,
#                             last_zero, no_inverse, no_cfscan, no_cfwind)
#                 if res == 0:
#                     continue
#                 elif res == 1:
#                     overflowed_workers[idx_worker] = True
#                     break
#                 else:
#                     haderror_workers[idx_worker] = True
#                     break
                
    
#     # check if any worker had an error
#     if np.any(haderror_workers):
#         return -1, new_seed, False
    
#     # number of set phases
#     n_filled += n_filled_workers.sum()
    
#     # get new seed
#     new_seed[:] = buffer[n_filled-1,:]
#     res = _next_windings_numba(
#                 new_seed, n_scans,
#                 last_zero, no_inverse, no_cfscan, no_cfwind)
    
#     if res == 0:
#         return n_filled, new_seed, False
#     elif res == 1:
#         return n_filled, new_seed, True
#     else:
#         return -1, new_seed, False





# @numba.njit(parallel=True, fastmath=True)
# def _fill_buffer_windings_numbap(buffer, seed, n_scans, last_zero, no_inverse,
#                                  no_comfacs_nscans, no_comfac_windings):
#     """
#     Given a seed set of winding numbers, fill a given buffer with consecutive
#     sets of winding numbers.
    
#     Parameters
#     ----------
#     buffer : (n_buffered,n_blocks) 2D array
#         Buffer array to store the winding numbers in.
#     seed : (n_blocks,) 1D array
#         Initial set of winding numbers.
#     n_scans : int
#         Number of scans for the cogwheel cycle.
#     last_zero : bool
#         Whether the last winding number shoud be kept zero. This is reasonable
#         if all CTPs have the same total coherence order change as the reference
#         path because then only the differences between winding numbers do
#         really matter.
#     no_inverse : bool
#         Whether the last non-zero winding number is counted up only to
#         n_scans//2 and not n_scans-1. This avoids generating the phase inverted
#         counterparts of other sets of winding numbers.
#     no_cfscan : bool
#         Whether to avoid sets of winding numbers, where every winding number and
#         the number of scans share a common factor. This would result in an
#         redundant cycle, i.e. a cycle that has smaller length but is repeated.
#     no_cfwind : bool
#         Whether to avoid sets of winding numbers, where the winding numbers 
#         share a common factor. Such cycles would be equivalent (selecting the)
#         same CTPs as the cycle with winding numbers, where the common factor
#         is devided out.
#         If this option is set, setting `no_cfscan` has no effect anymore.
    
#     Returns
#     -------
#     n_filled : int
#         Number of sets of winding numbers written to the buffer. Equal to the
#         number of rows in buffer if the buffer has been filled or smaller.
#     new_seed : (n_blocks,) 1D array
#         Seed for the next filling of the buffer.
#     all_done : bool
#         Whether the end of the counting has been reached.
#     """
    
#     # check shape of input
#     if not buffer.ndim == 2:
#         raise ValueError("`buffer` must be two dimensional!")
#     if not seed.ndim == 1:
#         raise ValueError("`seed` must be one dimensional!")
#     if not buffer.shape[1] == seed.size:
#         raise ValueError("Shapes of `buffer` and `seed` are not compatible!")
    
#     # copy seed to private working array
#     n_buffered = buffer.shape[0]
#     n_blocks  = seed.size
#     n_workers = numba.get_num_threads()
    
#     # allocate working array and copy seed
#     windings_working = np.zeros(n_blocks, dtype=seed.dtype)
#     windings_working[:] = seed[:]
#     # for output of new seed
#     new_seed = np.zeros(n_blocks, dtype=seed.dtype)
#     n_filled = 0
    
#     # just fill whole buffer sequentially, no parallelization needed
#     if n_buffered <= n_workers:
#         for idx in range(n_buffered):
#             buffer[idx,:] = windings_working[:]
#             n_filled += 1
#             #res = _count_up_windings_numba(windings_working, n_scans, last_zero, no_inverse)
#             res = _next_windings_numba(windings_working, n_scans, 
#                      last_zero, no_inverse, no_comfacs_nscans, no_comfac_windings)
#             if res == 0:
#                 continue
#             elif res == 1:
#                 new_seed[:] = windings_working[:]
#                 return n_filled, new_seed, True
#             else:
#                 return -1, new_seed, False
        
#         # buffer is now filled
#         new_seed[:] = windings_working[:]
#         return n_filled, new_seed, False
    
        
#     # set of winding numbers for each worker
#     windings_worker = np.zeros((n_workers,n_blocks), dtype=seed.dtype)
    
#     # initialize the workers sequentially
#     for idx_worker in range(n_workers):
#         windings_worker[idx_worker,:] = windings_working[:]
#         buffer[idx_worker,:] = windings_working[:]
#         n_filled += 1
#         #res = _count_up_windings_numba(windings_working, n_scans, last_zero, no_inverse)
#         res = _next_windings_numba(windings_working, n_scans, 
#                      last_zero, no_inverse, no_comfacs_nscans, no_comfac_windings)
#         if res == 0:
#             continue
#         elif res == 1:
#             new_seed[:] = windings_working[:]
#             return n_filled, new_seed, True
#         else:
#             return -1, new_seed, False
        
#     # buffer cannot be filled at this point, either overflow before or still work to do
#     if n_filled == n_buffered:
#         return -1, new_seed, False
    
#     # end of sequential setup phase, entering the parallel phase
    
#     # store how many rows have been filled by each worker
#     n_filled_worker = np.zeros(n_workers, dtype=np.uint64)
#     # store whether worker has reached overflow or not
#     overflowed_worker = np.zeros(n_workers, dtype=np.bool_)
    
#     # start workers to pupulate buffer in parallel
#     for idx_worker in numba.prange(n_workers):
        
#         # loop for each worker
#         overflow = False
#         for idx_buffer in range(idx_worker+n_workers, n_buffered, n_workers):
            
#             # try to count up own set of winding numbers
#             for _ in range(n_workers):
#                 #res = _count_up_windings_numba(windings_worker[idx_worker,:], n_scans, last_zero, no_inverse)
#                 res = _next_windings_numba(windings_worker[idx_worker,:], n_scans, 
#                      last_zero, no_inverse, no_comfacs_nscans, no_comfac_windings)
#                 if res != 0:
#                     overflow = True
#                     overflowed_worker[idx_worker] = True
#                     break
            
#             # set row if no overflow occured, else break the loop
#             if overflowed_worker[idx_worker]:
#                 break
#             else:
#                 buffer[idx_buffer,:] = windings_worker[idx_worker,:]
#                 n_filled_worker[idx_worker] += 1

    
#     n_filled += n_filled_worker.sum()
#     n_overflowed = 0
#     for idx_worker in range(n_workers):
#         if overflowed_worker[idx_worker]:
#             n_overflowed += 1
    
#     # if no worker overflowed, buffer must be filled
#     if n_overflowed > 0:
        
#         # if any overflow, buffer cannot be filled completely
#         if not n_filled < n_buffered:
#             return -1, new_seed, False
        
#         # number of overflows must match
#         if not min(n_buffered-n_filled, n_workers) == n_overflowed:
#             return -1, new_seed, False
        
#         # verify that correct workers overflowed and correct rows were set
#         last_idx = (n_filled-1)%n_workers
#         for idx_worker in range(n_workers):
#             if idx_worker <= last_idx:
#                 if not n_filled_worker[idx_worker] == (n_filled-1)//n_workers:
#                     return -1, new_seed, False
#             else:
#                 if not n_filled_worker[idx_worker] == (n_filled-1)//n_workers-1:
#                       return -2, new_seed, False
#             if (idx_worker-last_idx-1)%n_workers < n_overflowed:
#                 if not overflowed_worker[idx_worker]:
#                     return -3, new_seed, False
#             else:
#                 if overflowed_worker[idx_worker]:
#                     return -4, new_seed, False
            
#         new_seed[:] = buffer[n_filled-1,:]
#         #res = _count_up_windings_numba(new_seed, n_scans, last_zero, no_inverse)
#         res = _next_windings_numba(new_seed, n_scans, 
#                      last_zero, no_inverse, no_comfacs_nscans, no_comfac_windings)
#         # recheck if overflow really happened
#         if not res == 1:
#             return -5, new_seed, False
        
#         new_seed[:] = windings_worker[last_idx,:]
#         return n_filled, new_seed, True
    
#     else:
        
#         # if not overflow, buffer must be filled completely
#         if not n_filled == n_buffered:
#             return -1, new_seed, False
        
#         # find index of worker, that filled the last row and count up its windings
#         last_idx = (n_filled-1)%n_workers
        
#         # generate new seed from last line
#         #res = _count_up_windings_numba(windings_worker[last_idx,:], n_scans, last_zero, no_inverse)
#         res = _next_windings_numba(windings_worker[last_idx,:], n_scans, 
#                      last_zero, no_inverse, no_comfacs_nscans, no_comfac_windings)
#         new_seed[:] = windings_worker[last_idx,:]
#         if res == 0:
#             return n_filled, new_seed, False
#         elif res == 1:
#             return n_filled, new_seed, True
#         else:
#             return -1, new_seed, False






##########################################################################
#                                                                        #
#  V   V   AAA   L       III   DDDD    AAA   TTTTT   III   N   N   GGGG  #
#  V   V  A   A  L        I    D   D  A   A    T      I    NN  N  G      #
#  V   V  AAAAA  L        I    D   D  AAAAA    T      I    N N N  G  GG  #
#   V V   A   A  L        I    D   D  A   A    T      I    N  NN  G   G  #
#    V    A   A  LLLLL   III   DDDD   A   A    T     III   N   N   GGG   #
#                                                                        #
##########################################################################



@numba.njit()
def are_ctps_passed_cogwheel_numba(n_scans, windings, dctps0):
    """
    Determine what CTPs are passed by a cogwheel phase cycle defined by the
    number of scans and winding numbers.
    
    Parameters
    ----------
    n_scans : int
        Number of scans for the cogwheel cycle.
    windings : (n_blocks,) 1D array
        Winding numbers for each pulse block. Each should be a number between
        0 and n_scans-1 as all numbers outside this interval are equivalent to
        one of those inside.
    dctps0 : (n_ctps,n_blocks) 2D array
        Coherence order changes relative to the coherence order changes of
        the reference path. The desired paths must be given first.
    
    Returns
    -------
    is_passed : (n_ctps,) array of bool
        Whether a CTP is passed by the phasecycle corresponing to the winding
        numbers.
    """
    
    # check size and shape of input
    if not windings.ndim == 1:
        raise ValueError('Internal error: `windings` must be 1D.')
    if not dctps0.ndim == 2:
        raise ValueError('Internal error: `dctps0` must be 2D.')
    if not windings.size == dctps0.shape[1]:
        raise ValueError('Internal error: Second dimensions of `winding_numbers` '
                         'and `dctps0` must have same size.')
        
    n_ctps   = dctps0.shape[0]
    n_blocks = windings.shape[0]
    
    # allocate output array
    is_passed = np.zeros(n_ctps, dtype=np.bool_)
    
    # loop over all CTPs
    for idx_ctp in range(n_ctps):
        # sum up total coherence change
        dcpts0summed = 0
        for idx_block in range(n_blocks):
            dcpts0summed += windings[idx_block]*dctps0[idx_ctp, idx_block]
        # if sum is zero, current cycle passes CTP
        if dcpts0summed % n_scans == 0:
            is_passed[idx_ctp] = True
        else:
            is_passed[idx_ctp] = False
    
    return is_passed





@numba.njit(fastmath=True)
def _cogwheel_check_valid_numba(n_scans, windings, dctps0, n_ctps_wanted, last_zero):
    """
    Check whether a cogwheel cycle is valid or not.
    
    A cogwheel cycle is valid if the sum of relative coherence order changes
    times the winding number per block is a multiple of the number of scans for
    every desired path and something else for every undesired path. This
    function is compiled with Numba and uses the fastmath flag.
    
    Parameters
    ----------
    n_scans : int
        Number of scans for the cogwheel cycle.
    windings : (n_blocks,) 1D array
        Winding numbers for each pulse block. Each should be a number between
        0 and n_scans-1 as all numbers outside this interval are equivalent to
        one of those inside.
    dctps0 : (n_ctps, n_blocks) 2D array
        Coherence order changes relative to the coherence order changes of
        the reference path. The desired paths must be given first.
    n_ctps_wanted : int
        Number of desired paths. The first n_ctps_wanted rows of dctps0 must
        be the desired paths, the following ones the undesired ones.
    last_zero : bool
        If set, the last winding number is considered to be zero and ignored in
        the summation saving a little time. This is only reasonable if all CTPs
        have the same total coherence order change. Wether this holds is not
        checked by this function.
    
    Returns
    -------
    is_valid : int
        The result 0 indicates a valid cycle, everything else an invalid cycle.
        1 indicates, that a desired path is blocked and 2 that an undesired
        path is not blocked.
    """
    
    # number of CTPs
    n_ctps = dctps0.shape[0]
    
    # do not consider the last winding number (assumed to be 0), only valid
    # if all CTPs have the same total coherence order change (not checked here)
    if last_zero:
        n_blocks = dctps0.shape[1] - 1
    else:
        n_blocks = dctps0.shape[1]

    # loop over all desired paths
    for idx_ctp in range(n_ctps_wanted):
            
        # sum up total coherence change
        dcpts0summed = 0
        for idx_block in range(n_blocks):
            dcpts0summed += windings[idx_block]*dctps0[idx_ctp, idx_block]
        
        # if any desired path is blocked then stop as cycle is invalid
        if dcpts0summed % n_scans != 0:
            return False
            
    # loop over all undesired paths
    for idx_ctp in range(n_ctps_wanted, n_ctps):
        
        # sum up total relative coherence order change times winding number
        dcpts0summed = 0
        for idx_block in range(n_blocks):
            dcpts0summed += windings[idx_block]*dctps0[idx_ctp, idx_block]
        
        # if any undesired path is passed then stop as cycle is invalid
        if dcpts0summed % n_scans == 0:
            return False
    
    return True





@numba.njit(fastmath=True, parallel=True)
def _cogwheels_check_valid_numba(n_scans, windings, n_check, dctps0, n_ctps_wanted, last_zero):
    """
    Check whether cogwheel cycles are valid or not.
    
    A cogwheel cycle is valid if the sum of relative coherence order changes
    times the winding number per block is a multiple of the number of scans for
    every desired path and something else for every undesired path. This
    function is compiled with Numba and uses the fastmath flag. The checking
    of different cogwheel cyles is parallized.
    
    Parameters
    ----------
    n_scans : int
        Number of scans for the cogwheel cycle.
    windings : (n_check,n_blocks) 2D array
        Winding numbers for each pulse block. Each should be a number between
        0 and n_scans-1 as all numbers outside this interval are equivalent to
        one of those inside. One row corresponds to one set of winding numbers.
    n_check : int
        Number of sets of winding numbers to check. Only the first n_check
        winding numbers are really checked, the rest is ignored.
    dctps0 : (n_ctps,n_blocks) 2D array
        Coherence order changes relative to the coherence order changes of
        the reference path. The desired paths must be given first.
    n_ctps_wanted : int
        Number of desired paths. The first n_ctps_wanted rows of dctps0 must
        be the desired paths, the following ones the undesired ones.
    last_zero : bool
        If set, the last winding number is considered to be zero and ignored in
        the summation saving a little time. This is only reasonable if all CTPs
        have the same total coherence order change. Wether this holds is not
        checked by this function.
    
    Returns
    -------
    is_valid : (n_check,) 1D array of bool
        For the first n_check sets of winding numbers whether the cycle is
        valid or not.
    """
    
    n_check = min(max(0,n_check), windings.shape[0])
    is_valid = np.zeros(n_check, dtype=np.bool_)
    
    for idx in numba.prange(n_check):
         res = _cogwheel_check_valid_numba(n_scans, windings[idx,:],
                                           dctps0, n_ctps_wanted, last_zero)
         is_valid[idx] = res
    
    return is_valid







###################################################################
#                                                                 #
#   SSSS  EEEEE   AAA   RRRR    CCCC  H   H   III   N   N   GGGG  #
#  S      E      A   A  R   R  C      H   H    I    NN  N  G      #
#   SSS   EEE    AAAAA  RRRR   C      HHHHH    I    N N N  G  GG  #
#      S  E      A   A  R  R   C      H   H    I    N  NN  G   G  #
#  SSSS   EEEEE  A   A  R   R   CCCC  H   H   III   N   N   GGG   #
#                                                                 #
###################################################################



@numba.njit()
def _search_cogwheel_exhaustive_numba(n_scans_min, n_scans_max,
                        last_zero, no_inverse, no_cfscan, no_cfwind,
                        windings_out, n_scans_out, windings_buffer,
                        dctps0, n_ctps_wanted, verbose=False):
    """
    Search cogwheel cycle.
    """
    
    # check all input arrays for correct shape
    if not dctps0.ndim == 2:
        raise ValueError('_search_windings_numba: `dctps0` should be 2D.')
    if not windings_out.ndim == 2:
        raise ValueError('_search_windings_numba: `windings_out` should be 2D.')
    if not windings_buffer.ndim == 2:
        raise ValueError('_search_windings_numba: `windings_buffer` should be 2D.')
    if not n_scans_out.ndim == 1:
        raise ValueError('_search_windings_numba: `n_scans_out` should be 1D.')
    
    n_blocks = dctps0.shape[1]
    if not windings_out.shape[1] == n_blocks:
        raise ValueError('_search_windings_numba: `windings_out` has not the correct size.')
    if not windings_buffer.shape[1] == n_blocks:
        raise ValueError('_search_windings_numba: `windings_buffer` has not the correct size.')
    
    # find the minimum and maximum number of scans checked
    n_scans_min = max(2, n_scans_min)
    n_scans_max = max(n_scans_min, n_scans_max)
    
    # number of windings to find and how many have been found
    n_find = windings_out.shape[0]
    n_found = 0
    
    # number of possible windings in buffer
    n_windings_buffer = windings_buffer.shape[0]
    
    # print what is about to happen
    if verbose:
        print('Searching from ... to ...', n_scans_min, n_scans_max)
        print('Try to find', n_find)
        print('Size of buffer', n_windings_buffer)
    
    # buffer for windings numbers
    init_windings = np.zeros(shape=(n_blocks,), dtype=windings_out.dtype)
    
    found_solution = False
    all_found = False
    
    # loop over the number of scans to check
    for n_scans in range(n_scans_min, n_scans_max+1):
        
        if verbose: print('Checking for', n_scans, 'scans...')
        init_windings[:] = 0
        
        all_checked = False
        while(not all_checked):
            
            # fill the buffer with next windings
            n_buffered, windings_working, all_checked = _fill_buffer_windings_numba(
                windings_buffer, init_windings, n_scans, last_zero, no_inverse, no_cfscan, no_cfwind,)
            init_windings[:] = windings_working[:]
            
            # check the sets of winding numbers
            is_valid = _cogwheels_check_valid_numba(n_scans, windings_buffer,
                                                    n_buffered, dctps0, n_ctps_wanted, last_zero)
            
            # copy solutions to output array
            for idx in range(n_buffered):
                if is_valid[idx]:
                    found_solution = True
                    windings_out[n_found,:] = windings_buffer[idx,:]
                    n_scans_out[n_found] = n_scans
                    n_found += 1
                    #if verbose: print('  --> Found solution:', windings_buffer[idx,:])
                    # break 
                    if n_found >= n_find:
                        all_found = True
                        break
                    
            if all_found:
                break
                
        if found_solution:
            break
        else:
            pass
            #if verbose: print('Nothing found...')
        
    else:
        #if verbose: print('All checked but nothing found...')
        return 0
    
    #if verbose: print('Found solutions!')
    return n_found





# def search_cogwheel_exhaustive(ctp, n_scans_max, n_scans_min=-1,
#                                last_zero=None, no_inverse=True, no_cfscan=True, no_cfwind=True,
#                                n_find=1, verbose=False):
#     """
    
#     Parameters
#     ----------
    
#     Returns
#     -------
#     """
    
#     dctps0, metadata = ctp.generate_numpy_array('dctps0', collapse=True, push_desired_up=True)
#     n_ctps_wanted = metadata['n_desired']
    
    
#     # check shape of input
#     if not dctps0.ndim == 2:
#         raise ValueError('dctps0 must be 2D!')
#     dctps0 = np.int64(dctps0)
    
#     n_blocks = dctps0.shape[1]
    
#     if last_zero is None:
#         dctps0_summed = np.sum(dctps0, axis=1)
#         if np.all(dctps0_summed == dctps0_summed[0]):
#             last_zero = True
#         else:
#             last_zero = False
        
#     # find the minimum and maximum number of scans checked
#     n_scans_min = int(max(2, n_scans_min))
#     n_scans_max = int(max(n_scans_min, n_scans_max))
    
#     # allocate the output arrays
#     windings_out = np.zeros((n_find, n_blocks), dtype=np.int64)
#     n_scans_out = np.zeros((n_find), dtype=np.int64)
    
#     # allocate the buffer of 32 MiB
#     n_buffered = 32*1024*1024 // (8*n_blocks)
#     windings_buffer = np.zeros((n_buffered, n_blocks), dtype=np.int64)
    
#     n_found = _search_cogwheel_exhaustive_numba(n_scans_min, n_scans_max,
#                             last_zero, no_inverse, no_cfscan, no_cfwind,
#                             windings_out, n_scans_out, windings_buffer,
#                             dctps0, n_ctps_wanted, verbose=verbose)
    
#     del windings_buffer
    
#     return windings_out[:n_found,:], n_scans_out[:n_found]



def search_cogwheel_exhaustive(ctp, n_scans_max, n_scans_min=-1,
                               last_zero=None, no_inverse=True, no_cfscan=False, no_cfwind=False,
                               n_find=1, verbose=0):
    """
    Parameters
    ----------
    
    Returns
    -------
    """
    
    dctps0, metadata = ctp.generate_numpy_array('dctps0', collapse=True, push_desired_up=True)
    n_ctps_wanted = metadata["n_desired"]
    
    if verbose >= 1:
        print("="*80)
        print("SEARCHING COGWHEEL CYCLES EXHAUSTIVELY")
        print("="*80)
    
    
    CACHE_MAX_MB = 1024.0
    DTYPE = np.int64
    
    # check shape of input
    if not dctps0.ndim == 2:
        raise ValueError("`dctps0` must be 2D!")
    
    n_ctps_wanted = int(n_ctps_wanted)
    if n_ctps_wanted < 0 or n_ctps_wanted >= dctps0.shape[0]:
        raise ValueError("nonono")
        
    n_blocks = dctps0.shape[1]
    
    # find whether to treat last winding number as zero based on CTPs
    if last_zero is None:
        dctps0_summed = np.sum(dctps0, axis=1)
        if np.all(dctps0_summed == dctps0_summed[0]):
            last_zero = True
        else:
            last_zero = False
            
    if verbose >= 1:
        print("--> `last_zero` is set to {}".format(last_zero))
        print("--> `no_inverse` is set to {}".format(no_inverse))
        print("--> `no_cfscan` is set to {}".format(no_cfscan))
        print("--> `no_cfwind` is set to {}".format(no_cfwind))
        
    
    # find the minimum and maximum number of scans checked
    n_scans_min = int(max(2, n_scans_min))
    n_scans_max = int(max(n_scans_min, n_scans_max))
    
    
    
    # allocate the cache
    n_cached = int(np.floor( CACHE_MAX_MB * (1024**2/np.dtype(DTYPE).itemsize/n_blocks) ))
    windings_cache = np.empty(shape=(n_cached,n_blocks), dtype=DTYPE)
    windings_cache.fill(0)
    
    if verbose >= 2:
        print("--> Allocated cache for {} sets of winding "
              "numbers ({:.3f} MB)".format(n_cached, windings_cache.nbytes/1024**2))
        
    # allocate array for output
    windings_out = np.empty(shape=(n_find,n_blocks), dtype=DTYPE)
    windings_out.fill(0)
    
    if verbose >= 2:
        print("--> Allocated output array for {} sets of winding "
              "numbers ({:.3f} kB)".format(n_find, windings_out.nbytes/1024))
    
    
    if verbose >= 1:
        print("\n"+"="*80)
        print("START Searching cogwheel cycles from {} to {} scans...".format(n_scans_min,n_scans_max))
        print("="*80)
    
        
    n_found = 0
    for n_scans in range(n_scans_min, n_scans_max+1):
        
        n_checked = 0
        
        if verbose >= 1:
            print("--> Searching for number of scans: {}".format(n_scans))
            
            
        # initial set of winding numbers
        windings_seed = np.empty((n_blocks,), dtype=DTYPE)
        res = _init_windings_numba(
            windings_seed, n_scans, False, False, False, False)
        
        all_done = False
        while not all_done:
            
            
            # fill buffer with winding numbers
            if verbose >= 2:
                print("    --> Initial set: ", windings_seed)
            n_filled, windings_seed, all_done = _fill_buffer_windings_numbap(
                windings_cache, windings_seed, n_scans,
                last_zero, no_inverse, no_cfscan, no_cfwind)
            
            n_checked += n_filled
            
            if verbose >= 2:
                print("    --> Cached {} sets of winding numbers".format(n_filled))
            
            # check all the winding numbers
            if verbose >= 2:
                print("    --> Checking cached winding numbers... ")
            are_valid = _cogwheels_check_valid_numba(
                n_scans, windings_cache, n_filled, dctps0, n_ctps_wanted, last_zero)
            
            if verbose >= 2:
                print("    --> Writing to output array... ")
            
            # write solutions to output array
            n_found = _copy_by_mask_numba(windings_cache, windings_out, are_valid, True, n_found)
            
            if n_found >= n_find:
                
                if verbose >= 1:
                    print("Enough solutions have been found.")
                
                break
            
            
            
        if verbose >= 2:
            print("    Total number of checked cycles: {}".format(n_checked))
        
        if n_found > 0:
            break
     
    
    if verbose >= 1:
        print("="*80)
        if n_found != 0:
            print("DONE Valid solution has been found.")
        else:
            print("DONE All number of scans searched.")
        print("="*80+"\n")
    
    
    
    # free cache memory
    del windings_cache
    
    if verbose >= 2:
        print("--> Cache for sets of winding numbers freed.")
        
        
    return windings_out



    



#######################################
#                                     #
#  N   N   III    CCCC   OOO    GGGG  #
#  NN  N    I    C      O   O  G      #
#  N N N    I    C      O   O  G  GG  #
#  N  NN    I    C      O   O  G   G  #
#  N   N   III    CCCC   OOO    GGG   #
#                                     #
#######################################



def cost_niCOG(windings, N, dCTPs0, S0):
    """
    Cost function for the selectivity of a cogwheel phase cylce.
    
    Parameters
    ----------
    windings : (Nb,) array_like
        Winding numbers for each block.
    N : int
        Number of scans.
    dCTPs0 : (Np,Nb) array_like
        Changes of coherence order for each block and path relative to the
        changes of coherence order for the reference path.
    S0 : (Np,) array_like
        Vector of wanted signal for each CTP averaged over all scans. Set the
        elements to 1 for a wanted pathway and 0 for an unwanted.
    
    Returns
    -------
    cost : float
        Value of the cost function.    
    """
    
    k = np.linspace(0,N-1,N)
    phases = windings[None,:] * k[:,None] * 2.0*np.pi/N
    dphi = np.sum(phases[None,:,:] * dCTPs0[:,None,:], axis=2)
    S = np.sum( np.exp(-1j*dphi), axis=1 ) / N
    
    return np.square(np.abs( S-S0 )).sum()





def jac_niCOG(windings, N,  dCTPs0, S0):
    """
    Analytical gradient for the selectivity of a cogwheel phase cylce.
    
    Parameters
    ----------
    windings : (Nb,) array_like
        Winding numbers for each block.
    N : int
        Number of scans.
    dCTPs0 : (Np,Nb) array_like
        Changes of coherence order for each block and path relative to the
        changes of coherence order for the reference path.
    S0 : (Np,) array_like
        Vector of wanted signal for each CTP averaged over all scans. Set the
        elements to 1 for a wanted pathway and 0 for an unwanted.
    
    Returns
    -------
    cost : float
        Value of the cost function.    
    """
    
    k = np.linspace(0,N-1,N)
    phases = windings[None,:] * k[:,None] * 2.0*np.pi/N
    dphi = np.sum(phases[None,:,:] * dCTPs0[:,None,:], axis=2)
    phfac = np.exp(-1j*dphi)
    S = np.sum( phfac, axis=1 ) / N
    
    summand = np.imag( dCTPs0 * np.conjugate(S-S0)[:,None] * np.sum(k[None,:]*phfac,axis=1)[:,None] )
    
    return np.sum(summand, axis=0) * 4.0*np.pi/N**2





def costjac_niCOG(windings, N,  dCTPs0, S0):
    """
    Cost function and gradient for the selectivity of a cogwheel phase cylce.
    
    Parameters
    ----------
    windings : (Nb,) array_like
        Winding numbers for each block.
    N : int
        Number of scans.
    dCTPs0 : (Np,Nb) array_like
        Changes of coherence order for each block and path relative to the
        changes of coherence order for the reference path.
    S0 : (Np,) array_like
        Vector of wanted signal for each CTP averaged over all scans. Set the
        elements to 1 for a wanted pathway and 0 for an unwanted.
    
    Returns
    -------
    cost : float
        Value of the cost function.    
    """
    
    k = np.linspace(0,N-1,N)
    phases = windings[None,:] * k[:,None] * 2.0*np.pi/N
    phfac = np.exp(-1j*np.sum(phases[None,:,:]*dCTPs0[:,None,:], axis=2))
    S = np.sum( phfac, axis=1 ) / N
    
    cost = np.square(np.abs( S-S0 )).sum()
    
    summand = np.imag( dCTPs0 * np.conjugate(S-S0)[:,None] * np.sum(k[None,:]*phfac,axis=1)[:,None] )
    jac = np.sum(summand, axis=0) * 4.0*np.pi/N**2
    
    return cost, jac





def jacnum_niCOG(windings, N, dCTPs0, S0, dwind=1e-10):
    """
    Numerical gradient for the selectivity of a cogwheel phase cylce.
    
    Parameters
    ----------
    windings : (Nb,) array_like
        Winding numbers for each block.
    N : int
        Number of scans.
    dCTPs0 : (Np,Nb) array_like
        Changes of coherence order for each block and path relative to the
        changes of coherence order for the reference path.
    S0 : (Np,) array_like
        Vector of wanted signal for each CTP averaged over all scans. Set the
        elements to 1 for a wanted pathway and 0 for an unwanted.
    
    Returns
    -------
    cost : float
        Value of the cost function.    
    """
    
    windings = np.copy(windings)
    jac = np.zeros(windings.size)
    
    for i in range(jac.size):
        windings[i] += dwind
        cost_p = cost_niCOG(windings, N, dCTPs0, S0)
        windings[i] -= 2.0*dwind
        cost_m = cost_niCOG(windings, N, dCTPs0, S0)
        windings[i] += dwind
        jac[i] = 0.5*(cost_p-cost_m)/dwind
    
    return jac





# @numba.njit(fastmath=True)
# def cogwheel_check_valid_numba(nScans, windings, dctps0_wanted, dctps0_unwanted):
    
#     nBlocks = windings.size
#     nWanted = dctps0_wanted.shape[0]
#     nUnwanted = dctps0_unwanted.shape[0]

#     # loop over all wanted paths
#     for idxPath in range(nWanted):
            
#         # sum up total coherence change
#         dcpts0sum = 0
#         for idxBlock in range(nBlocks):
#             dcpts0sum += windings[idxBlock]*dctps0_wanted[idxPath, idxBlock]
        
#         # if any desired path is blocked then stop
#         if dcpts0sum % nScans != 0:
#             return 1
            
#     # loop over all unwanted paths
#     for idxPath in range(nUnwanted):
        
#         # sum up total coherence change
#         dcpts0sum = 0
#         for idxBlock in range(nBlocks):
#             dcpts0sum += windings[idxBlock]*dctps0_unwanted[idxPath, idxBlock]
        
#         # if any undesired path is passed then stop
#         if dcpts0sum % nScans == 0:
#             return 2
    
#     return 0



# @numba.njit(parallel=True, fastmath=True)
# def cogwheels_check_valid_numba(nScans, windings, dctps0_wanted, dctps0_unwanted):
    
#     nCogs = windings.shape[0]
#     results = np.full(nCogs, -1, dtype=np.int64)
    
#     for idxCog in numba.prange(nCogs):
#         results[idxCog] = cogwheel_check_valid_numba(nScans, windings[idxCog], dctps0_wanted, dctps0_unwanted)
        
#     return results



# @numba.njit(parallel=True)
# def search_coghweel_exhaustive(nScansMin, nScansMax, dCTPs0Wanted, dCTPs0Unwanted, nFind=1,
#                              verbose=False, breakOnZero=False, breakOnHalf=True, nDist=5000):
#     """
#     Find cogwheel phase cycle by exhaustive search.
    
#     Parameters
#     ----------
#     nScansMin : int
#         Minimum number of scans to search for a cogwheel cycle.
#     nScansMax : int
#         Maximum number of scans to search for a cogwheel cycle.
#     dCTPs0Wanted : (nWanted, nBlocks) ndarray
#         Changes of coherence order for each block and wanted path relative to
#         the changes of coherence order for the reference path.
#     dCTPs0Unwanted : (nUnwanted, nBlocks) ndarray
#         Changes of coherence order for each block and unwanted path relative to
#         the changes of coherence order for the reference path.
#     nFind : int
#         Number of solutions to find. The search will terminate when this number
#         of solution is found or all sets of winding numbers are searched for
#         the minimum number of scans, for which solutions exist.
#     breakOnZero : bool
#         The search is terminated for the current number of scans, when the last
#         winding number gets greater than zero. This means that only sets of
#         winding numbers are considered, that are not equal in their difference,
#         e.g. (1,2,0) is searched but (2,3,1) not. This is reasonable if all
#         CTPs start and end with the same coherence order. Default to False.
#     breakOnHalf : bool
#       The search is terminated for the current number of scans, when the last
#       winding number gets greater than nScans//2. This means that only sets of
#       winding numbers are searched, that are no phase inverted counter part of
#       each other. Defaults to True.
#     nDist : int
#         Number of sets of winding numbers that are searched simultaneously per
#         worker when running in parallel mode.
    
#     Returns
#     -------
#     nScans : int
#         Number of scans for the solutions. When no solutions up to nScansMax
#         are found, -1 is returned.
#     validWindings : (nFound, nBlocks) ndarray
#         Winding numbers of the solutions.
#     """
    
#     # number of scans must be at least 2
#     nScansMin = max(2, nScansMin)
#     nScansMax = max(2, nScansMax)
    
#     # check shape of arrays
#     if not dCTPs0Wanted.ndim == 2 or not dCTPs0Unwanted.ndim == 2:
#         raise ValueError('Coherence order changes must be 2D arrays.')
#     if not dCTPs0Wanted.shape[1] == dCTPs0Unwanted.shape[1]:
#         raise ValueError('Coherence order changes must be of equal size in 2nd dimension.')
#     nBlocks = dCTPs0Wanted.shape[1]
    
#     nFound = 0
#     foundSolution = False
#     validWindings = np.zeros((nFind, nBlocks), dtype=np.int64)
#     nProcs = numba.get_num_threads()*nDist
    
#     # loop over all numbers of scans
#     for nScans in range(nScansMin, nScansMax+1):
        
#         if verbose: print(nScans)
        
#         # set variables for this number of scans
#         allWindingsChecked = False
#         windings = np.zeros(nBlocks, dtype=np.int64)
#         currentWindings = np.zeros((nProcs, nBlocks), dtype=np.int64)
        
#         # infinite loop, that breaks until highest set of windings is reached
#         while(True):
            
#             # generate the next nProc sets of winding numbers
#             for idxProc in range(nProcs):
                
#                 # append to current windings
#                 currentWindings[idxProc] = windings
                
#                 # generate the next set of winding numbers
#                 nSetZero = 0
#                 for idxBlock in range(nBlocks):
#                     if windings[idxBlock] < nScans-1:
#                         windings[idxBlock] += 1
#                         break
#                     else:
#                         windings[idxBlock] = 0
#                         nSetZero += 1
                
                
#                 # break conditions
#                 if breakOnZero:
#                     if breakOnHalf and nBlocks > 1:
#                         if windings[-2] > nScans//2:
#                             nCheck = idxProc + 1; allWindingsChecked = True; break
#                     if windings[-1] > 0:
#                         nCheck = idxProc + 1; allWindingsChecked = True; break
                
#                 if breakOnHalf and windings[-1] > nScans//2:
#                     nCheck = idxProc + 1; allWindingsChecked = True; break
                
#                 if nSetZero == nBlocks:
#                     nCheck = idxProc + 1; allWindingsChecked = True; break
                
#                 nCheck = idxProc + 1
            
#             # check the generated windings
#             results = np.full(nCheck, -1, dtype=np.int64)
#             for idxCheck in numba.prange(nCheck):
#                 results[idxCheck] = cogwheel_check_valid_numba(nScans, currentWindings[idxCheck],
#                                                                dCTPs0Wanted, dCTPs0Unwanted)
            
#             # write the valid windings to output array
#             for idxCheck in range(nCheck):
#                 if results[idxCheck] == 0:
#                     foundSolution = True
#                     validWindings[nFound] = currentWindings[idxCheck]
#                     nFound += 1
                
#                 # done when enough solutions are found
#                 if nFound == nFind:
#                     return nScans, validWindings
            
#             # go to next number of scans if all are checked
#             if allWindingsChecked:
#                 break
        
#         # do not check higher scan numbers if solution was found
#         if foundSolution:
#             return nScans, validWindings[:nFound]
        
#     if verbose: print('No cogwheel cycle found!')
    
#     return -1, np.zeros((1,nBlocks), dtype=np.int64)



# @numba.njit()
# def search_coghweel_random(Nmin, Nmax, nTries, dctps0_wanted, dctps0_unwanted, verbose=False):
    
#     nBlocks = dctps0_wanted.shape[1]
    
#     for nScans in range(Nmin,Nmax+1):
        
#         if verbose: print(nScans)
        
#         for idxTry in range(nTries):
            
#             windings = np.random.randint(0, nScans, size=nBlocks)
            
#             check = cogwheel_check_valid_numba(nScans, windings, dctps0_wanted, dctps0_unwanted)
#             if check == 0:
#                 return nScans, windings
    
#     return -1, windings*0



# @numba.njit(parallel=True, fastmath=True)
# def cogwheels_check_valid_numba(nScans, windings, dctps0_wanted, dctps0_unwanted):
    
#     nCogs = windings.shape[0]
#     nBlocks = windings.shape[1]
#     nWanted = dctps0_wanted.shape[0]
#     nUnwanted = dctps0_unwanted.shape[0]
    
#     results = np.full(nCogs, -1, dtype=np.int64)
    
#     for idxCog in numba.prange(nCogs):
        
#         wantedSupressed = False
#         unwantedPassed = False
    
#         # loop over all wanted paths
#         for idxPath in range(nWanted):
                
#             # sum up total coherence change
#             dcpts0sum = 0
#             for idxBlock in range(nBlocks):
#                 dcpts0sum += windings[idxCog, idxBlock]*dctps0_wanted[idxPath, idxBlock]
            
#             # if any desired path is blocked then stop
#             if dcpts0sum % nScans != 0:
#                 wantedSupressed = True
#                 break
                
#         # if wanted path is supressed, we are done here
#         if wantedSupressed:
#             results[idxCog] = 1
#         else:
#             # loop over all unwanted paths
#             for idxPath in range(nUnwanted):
                
#                 # sum up total coherence change
#                 dcpts0sum = 0
#                 for idxBlock in range(nBlocks):
#                     dcpts0sum += windings[idxCog, idxBlock]*dctps0_unwanted[idxPath, idxBlock]
                
#                 # if any undesired path is passed then stop
#                 if dcpts0sum % nScans == 0:
#                     unwantedPassed = True
#                     break
            
#             # if unwanted path is passed, we are done here
#             if unwantedPassed:
#                 results[idxCog] = 2
#             else:
#                 results[idxCog] = 0
            
#     return results



# @numba.njit(parallel=True)
# def cogwheels_check_valid_numba(nScans, windings, dctps0_wanted, dctps0_unwanted):
    
#     nCogs = windings.shape[0]
#     nBlocks = windings.shape[1]
#     nWanted = dctps0_wanted.shape[0]
#     nUnwanted = dctps0_unwanted.shape[0]
    
#     results = np.full(nCogs, -1, dtype=np.int64)
    
#     for idxCog in numba.prange(nCogs):
        
#         wantedSupressed = False
#         unwantedPassed = False
        
#         # loop over all wanted paths
#         for idxPath in range(nWanted):
                
#             # sum up total coherence change
#             dcpts0sum = 0
#             for idxBlock in range(nBlocks):
#                 dcpts0sum += windings[idxCog, idxBlock]*dctps0_wanted[idxPath, idxBlock]
            
#             # if any desired path is blocked then stop
#             if dcpts0sum % nScans != 0:
#                 wantedSupressed = True
#                 results[idxCog] = 1
#                 break
        
#         if not wantedSupressed:
#             # loop over all unwanted paths
#             for idxPath in range(nUnwanted):
                
#                 # sum up total coherence change
#                 dcpts0sum = 0
#                 for idxBlock in range(nBlocks):
#                     dcpts0sum += windings[idxCog, idxBlock]*dctps0_unwanted[idxPath, idxBlock]
                
#                 # if any undesired path is passed then stop
#                 if dcpts0sum % nScans == 0:
#                     unwantedPassed = True
#                     results[idxCog] = 2
#                     break
                
#         if not (wantedSupressed or unwantedPassed):
#             results[idxCog] = 0
    
#     return results


# OLD IMPLEMENTATION not avoiding e.g. [1,3,2,0,0] (n_scans=4) although equivalent to [3,1,2,0,0]
# @numba.njit(fastmath=True)
# def _count_up_windings_numba(windings, n_scans, last_zero, only_half):
#     """
#     Generate the next set of winding numbers from a given set.
    
#     The operation is performed inplace.
    
#     Parameters
#     ----------
#     windings : 1D array
#         Set of winding numbers to increase inplace.
#     n_scans : int
#         Number of scans for the cogwheel cycle.
#     last_zero : bool
#         Whether the last winding number shoud be kept zero. This is reasonable
#         if all CTPs have the same total coherence order change as the reference
#         path because then only the differences between winding numbers do
#         really matter.
#     only_half : bool
#         Whether the last non-zero winding number is counted up only to
#         n_scans//2 and not n_scans-1. This avoids generating the phase inverted
#         counterparts of other sets of winding numbers.
    
#     Returns
#     -------
#     status : int
#         0 if the set of winding numbers could be counted up, 1 otherwise. In
#         that case the last possible set of winding numbers was generated and
#         the array should be back to all zeroes.
#     """
    
#     # find last active idx
#     if last_zero:
#         idx_max = windings.size - 2
#     else:
#         idx_max = windings.size - 1
    
#     if only_half:
#         final_max = n_scans//2
#     else:
#         final_max = n_scans - 1
        
#     # get index of last zero
#     idx_last_nonzero = idx_max
#     for idx in range(idx_max, -1, -1):
#         if windings[idx] != 0:
#             break
#         idx_last_nonzero -= 1
#     else:
#         # in this case all are zero
#         if idx_max < 0 and last_zero:
#             return 1
#         if windings[0] < final_max:
#             windings[0] += 1
#             return 0
#         else:
#             windings[0] = 0
#             return 1
        
#     for idx in range(0, idx_last_nonzero):
#         if windings[idx] < n_scans - 1:
#             windings[idx] += 1
#             return 0
#         else:
#             windings[idx] = 0
        
#     if windings[idx_last_nonzero] < final_max:
#         windings[idx_last_nonzero] += 1
#         return 0
#     else:
#         windings[idx_last_nonzero] = 0
        
#     if idx_last_nonzero < idx_max:
#         windings[idx_last_nonzero+1] = 1
#         return 0
#     else:
#         return 1


