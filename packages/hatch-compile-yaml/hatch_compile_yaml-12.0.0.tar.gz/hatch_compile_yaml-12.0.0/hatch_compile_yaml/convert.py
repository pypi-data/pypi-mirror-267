import io
import json
import yaml
import msgpack
from pathlib import Path
import enum
from typing import Callable, Dict, Tuple

class FileFormat(enum.Enum):
    YAML = "yaml"
    JSON = "json"
    MSGPACK = "msgpack"

def yaml_load(file_content):
    with io.BytesIO(file_content) as bio:
        return yaml.safe_load(bio)

def json_load(file_content):
    with io.BytesIO(file_content) as bio:
        return json.load(bio)

def msgpack_load(file_content):
    with io.BytesIO(file_content) as bio:
        return msgpack.unpack(bio, raw=False)

# Define a dictionary mapping file formats to their respective load and save functions
FORMAT_FUNCTIONS: Dict[FileFormat, Tuple[Callable, Callable]] = {
    FileFormat.YAML: (yaml_load, lambda data, f: yaml.dump(data, f)),
    FileFormat.JSON: (json_load, lambda data, f: json.dump(data, f, indent=4)),
    FileFormat.MSGPACK: (msgpack_load, lambda data, f: msgpack.pack(data, f))
}

def convert_data_file(source_path: Path, target_path: Path, target_format: str = "msgpack", remove_source_files: bool = True):
    target_format_enum = FileFormat[target_format.upper()]
    load_func, save_func = FORMAT_FUNCTIONS[target_format_enum]

    # Load the source data
    with source_path.open("rb") as f:
        file_content = f.read()
    
    data = load_func(file_content)

    # Convert and save the data to the target format
    with target_path.open("wb") as f:
        save_func(data, f)

    # Optionally remove the source file
    if remove_source_files:
        source_path.unlink()

