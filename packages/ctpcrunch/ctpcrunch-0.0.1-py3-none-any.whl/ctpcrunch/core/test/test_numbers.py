import numpy as np
import unittest
from ctpcrunch.core import numbers

class TestIsPrime(unittest.TestCase):
    
    def test__is_prime_numba(self):
        
        primes_below100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        
        primes_u4 = [i for i in range(0,100) if numbers._is_prime_numba(np.uint32(i))]
        primes_u8 = [i for i in range(0,100) if numbers._is_prime_numba(np.uint64(i))]
        primes_i4 = [i for i in range(0,100) if numbers._is_prime_numba(np.int32(i))]
        primes_i8 = [i for i in range(0,100) if numbers._is_prime_numba(np.int64(i))]
        
        self.assertEqual(primes_below100, primes_u4)
        self.assertEqual(primes_below100, primes_u8)
        self.assertEqual(primes_below100, primes_i4)
        self.assertEqual(primes_below100, primes_i8)
        
        del primes_below100, primes_u4, primes_u8, primes_i4, primes_i8
        

if __name__ == '__main__':
    unittest.main()
    
    
    





