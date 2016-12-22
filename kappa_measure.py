# -*- coding: utf-8 -*-
"""
Compute kappa measure, given the list of agreement from both the judges
"""

from __future__ import division
def computeKappa(): 
    print('Use the following template of input: 1, 0, 0 and press enter when done.')
    relevancy1 = [int(x) for x in raw_input('User1, please give the list of your relevancy judgement: ').split(',')]
    relevancy2 = [int(x) for x in raw_input('User2, please give the list of your relevancy judgement: ').split(',')]
    agreement = [1 if relevancy1[x] == relevancy2[x] else 0 for x in range(len(relevancy1))]
    pa = float(sum(agreement)/len(relevancy1))
    pr = (relevancy1.count(1) + relevancy2.count(1))/(len(relevancy1)*2)
    pn = (relevancy1.count(0) + relevancy2.count(0))/(len(relevancy1)*2)
    pe = (pr*pr) + (pn*pn)
    kappa = (pa - pe)/(1 - pe)
    print kappa
    return kappa
    
computeKappa()