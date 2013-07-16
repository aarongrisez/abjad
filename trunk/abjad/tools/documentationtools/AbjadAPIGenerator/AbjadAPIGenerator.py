import importlib
import os
from abjad.tools import abctools
from abjad.tools.documentationtools.APICrawler import APICrawler
from abjad.tools.documentationtools.ClassDocumenter import ClassDocumenter
from abjad.tools.documentationtools.FunctionDocumenter \
	import FunctionDocumenter


class AbjadAPIGenerator(abctools.AbjadObject):
    '''Creates Abjad's API ReST:

        * writes ReST pages for individual classes and functions
        * writes the API index ReST
        * handles sorting tools packages into composition, manual-loading 
          and unstable
        * handles ignoring private tools packages

    Returns `AbjadAPIGenerator` instance.
    '''

    ### CLASS VARIABLES ###

    _api_title = 'Abjad API'

    _package_descriptions = {
        'core': 'Core composition packages',
        'demos': 'Demos and example packages',
        'internals': 'Abjad internal packages',
        'unstable': 'Unstable packages (load manually)',
    }

    _undocumented_packages = (
        'materialpackages',
        'scorepackages',
    )

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, verbose=False):
        from abjad.tools import documentationtools

        if verbose:
            print 'Now making Sphinx TOCs ...'

        ignored_directories = ['.svn', 'test', '__pycache__']
        ignored_directories.extend(self._undocumented_packages)

        all_visited_modules = []
        for code_path, docs_path, package_prefix in self.path_definitions:
            if not os.path.exists(code_path):
                os.makedirs(code_path)
            if not os.path.exists(docs_path):
                os.makedirs(docs_path)
            crawler = APICrawler(code_path, docs_path, self.root_package,
                ignored_directories=ignored_directories, prefix=package_prefix)
            all_visited_modules.extend(crawler())
        package_dictionary, tools_package_dictionary = \
            self._sort_modules(all_visited_modules)

        if verbose:
            print 'Now making API index ...'

        document = documentationtools.ReSTDocument()
        document.append(documentationtools.ReSTHeading(
            level=0,
            text=self._api_title,
            ))

        for package_group, packages in sorted(package_dictionary.items()):
            if packages:
                document.append(documentationtools.ReSTHeading(
                    level=1,
                    text=self._package_descriptions[package_group]
                    ))
                document.append(documentationtools.ReSTTOCDirective(
                    options={'maxdepth': 1},
                    ))
                for package_module, package_dictionary in sorted(
                    packages.items()):
                    document.extend(self._create_package_toc(
                        package_module,
                        package_dictionary,
                        tools_package_dictionary,
                        ))

        f = open(self.docs_api_index_path, 'w')
        f.write(document.rest_format)
        f.close()

        if verbose:
            print ''
            print '... Done.'
            print ''

    ### PRIVATE METHODS ###

    def _create_package_toc(self, 
        package_module,
        package_dictionary,
        tools_package_dictionary,
        ):
        package_name = package_module.__name__.split('.')[
            self.tools_package_path_index]
        from abjad.tools import documentationtools
        result = [documentationtools.ReSTHeading(
            level=2,
            text=':py:mod:`{} <{}>`'.format(
                package_name, tools_package_dictionary[package_name])
            )
        ]
        only_html = documentationtools.ReSTOnlyDirective(argument='html')
        only_latex = documentationtools.ReSTOnlyDirective(argument='latex')
        if package_dictionary['abstract_classes']:
            only_latex.append(documentationtools.ReSTHeading(
                level=3,
                text='Abstract Classes'
                ))
            toc_html = documentationtools.ReSTTOCDirective(
                options={'maxdepth': 1},
                )
            toc_latex = documentationtools.ReSTTOCDirective()
            for obj in package_dictionary['abstract_classes']:
                toc_entry = self._module_name_to_toc_entry(obj.module_name)
                toc_html.append(toc_entry)
                toc_latex.append(toc_entry)
            only_html.append(toc_html)
            only_latex.append(toc_latex)
        if package_dictionary['concrete_classes']:
            only_latex.append(documentationtools.ReSTHeading(
                level=3,
                text='Concrete Classes'
                ))
            if package_dictionary['abstract_classes']:
                only_html.append(documentationtools.ReSTHorizontalRule())
            toc_html = documentationtools.ReSTTOCDirective(
                options={'maxdepth': 1},
                )
            toc_latex = documentationtools.ReSTTOCDirective()
            for obj in package_dictionary['concrete_classes']:
                toc_entry = self._module_name_to_toc_entry(obj.module_name)
                toc_html.append(toc_entry)
                toc_latex.append(toc_entry)
            only_html.append(toc_html)
            only_latex.append(toc_latex)
        if package_dictionary['functions']:
            only_latex.append(documentationtools.ReSTHeading(
                level=3,
                text='Functions'
                ))
            toc_html = documentationtools.ReSTTOCDirective(
                options={'maxdepth': 1},
                )
            toc_latex = documentationtools.ReSTTOCDirective()
            if package_dictionary['concrete_classes'] or \
                package_dictionary['abstract_classes']:
                only_html.append(documentationtools.ReSTHorizontalRule())
            for obj in package_dictionary['functions']:
                toc_entry = self._module_name_to_toc_entry(obj.module_name)
                toc_html.append(toc_entry)
                toc_latex.append(toc_entry)
            only_html.append(toc_html)
            only_latex.append(toc_latex)
        result.extend([only_html, only_latex])
        return result

    def _module_name_to_toc_entry(self, module_name):
        parts = module_name.split('.')[self.tools_package_path_index-1:-1]
        return '/'.join(parts)

    def _sort_modules(self, objects):
        package_dictionary = {}
        tools_package_dictionary = {}
        for obj in sorted(objects, key=lambda x: x.module_name):
            tools_package_name = obj.module_name.split('.')[
                self.tools_package_path_index]
            tools_package_path = '.'.join(
                obj.module_name.split('.')[:self.tools_package_path_index + 1])
            tools_package_module = importlib.import_module(tools_package_path)
            if tools_package_name not in tools_package_dictionary:
                tools_package_dictionary[tools_package_name] = tools_package_path
            if hasattr(tools_package_module, '_documentation_section'):
                declared_documentation_section = \
                    getattr(tools_package_module, '_documentation_section')
                if declared_documentation_section not in package_dictionary:
                    package_dictionary[declared_documentation_section] = {}
                collection = package_dictionary[declared_documentation_section]
            else:
                continue
            if tools_package_module not in collection:
                collection[tools_package_module] = {
                    'abstract_classes': [],
                    'concrete_classes': [],
                    'functions': []
                }
            if isinstance(obj, ClassDocumenter):
                if obj.is_abstract:
                    collection[tools_package_module][
                        'abstract_classes'].append(obj)
                else:
                    collection[tools_package_module][
                        'concrete_classes'].append(obj)
            else:
                collection[tools_package_module]['functions'].append(obj)
        return package_dictionary, tools_package_dictionary


    ### PUBLIC PROPERTIES ###

    @property
    def docs_api_index_path(self):
        '''Path to index.rst for Abjad API.
        '''
        from abjad import abjad_configuration
        return os.path.join(
            abjad_configuration.abjad_directory_path, 
            'docs', 'source', 'api', 'index.rst')

    @property
    def package_prefix(self):
        return ('abjad.tools.', 'abjad.demos.')

    @property
    def path_definitions(self):
        '''Code path / docs path / package prefix triples.
        '''
        from abjad import abjad_configuration
        return (
            (
                os.path.join(
                    abjad_configuration.abjad_directory_path, 'tools'),
                os.path.join(
                    abjad_configuration.abjad_directory_path, 
                    'docs', 'source', 'api', 'tools'),
                'abjad.tools.',
            ),
            (
                os.path.join(
                    abjad_configuration.abjad_directory_path, 'demos'),
                os.path.join(
                    abjad_configuration.abjad_directory_path, 
                    'docs', 'source', 'api', 'demos'),
                'abjad.demos.',
            ),
        )

    @property
    def root_package(self):
        return 'abjad'

    @property
    def tools_package_path_index(self):
        return 2
