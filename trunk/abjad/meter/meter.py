from abjad.core.grobhandler import _GrobHandler
from abjad.helpers.denominator_to_multiplier import _denominator_to_multiplier
from abjad.helpers.is_power_of_two import _is_power_of_two
from abjad.rational.rational import Rational


class Meter(_GrobHandler):

   def __init__(self, *args):
      _GrobHandler.__init__(self, 'TimeSignature')
      self.suppress = False
      if len(args) == 1 and isinstance(args[0], Meter):
         meter = args[0]
         self.numerator = meter.numerator
         self.denominator = meter.denominator
      elif len(args) == 1 and isinstance(args[0], Rational):
         self.numerator = args[0]._n
         self.denominator = args[0]._d
      elif len(args) == 1 and isinstance(args[0], tuple):
         numerator, denominator = args[0][0], args[0][1]
         self.numerator = numerator
         self.denominator = denominator
      elif len(args) == 2 and all([isinstance(x, int) for x in args]):
         self.numerator = args[0]
         self.denominator = args[1]
      else:
         raise ValueError('invalid %s meter initialization.' % str(args))

   ### OVERLOADS ###

   def __eq__(self, arg):
      if isinstance(arg, Meter):
         return self.pair == arg.pair
      elif isinstance(arg, tuple):
         return self.pair == arg
      else:
         return False

   def __ge__(self, arg):
      if isinstance(arg, Meter):
         return self.duration >= arg.duration
      else:
         raise TypeError
   
   def __gt__(self, arg):
      if isinstance(arg, Meter):
         return self.duration > arg.duration
      else:
         raise TypeError
   
   def __le__(self, arg):
      if isinstance(arg, Meter):
         return self.duration <= arg.duration
      else:
         raise TypeError
   
   def __lt__(self, arg):
      if isinstance(arg, Meter):
         return self.duration < arg.duration
      else:
         raise TypeError
   
   def __ne__(self, arg):
      return not self == arg

   def __nonzero__(self):
      return True
   
   def __repr__(self):
      return 'Meter(%s, %s)' % (self.numerator, self.denominator)

   def __str__(self):
      return '%s/%s' % (self.numerator, self.denominator)

   ### PUBLIC ATTRIBUTES ###

   @apply
   def denominator( ):
      def fget(self):
         return self._denominator
      def fset(self, arg):
         assert isinstance(arg, int)
         self._denominator = arg
      return property(**locals( ))

   @property
   def duration(self):
      return Rational(self.numerator, self.denominator)

   @property
   def format(self):
      return r'\time %s/%s' % (self.numerator, self.denominator)

   @property
   def multiplier(self):
      return _denominator_to_multiplier(self.denominator)

   @property
   def nonbinary(self):
      return not _is_power_of_two(self.denominator)

   @apply
   def numerator( ):
      def fget(self):
         return self._numerator
      def fset(self, arg):
         assert isinstance(arg, int)
         self._numerator = arg
      return property(**locals( ))

   @apply
   def pair( ):
      def fget(self):
         return self.numerator, self.denominator
      def fset(self, arg):
         if isinstance(arg, tuple) and len(arg) == 2 and \
            isinstance(arg[0], (int, float, long)) and \
            isinstance(arg[1], (int, float, long)):
            self.numerator = arg[0]
            self.denominator = arg[1]
         else:
            raise ValueError('meter %s must be (m . n) pair.' % str(arg))
      return property(**locals( ))

   ### TODO: Determine whether this property should implement 
   ###       here on Meter or on _MeterInterface

   @apply
   def suppress( ):
      def fget(self):
         return self._suppress
      def fset(self, arg):
         assert isinstance(arg, bool)
         self._suppress = arg
      return property(**locals( ))
