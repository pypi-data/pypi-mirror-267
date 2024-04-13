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
FORMAT_FUNCTIONS: dict[FileFormat, tuple[Callable, Callable]] = {
    FileFormat.YAML: (
        lambda f: yaml.safe_load(f.read().decode("utf-8")),
        lambda data, f: f.write(yaml.safe_dump(data).encode("utf-8")),
    ),
    FileFormat.JSON: (
        lambda f: json.loads(f.read().decode("utf-8")),
        lambda data, f: f.write(json.dumps(data, indent=4).encode("utf-8")),
    ),
    FileFormat.MSGPACK: (
        lambda f: msgpack.unpackb(f.read()),
        lambda data, f: f.write(msgpack.packb(data)),
    ),
}


def resolve_file_format(extension: str) -> FileFormat:
    if extension in EXTENSION_TO_FORMAT:
        return EXTENSION_TO_FORMAT[extension]
    else:
        raise ValueError(f"Unsupported file extension: {extension}")


def convert_data_file(source_path: Path, target_path: Path, target_format: str = "msgpack", remove_source_files: bool = True):
    target_format = FileFormat[target_format.upper()]
    source_format = resolve_file_format(source_path.suffix)

    load_func, _ = FORMAT_FUNCTIONS[source_format]
    _, save_func = FORMAT_FUNCTIONS[target_format]

    # Load the source data
    with source_path.open("rb") as f:
        data = load_func(f)

    # Convert and save the data to the target format
    with target_path.open("wb") as f:
        save_func(data, f)

    # Optionally remove the source file
    if remove_source_files:
        source_path.unlink()
