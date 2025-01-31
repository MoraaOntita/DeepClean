import sys
import os
import yaml

# Ensure the project root directory is in sys.path
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, base_dir)

def load_config():
    """Load the config.yaml file and resolve paths."""
    config_path = os.path.join(base_dir, "sleeklady", "configurations", "config.yaml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Resolve paths dynamically
    for key, relative_path in config.get("paths", {}).items():
        expanded_path = os.path.expandvars(relative_path)
        config["paths"][key] = os.path.abspath(expanded_path)

    return config

CONFIG = load_config()
