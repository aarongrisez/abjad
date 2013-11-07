# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import marktools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from experimental.tools.handlertools.DynamicHandler import DynamicHandler


class TerracedDynamicsHandler(DynamicHandler):
    r'''Terraced dynamics.
    '''

    def __init__(self, dynamics=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        if dynamics is None:
            dynamics = []
        self.dynamics = dynamics

    ### SPECIAL METHODS ###

    def __call__(self, expr, offset=0):
        dynamics = datastructuretools.CyclicList(self.dynamics)
        for i, note_or_chord in enumerate(
            iterate(expr).by_class((scoretools.Note, scoretools.Chord))):
            dynamic_name = dynamics[offset + i]
            if self.minimum_duration <= note_or_chord._get_duration():
                #marktools.DynamicMark(dynamic_name)(note_or_chord)
                command = marktools.LilyPondCommandMark(dynamic_name, 'right')
                attach(command, note_or_chord)
        return expr

    ###  PUBLIC PROPERTIES ###

    @apply
    def dynamics():
        def fget(self):
            return self._dynamics
        def fset(self, dynamics):
            if dynamics is None:
                self._dynamics = dynamics
            elif all(
                marktools.DynamicMark.is_dynamic_name(x) for x in dynamics):
                self._dynamics = dynamics
            else:
                raise TypeError(dynamics)
        return property(**locals())
