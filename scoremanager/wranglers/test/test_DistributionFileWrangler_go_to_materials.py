# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_go_to_materials_01():
    r'''Goes from score distribution files to score materials.
    '''

    input_ = 'red~example~score d m q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution files',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_DistributionFileWrangler_go_to_materials_02():
    r'''Goes from distribution file library to material library.
    '''

    input_ = 'd m q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - distribution files',
        'Score manager - materials',
        ]
    assert score_manager._transcript.titles == titles