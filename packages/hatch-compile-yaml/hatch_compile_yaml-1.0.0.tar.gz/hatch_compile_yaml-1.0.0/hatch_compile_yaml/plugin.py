import os

import msgpack
import yaml
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class YamlToMsgpack(BuildHookInterface):
    PLUGIN_NAME = "yaml-to-msgpack"
    
    def initialize(self, version, build_data):
        print("Initializing YamlToMsgpack build hook")  # Debugging statement
        for root, dirs, files in os.walk(self.root):
            for file in files:
                if file == "config.yaml":
                    print(f"Found config.yaml: {os.path.join(root, file)}")
                    
                    yaml_file_path = os.path.join(root, file)
                    msgpack_file_path = yaml_file_path.replace(".yaml", ".msgpack")

                    with open(yaml_file_path) as f:
                        data = yaml.safe_load(f)
                    with open(msgpack_file_path, "wb") as f:
                        msgpack.pack(data, f)
