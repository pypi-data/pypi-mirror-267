import enum
import json
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



def convert_data_file(source_path: Path, target_path: Path, target_format: str = "msgpack", remove_source_files: bool = True):
    load_func, save_func = FORMAT_FUNCTIONS[FileFormat[target_format.upper()]]
    with source_path.open("rb") as f:
        raw_data = f.read()
        print(f"Raw data read from file: {raw_data[:100]}...")  # Print the first 100 bytes
        data = load_func(raw_data)

    with target_path.open("wb") as f:
        print(f"Data to be saved: {data}")
        save_func(data, f)

    if remove_source_files:
        source_path.unlink()
