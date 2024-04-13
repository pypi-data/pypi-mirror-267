from hatchling.plugin import hookimpl

from hatch_compile_yaml.plugin import YamlToMsgpack


@hookimpl
def hatch_register_build_hook():
    return YamlToMsgpack
