# -*- coding: utf-8 -*-
"""
Created on Sun Aug 09 00:04:38 2015

@author: lyc
"""

import numpy as np

class Ad:
    def __init__(self, is_power2):
        if not is_power2:
            self.duration = np.random.randint(low = 10, high = 30)
        else:
            self.duration = 2 ** np.random.randint(low = 1, high = 8)
        self.bid = (np.random.random() + 1) * self.duration
        self.price = self.bid
    def __getitem__(self, key):
        exec 'ans = self.' + key
        return ans
    def __setitem__(self, key, item):
        exec 'self.' + key + ' = ' + str(item)
    def get(self, key, default):
        try:
            exec 'return self.' + key
        except:
            return default

def data_sampler(n_ad, is_power2 = False):
    '''Returns a list of n_ad ads.'''
    return [Ad(is_power2) for i in range(n_ad)]

def select_winners(ads, max_duration):
    '''Computes the set of winners that has the maximum total price.
    The numbers of winners are returned.'''
    import pulp as pp
    prob = pp.LpProblem('select winners', pp.LpMaximize)
    x = pp.LpVariable.dict('x', range(len(ads)), 0, 1.5, pp.LpInteger)
    prob += sum([ad['price'] * x[i] for i, ad in enumerate(ads)])
    prob += sum([ad['duration'] * x[i] for i, ad in enumerate(ads)])\
            <= max_duration
    prob.solve()
    ans = []
    for i,ad in enumerate(ads):
        if pp.value(x[i]) == 1:
            ans.append(i)
    return ans
    
def total_price(ads, numbers = 'all'):
    if numbers == 'all':
        return sum([ad['price'] for ad in ads])
    ans = 0
    for i in numbers:
        ans += ads[i]['price']
    return ans