import os
import re
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

from hatch_compile_yaml.convert import convert_data_file


class DataFileConverter(BuildHookInterface):
    PLUGIN_NAME = "convert-data-file"

    def initialize(self, _, build_data):
        options = build_data.get("options", {})
        pattern = options.get("pattern", r".*\.(yaml|yml)$")
        pattern_regex = re.compile(pattern)

        for root, _, files in os.walk(self.root):
            for file in files:
                file_path = Path(root) / file
                if pattern_regex.match(file):
                    convert_data_file(file_path, **options)
