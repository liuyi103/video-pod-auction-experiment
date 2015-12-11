from unittest import TestCase
from basic_functions import *

__author__ = 'xutin'


class TestGet_coutour(TestCase):
    def test_get_coutour(self):
        max_duration = 6
        ad1 ,ad2, ad3 = Ad(), Ad(), Ad()
        ad1.duration = 1
        ad1.price = 1
        ad2.duration = 2
        ad2.price = 2
        ad3.duration = 2
        ad3.price = 3
        ads = [ad1, ad2, ad3]

        ans1 = get_coutour(ads, max_duration, False)
        ans2 = get_coutour(ads, max_duration, True)

        print ans1
        print ans2