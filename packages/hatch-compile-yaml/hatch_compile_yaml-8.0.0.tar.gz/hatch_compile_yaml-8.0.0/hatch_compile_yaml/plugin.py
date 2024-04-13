import os
import re
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

from hatch_compile_yaml.convert import FileFormat, convert_data_file

DEFAULT_PATTERN = r".*\.(yaml|yml)$"

class DataFileConverter(BuildHookInterface):
    PLUGIN_NAME = "convert-data-file"

    def initialize(self, version, build_data):
        options = build_data.get("options", {})
        pattern = options.get("pattern", DEFAULT_PATTERN)
        target_format = options.get("target_format", "MSGPACK")  # Default to msgpack
        pattern_regex = re.compile(pattern)

        # Determine the output directory from build_data or use 'dist' as default
        output_dir = Path(build_data.get("output_directory", "dist"))

        for root, _, files in os.walk(self.root):
            for file in files:
                file_path = Path(root) / file
                if pattern_regex.match(file):
                    # Define the target path in the specified build output directory
                    target_path = output_dir / file_path.with_suffix(f".{target_format}").name
                    convert_data_file(file_path, target_path, FileFormat[target_format.upper()], options.get("remove_source_files", True))
