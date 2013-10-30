# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import notetools


def color_leaf(leaf, color):
    r'''Color note:

    ::

        >>> note = Note("c'4")

    ::

        >>> labeltools.color_leaf(note, 'red')
        Note("c'4")

    ..  doctest::

        >>> f(note)
        \once \override Accidental #'color = #red
        \once \override Beam #'color = #red
        \once \override Dots #'color = #red
        \once \override NoteHead #'color = #red
        \once \override Stem #'color = #red
        c'4

    ::

        >>> show(note) # doctest: +SKIP

    Color rest:

    ::

        >>> rest = Rest('r4')

    ::

        >>> labeltools.color_leaf(rest, 'red')
        Rest('r4')

    ..  doctest::

        >>> f(rest)
        \once \override Dots #'color = #red
        \once \override Rest #'color = #red
        r4

    ::

        >>> show(rest) # doctest: +SKIP

    Color chord:

    ::

        >>> chord = Chord("<c' e' bf'>4")

    ::

        >>> labeltools.color_leaf(chord, 'red')
        Chord("<c' e' bf'>4")

    ..  doctest::

        >>> f(chord)
        \once \override Accidental #'color = #red
        \once \override Beam #'color = #red
        \once \override Dots #'color = #red
        \once \override NoteHead #'color = #red
        \once \override Stem #'color = #red
        <c' e' bf'>4

    ::

        >>> show(chord) # doctest: +SKIP

    Return `leaf`.
    '''

    # color leaf
    if isinstance(leaf, (notetools.Note, scoretools.Chord)):
        leaf.override.accidental.color = color
        leaf.override.beam.color = color
        leaf.override.dots.color = color
        leaf.override.note_head.color = color
        leaf.override.stem.color = color
    elif isinstance(leaf, scoretools.Rest):
        leaf.override.dots.color = color
        leaf.override.rest.color = color

    # return leaf
    return leaf
