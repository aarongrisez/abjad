from abjad import *


def test_mathtools_arithmetic_mean_01( ):
   '''Return an exact integer or rational.'''
   
   assert mathtools.arithmetic_mean([1, 2, 3, 4, 5]) == 3
   assert mathtools.arithmetic_mean([10, 10, 10]) == 10
   assert mathtools.arithmetic_mean([1, 1, 2, 3, 10]) == Fraction(17, 5)
   assert mathtools.arithmetic_mean([0, 1, 10]) == Fraction(11, 3)


def test_mathtools_arithmetic_mean_02( ):
   '''Return float.'''

   assert mathtools.arithmetic_mean([1.0, 2.0, 3.0, 4.0, 5.0]) == 3.0
   assert mathtools.arithmetic_mean([10, 10, 10.0]) == 10.0
