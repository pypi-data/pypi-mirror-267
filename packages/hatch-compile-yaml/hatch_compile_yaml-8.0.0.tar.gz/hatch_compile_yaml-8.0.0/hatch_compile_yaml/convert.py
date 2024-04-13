import enum
import json
from collections.abc import Callable
from pathlib import Path

import msgpack
import yaml


class FileFormat(enum.Enum):
    YAML = "yaml"
    JSON = "json"
    MSGPACK = "msgpack"


EXTENSION_TO_FORMAT = {
    ".yaml": FileFormat.YAML,
    ".yml": FileFormat.YAML,
    ".json": FileFormat.JSON,
    ".msgpack": FileFormat.MSGPACK,
}


# Define a dictionary that maps file formats to their respective load and save functions

FORMAT_FUNCTIONS = {
    FileFormat.YAML: (lambda f: yaml.safe_load(f), lambda data, f: yaml.dump(data, f)),
    FileFormat.JSON: (lambda f: json.load(f), lambda data, f: json.dump(data, f, indent=4)),
    FileFormat.MSGPACK: (lambda f: msgpack.unpack(f, raw=False), lambda data, f: msgpack.pack(data, f))
}



def resolve_file_format(extension: str) -> FileFormat:
    if extension in EXTENSION_TO_FORMAT:
        return EXTENSION_TO_FORMAT[extension]
    else:
        raise ValueError(f"Unsupported file extension: {extension}")


def convert_data_file(source_path: Path, target_path: Path, target_format: FileFormat, remove_source_files: bool = True):
    # Resolve format and get corresponding load and save functions
    load_func, save_func = FORMAT_FUNCTIONS[FileFormat[target_format]]

    # Load the source data
    with source_path.open("rb") as f:
        data = load_func(f)

    # Convert and save the data to the target format
    with target_path.open("wb") as f:
        save_func(data, f)

    # Optionally remove the source file
    if remove_source_files:
        source_path.unlink()
