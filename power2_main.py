# -*- coding: utf-8 -*-
"""
Created on Sun Aug 09 00:09:12 2015

@author: lyc
"""

from basic_functions import *

if __name__ == '__main__':
    max_duration = 45
    ads = data_sampler(100, True)
    winner_numbers = select_winners(ads, max_duration)
    print total_price(ads, winner_numbers)