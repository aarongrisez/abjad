# -*- encoding: utf-8 -*-
from scoremanager.wizards.Wizard import Wizard


class RhythmMakerCreationWizard(Wizard):
    r'''Rhythm-maker creation wizard.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_handler_editor_class_name_suffix',
        )

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import iotools
        Wizard.__init__(
            self,
            session=session,
            target=target,
            )
        selector = iotools.Selector(session=self._session)
        selector = selector.make_rhythm_maker_class_name_selector()
        self._selector = selector
        self._handler_editor_class_name_suffix = 'Editor'

    ### PUBLIC PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'rhythm-maker creation wizard'