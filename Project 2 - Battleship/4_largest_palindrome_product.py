'''
A palindromic number reads the same both ways. 
The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.
'''
import logging
logging.basicConfig(filename='4_largest_palindrome_product.log',level=logging.DEBUG)
# logging.debug('')
# logging.info('So should this')


# make all 3-digit numbers
three_digit_numbers = [range(1000, 100000)]
logging.info("\n".join(three_digit_numbers))
# make all 3 - digit numbers products


# arrange for largest number first
# check for palindromes