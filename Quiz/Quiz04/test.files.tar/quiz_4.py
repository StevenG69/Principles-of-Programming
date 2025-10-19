# Written by Hongyin Zhou for COMP9021
#
# Call "trinumber" any integer that is the product of
# 3 prime numbers, for instance:
# - 8, equal to 2 x 2 x 2
# - 363, equal to 3 x 11 x 11
# - 455, equal to 5 x 7 x 13
# - 231, equal to 3 x 7 x 11
# - 782, equal to 2 x 17 x 23
#
# Given a trinumber n, call "gap in its decomposition"
# the minimum of
# - the difference between second and first primes
#   in n's decomposition, and
# - the difference between third and second primes
#   in n's decomposition
# (ordering the 3 primes from smallest to largest).
# For instance,
# - the gap in the decomposition of 8 is 0 (2 - 2)
# - the gap in the decomposition of 363 is 0 (11 - 11)
# - the gap in the decomposition of 455 is 2 (7 - 5)
# - the gap in the decomposition of 231 is 4 (7 - 3 or 11 - 7)
# - the gap in the decomposition of 782 is 6 (23 - 17)
#
# Implements a function tri_numbers(n) that outputs:
# - the number of trinumbers at most equal to n included;
# - the largest trinumber at most equal to n included;
# - the maximum gap in the decomposition of trinumbers
#   at most equal to n included;
# - ordered from smallest to largest, the numbers having
#   that maximum gap in their decompositions,
#   together with their decompositions.
#
# You can assume that n is an integer at least equal to 8.
# In the tests, its value won't exceed 50_000_000.

from math import sqrt

# Sieve of Eratosthenes to find all primes up to n
def sieve_of_primes_up_to(n):
    sieve = [True] * (n + 1)
    sieve[0], sieve[1] = False, False  # 0 and 1 are not primes
    for p in range(2, int(sqrt(n)) + 1):
        if sieve[p]:
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]

# Function to calculate trinumbers and analyze gaps
def tri_numbers(n):
    primes = sieve_of_primes_up_to(n // 2)  # primes up to n/2
    count = 0
    max_tri_number = 0
    max_tri_number_prime_list = []
    max_gap = 0
    max_gap_prime_list = []

    # Iterate through prime triplets
    for i in range(len(primes)):
        for j in range(i, len(primes)):
            if primes[i] * primes[j] > n:
                break  # Exit if the product exceeds n
            for k in range(j, len(primes)):
                tri_num = primes[i] * primes[j] * primes[k]
                if tri_num > n:
                    break  # Exit if the trinumber exceeds n
                count += 1
                # Check for maximum trinumber
                if tri_num > max_tri_number:
                    max_tri_number = tri_num
                    max_tri_number_prime_list = [primes[i], primes[j], primes[k]]
                # Check for maximum gap in the prime triplet
                gap = min(primes[j] - primes[i], primes[k] - primes[j])
                if gap > max_gap:
                    max_gap = gap
                    max_gap_prime_list = [(tri_num, primes[i], primes[j], primes[k])]
                elif gap == max_gap:
                    max_gap_prime_list.append((tri_num, primes[i], primes[j], primes[k]))

    # Output the results
    print(f"There {"is" if count == 1 else "are"} {count} {"trinumber" if count == 1 else "trinumbers"} at most equal to {n}.")
    print(f"The largest one is {max_tri_number}, equal to {max_tri_number_prime_list[0]} x {max_tri_number_prime_list[1]} x {max_tri_number_prime_list[2]}.")
    print(f"\nThe maximum gap in decompositions is {max_gap}.")
    print("It is achieved with:")
    for tri_num, p1, p2, p3 in sorted(max_gap_prime_list):
        print(f"  {tri_num} = {p1} x {p2} x {p3}")

