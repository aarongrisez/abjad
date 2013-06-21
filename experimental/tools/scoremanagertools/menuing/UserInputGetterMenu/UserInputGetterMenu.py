import types
from abjad.tools import stringtools
from experimental.tools.scoremanagertools import predicates
from experimental.tools.scoremanagertools.menuing.Menu import Menu
from experimental.tools.scoremanagertools.menuing.UserInputGetterMixin \
    import UserInputGetterMixin


class UserInputGetterMenu(Menu, UserInputGetterMixin):
    '''User input getter menu.

    .. note:: add docstring.

    Return user input getter.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None, where=None):
        Menu.__init__(self, session=session, where=where)
        UserInputGetterMixin.__init__(self)
        self._prompts = []
        self.allow_none = False
        self.capitalize_prompts = True
        self.include_newlines = False
        self.number_prompts = False
        self.prompt_character = '>'

    ### SPECIAL METHODS ###

    def __len__(self):
        '''Number of prompts in user input getter menu.

        Return nonnegative integer.
        '''
        return len(self.prompts)
        
    def __repr__(self):
        '''Interpreter representation of user input getter.

        Return string.
        '''
        return '<{} ({})>'.format(type(self).__name__, len(self))

    ### PRIVATE PROPERTIES ###

    @property
    def _current_prompt(self):
        return self.prompts[self.prompt_index]

    ### PRIVATE METHODS ###

    def _apply_validation_functions_to_value(self, value):
        if self.allow_none and value is None:
            return True
        validation_function = self._current_prompt.validation_function
        if validation_function is not None:
            return self._evaluate_test(validation_function, value)
        return True

    def _change_user_response_to_value(self, user_response):
        setup_statements = self._current_prompt.setup_statements
        assert isinstance(setup_statements, list)
        if setup_statements:
            value = self._get_value_from_setup_statements(
                user_response, setup_statements)
            if value is None and not user_response == 'None':
                return '!!!'
        else:
            value = self._get_value_from_direct_evaluation(user_response)
        return value

    def _display_help(self):
        if True:
            lines = []
            lines.append(self._current_prompt.help_string)
            lines.append('')
            self._io.display(lines)

    def _display_help(self):
        lines = []
        if True:
            lines.append(self._current_prompt.help_string)
        else:
            lines.append('help string not available.')
        lines.append('')
        self._io.display(lines)

    def _evaluate_test(self, test, argument):
        if isinstance(test, types.TypeType):
            return isinstance(argument, test)
        else:
            return test(argument)

    def _get_value_from_direct_evaluation(self, user_response):
        try:
            value = eval(user_response)
        except (NameError, SyntaxError):
            value = user_response
        return value

    def _get_value_from_setup_statements(
        self, user_response, setup_statements):
        for setup_statement in setup_statements:
            try:
                command = setup_statement.format(user_response)
                exec(command)
            except:
                try:
                    command = setup_statement.format(repr(user_response))
                    exec(command)
                except:
                    self._display_help()
                    return '!!!'
        return value

    def _indent_and_number_prompt(self, prompt):
        if self.number_prompts:
            prompt_number = self.prompt_index + 1
            prompt = '({}/{}) {}'.format(prompt_number, len(self), prompt)
        return prompt

    def _load_prompt(self):
        prompt_string = self._current_prompt.prompt_string
        if self.capitalize_prompts:
            prompt_string = stringtools.capitalize_string_start(prompt_string)
        self._menu_lines.append(prompt_string)

    def _move_to_prev_prompt(self):
        self.values.pop()
        self.prompt_index = self.prompt_index - 1

    def _present_prompt_and_store_value(self, include_chevron=True):
        '''True when user response obtained. Or when user skips prompt.
        False when user quits system or aborts getter.
        '''
        self._load_prompt()
        while True:
            prompt = self._menu_lines[-1]
            prompt = self._indent_and_number_prompt(prompt)
            default = str(self._current_prompt.default_value)
            include_chevron = self._current_prompt.include_chevron
            user_response = self._io.handle_raw_input_with_default(
                prompt, 
                default=default,
                include_chevron=include_chevron, 
                include_newline=self.include_newlines,
                prompt_character=self.prompt_character, 
                capitalize_prompt=self.capitalize_prompts)
            if user_response is None:
                self.prompt_index = self.prompt_index + 1
                break
            user_response = self._handle_hidden_menu_section_return_value(
                user_response)
            if self._session.backtrack():
                return False
            elif user_response is None:
                continue
            elif user_response == 'help':
                self._display_help()
            elif user_response == 'prev':
                self._move_to_prev_prompt()
                break
            elif user_response == 'skip':
                break
            elif isinstance(user_response, str):
                if self._store_value(user_response):
                    break
            else:
                self._io.print_not_yet_implemented()
        return True

    def _present_prompts_and_store_values(self, include_chevron=True):
        self._clear_terminal()
        self._menu_lines, self.values, self.prompt_index = [], [], 0
        while self.prompt_index < len(self):
            if not self._present_prompt_and_store_value(
                include_chevron=include_chevron):
                break

    def _run(self, user_input=None, include_chevron=True):
        self._io.assign_user_input(user_input=user_input)
        with self.backtracking:
            self._present_prompts_and_store_values(
                include_chevron=include_chevron)
        if len(self.values) == 1:
            return self.values[0]
        else:
            return self.values

    def _store_value(self, user_response):
        assert isinstance(user_response, str)
        if self.allow_none and user_response in ('', 'None'):
            value = None
        else:
            if self._try_to_store_value_from_target_menu_section(
                user_response):
                return True
            value = self._change_user_response_to_value(user_response)
            if value == '!!!':
                return False
            if not self._apply_validation_functions_to_value(value):
                self._display_help()
                return False
        self.values.append(value)
        self.prompt_index = self.prompt_index + 1
        return True

    def _store_value_from_target_menu_section(self, user_response):
        target_menu_section = self._current_prompt.target_menu_section
        assert target_menu_section is not None
        assert target_menu_section.is_numbered
        value = target_menu_section._argument_range_string_to_numbers(
            user_response)
        # TODO: maybe return list always from _argument_range*?
        if value is None:
            value = []
        self.values.append(value)
        self.prompt_index = self.prompt_index + 1

    def _try_to_store_value_from_target_menu_section(self, user_response):
        target_menu_section = self._current_prompt.target_menu_section
        if target_menu_section and self._apply_validation_functions_to_value(
            user_response):
            self._store_value_from_target_menu_section(user_response)
            return True
        else:
            return False

    ### PUBLIC PROPERTIES ###

    @apply
    def allow_none():
        def fget(self):
            return self._allow_none
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._allow_none = expr
        return property(**locals())

    @apply
    def capitalize_prompts():
        def fget(self):
            return self._capitalize_prompts
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._capitalize_prompts = expr
        return property(**locals())

    @apply
    def include_newlines():
        def fget(self):
            return self._include_newlines
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._include_newlines = expr
        return property(**locals())

    @apply
    def number_prompts():
        def fget(self):
            return self._number_prompts
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._number_prompts = expr
        return property(**locals())

    @property
    def prompts(self):
        return self._prompts

    @apply
    def prompt_character():
        def fget(self):
            return self._prompt_character
        def fset(self, expr):
            assert isinstance(expr, str)
            self._prompt_character = expr
        return property(**locals())
