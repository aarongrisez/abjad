from experimental.tools.scoremanagertools import selectors
from experimental.tools.scoremanagertools.wizards.Wizard import Wizard


class ParameterSpecifierCreationWizard(Wizard):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'parameter specifier creation wizard'

    ### PUBLIC METHODS ###

    # TODO: maybe abstract up to Wizard?
    def get_target_editor(self, target_class_name, target=None):
        target_editor_class_name = target_class_name + self.target_editor_class_name_suffix
        command = 'from experimental.tools.scoremanagertools.editors import {} as target_editor_class'.format(target_editor_class_name)
        exec(command)
        target_editor = target_editor_class(session=self._session, target=target)
        return target_editor

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        self._session.cache_breadcrumbs(cache=cache)
        self._session.push_breadcrumb(self.breadcrumb)
        selector = selectors.ParameterSpecifierClassNameSelector(session=self._session)
        self._session.push_backtrack()
        target_class_name = selector.run()
        self._session.pop_backtrack()
        if self._session.backtrack():
            self._session.pop_breadcrumb()
            self._session.restore_breadcrumbs(cache=cache)
            return
        target_editor = self.get_target_editor(target_class_name)
        self._session.push_backtrack()
        target_editor.run()
        self._session.pop_backtrack()
        if self._session.backtrack():
            self._session.pop_breadcrumb()
            self._session.restore_breadcrumbs(cache=cache)
            return
        self._session.pop_breadcrumb()
        self._session.restore_breadcrumbs(cache=cache)
        self.target = target_editor.target
        return self.target
