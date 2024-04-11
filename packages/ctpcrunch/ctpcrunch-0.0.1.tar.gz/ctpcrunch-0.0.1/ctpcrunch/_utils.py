# small script to find phase cycles
import warnings
import numpy as np
import numba as nb

__version__ = '0.4'



#######################################################################
#                                                                     #
#   U   U  TTTTT   III   L       III   TTTTT   III   EEEEE   SSSS     #
#   U   U    T      I    L        I      T      I    E      S         #
#   U   U    T      I    L        I      T      I    EEE     SSS      #
#   U   U    T      I    L        I      T      I    E          S     #
#    UUU     T     III   LLLLL   III     T     III   EEEEE  SSSS      #
#                                                                     #
#######################################################################



def all_combis(*args):
    """
    Return all combinations obtained by choosing one element from N lists.
    
    An array is constructed containing each possible ordered combination
    obtained by choosing one element from a list of variable length per
    position. Each position has its own list.
    
    Parameters
    ----------
    args : array_like
        Lists containing elements for each position.
            
    Returns
    -------
    combis : 2D array
        Array of all combinations obtained by choosing one element from
        each list.
    """
    
    # initialize the lists
    elements = [np.asarray(e).flatten() for e in args]
    dtype = np.find_common_type([e.dtype for e in elements], [])
    
    # get length of list and products for number of repetitions
    lengths = [e.size for e in elements]
    cumprod = np.concatenate(([1], np.cumprod(lengths)))
    cumprod_inv = np.concatenate(([1], np.cumprod(lengths[::-1])))
    
    # allocate space
    combis = np.zeros(shape=(cumprod[-1], len(lengths)), dtype=dtype)
    
    for i in range(len(lengths)):
        combis[:,i] = np.tile(np.repeat(elements[i], cumprod_inv[-2-i]),
                              cumprod[i])
    
    return combis



def construct_ctps(nblocks, pmax, start=0, end=-1):
    """
    Construct an array with all possible coherence order transfer pathways
    possible.
    
    Parameters
    ----------
    nblocks : int
        Number of steps or pulse blocks changing the coherence order.
    pmax : (int, list of lists)
        Maximum possible coherence order present between all pulse blocks or
        a list of maximum possible coherence orders between each consecutive
        pair of pulse blocks.
    start : (int, array_like, str), optional
        Coherence order or list of possible coherence orders at the start.
        Defaults to 0. If 'all', set to pmax.
    end : (int, array_like, str), optional
        Coherence order of list of possible coherence orders at the end.
        Defaults to -1 assuming a perfect quadrature detector.
        If 'all', set to pmax.
    
    Returns
    -------
    CTPs : array_like
        All CTPs possible.
    """
    
    if type(pmax) is int:
    
        if start == 'all' : start = pmax
        if end   == 'all' :   end = pmax
        
        coherences = np.linspace(-pmax, pmax, 2*pmax+1, dtype=int)
        return all_combis(start, *[coherences]*(nblocks-1), end)
    
    elif hasattr(pmax, '__iter__'):
        
        # convert to array
        pmax = np.asarray(pmax).flatten()
        if not len(pmax) == nblocks-1:
            raise ValueError('Length of "pmax" must be one element shorter than the number of blocks.')
        
        coherences = [np.linspace(-p, p, 2*p+1, dtype=int) for p in pmax]
        return all_combis(start, *coherences, end)
        
    else:
        raise TypeError('"pmax" must be integer or a iterable list.')



def get_next_combis(start, steps, nblocks, divisor):
    """
    Generate combinations of integers in the half-open interval [0,divisor).
    
    This function effectively converts a range from consecutive integers
    from 'start' to 'start'+'steps'-1 into their representation in the base of 
    the divisor. This functions is useful to generate some combination of 
    winding numbers for exhaustive cogwheel phase cycle searches.
    
    Parameters
    ----------
    start : int
        Start of the array of consecutive integers that are to be converted.
    steps : int
        Number of steps and total number of integers to be converted.
    nblocks : int
        Number of blocks of the output array. Corresponds to the number of
        digits of the base-'divisor' number.
    divisor : int
        Divisor that corresponds to the base of counting. All numbers in 'out'
        will be elements of the half-open interval [0,divisor).
    
    Returns
    -------
    out : ndarray, shape (steps, nblocks)
        Output array with the first dimension encoding the converted number and
        the second dimension encoding the digit.
    """
    
    # some checks on the input
    if start < 0:
        raise ValueError("'start' must be non-negative!")
    if steps < 1:
        raise ValueError("There must be at least one step!")
    if nblocks < 1:
        raise ValueError("There must be a least one block!")
    if divisor < 1:
        raise ValueError("Divisor must be at least one!")

    # counting array, choose unsigned integers to represent large numbers    
    cnt = np.arange(start, start+steps, 1, dtype=np.uint64)
    
    # allocate memory for output array
    out = np.zeros(shape=(steps, nblocks), dtype=int)
    
    # start counting
    for i in range(nblocks):
        cnt, out[:,-1-i] = np.divmod(cnt, divisor, dtype=np.uint64)
        
    return out



def get_wantedctp_idx(ctps, ctps_wanted):
    """
    Get indices of desired pathways.

    Parameters
    ----------
    ctps : (nPaths, nBlocks), 2D array
        Coherence transfer paths (CTPs).
    ctps_wanted : (nWanted, nBlocks), 2D array
        List of wanted CTPs. If any CTP is given in 'ctps_wanted' which
        is not present in the 'ctps', a warning is given.
    """
    
    # convert input to arrays
    ctps = np.atleast_2d(np.asarray(ctps))
    ctps_wanted = np.atleast_2d(np.asarray(ctps_wanted))
    
    # check shape of input
    if not ctps.ndim == 2:
        raise ValueError("'ctps' must be two dimensional!")
    if not ctps_wanted.ndim == 2:
        raise ValueError("'ctps_wanted' must be one dimensonal!")
    if not ctps.shape[1] == ctps_wanted.shape[1]:
        raise ValueError("Sizes of 'ctps' and 'ctps_wanted' do not match!")
    
    allidx = np.linspace(0, ctps.shape[0]-1, ctps.shape[0], dtype=np.int64)
    mask = np.any(np.all(ctps[None,:,:] == ctps_wanted[:,None,:], axis=2), axis=0)
    
    return allidx[mask]



def split_ctps_wanted(ctps, ctps_wanted):
    """
    Split a list of CTPs in wanted and unwated CTPs.py
    
    Parameters
    ----------
    ctps : (nPaths, nBlocks), 2D array
        Coherence transfer paths (CTPs).
    ctps_wanted : (nWanted, nBlocks), 2D array
        List of wanted CTPs. If any CTP is given in 'ctps_wanted' which
        is not present in the 'ctps', a warning is given.

    Returns
    -------
    wanted_ctps : (nWanted, nBlocks)
        Wanted CTPs.
    unwanted_ctps : (nUnwanted, nBlocks)
        Unwanted CTPs.
    """

    # convert input to arrays
    ctps = np.atleast_2d(np.asarray(ctps))
    ctps_wanted = np.atleast_2d(np.asarray(ctps_wanted))
    
    # check shape of input
    if not ctps.ndim == 2:
        raise ValueError("'ctps' must be two dimensional!")
    if not ctps_wanted.ndim == 2:
        raise ValueError("'ctps_wanted' must be two dimensonal!")
    if not ctps.shape[1] == ctps_wanted.shape[1]:
        raise ValueError("Sizes of 'ctps' and 'ctps_wanted' do not match!")

    # split in wanted and unwated CTPs
    wanted_idx = get_wantedctp_idx(ctps, ctps_wanted)

    if wanted_idx.size < ctps_wanted.shape[0]:
        warnings.warn("DAS IST EIN TEST")

    wanted_ctps = np.copy(ctps[wanted_idx,:])
    unwanted_ctps = np.delete(ctps, wanted_idx, axis=0)
    
    return wanted_ctps, unwanted_ctps


def prepare_ctps(ctps, ctps_wanted):
    """Prepare ctps.
    
    Wanted ctps are copied to the beginning of the array.
    
    This function is compiled with numba.
    
    Parameters
    ----------
    ctps : ()
        pass
    ctps_wanted : ()
        pass
    
    Returns
    -------
    ctps_out : 
        pass
    """
    
    ctps = np.atleast_2d(ctps)
    ctps_wanted = np.atleast_2d(ctps_wanted)
    
    if not ctps.ndim == ctps_wanted.ndim == 2:
        raise ValueError("`ctps` and `ctps_wanted` must both be one or two dimensional.")
    if not ctps.shape[1] == ctps_wanted.shape[1]:
        raise ValueError("`ctps` and `ctps_wanted` must have equal number of columns.")

    ctps_out = np.zeros_like(ctps)
    _prepare_ctps_numba(ctps, ctps_wanted, ctps_out)

    # code w/o numba
    # idx = np.argwhere(np.any(np.all(ctps[:,None,:] == ctps_wanted[None,:,:], axis=2), axis=1))[:,0]
    # if not idx.size == ctps_wanted.shape[0]:
    #     raise ValueError("lol")
    
    # ctps_out = np.concatenate((ctps[idx,:], np.delete(ctps, idx, axis=0)), axis=0)
    
    return ctps_out


@nb.njit()
def _prepare_ctps_numba(ctps, ctps_wanted, ctps_out):
    """Prepare ctps.
    
    Wanted ctps are copied to the beginning of the array.
    
    This function is compiled with numba.
    
    Parameters
    ----------
    ctps : ()
        pass
    ctps_wanted : ()
        pass
    ctps_out : ()
        pass
    
    Returns
    -------
    ctps_out : 
        pass
    """
    

    # check shape and size of input
    if not ctps.ndim == 2:
        raise ValueError("Error in `_prepare_ctps_numba`: `ctps` must be castable to 2D.")
    if not ctps_out.ndim == 2:
        raise ValueError("Error in `_prepare_ctps_numba`: `ctps_out` must be castable to 2D.")
    if not ctps_wanted.ndim == 2:
        raise ValueError("Error in `_prepare_ctps_numba`: `ctps_wanted` must be castable to 2D.")
        
    n_ctps   = ctps.shape[0]
    n_blocks = ctps.shape[1]
    n_wanted = ctps_wanted.shape[0]

    if not ctps_out.shape[0] == n_ctps:
        raise ValueError("Error in `_prepare_ctps_numba`: `ctps_out` and `ctps` have same number of rows.")
    if n_wanted > n_ctps:
        raise ValueError("Error in `_prepare_ctps_numba`: More CTPs in `ctps_wanted` than in `ctps`.")    
    if not ctps_wanted.shape[1] == n_blocks:
        raise ValueError("Error in `_prepare_ctps_numba`: `ctps` and `ctps_wanted` must have same number of columns.")
    if not ctps_out.shape[1] == n_blocks:
        raise ValueError("Error in `_prepare_ctps_numba`: `ctps` and `ctps_out` must have same number of columns.")

    # allocate array for where cetain ctps_wanted is in ctps
    indices_wanted = np.zeros(n_wanted, dtype=np.uint64)
    indices_wanted.fill(n_ctps)
    
    # loop over all wanted ctps
    for idx_wanted in range(n_wanted):
        # loop over all ctps and check, whether it equals the wanted ctp
        for idx_ctp in range(n_ctps):
            for k in range(n_blocks):
                if ctps[idx_ctp,k] != ctps_wanted[idx_wanted,k]:
                    break
            else:
                # check if not occured already, then copy index
                if indices_wanted[idx_wanted] == n_ctps:
                    indices_wanted[idx_wanted] = idx_ctp
                else:
                    raise ValueError("Error in `_prepare_ctps_numba`: Wanted CTP in "
                                     "`ctps_wanted` appears more than once in `ctps`.") 
        
        # check if this wanted ctp has been found anywhere
        if indices_wanted[idx_wanted] == n_ctps:
            raise ValueError("Error in `_prepare_ctps_numba`: Wanted CTP in "
                             "`ctps_wanted` does not appear in `ctps`.") 
    
    # check if all wanted ctps are unique by checking their indices
    for i in range(n_wanted):
        for j in range(i+1,n_wanted):
            if indices_wanted[i] == indices_wanted[j]:
                raise ValueError("Error in `_prepare_ctps_numba`: Not all wanted "
                                 "CTPs in `ctps_wanted` are unique.") 
    
    
    # copy the wanted ctps to front of output array
    for i in range(n_wanted):
        ctps_out[i,:] = ctps[indices_wanted[i],:]
    
    # sort indices of wanted ctps to make second copy step work
    indices_wanted.sort()
    
    # again loop over all ctps to copy to output array
    idx_out    = n_wanted
    idx_wanted = 0
    for i in range(n_ctps):
        
        # skip if current ctp is one of the wanted ones (already in output)
        if idx_wanted < n_wanted:
            if indices_wanted[idx_wanted] == i:
                idx_wanted += 1
                continue
        
        # copy to the current line
        ctps_out[idx_out,:] = ctps[i,:]
        idx_out += 1



#################################################################################
#                                                                               #
#   SSSS   III    GGGG  N   N   AAA   L              CCCC   AAA   L       CCCC  #
#  S        I    G      NN  N  A   A  L             C      A   A  L      C      #
#   SSS     I    G  GG  N N N  AAAAA  L             C      AAAAA  L      C      #
#      S    I    G   G  N  NN  A   A  L             C      A   A  L      C      #
#  SSSS    III    GGG   N   N  A   A  LLLLL          CCCC  A   A  LLLLL   CCCC  #
#                                                                               #
#################################################################################



def get_S0(ctps, ctps_wanted):
    """
    Construct the reference signal for desired CTPs from a list of CTPs.
    
    S0 is 1 for desired CTPs and 0 elsewise.    
    
    Parameters
    ----------
    ctps : array_like, shape (Nctps, Nblocks)
        Coherence transfer paths.
    ctps_wanted: array_like, shape (Nwanted, Nblocks)
        Desired coherence transfer paths.
    
    Returns
    -------
    S0 : array, shape (Nctp,)
        Array with 1 at wanted CTPs ans 0 elsewise.    
    """
    
    # cast to numpy arrays
    ctps = np.asarray(ctps)
    ctps_wanted = np.asarray(ctps_wanted)
    
    # check shape and dimensions
    if not ctps.ndim == 2:
        raise ValueError('ctps must be 2D!')
    if not ctps_wanted.ndim == 2:
        raise ValueError("ctps_wanted must be 2D!")
    if not ctps.shape[1] == ctps_wanted.shape[1]:
        raise ValueError('ctps and ctps_wanted must have identical shape in last dimension.')
    
    # allocate space
    S0 = np.zeros(ctps.shape[0])
    for idx, ctp_wanted in enumerate(ctps_wanted):
        areequal = (ctps==ctp_wanted).all(axis=1)
        S0[areequal] = 1
        
    return S0



def calculate_signal_rec(phases, rec, dctps):
    """
    Calculate complex signal of coherence transfer paths for given pulse and 
    receiver phases.
    
    Parameters
    ----------
    phases : array_like, shape (Nscans, Nblocks-1)
        Phases for each pulse block an scan.
    rec : array_like, shape (Nscans,)
        Receiver phase for each scan.
    dctps : array_like, shape (Nctps, Nblocks-1)
        Differences in coherence order for each coherence transfer pathway and
        pulse block
    
    Returns
    -------
    signal : array, shape (Nctps,)
        Signal vector averaged over all scans.
    """
    
    return np.exp(-1.0j*( np.matmul(dctps, phases.T) + rec[None,:] )).mean(axis=1)



def calculate_signal_dctps(phases, dctp_ref, dctps):
    """   
    Calculate complex signal of coherence transfer paths for given pulse phases
    and a reference coherence transfer path.
    
    Parameters
    ----------
    phases : array_like, shape (Nscans, Nblocks-1)
        Phases for each pulse block an scan.
    dctp_ref : array_like, shape (Nblocks-1,)
        Reference coherence transfer path.
    dctps : array_like, shape (Nctps, Nblocks-1)
        Differences in coherence order for each coherence transfer pathway and
        pulse block.
    
    Returns
    -------
    signal : array, shape (Nctps,)
        Signal vector averaged over all scans.    
    """
    
    return np.exp(-1.0j*( np.matmul(dctps-dctp_ref[None, :], phases.T))).mean(axis=1)



def calculate_signal_dctps0(phases, dctps0):
    """   
    Calculate complex signal of coherence transfer paths for given pulse phases
    and a reference coherence transfer path.
    
    Parameters
    ----------
    phases : array_like, shape (Nscans, Nblocks-1)
        Phases for each pulse block an scan.
    dctps0 : array_like, shape (Nctps, Nblocks-1)
        Differences in coherence order for each coherence transfer pathway and
        pulse block minus the differences in coherence order for the reference
        path whose phase is held constant by the receiver.
    
    Returns
    -------
    signal : array, shape (Nctps,)
        Signal vector averaged over all scans.    
    """
    
    return np.exp(-1.0j*( np.matmul(dctps0, phases.T))).mean(axis=1)





###################################################################
#                                                                 #
#   CCCC  Y   Y   CCCC  L      EEEEE          GGGG  EEEEE  N   N  #
#  C       Y Y   C      L      E             G      E      NN  N  #
#  C        Y    C      L      EEE           G  GG  EEE    N N N  #
#  C        Y    C      L      E             G   G  E      N  NN  #
#   CCCC    Y     CCCC  LLLLL  EEEEE          GGG   EEEEE  N   N  #
#                                                                 #
###################################################################

def generate_phasecycle_lists(cycles, reccycle):
    """Get phase cycle table from individual phase cycles.
    
    Parameters
    ----------
    cycles : list of list
    reccycle : list

    Returns
    -------
    phases : 2D array
        List of phases for each block. First dimension
        encodes the phases for each scan, second dimenson
        encodes the phase for each block
    receiver : 1D array
        receiver phase to select the given CTP.    
    """

    # check if all cycles have correct shape
    cycles_conv = []
    for cycle in cycles:
        cycle = np.array(cycle, dtype=np.float64)
        if not cycle.ndim == 1:
            raise ValueError("Each phase cycle in the cycle list must be a 1D array or list!")
        cycles_conv.append(cycle)
    cycles = cycles_conv

    # check if receiver has correct format
    reccycle = np.array(reccycle, dtype=np.float64)
    if not reccycle.ndim == 1: 
        raise ValueError("Receiver phase cycle must be a 1D list or array!")

    # number of pulse blocks
    n_blocks = len(cycles)

    # get length of all individual phase cycles and receiver phase
    lengths = [c.shape[0] for c in cycles]
    lengths.append(reccycle.shape[0])

    # get lowest common multiple of all phase cycle lengths
    n_scans = 1
    for length in lengths:
        n_scans = np.lcm(n_scans, length)

    # construct data arrays
    phases = np.zeros(shape=(n_scans, n_blocks), dtype=np.float64)
    for idx, cycle in enumerate(cycles):
        phases[:, idx] = np.tile(cycle, n_scans//lengths[idx])

    receiver = np.tile(reccycle, n_scans//reccycle.shape[0])

    # sanity check if receiver an pulse blocks need same number of scans
    if not receiver.shape[0] == phases.shape[0]:
        raise ValueError("Receiver and pulse blocks do not use the same number of scans and you can do nothing to correct it!")


    return phases, receiver



def generate_phcycle_nested(nblocks, steplengths, pulses, pathway, unit='rad'):
    """
    Generate a nested phase cycle for a pulse sequence with n blocks.
    
    Paramters
    ---------
    nblocks : int
        Number of pulse blocks in the pulse sequence.
    steplengths : list of size 'nblocks'
        Number of steps for the particular step's phase cycle. For 4, the
        corresponding phase cycle would go through 0°, 90°, 180° and 270°.
    pulses : lists of 'nblocks' lists or None
        Indices of pulses that are cycles in a certain step. Start counting
        from 0! If None, each block is cycled one after another.
    pathway : array_like, shape (nblock,)
        Coherence order changes for the desired pathway.
    unit : str, optional
        Unit for the phases. Either 'rad' und 'deg' for radient or degree.
        Defaults to 'rad'.
    
    Returns
    -------
    phases : ndarray, shape (nscans, nblocks)
        List of phases for each block. First dimension
        encodes the phases for each scan, second dimenson
        encodes the phase for each block
    receiver : array, shape (nscans,)
        receiver phase to select the given CTP.
    """
    
    steplengths = np.asarray(steplengths)
    pathway = np.asarray(pathway)
    
    if pathway.size != nblocks:
        raise ValueError("Number of steps in the desired pathway must be identical to number of blocks!")
    
    # total necessary number of scans
    nscans = np.prod(steplengths)
    
    # cumulative products of step lenghts
    cumprod = np.concatenate(([1], np.cumprod(steplengths)))
    cumprod_inv = np.concatenate(([1], np.cumprod(steplengths[::-1])))

    # do some sanity checks
    
    # allocate space
    phases = np.zeros(shape=(nscans, nblocks))
    
    for idx, nstep in enumerate(steplengths):
        
        ph_increment = np.repeat(np.linspace(0.0, 2.0*np.pi, nstep, endpoint=False), cumprod[idx])
        ph_increment = np.tile(ph_increment, cumprod_inv[-2-idx])
        phases[:,pulses[idx]] += ph_increment[:,None]
    
    phases = np.mod(phases, 2.0*np.pi)
    
    # compute receiver phase
    receiver = np.mod(-np.sum(phases*pathway[None,:], axis=1), 2.0*np.pi)
        
    
    # convert to desired unit
    if unit in ['rad', 'radiant']:
        pass
    elif unit in ['deg', 'degree', '°']:
        phases *= 180.0/np.pi
        receiver *= 180.0/np.pi
    else:
        raise ValueError("Unkown phase unit '{}', choose 'degree' or 'radiant'.".format(unit))
    
    
    return phases, receiver



# def generate_phasecycle_nested(lengths, delta_ps):
#     """Generate phases of nested phase cycle.
    
#     Parameters
#     ----------
#     lengths : list
#         Length of the phase cycles for each block.
#     delta_ps : list
#         One of the desired coherence changes for each
#         block. Needed to construct receiver phase.
            
#     Returns
#     -------
#     phases : 2D array
#         List of phases for each block. First dimension
#         encodes the phases for each scan, second dimenson
#         encodes the phase for each block
#     receiver : 1D array
#         receiver phase to select the given CTP.    
#     """
    
#     lengths = np.array(lengths)
#     delta_ps = np.array(delta_ps)
#     total_length = np.prod(lengths)
#     if lengths.size!=delta_ps.size:
#         raise ValueError("Number of phase cycling blocks does not equal number of coherence changes.")
#     steps = lengths.size
    
#     phases = np.zeros(shape=(total_length, steps))
    
#     for idx,length in enumerate(lengths):
        
#         before = np.prod(lengths[:-(steps-idx)])
#         after = np.prod(lengths[idx+1:])
#         k = np.linspace(0,length-1,int(length))
#         phases[:,idx] = 2.0*np.pi/length * np.tile(np.repeat(k, after), before)
    
#     receiver = np.mod(-(phases*delta_ps[None,:]).sum(axis=1), 2.0*np.pi)
    
#     return phases, receiver



def generate_phasecycle_cogwheel(Ns, windings, winding_rec, unit='rad'):
    """Generate phases of a cogwheel phase cycle.
    
    Parameters
    ----------
    Ns : int
        Number of scans for the cogwheel phase cycle.
    windings : list
        List of winding numbers for each pule block.
    winding_rec : int
        Winding number of receiver.
    
    Returns
    -------
    phases : 2D array
        List of phases for each block. First dimension encodes the phases for 
        each scan, second dimenson encodes the phase for each block
    receiver : 1D array
        Receiver phase to select the given CTP.    
    """
    
    windings = np.array(windings)
    steps = np.linspace(0,Ns-1,Ns)
    
    phases = np.mod(2.0*np.pi/Ns * steps[:,None]*windings[None,:], 2.0*np.pi)
    receiver = np.mod(2.0*np.pi*winding_rec*steps/Ns, 2.0*np.pi)

    # convert to desired unit
    if unit in ['rad', 'radiant']:
        pass
    elif unit in ['deg', 'degree', '°']:
        phases *= 180.0/np.pi
        receiver *= 180.0/np.pi
    else:
        raise ValueError("Unkown phase unit '{}', choose 'degree' or 'radiant'.".format(unit))
    
    return phases, receiver





