# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_marktools_LilyPondCommand___setattr___01():
    r'''Slots constrain LilyPond command marks.
    '''

    lilypond_command = marktools.LilyPondCommand('break')

    assert pytest.raises(AttributeError, "lilypond_command.foo = 'bar'")
