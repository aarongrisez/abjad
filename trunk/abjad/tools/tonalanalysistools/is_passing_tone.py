from abjad.tools import componenttools
from abjad.tools import notetools


def is_passing_tone(note):
    r'''.. versionadded:: 2.0

    True when `note` is both preceeded and followed by scalewise
    sibling notes. Otherwise false. ::

        >>> t = Staff("c'8 d'8 e'8 f'8")
        >>> for note in t:
        ...     print '%s\t%s' % (note, tonalanalysistools.is_passing_tone(note))
        ...
        c'8     False
        d'8     True
        e'8     True
        f'8     False

    Return boolean.
    '''
    from abjad.tools import tonalanalysistools

    if not isinstance(note, notetools.Note):
        raise TypeError('must be note: {!r}'.format(note))

    previous_note = note._get_namesake(-1)
    next_note = note._get_namesake(1)

    if previous_note is None or next_note is None:
        return False

    notes = [previous_note, note, next_note]
    selection = tonalanalysistools.select(notes)
    return selection.are_scalar_notes()
