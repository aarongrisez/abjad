from abjad.tools.importtools._import_public_names_from_path_into_namespace import _import_public_names_from_path_into_namespace


def _import_structured_package(path, namespace):
   '''Alias _import_structured_package.
   '''
   
   _import_public_names_from_path_into_namespace(path, namespace)

   del(namespace['_import_structured_package'])
