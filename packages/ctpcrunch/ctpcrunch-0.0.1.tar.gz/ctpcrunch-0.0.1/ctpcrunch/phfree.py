import numpy as np
import numba

############################################################################################
#                                                                                          #
#    GGGG  RRRR    AAA   DDDD    III   EEEEE  N   N  TTTTT          OOO   PPPP   TTTTT     #
#   G      R   R  A   A  D   D    I    E      NN  N    T           O   O  P   P    T       #
#   G  GG  RRRR   AAAAA  D   D    I    EEE    N N N    T           O   O  PPPP     T       #
#   G   G  R  R   A   A  D   D    I    E      N  NN    T           O   O  P        T       #
#    GGG   R   R  A   A  DDDD    III   EEEEE  N   N    T            OOO   P        T       #
#                                                                                          #
############################################################################################

def cost_delta2(S, S0):
    """Cost function for given signal and refernce Signal.
    
    Absolute possible minimum is 0.
    """
    
    return np.mean(np.square(np.abs(S-S0)))




def phfree_cost(phases, dctps0, S0):
    """Cost function for given signal and refernce Signal.
    
    Absolute possible minimum is 0.
    """
    
    Np, Nb = dctps0.shape[0], dctps0.shape[1]
    Ns = int(phases.size/Nb)
    
    exponent = np.matmul(dctps0, phases.reshape(Ns,Nb).T)
    S = np.exp(-1j*exponent).mean(axis=1)
    
    return np.mean(np.square(np.abs(S-S0)))



def phfree_jac(phases, dctps0, S0):
    """Das ist richtig!..."""
    
    Np, Nb = dctps0.shape[0], dctps0.shape[1]
    Ns = int(phases.size/Nb)
    
    exponent = np.exp(-1j*np.matmul(dctps0, phases.reshape(Ns,Nb).T)) # has shape (Np, Ns)
    dSstar = np.conj((exponent.mean(axis=1)-S0))                      # has shape (Np,)
    
    # g has (Ns, Nb)
    g = 2.0/(Np*Ns) * np.matmul( np.imag( exponent*dSstar[:,None]).T, dctps0 )
    
    return g.flatten()


def phfree_jacnum(phases, dctps0, S0, dph=1e-5):
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
    
    phases = np.copy(phases)
    jac = np.zeros(phases.shape)
    
    for i in range(jac.shape[0]):
        for j in range(jac.shape[1]):
            phases[i,j] += dph
            cost_p = phfree_cost(phases, dctps0, S0)
            phases[i,j] -= 2.0*dph
            cost_m = phfree_cost(phases, dctps0, S0)
            phases[i,j] += dph
            jac[i,j] = 0.5*(cost_p-cost_m)/dph
    
    return jac


def phfree_costjac(phases, dctps0, S0):
    """Das ist richtig!..."""
    
    # phases has shape (Ns, Nb)
    # dctps0 has shape (Np, Nb)
    
    Np, Nb = dctps0.shape[0], dctps0.shape[1]
    Ns = int(phases.size/Nb)
    
    exponent = np.matmul(dctps0, phases.reshape(Ns,Nb).T) # has shape (Np, Ns)
    dS = np.exp(-1j*exponent).mean(axis=1) - S0           # has shape (Np,)
    
    # g has (Ns, Nb)
    g = 2.0/(Np*Ns) * np.matmul( np.imag(np.exp(-1j*exponent)*np.conj(dS)[:,None]).T, dctps0 )
    
    return np.mean(np.square(np.abs(dS))), g.flatten()



def phfree_hessiannum(phases, dctps0, S0, dph=1e-6):
    
    Np, Nb = dctps0.shape[0], dctps0.shape[1]
    Ns = int(phases.size/Nb)
    
    phases = np.copy(phases).flatten()
    hessian = np.zeros(shape=(phases.size, phases.size))
    
    for i in range(phases.size):
        # diagonal element
        cost_0 = phfree_cost(phases, dctps0, S0)
        phases[i] += dph
        cost_p = phfree_cost(phases, dctps0, S0)
        phases[i] -= 2.0*dph
        cost_m = phfree_cost(phases, dctps0, S0)
        
        hessian[i,i] = (cost_p-2.0*cost_0+cost_m)/dph**2
        
        for j in range(i+1,phases.size):
            # off diagonal elements
            phases[j] -= dph
            cost_mm = phfree_cost(phases, dctps0, S0)
            phases[j] += 2.0*dph
            cost_mp = phfree_cost(phases, dctps0, S0)
            phases[i] += 2.0*dph
            cost_pp = phfree_cost(phases, dctps0, S0)
            phases[j] -= 2.0*dph
            cost_pm = phfree_cost(phases, dctps0, S0)
            
            hessian[i,j] = hessian[j,i] = 0.25*(cost_pp-cost_pm-cost_mp+cost_mm)/dph**2
            phases[i] -= dph
            phases[j] += dph
    
    return hessian











# numba compiled functions for various

@numba.njit(parallel=False)
def phfree_cost_numba(phases, dctps0, S0):
    """Cost function for given signal and refernce Signal.
    
    Absolute possible minimum is 0.
    """
    
    # get the dimension of all arrays
    Np, Nb = dctps0.shape[0], dctps0.shape[1]
    Ns = int(phases.size//Nb)
    
    S0real = S0.real
    S0imag = S0.imag
    
    # reshape phases so it can be used with 1D or 2D array as input
    phases = phases.reshape((Ns,Nb))
    
    # compute signal and cost
    cost = 0.0
    for i in numba.prange(Np):
        S_real = 0.0
        S_imag = 0.0
        for j in range(Ns):
            
            phshift = 0.0
            for k in range(Nb):
                phshift += phases[j,k] * dctps0[i,k]
            
            S_real += np.cos(phshift)
            S_imag -= np.sin(phshift)
        
        dS_real = S_real/Ns - S0real[i]
        dS_imag = S_imag/Ns - S0imag[i]
        cost += np.square(dS_real) + np.square(dS_imag) 
        
    return cost/Np



@numba.njit(parallel=False)
def phfree_jac_numba(phases, dctps0, S0):
    
    # get the dimension of all arrays
    Np, Nb = dctps0.shape[0], dctps0.shape[1]
    Ns = int(phases.size//Nb)
    # reshape phases so it can be used with 1D or 2D array as input
    phases = phases.reshape((Ns,Nb))
    
    S0real = S0.real
    S0imag = S0.imag
    
    # compute jac
    jac = np.zeros(phases.shape)
    cos = np.zeros((Np, Ns))
    sin = np.zeros((Np, Ns))
    for i in numba.prange(Np):
        S_real = 0.0
        S_imag = 0.0
        for j in range(Ns):
            
            phshift = 0.0
            for k in range(Nb):
                phshift += phases[j,k] * dctps0[i,k]      
            
            cos[i,j] += np.cos(phshift)
            sin[i,j] += np.sin(phshift)
            S_real += cos[i,j]
            S_imag -= sin[i,j]
            
        dS_real = S_real/Ns - S0real[i]
        dS_imag = S_imag/Ns - S0imag[i]
        
        # compute elements of jacobian
        for j in range(Ns):
            helper = -(cos[i,j]*dS_imag + sin[i,j]*dS_real)
            for k in range(Nb):
                jac[j,k] += helper*dctps0[i,k]
    
    return 2.0/(Np*Ns)*jac.flatten()



@numba.njit(parallel=False)
def phfree_costjac_numba(phases, dctps0, S0):
    
    # get the dimension of all arrays
    Np, Nb = dctps0.shape[0], dctps0.shape[1]
    Ns = int(phases.size//Nb)
    # reshape phases so it can be used with 1D or 2D array as input
    phases = phases.reshape((Ns,Nb))
    
    S0real = S0.real
    S0imag = S0.imag
        
    # compute cost and jac
    cost = 0.0
    jac = np.zeros(phases.shape)
    cos = np.zeros((Np, Ns))
    sin = np.zeros((Np, Ns))
    for i in numba.prange(Np):
        S_real = 0.0
        S_imag = 0.0
        for j in range(Ns):
            
            phshift = 0.0
            for k in range(Nb):
                phshift += phases[j,k] * dctps0[i,k]      
            
            cos[i,j] += np.cos(phshift)
            sin[i,j] += np.sin(phshift)
            S_real += cos[i,j]
            S_imag -= sin[i,j]
            
        dS_real = S_real/Ns - S0real[i]
        dS_imag = S_imag/Ns - S0imag[i]
        cost += np.square(dS_real) + np.square(dS_imag) 
        
        # compute elements of jacobian
        for j in range(Ns):
            helper = -(cos[i,j]*dS_imag + sin[i,j]*dS_real)
            for k in range(Nb):
                jac[j,k] += helper*dctps0[i,k]
    
    return cost/Np, 2.0/(Np*Ns)*jac.flatten()



@numba.njit(parallel=False)
def phfree_hess_numba(phases, dctps0, S0):
    
    # get the dimension of all arrays
    Np, Nb = dctps0.shape[0], dctps0.shape[1]
    Ns = int(phases.size/Nb)
    
    # reshape phases so it can be used with 1D or 2D array as input
    phases = phases.reshape((Ns,Nb))
    
    # pre-computation signal and exponent
    cos = np.zeros((Np, Ns))
    sin = np.zeros((Np, Ns))
    dS_real = np.zeros(Np)
    dS_imag = np.zeros(Np)
    for i in numba.prange(Np):
        S_real = 0.0
        S_imag = 0.0
        for j in range(Ns):
            
            exponent = 0.0
            for k in range(Nb):
                exponent += phases[j,k] * dctps0[i,k]      
            
            cos[i,j] = np.cos(exponent)
            sin[i,j] = np.sin(exponent)
            S_real += cos[i,j]
            S_imag -= sin[i,j]
        
        dS_real[i] = S_real/Ns - S0[i].real
        dS_imag[i] = S_imag/Ns - S0[i].imag
    
    # allocate space
    hessian = np.zeros((Ns*Nb, Ns*Nb))
    
    # outer loop over all j blocks
    for j1 in numba.prange(Ns):
        
        # diagonal block j1 = j2
        for k1 in range(Nb):
            
            # the diagonal element
            element = 0.0
            for i in range(Np):
                element +=  dctps0[i,k1]*dctps0[i,k1] * \
                    ( 1.0 + Ns*(sin[i,j1]*dS_imag[i]-cos[i,j1]*dS_real[i]) )
            element *= 2.0/(Np*Ns**2)
            hessian[j1*Nb+k1,j1*Nb+k1] = element
            
            # all the other elements
            for k2 in range(k1+1,Nb):
                
                element = 0.0
                for i in range(Np):
                    element += dctps0[i,k1]*dctps0[i,k2] * \
                        ( 1.0 + Ns*(sin[i,j1]*dS_imag[i]-cos[i,j1]*dS_real[i]) )
                element *= 2.0/(Np*Ns**2)
                hessian[j1*Nb+k1,j1*Nb+k2] = element
                hessian[j1*Nb+k2,j1*Nb+k1] = element
                
        
        # the other blocks j1 != j2
        for j2 in range(j1+1,Ns):
            for k1 in range(Nb):
                
                # the diagonal element
                element = 0.0
                for i in range(Np):
                    element +=  dctps0[i,k1]*dctps0[i,k1] * \
                        (cos[i,j1]*cos[i,j2] + sin[i,j1]*sin[i,j2])
                element *= 2.0/(Np*Ns**2)
                hessian[j1*Nb+k1,j2*Nb+k1] = element
                hessian[j2*Nb+k1,j1*Nb+k1] = element
                
                # all the other elements
                for k2 in range(k1+1,Nb):
                    
                    element = 0.0
                    for i in range(Np):
                        element += dctps0[i,k1]*dctps0[i,k2] * \
                            (cos[i,j1]*cos[i,j2] + sin[i,j1]*sin[i,j2])
                    element *= 2.0/(Np*Ns**2)
                    hessian[j1*Nb+k1,j2*Nb+k2] = element
                    hessian[j1*Nb+k2,j2*Nb+k1] = element
                    hessian[j2*Nb+k1,j1*Nb+k2] = element
                    hessian[j2*Nb+k2,j1*Nb+k1] = element                    
    
    return hessian



@numba.njit(parallel=False)
def phfree_hessp_numba(phases, p, dctps0, S0):
    
    # get the dimension of all arrays
    Np, Nb = dctps0.shape[0], dctps0.shape[1]
    Ns = int(phases.size/Nb)
    # reshape phases so it can be used with 1D or 2D array as input
    phases = phases.reshape((Ns,Nb))
    p = p.reshape((Ns,Nb))  
        
    # pre-compute
    cos = np.zeros((Np, Ns))
    sin = np.zeros((Np, Ns))
    dS_real = np.zeros(Np)
    dS_imag = np.zeros(Np)
    dctps0_p = np.zeros((Np,Ns))
    for i in numba.prange(Np):
        S_real = 0.0
        S_imag = 0.0
        for j in range(Ns):
            
            exponent = 0.0
            for k in range(Nb):
                exponent += phases[j,k] * dctps0[i,k]
                dctps0_p[i,j] += dctps0[i,k] * p[j,k]
            
            cos[i,j] += np.cos(exponent)
            sin[i,j] += np.sin(exponent)
            S_real += cos[i,j]
            S_imag -= sin[i,j]
            
        dS_real[i] = S_real/Ns - S0[i].real
        dS_imag[i] = S_imag/Ns - S0[i].imag
    
    # compute Hessian*p
    hessp = np.zeros(phases.shape)
    for j in numba.prange(Ns):
        for k in range(Nb):
            
            for i in range(Np):
                sum_cos = 0.0
                sum_sin = 0.0
                for J in range(Ns):
                    sum_cos += dctps0_p[i,J] * cos[i,J]
                    sum_sin += dctps0_p[i,J] * sin[i,J]

                sum_cos -= Ns * dctps0_p[i,j] * dS_real[i]
                sum_sin += Ns * dctps0_p[i,j] * dS_imag[i]
                hessp[j,k] += dctps0[i,k] * (cos[i,j]*sum_cos + sin[i,j]*sum_sin)
    
    return 2.0/(Np*Ns**2) * hessp.flatten()









@numba.njit(parallel=False)
def phfreerec_cost_numba(phases, dctps, S0):
    """Cost function for given signal and refernce Signal.
    
    Absolute possible minimum is 0.
    """
    
    # get the dimension of all arrays
    Np, Nb = dctps.shape[0], dctps.shape[1]
    Ns = int(phases.size//(Nb+1))
    
    # reshape phases so it can be used with 1D or 2D array as input
    phases = phases.reshape((Ns,Nb+1))
    
    S0real = S0.real
    S0imag = S0.imag
    
    # compute signal and cost
    cost = 0.0
    for i in numba.prange(Np):
        S_real = 0.0
        S_imag = 0.0
        for j in range(Ns):
            
            phshift = phases[j,Nb]
            for k in range(Nb):
                phshift += phases[j,k] * dctps[i,k]
            
            S_real += np.cos(phshift)
            S_imag -= np.sin(phshift)
        
        dS_real = S_real/Ns - S0real[i]
        dS_imag = S_imag/Ns - S0imag[i]
        cost += np.square(dS_real) + np.square(dS_imag) 
        
    return cost/Np



@numba.njit(parallel=False)
def phfreerec_jac_numba(phases, dctps, S0):
    
    # get the dimension of all arrays
    Np, Nb = dctps.shape[0], dctps.shape[1]
    Ns = int(phases.size//(Nb+1))
    # reshape phases so it can be used with 1D or 2D array as input
    phases = phases.reshape((Ns,Nb+1))
    
    S0real = S0.real
    S0imag = S0.imag
    
    # compute jac
    jac = np.zeros(phases.shape)
    cos = np.zeros((Np, Ns))
    sin = np.zeros((Np, Ns))
    for i in numba.prange(Np):
        S_real = 0.0
        S_imag = 0.0
        for j in range(Ns):
            
            phshift = phases[j,Nb]
            for k in range(Nb):
                phshift += phases[j,k] * dctps[i,k]      
            
            cos[i,j] += np.cos(phshift)
            sin[i,j] += np.sin(phshift)
            S_real += cos[i,j]
            S_imag -= sin[i,j]
            
        dS_real = S_real/Ns - S0real[i]
        dS_imag = S_imag/Ns - S0imag[i]
        
        # compute elements of jacobian
        for j in range(Ns):
            helper = -(cos[i,j]*dS_imag + sin[i,j]*dS_real)
            jac[j,Nb] += helper
            for k in range(Nb):
                jac[j,k] += helper*dctps[i,k]
    
    return 2.0/(Np*Ns)*jac.flatten()



@numba.njit(parallel=False)
def phfreerec_costjac_numba(phases, dctps, S0):
    
    # get the dimension of all arrays
    Np, Nb = dctps.shape[0], dctps.shape[1]
    Ns = int(phases.size//(Nb+1))
    # reshape phases so it can be used with 1D or 2D array as input
    phases = phases.reshape((Ns,Nb+1))
    
    S0real = S0.real
    S0imag = S0.imag
        
    # compute cost and jac
    cost = 0.0
    jac = np.zeros(phases.shape)
    cos = np.zeros((Np, Ns))
    sin = np.zeros((Np, Ns))
    for i in numba.prange(Np):
        S_real = 0.0
        S_imag = 0.0
        for j in range(Ns):
            
            phshift = phases[j,Nb]
            for k in range(Nb):
                phshift += phases[j,k] * dctps[i,k]      
            
            cos[i,j] += np.cos(phshift)
            sin[i,j] += np.sin(phshift)
            S_real += cos[i,j]
            S_imag -= sin[i,j]
            
        dS_real = S_real/Ns - S0real[i]
        dS_imag = S_imag/Ns - S0imag[i]
        cost += np.square(dS_real) + np.square(dS_imag) 
        
        # compute elements of jacobian
        for j in range(Ns):
            helper = -(cos[i,j]*dS_imag + sin[i,j]*dS_real)
            jac[j,Nb] += helper
            for k in range(Nb):
                jac[j,k] += helper*dctps[i,k]
    
    return cost/Np, 2.0/(Np*Ns)*jac.flatten()








@numba.njit(parallel=False)
def phfreew_cost_numba(phases, dctps0, S0, weights):
    """Cost function for given signal and refernce Signal.
    
    Absolute possible minimum is 0.
    """
    
    # get the dimension of all arrays
    Np, Nb = dctps0.shape[0], dctps0.shape[1]
    Ns = int(phases.size//Nb)
    
    S0real = S0.real
    S0imag = S0.imag
    
    # reshape phases so it can be used with 1D or 2D array as input
    phases = phases.reshape((Ns,Nb))
    
    # compute signal and cost
    cost = 0.0
    for i in numba.prange(Np):
        S_real = 0.0
        S_imag = 0.0
        for j in range(Ns):
            
            phshift = 0.0
            for k in range(Nb):
                phshift += phases[j,k] * dctps0[i,k]
            
            S_real += np.cos(phshift)
            S_imag -= np.sin(phshift)
        
        dS_real = S_real/Ns - S0real[i]
        dS_imag = S_imag/Ns - S0imag[i]
        cost += weights[i]*(np.square(dS_real) + np.square(dS_imag) )
        
    return cost/Np



@numba.njit(parallel=False)
def phfreew_jac_numba(phases, dctps0, S0, weights):
    
    # get the dimension of all arrays
    Np, Nb = dctps0.shape[0], dctps0.shape[1]
    Ns = int(phases.size//Nb)
    # reshape phases so it can be used with 1D or 2D array as input
    phases = phases.reshape((Ns,Nb))
    
    S0real = S0.real
    S0imag = S0.imag
    
    # compute jac
    jac = np.zeros(phases.shape)
    cos = np.zeros((Np, Ns))
    sin = np.zeros((Np, Ns))
    for i in numba.prange(Np):
        S_real = 0.0
        S_imag = 0.0
        for j in range(Ns):
            
            phshift = 0.0
            for k in range(Nb):
                phshift += phases[j,k] * dctps0[i,k]      
            
            cos[i,j] += np.cos(phshift)
            sin[i,j] += np.sin(phshift)
            S_real += cos[i,j]
            S_imag -= sin[i,j]
            
        dS_real = S_real/Ns - S0real[i]
        dS_imag = S_imag/Ns - S0imag[i]
        
        # compute elements of jacobian
        for j in range(Ns):
            helper = -weights[i]*(cos[i,j]*dS_imag + sin[i,j]*dS_real)
            for k in range(Nb):
                jac[j,k] += helper*dctps0[i,k]
    
    return 2.0/(Np*Ns)*jac.flatten()



@numba.njit(parallel=False)
def phfreew_costjac_numba(phases, dctps0, S0, weights):
    
    # get the dimension of all arrays
    Np, Nb = dctps0.shape[0], dctps0.shape[1]
    Ns = int(phases.size//Nb)
    # reshape phases so it can be used with 1D or 2D array as input
    phases = phases.reshape((Ns,Nb))
    
    S0real = S0.real
    S0imag = S0.imag
        
    # compute cost and jac
    cost = 0.0
    jac = np.zeros(phases.shape)
    cos = np.zeros((Np, Ns))
    sin = np.zeros((Np, Ns))
    for i in numba.prange(Np):
        S_real = 0.0
        S_imag = 0.0
        for j in range(Ns):
            
            phshift = 0.0
            for k in range(Nb):
                phshift += phases[j,k] * dctps0[i,k]      
            
            cos[i,j] += np.cos(phshift)
            sin[i,j] += np.sin(phshift)
            S_real += cos[i,j]
            S_imag -= sin[i,j]
            
        dS_real = S_real/Ns - S0real[i]
        dS_imag = S_imag/Ns - S0imag[i]
        cost += weights[i]*(np.square(dS_real) + np.square(dS_imag))
        
        # compute elements of jacobian
        for j in range(Ns):
            helper = -weights[i]*(cos[i,j]*dS_imag + sin[i,j]*dS_real)
            for k in range(Nb):
                jac[j,k] += helper*dctps0[i,k]
    
    return cost/Np, 2.0/(Np*Ns)*jac.flatten()










@numba.njit(parallel=False)
def phfreewrec_cost_numba(phases, dctps, S0, weights):
    """Cost function for given signal and refernce Signal.
    
    Absolute possible minimum is 0.
    """
    
    # get the dimension of all arrays
    Np, Nb = dctps.shape[0], dctps.shape[1]
    Ns = int(phases.size//(Nb+1))
    
    # reshape phases so it can be used with 1D or 2D array as input
    phases = phases.reshape((Ns,Nb+1))
    
    S0real = S0.real
    S0imag = S0.imag
    
    # compute signal and cost
    cost = 0.0
    for i in numba.prange(Np):
        S_real = 0.0
        S_imag = 0.0
        for j in range(Ns):
            
            phshift = phases[j,Nb]
            for k in range(Nb):
                phshift += phases[j,k] * dctps[i,k]
            
            S_real += np.cos(phshift)
            S_imag -= np.sin(phshift)
        
        dS_real = S_real/Ns - S0real[i]
        dS_imag = S_imag/Ns - S0imag[i]
        cost += weights[i]*(np.square(dS_real) + np.square(dS_imag))
        
    return cost/Np



@numba.njit(parallel=False)
def phfreewrec_jac_numba(phases, dctps, S0, weights):
    
    # get the dimension of all arrays
    Np, Nb = dctps.shape[0], dctps.shape[1]
    Ns = int(phases.size//(Nb+1))
    # reshape phases so it can be used with 1D or 2D array as input
    phases = phases.reshape((Ns,Nb+1))
    
    S0real = S0.real
    S0imag = S0.imag
    
    # compute jac
    jac = np.zeros(phases.shape)
    cos = np.zeros((Np, Ns))
    sin = np.zeros((Np, Ns))
    for i in numba.prange(Np):
        S_real = 0.0
        S_imag = 0.0
        for j in range(Ns):
            
            phshift = phases[j,Nb]
            for k in range(Nb):
                phshift += phases[j,k] * dctps[i,k]      
            
            cos[i,j] += np.cos(phshift)
            sin[i,j] += np.sin(phshift)
            S_real += cos[i,j]
            S_imag -= sin[i,j]
            
        dS_real = S_real/Ns - S0real[i]
        dS_imag = S_imag/Ns - S0imag[i]
        
        # compute elements of jacobian
        for j in range(Ns):
            helper = -weights[i]*(cos[i,j]*dS_imag + sin[i,j]*dS_real)
            jac[j,Nb] += helper
            for k in range(Nb):
                jac[j,k] += helper*dctps[i,k]
    
    return 2.0/(Np*Ns)*jac.flatten()


@numba.njit(parallel=False)
def phfreewrec_costjac_numba(phases, dctps, S0, weights):
    
    # get the dimension of all arrays
    Np, Nb = dctps.shape[0], dctps.shape[1]
    Ns = int(phases.size//(Nb+1))
    # reshape phases so it can be used with 1D or 2D array as input
    phases = phases.reshape((Ns,Nb+1))
    
    S0real = S0.real
    S0imag = S0.imag
        
    # compute cost and jac
    cost = 0.0
    jac = np.zeros(phases.shape)
    cos = np.zeros((Np, Ns))
    sin = np.zeros((Np, Ns))
    for i in numba.prange(Np):
        S_real = 0.0
        S_imag = 0.0
        for j in range(Ns):
            
            phshift = phases[j,Nb]
            for k in range(Nb):
                phshift += phases[j,k] * dctps[i,k]      
            
            cos[i,j] += np.cos(phshift)
            sin[i,j] += np.sin(phshift)
            S_real += cos[i,j]
            S_imag -= sin[i,j]
            
        dS_real = S_real/Ns - S0real[i]
        dS_imag = S_imag/Ns - S0imag[i]
        cost += weights[i]*(np.square(dS_real) + np.square(dS_imag))
        
        # compute elements of jacobian
        for j in range(Ns):
            helper = -weights[i]*(cos[i,j]*dS_imag + sin[i,j]*dS_real)
            jac[j,Nb] += helper
            for k in range(Nb):
                jac[j,k] += helper*dctps[i,k]
    
    return cost/Np, 2.0/(Np*Ns)*jac.flatten()



# @numba.njit(parallel=False)
# def phfree_cost_numba(phases, dctps0, S0):
#     """Cost function for given signal and refernce Signal.
    
#     Absolute possible minimum is 0.
#     """
    
#     # get the dimension of all arrays
#     Np, Nb = dctps0.shape[0], dctps0.shape[1]
#     Ns = int(phases.size/Nb)
    
#     # reshape phases so it can be used with 1D or 2D array as input
#     phases = phases.reshape((Ns,Nb))
    
#     # compute signal and cost
#     cost = 0.0
#     for i in numba.prange(Np):
#         S_real = 0.0
#         S_imag = 0.0
#         for j in range(Ns):
            
#             exponent = 0.0
#             for k in range(Nb):
#                 exponent += phases[j,k] * dctps0[i,k]
            
#             S_real += np.cos(exponent)
#             S_imag -= np.sin(exponent)
        
#         dS_real = S_real/Ns - S0[i].real
#         dS_imag = S_imag/Ns - S0[i].imag
#         cost += np.square(dS_real) + np.square(dS_imag) 
        
#     return cost/Np


# @numba.njit(parallel=False)
# def phfree_jac_numba(phases, dctps0, S0):
    
#     # get the dimension of all arrays
#     Np, Nb = dctps0.shape[0], dctps0.shape[1]
#     Ns = int(phases.size/Nb)
#     # reshape phases so it can be used with 1D or 2D array as input
#     phases = phases.reshape((Ns,Nb))  
    
#     # compute jac
#     jac = np.zeros(phases.shape)
#     cos = np.zeros((Np, Ns))
#     sin = np.zeros((Np, Ns))
#     for i in numba.prange(Np):
#         S_real = 0.0
#         S_imag = 0.0
#         for j in range(Ns):
            
#             exponent = 0.0
#             for k in range(Nb):
#                 exponent += phases[j,k] * dctps0[i,k]      
            
#             cos[i,j] += np.cos(exponent)
#             sin[i,j] += np.sin(exponent)
#             S_real += cos[i,j]
#             S_imag -= sin[i,j]
            
#         dS_real = S_real/Ns - S0[i].real
#         dS_imag = S_imag/Ns - S0[i].imag
        
#         # compute elements of jacobian
#         for j in range(Ns):
#             for k in range(Nb):
#                 jac[j,k] -= (cos[i,j]*dS_imag + sin[i,j]*dS_real)*dctps0[i,k]
    
#     return 2.0/(Np*Ns)*jac.flatten()


# @numba.njit(parallel=False)
# def phfree_costjac_numba(phases, dctps0, S0):
    
#     # get the dimension of all arrays
#     Np, Nb = dctps0.shape[0], dctps0.shape[1]
#     Ns = int(phases.size/Nb)
#     # reshape phases so it can be used with 1D or 2D array as input
#     phases = phases.reshape((Ns,Nb))  
        
#     # compute cost and jac
#     cost = 0.0
#     jac = np.zeros(phases.shape)
#     cos = np.zeros((Np, Ns))
#     sin = np.zeros((Np, Ns))
#     for i in numba.prange(Np):
#         S_real = 0.0
#         S_imag = 0.0
#         for j in range(Ns):
            
#             exponent = 0.0
#             for k in range(Nb):
#                 exponent += phases[j,k] * dctps0[i,k]      
            
#             cos[i,j] += np.cos(exponent)
#             sin[i,j] += np.sin(exponent)
#             S_real += cos[i,j]
#             S_imag -= sin[i,j]
            
#         dS_real = S_real/Ns - S0[i].real
#         dS_imag = S_imag/Ns - S0[i].imag
#         cost += np.square(dS_real) + np.square(dS_imag) 
        
#         # compute elements of jacobian
#         for j in range(Ns):
#             for k in range(Nb):
#                 jac[j,k] -= (cos[i,j]*dS_imag + sin[i,j]*dS_real)*dctps0[i,k]
    
#     return cost/Np, 2.0/(Np*Ns)*jac.flatten()
