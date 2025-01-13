import sys
import os
import yaml

# Ensure the project root directory is in the sys.path
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_dir)

def load_config():
    # Load the config.yaml file
    config_path = os.path.join(base_dir, "sleeklady", "configurations", "config.yaml")
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Load and resolve paths
    for key, relative_path in config["paths"].items():
        # Expand environment variables (e.g., ${DATA_FOLDER:-./Data}) and fallback to default if not set
        expanded_path = os.path.expandvars(relative_path)

        # Resolve the final absolute path
        config["paths"][key] = os.path.abspath(expanded_path)

    
    return config

CONFIG = load_config()
