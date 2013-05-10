import os
from experimental.tools.scoremanagertools.proxies.FilesystemAssetProxy import FilesystemAssetProxy


class FileProxy(FilesystemAssetProxy):

    ### CLASS ATTRIBUTES ###

    _generic_class_name = 'file'
    _temporary_asset_name = 'temporary_file.txt'

    ### INITIALIZER ###

    def __init__(self, file_path=None, session=None):
        FilesystemAssetProxy.__init__(self, filesystem_path=file_path, session=session)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def extension(self):
        return ''

    @property
    def file_lines(self):
        result = []
        if self.file_path:
            if os.path.exists(self.file_path):
                file_pointer = file(self.file_path)
                result.extend(file_pointer.readlines())
                file_pointer.close()
        return result

    @property
    def file_path(self):
        return self.filesystem_path

    @property
    def format(self):
        return ''.join(self.formatted_lines)

    @property
    def formatted_lines(self):
        return self.file_lines

    @property
    def name_without_extension(self):
        if self.filesystem_basename:
            if '.' in self.filesystem_basename:
                return self.filesystem_basename[:self.filesystem_basename.rindex('.')]
            else:
                return self.filesystem_basename

    ### PUBLIC METHODS ###

    def display_formatted_lines(self):
        self._io.display(self.formatted_lines)

    def edit(self):
        os.system('vi + {}'.format(self.file_path))

    def fix(self):
        pass

    def has_line(self, line):
        file_reference = open(self.file_path, 'r')
        for file_line in file_reference.readlines():
            if file_line == line:
                file_reference.close()
                return True
        file_reference.close()
        return False

    def make_empty_asset(self, is_interactive=False):
        if not self.exists:
            file_reference = file(self.file_path, 'w')
            file_reference.write('')
            file_reference.close()
        self._io.proceed(is_interactive=is_interactive)

    def profile(self):
        pass

    def view(self):
        os.system('vi -R {}'.format(self.file_path))
