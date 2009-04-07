from abjad.clef.clef import Clef
from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
import types


class _ClefInterface(_Interface, _GrobHandler):
   '''Handle LilyPond Clef grob.
      Interface to find effective clef.
      Interface to force clef changes.'''
   
   def __init__(self, client):
      '''Bind client and LilyPond Clef grob.
         Set forced to None.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Clef')
      self._forced = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def change(self):
      '''True if clef changes here, otherwise False.'''
      return bool(hasattr(self.client, 'prev') and \
         self.client.prev.clef.name != self.name)

   @property
   def effective(self):
      '''Return effective clef or else treble.'''
      cur = self.client
      while cur is not None:
         #if cur.clef._forced:
         #   return cur.clef._forced
         if cur.clef.forced:
            return cur.clef.forced
         else:
            cur = getattr(cur, 'prev', None)
      for x in self.client.parentage.parentage[1:]:
         #if hasattr(x, 'clef') and x.clef._forced:
         #   return x.clef._forced
         if hasattr(x, 'clef') and x.clef.forced:
            return x.clef.forced
      return Clef('treble')

   @apply
   def forced( ):
      '''Forced clef change here.'''
      def fget(self):
         return self._forced
      def fset(self, arg):
#         if isinstance(arg, (Clef, types.NoneType)):
#            self._forced = arg
#         elif isinstance(arg, str):
#            self._forced = Clef(arg)
#         else:
#            raise ValueError('unknown clef specification.')
         assert isinstance(arg, (Clef, types.NoneType))
         self._forced = arg
      return property(**locals( ))

   @property
   def name(self):
      '''Name of effective clef as string.'''
      return self.effective.name

   @property
   def opening(self):
      '''Format contribution at container opening or before leaf.'''
      result = [ ]
      if self.forced or self.change:
         result.append(self.effective.format)
      return result
