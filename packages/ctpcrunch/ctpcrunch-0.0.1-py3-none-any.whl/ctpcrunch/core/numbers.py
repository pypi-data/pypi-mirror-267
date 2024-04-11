# small script to find phase cycles
import math
import numpy as np
import numba as nb


from .array import _row_in_array_numba



@nb.njit(['b1(u4)', 'b1(u8)', 'b1(i4)', 'b1(i8)'],
         cache=True)
def _is_prime_numba(n):
    """Primality test using 6k+-1 optimization.
    
    Parameters
    ----------
    n : int
        Number to check for primality.
    
    Returns
    -------
    is_prime : bool
        Wether the number is prime or not. False is also returned if
        a number smaller than 2 was given.
    """
    
    # get dtype of input
    DTYPE = type(n)
    
    # check for smaller cases
    if n <= DTYPE(3):
        return n > DTYPE(1)
    if n%DTYPE(2) == DTYPE(0) or n%DTYPE(3) == DTYPE(0):
        return False
    
    # check all possible divisors of form 6*i +- 1
    i = DTYPE(5)
    stop = DTYPE(np.floor(np.sqrt(n)))
    while i <= stop:
        if n%i == DTYPE(0) or n%(i + DTYPE(2)) == DTYPE(0):
            return False
        i += DTYPE(6)
    
    # if no divisor is found, number must be prime 
    return True





@nb.njit(['i8[:,:](i8, i8)'], cache=True)
def _generate_all_factorizations_numba(n, max_n_factors):
    """
    Calculate prime factorization of a number with a given list of primes.
    """
    
    # number of elements to pre-allocate to avoid appending and copying
    n_alloc = 64
    
    # find the prime factorization of n
    
    # allocate some space for prime factors
    prime_factorization = np.ones(n_alloc, dtype=np.int64)
    
    # count the number of prime factors
    n_prime_factors = 0
    n_work = n
    
    # devide out all factors of 2
    while(n_work % 2 == 0):
        if n_prime_factors >= n_alloc:
            prime_factorization = np.append(prime_factorization, 2)
        else:
            prime_factorization[n_prime_factors] = 2
        n_work = n_work//2
        n_prime_factors += 1
        
    # devide out all factors of 3
    while(n_work % 3 == 0):
        if n_prime_factors >= n_alloc:
            prime_factorization = np.append(prime_factorization, 3)
        else:
            prime_factorization[n_prime_factors] = 3
        n_work = n_work//3
        n_prime_factors += 1
    
    # only check the factors up to sqrt(n_work), 2 and 3 are no factors of n
    stop = np.int64(np.floor(np.sqrt(n_work)))
    
    # # loop over remaining possible factors of form 6k+-1, that might be prime
    # # the smallest next valid factor is always prime, so only real primes are found
    i = 5
    while(i <= stop):
        
        # if n_work = 1, all factors are found
        if n_work == 1:
            break
        
        # check divisibility by possible prime 6k-1
        while(n_work % i == 0):
            if n_prime_factors >= n_alloc:
                pass
                #prime_factorization = np.append(prime_factorization, DTYPE(i))
            else:
                prime_factorization[n_prime_factors] = i
            n_work = n_work // i
            n_prime_factors += 1
        
        # check divisibility by possible prime 6k+1
        while(n_work % (i+2) == 0):
            if n_prime_factors >= n_alloc:
                prime_factorization = np.append(prime_factorization, i+2)
            else:
                prime_factorization[n_prime_factors] = i+2
            n_work = n_work // (i+2)
            n_prime_factors += 1
        
        # go to next pair of possible primes 6(k+1)+-1
        i += 6
    
    # there should be no factors left now, if n_work ist not one, it was prime
    if not n_work == 1:
        if n_prime_factors >= n_alloc:
            prime_factorization = np.append(prime_factorization, n_work)
        else:
            prime_factorization[n_prime_factors] = n_work
        n_prime_factors += 1
        
    # crop array to number of prime factors
    prime_factorization = prime_factorization[:n_prime_factors]
    
    
    # now generate all factorizations from prime factorization
    
    # handle smaller cases separately
    if n_prime_factors == 1:
        factorizations = np.array([[prime_factorization[0]]], dtype=np.int64)
        cropping_indices = np.array([0], dtype=np.int64)
    
    elif n_prime_factors == 2:
        fac1 = prime_factorization.min()
        fac2 = prime_factorization.max()
        factorizations = np.array([[fac1,fac2],[fac1*fac2,1]], dtype=np.int64)
        cropping_indices = np.array([0,1], dtype=np.int64)
    
    # handle the general case with 3 or more prime factors, allocate some space first
    else:
        factorizations = np.ones((n_alloc, n_prime_factors), dtype=np.int64)
        # total number of factorizations found
        n_factorizations = 0
        # stores the borders of the layers
        cropping_indices = np.zeros(n_prime_factors, dtype=np.int64)
        
        # initialize first row with all prime factors
        if n_factorizations >= n_alloc:
            factorizations = np.append(factorizations, prime_factorization.reshape(1,n_prime_factors), axis=0)
        else:
            factorizations[0,:] = prime_factorization[:]
        n_factorizations += 1
        cropping_indices[0] = 0
        
        # allocate space for working array
        working = np.zeros(n_prime_factors, dtype=prime_factorization.dtype)
        
        # indices to mark first and last row of the currently to be reduced array
        idx_red_start = 0
        idx_red_end = 0
        
        for idx_layer in range(n_prime_factors-2):
            # number of relevant factors in this layer
            n_facs_layer = n_prime_factors - idx_layer
            # number of new smaller factorizations found for this layer
            n_new_factorizations = 0
            
            cropping_indices[idx_layer+1] = n_factorizations
            
            # loop over all rows to reduce in current layer
            for idx_red in range(idx_red_start, idx_red_end+1):
                
                fac_i = 0
                for i in range(n_facs_layer):
                    # only try this factor, if it differs from previous
                    if factorizations[idx_red,i] == fac_i:
                        continue
                    fac_i = factorizations[idx_red,i]
                    
                    fac_j = 0
                    for j in range(i+1, n_facs_layer):
                        # only try this factor, if it differs from previous
                        if factorizations[idx_red,j] == fac_j:
                            continue
                        fac_j = factorizations[idx_red,j]
                        
                        # build new factorization
                        working[:] = factorizations[idx_red,:]
                        working[i], working[j] = fac_i*fac_j, n+1
                        
                        # sort the new factorization
                        working[:n_facs_layer] = np.sort(working[:n_facs_layer])
                        working[n_facs_layer-1] = 1
                        
                        # check if this factorization is new
                        if not _row_in_array_numba(working[:n_facs_layer-1], factorizations[idx_red_end+1:idx_red_end+1+n_new_factorizations,:n_facs_layer-1]):
                            # append this factorization to all factorizations
                            if n_factorizations >= n_alloc:
                                factorizations = np.append(factorizations, working.reshape(1,n_prime_factors), axis=0)
                            else:
                                factorizations[n_factorizations] = working[:]
                            n_factorizations += 1
                            n_new_factorizations += 1
                            
            # done with this reduction layer, update indices for next iteration
            idx_red_start = idx_red_end+1
            idx_red_end = idx_red_end+n_new_factorizations
                
        
        cropping_indices[-1] = n_factorizations
        
        # the last layer, reduction to one factor that is just n
        final_factor = factorizations[n_factorizations-1,0] * factorizations[n_factorizations-1,1]
        if n_factorizations >= n_alloc:
            working[:] = 1
            working[0] = final_factor
            factorizations = np.append(factorizations, working.reshape(1,n_prime_factors), axis=0)
        else:
            factorizations[n_factorizations,0] = final_factor
        n_factorizations += 1
        
        # sanity check, if final factor is original number
        if not factorizations[n_factorizations-1,0] == n:
            raise ValueError('Final factor does not match initial number.')
        
        # crop array to number of factorizations
        factorizations = factorizations[:n_factorizations,:]
    
    # crop to max_n_factors
    if max_n_factors > 0:
        max_n_factors = min(n_prime_factors, max_n_factors)
        cropping_idx = cropping_indices[n_prime_factors-max_n_factors]
        factorizations = np.ascontiguousarray(factorizations[cropping_idx:,:max_n_factors])
    
    return factorizations











@nb.njit(['u4(u4, u4)', 'u8(u8, u8)', 'i4(i4, i4)', 'i8(i8, i8)'],
         cache=True)
def _binomcoeff_numba(n, k):
    """Calculate binomial coefficient (n, k) = n!/(k!*/(n-k)!), which is
    the number to choose k from n distinguishable elements without repetition.
    
    This function is jitted with Numba and accepts signed and unsigned integer
    types. Overflow is detected and in that case 0 is returned.
    
    Parameters
    ----------
    n : int
        Number of elements to choose from.
    k : int
        Number of elements to choose with 0 <= k <= n.
        
    Returns
    -------
    result : int
        Binomial coefficient or 0 if an error occured like overflow.
    """
    
    # find dtype of input and maximum representable value
    INT_MAX = np.iinfo(n).max
    DTYPE = type(n)
    
    # handle forbidden cases
    if n < k or n < DTYPE(0) or k < DTYPE(0): return 0
    # use symmetry to minimize number of necessary multiplications
    if n-k < k: k = n-k
    # handle easy cases
    if k == DTYPE(0): return 1
    if k == DTYPE(1): return n
    
    # variable to store the result in (casting to correct dtype)
    result = DTYPE(1)
    
    # variable is initialized and casted to avoid casting errors in gcd
    d = DTYPE(0)
    for _ in range(k):
        d += DTYPE(1)
        
        # result might overflow
        if result >= INT_MAX//n:
            
            g = np.gcd(n, d); nr = n//g; dr = d//g
            g = np.gcd(result, dr); result = result//g; dr = dr//g
            
            # result will overflow
            if result >= INT_MAX//nr:
                return 0
            else:
                result *= nr
                result //= dr
                n -= DTYPE(1)
        
        # result will not overflow, just multiply first
        else:
            result *= n
            result //= d
            n -= DTYPE(1)
    
    return result





@nb.njit(['u4(u4, u4[:])', 'u8(u8, u8[:])', 'i4(i4, i4[:])', 'i8(i8, i8[:])'],
         cache=True)
def _multinomcoeff_numba(n, ks):
    """Calculate multinomial coefficient
        (n, k1, k2, ..., km) = n!/(k1! * k2! * ... * km!)
    
    This function computes the number of ways to put n objects in m bins, where
    the first bin holds k1 objects, the second k2 and so on. The value is
    computed by a product of binomial coefficients using
    
        n!/(k1! * k2! * ... * km!) = (k1, k1) * (k1+k2, k2) * ... * (n, km)
    
    This function is jitted with Numba.
    
    Parameters
    ----------
    n : int
        Total number of elements to choose from.
    ks : array of ints
        Sizes of groups of indistuingishable elements. 
        Their sum must equal `n`.
        
    Returns
    -------
    result : int
        The multinomial coefficient or 0 if some error occured (`n` or any
        element of `ks` ^negative or overflow error).
    """
    
    # find dtype of input and maximum representable value
    INT_MAX = np.iinfo(n).max
    DTYPE = type(n)
    
    # check if input is not negative and sum(ks) == n
    if n < DTYPE(0): return 0
    summed = DTYPE(0)
    for k in ks:
        if k < DTYPE(0): return 0
        summed += k
    if summed != n: return 0
    
    result = DTYPE(1)
    for k in ks:
        f = _binomcoeff_numba(n, k)
        if result >= INT_MAX//f: return 0
        result *= f
        n -= k
        
    return result





@nb.njit()
def _log2_binomcoeff_numba(n, k):
    """
    Calculate log2 of the binomial coefficient (n, k) = n!/(k!*(n-k)!).

    Parameters
    ----------
    n : int
        Number of elements to choose from.
    k : int
        Number of elements to choose with 0 <= k <= n.

    result : int
        Log base 2 of binomial coefficient.
    """
    
    # 1 / ln(2)
    invlog2 = 1.442695040888963407359924681001892137426646
    
    if k < 0 or k > n:
        raise ValueError("It should be 0 <= k <= n.")
        
    res = math.lgamma(n+1) - ( math.lgamma(k+1) + math.lgamma(n-k+1) )
    
    return res * invlog2





@nb.njit(['u4(u4[:])', 'u8(u8[:])', 'i4(i4[:])', 'i8(i8[:])'],
         cache=True)
def _smallest_common_divisor_numba(a):
    """
    Find the smallest common divisor greater than one of an array of integers.
    Or return 0 if all numbers are 0 or 1 if numbers are coprime.

    The sign of all integers is ignored. All zeros are ignored as zero is
    considerd to be divisible by everything. Some sample outputs:

        [0, 0, 0, 0] --> 0
        [2,-4, 8, 0] --> 2
        [2, 4, 6,-3] --> 1
        [1, 0,-1, 0] --> 1

    This functions works by first finding the smallest absolute value in
    `a` greater than one. If no value greater (absolute value) than one
    (or zero) exist then one (or zero) is returned. If all elements in
    `a` share a common factor it must be a prime factor of this smallest
    value. Divisibility is then checked for all those possible prime factors.
    
    Parameters
    ----------
    a : array of int
        Integers to find the smallest common divisor greater than one of.

    Returns
    -------
    val : int
        Smallest common divisor greater than one shared by all integers in a
        (always positive) or one if all integers are coprime or zero if all
        integers in a are zero.
    """
    
    if not a.ndim == 1:
        raise ValueError("`windings` must be a 1D array.")
    
    n = a.size
    
    # get minimum absolute value greater than zero
    val_min = 0
    for i in range(n):
        if not val_min == 0:
            if not abs(a[i]) == 0 and abs(a[i]) < val_min:
                val_min = abs(a[i])
        elif abs(a[i]) > val_min:
            val_min = abs(a[i])
    # if no element is bigger than one, just return val_min (0 or 1)
    if val_min < 2:
        return val_min
    
    # check divisibility by 2
    if val_min%2 == 0:
        val_min = val_min//2
        # iterate over array elements greater than 0, see if all are divisible
        for i in range(n):
            if not a[i]%2 == 0: break
        else:
            # if so, this is the smallest common divisor
            return 2
        # divide out this factor
        while val_min%2 == 0:
            val_min = val_min//2
    
    # check divisibility by 3
    if val_min%3 == 0:
        val_min = val_min//3
        # iterate over array elements greater than 0, see if all are divisible
        for i in range(n):
            if not a[i]%3 == 0: break
        else:
            # if so, this is the smallest common divisor
            return 3
        # divide out this factor
        while val_min%3 == 0:
            val_min = val_min//3
    
    # check divisibility by all other prime factors (6k+-1 filter)
    div = 5
    while val_min > 1:
        
        # check divisibility by 6k-1
        if val_min%div == 0:
            val_min = val_min//div
            # iterate over array elements greater than 0, see if all are divisible
            for i in range(n):
                if not a[i]%div == 0: break
            else:
                # if so, this is the smallest common divisor
                return div
            # divide out this factor
            while val_min%div == 0:
                val_min = val_min//div
        
        # check divisibility by 6k+1
        if val_min%(div+2) == 0:
            val_min = val_min//(div+2)
            # iterate over array elements greater than 0, see if all are divisible
            for i in range(n):
                if not a[i]%(div+2) == 0: break
            else:
                # if so, this is the smallest common divisor
                return div+2
            # divide out this factor
            while val_min%(div+2) == 0:
                val_min = val_min//(div+2)
        
        div += 6
    
    # if no common factor was found, elements in `a` are coprime
    return 1





@nb.njit(['u4(u4,u4[:])', 'u8(u8,u8[:])', 'i4(i4,i4[:])', 'i8(i8,i8[:])'],
         cache=True)
def _smallest_common_divisor_addval_numba(a0, a):
    """
    Utility function.
    
    Parameters
    ----------
    a0 : int
        Additional value to consider together with `a`.
    a : array of int
        Integers to find the smallest common divisor greater than one of 
        together with `a0`.

    Returns
    -------
    val : int
        Smallest common divisor greater than one shared by all integers in a
        (always positive) or one if all integers are coprime or zero if all
        integers in a are zero.
    """
    
    if not a.ndim == 1:
        raise ValueError("`windings` must be a 1D array.")
    
    n = a.size
    
    # get minimum absolute value greater than zero
    val_min = 0
    for i in range(n):
        if not val_min == 0:
            if not abs(a[i]) == 0 and abs(a[i]) < val_min:
                val_min = abs(a[i])
        elif abs(a[i]) > val_min:
            val_min = abs(a[i])
                
    # if no winding is bigger than one, just return val_min
    if val_min < 2:
        return val_min
    # check if val can make val_min smaller
    if not abs(a0) == 0 and abs(a0) < val_min:
        val_min = abs(a0)
    
    # divisibility by 2
    if val_min%2 == 0:
        val_min = val_min//2
        # iterate over array elements greater than 0, see if all are divisible
        if a0%2 == 0:
            for i in range(n):
                if not a[i]%2 == 0: break
            else:
                return 2
        # divide out this factor
        while val_min%2 == 0:
            val_min = val_min//2
    
    # divisibility by 3
    if val_min%3 == 0:
        val_min = val_min//3
        # iterate over array elements greater than 0, see if all are divisible
        if a0%3 == 0:
            for i in range(n):
                if not a[i]%3 == 0: break
            else:
                return 3
        # divide out this factor
        while val_min%3 == 0:
            val_min = val_min//3
    
    # divisibility by all other prime factors (6k+-1 filter)
    div = 5
    while val_min > 1:
        
        if val_min%div == 0:
            val_min = val_min//div
            # iterate over array elements greater than 0, see if all are divisible
            if a0%div == 0:
                for i in range(n):
                    if not a[i]%div == 0: break
                else:
                    return div
            # divide out this factor
            while val_min%div == 0:
                val_min = val_min//div
            
        if val_min%(div+2) == 0:
            val_min = val_min//(div+2)
            # iterate over array elements greater than 0, see if all are divisible
            if a0%(div+2) == 0:
                for i in range(n):
                    if not a[i]%(div+2) == 0: break
                else:
                    return div+2
            # divide out this factor
            while val_min%(div+2) == 0:
                val_min = val_min//(div+2)
        
        div += 6
    
    return 1



