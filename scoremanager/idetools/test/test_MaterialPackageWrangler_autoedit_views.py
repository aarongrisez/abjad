# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__MaterialPackageWrangler_views__.py',
    )
metadata_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__metadata__.py',
    )


def test_MaterialPackageWrangler_autoedit_views_01():

    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(views_file)
        os.remove(metadata_file)
        input_ = "M va add _test add 'example~notes'~in~:ds:"
        input_ += " add 'example~numbers'~in~:ds: done"
        input_ += " ren _test _new_test"
        input_ += " _new_test rm 'example~notes' done"
        input_ += " rm _new_test done q"
        score_manager._run(input_=input_)
        transcript = score_manager._transcript

    lines = [
        'Abjad IDE - materials - views - _test (EDIT)',
        '',
        '      elements - add (add)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - materials - views - _test (EDIT)',
        '',
        "   1: 'example notes' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - materials - views - _test (EDIT)',
        '',
        "   1: 'example notes' in :ds:",
        "   2: 'example numbers' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - materials - views (EDIT)',
        '',
        "   1: _test: 'example notes' in :ds:, 'example numbers' in :ds:",
        '',
        '      element - rename (ren)',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - materials - views (EDIT)',
        '',
        "   1: _new_test: 'example notes' in :ds:, 'example numbers' in :ds:",
        '',
        '      element - rename (ren)',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - materials - views - _new_test (EDIT)',
        '',
        "   1: 'example notes' in :ds:",
        "   2: 'example numbers' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - materials - views - _new_test (EDIT)',
        '',
        "   1: 'example numbers' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - materials - views (EDIT)',
        '',
        "   1: _new_test: 'example numbers' in :ds:",
        '',
        '      element - rename (ren)',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - materials - views (EDIT)',
        '',
        '      elements - add (add)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)