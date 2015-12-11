"""
Created on Sat Aug 08 22:31:09 2015

@author: lyc
"""

from basic_functions import *

if __name__ == '__main__':
    max_duration = 200
    ads = data_sampler(100)
    winners = set(select_winners(ads, max_duration))
    losers = set(ads) - winners
    bar = [i[1] for i in get_coutour(losers, max_duration, True)]
    
    ## Using pulp
    constraints = {}
    for winner in winners:
        constraints[(winner,)] = bar[winner['duration']]
    
    while True:
        get_solution(winners, constraints)
        lower_coutour = get_coutour(winners, max_duration, False)
        finish = True
        for k, tmp in enumerate(lower_coutour):
            ads, min_value = tmp
            if len(ads) == 0:
                continue
            if min_value < bar[k] - 1e-5:
                constraints[tuple(ads)] = bar[k]
                finish = False
        if finish:
            break
    print sum([winner.price for winner in winners])
    
    # using cplex directly
    from cplex import Cplex
    winners = list(winners)
    id2num = {id(winner):k for k, winner in enumerate(winners)}
    prob = Cplex()
    lb = [bar[winner.duration] for winner in winners]
    ub = [winner.bid for winner in winners]
    prob.objective.set_sense(prob.objective.sense.minimize)
    obj = [1] * len(winners)
    prob.variables.add(obj, lb, ub)
    while True:
        prob.solve()
        prices = prob.solution.get_values()
        for i in range(len(winners)):
            winners[i].price = prices[i]
        lower_coutour = get_coutour(winners, max_duration, False)
        finish = True
        for k, tmp in enumerate(lower_coutour):
            ads, min_value = tmp
            if len(ads) == 0:
                continue
            if min_value < bar[k] - 1e-5:
                prob.linear_constraints.add([[[id2num[id(ad)] for ad in ads],[1] * len(ads)]],\
                ['G'], [bar[k]])
                finish = False
        if finish:
            break
    print sum(prob.solution.get_values())
    
    
    