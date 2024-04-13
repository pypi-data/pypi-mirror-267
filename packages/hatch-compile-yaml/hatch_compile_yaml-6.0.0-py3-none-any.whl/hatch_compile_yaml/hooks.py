from hatchling.plugin import hookimpl

from hatch_compile_yaml.plugin import DataFileConverter


@hookimpl
def hatch_register_build_hook():
    return DataFileConverter
