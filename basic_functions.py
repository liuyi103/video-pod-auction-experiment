# -*- coding: utf-8 -*-
"""
Created on Sun Aug 09 00:04:38 2015

@author: lyc
"""

import numpy as np
import copy
import pulp as pp

class Ad:
    def __init__(self, is_power2 = False):
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
    prob += sum([ad['bid'] * x[i] for i, ad in enumerate(ads)])
    prob += sum([ad['duration'] * x[i] for i, ad in enumerate(ads)])\
            <= max_duration
    prob.solve()
    ans = []
    for i,ad in enumerate(ads):
        if pp.value(x[i]) == 1:
            ans.append(ad)
    return ans
    
def total_price(ads):
    # if numbers == 'all':
    #     return sum([ad['price'] for ad in ads])
    ans = 0
    for ad in ads:
        ans += ad['price']
    return ans

def get_coutour(ads, max_duration, is_losers = True):
    '''
    get the contour for the given ads, if the ads are losers, then, we want to get the ipper coutour, if winners, lower
    :param ads: winners of losers, the prices are always used.
    :param max_duration:
    :param is_losers: whether he ads are losers
    :return: a list of (corresponding_ads, total_price)
    '''
    super_ad = None # a blank place-taker
    if not is_losers:
        total_duration = sum([ad.duration for ad in ads])
        gap = max_duration -total_duration
        if gap > 0:
            super_ad = Ad(0)
            super_ad.duration = gap
            super_ad.bid = 0
            super_ad.price = 0
            ads.append(super_ad)
    ans = [[[], 0] for i in range(max_duration + 1)]
    for ad in ads:
        for duration in range(max_duration, 0, -1):
            if ad['duration'] > duration:
                break
            tmp = ans[duration - ad['duration']][1] + ad.price
            if is_losers and (tmp > ans[duration][1]):
                ans[duration][1] = tmp
                ans[duration][0] = copy.copy(ans[duration - ad['duration']][0]) + [ad]
            if not is_losers and (duration == ad.duration or ans[duration - ad['duration']][1] > 0) and\
                    (tmp < ans[duration][1] or len(ans[duration][0]) == 0):
                ans[duration][1] = tmp
                ans[duration][0] = copy.copy(ans[duration - ad['duration']][0]) + [ad]
    if not is_losers:
        for i in range(1 + max_duration):
            if super_ad in ans[i][0]:
                ans[i][0].remove(super_ad)
    return ans

def get_solution(winners, constraints):
    '''
    Get the optimal set of winners
    :param winners: The set of winners
    :param constraints: a list of constraints, for each constraint is a list of winners and a minimal value
    :return: nothing, but the winners is updated.
    '''
    prob = pp.LpProblem('get solution', pp.LpMinimize)
    p = pp.LpVariable.dict('p', [id(i) for i in winners], 0)
    prob += pp.lpSum(p)
    for ads in constraints:
        min_value = constraints[ads]
        prob += pp.lpSum([p[id(i)] for i in ads]) >= min_value
    prob.solve()
    for winner in winners:
        winner.price = pp.value(p[id(winner)])

