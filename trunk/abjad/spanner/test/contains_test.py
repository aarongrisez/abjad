from abjad import *


def test_contains_01( ):
   '''
   Spanner containment tests components.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[1])

   r'''
   \new Voice {
      {
         c'8
         d'8
      }
      {
         e'8 [
         f'8 ]
      }
      {
         g'8
         a'8
      }
   }
   '''

   assert t[1] in p
   assert t[1][0] not in p
   assert t[1][1] not in p


def test_contains_02( ):
   '''
   Spanner containment tests components.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[ : ])

   r'''
   \new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }
   '''

   assert all([x in p for x in (t[0], t[1], t[2])])
   assert not any([x in p for x in t.leaves])
