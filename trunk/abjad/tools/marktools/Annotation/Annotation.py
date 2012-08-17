from abjad.tools.componenttools.Component import Component
from abjad.tools.marktools.Mark import Mark
import copy


class Annotation(Mark):
    r'''.. versionadded:: 2.0

    User-defined annotation::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> pitch = pitchtools.NamedChromaticPitch('ds')
        >>> marktools.Annotation('special pitch', pitch)(staff[0])
        Annotation('special pitch', NamedChromaticPitch('ds'))(c'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    Annotations contribute no formatting.

    Annotations implement ``__slots__``.
    '''

    __slots__ = ('_format_slot', '_name', '_value', )

    _format_slot = None

    def __init__(self, *args):
        Mark.__init__(self)
        if len(args) == 1 and isinstance(args[0], type(self)):
            self._name = copy.copy(args[0].name)
            self._value = copy.copy(args[0].value)
        elif len(args) == 1 and not isinstance(args[0], type(self)):
            self._name = copy.copy(args[0])
            self._value = None
        elif len(args) == 2:
            self._name = copy.copy(args[0])
            self._value = copy.copy(args[1])
        else:
            raise ValueError('unknown annotation initialization signature.')

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(self.name, self.value)

    __deepcopy__ = __copy__

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.name == arg.name:
                if self.value == self.value:
                    return True
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        if self.value is None:
            return repr(self.name)
        return ', '.join([repr(self.name), repr(self.value)])

    ### PUBLIC PROPERTIES ###

    @apply
    def name():
        def fget(self):
            '''Get name of annotation::

                >>> pitch = pitchtools.NamedChromaticPitch('ds')
                >>> annotation = marktools.Annotation('special_pitch', pitch)
                >>> annotation.name
                'special_pitch'

            Set name of annotation::

                >>> annotation.name = 'revised special pitch'
                >>> annotation.name
                'revised special pitch'

            Set string.
            '''
            return self._name
        def fset(self, name):
            assert isinstance(name, str)
            self._name = name
        return property(**locals())

    @apply
    def value():
        def fget(self):
            '''Get value of annotation::

                >>> annotation.value
                NamedChromaticPitch('ds')

            Set value of annotation::

                >>> annotation.value = pitchtools.NamedChromaticPitch('e')
                >>> annotation.value
                NamedChromaticPitch('e')

            Set arbitrary object.
            '''
            return self._value
        def fset(self, value):
            self._value = value
        return property(**locals())
