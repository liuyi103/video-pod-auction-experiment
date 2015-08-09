"""
Created on Sat Aug 08 22:31:09 2015

@author: lyc
"""

from basic_functions import *

if __name__ == '__main__':
    max_duration = 45
    ads = data_sampler(100)
    winner_numbers = select_winners(ads, max_duration)
    print total_price(ads, winner_numbers)