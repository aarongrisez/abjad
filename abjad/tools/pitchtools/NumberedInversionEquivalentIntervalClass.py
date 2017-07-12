# -*- coding: utf-8 -*-
import numbers
from abjad.tools import mathtools
from abjad.tools.pitchtools.NumberedIntervalClass import NumberedIntervalClass


class NumberedInversionEquivalentIntervalClass(NumberedIntervalClass):
    '''Numbered inversion-equivalent interval-class.

    ::

        >>> import abjad

    ..  container:: example

        Initializes from integer:

        ::

            >>> abjad.NumberedInversionEquivalentIntervalClass(0)
            NumberedInversionEquivalentIntervalClass(0)

        ::

            >>> abjad.NumberedInversionEquivalentIntervalClass(1)
            NumberedInversionEquivalentIntervalClass(1)

    ..  container:: example

        Initializes from float:

        ::

            >>> abjad.NumberedInversionEquivalentIntervalClass(1.5)
            NumberedInversionEquivalentIntervalClass(1.5)

    ..  container:: example

        Initializes from string:

        ::

            >>> abjad.NumberedInversionEquivalentIntervalClass('1')
            NumberedInversionEquivalentIntervalClass(1)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, interval_class_token=None):
        from abjad.tools import pitchtools
        if isinstance(interval_class_token, type(self)):
            number = interval_class_token.number
        elif isinstance(interval_class_token, numbers.Number):
            if not 0 <= interval_class_token <= 6:
                message = 'must be between 0 and 6, inclusive.'
                raise ValueError(message)
            number = interval_class_token
        elif getattr(interval_class_token, 'semitones', None) is not None:
            number = interval_class_token.semitones
            number %= 12
            if 6 < number:
                number = 12 - number
        elif interval_class_token is None:
            number = 0
        elif isinstance(interval_class_token, str):
            number = float(interval_class_token)
            if mathtools.is_integer_equivalent(number):
                number = int(number)
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, interval_class_token)
            raise TypeError(message)
        self._number = number

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Absolute value of numbered inversion-equivalent interval-class.

        Returns new numbered inversion-equivalent interval-class.
        '''
        return type(self)(abs(self.number))

    def __copy__(self):
        r'''Copies numbered inversion-equivalent interval-class.

        Returns new numbered inversion-equivalent interval-class.
        '''
        return type(self)(self.number)

    def __lt__(self, argument):
        r'''Is true when `argument` is a numbered inversion-equivalent
        interval-class with a number less than this numbered
        inversion-equivalent interval-class.
        '''
        if isinstance(argument, type(self)):
            return self.number < argument.number
        return False

    def __neg__(self):
        r'''Negates numbered inversion-equivalent interval-class.

        Returns new numbered inversion-equivalent interval-class.
        '''
        return type(self)(self.number)

    def __str__(self):
        r'''String representation of numbered inversion-equivalent
        interval-class.

        Returns string.
        '''
        return str(self.number)
