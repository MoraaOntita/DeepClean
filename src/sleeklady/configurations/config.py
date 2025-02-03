import sys
import os
import yaml
import json

# Ensure the project root directory is in sys.path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, base_dir)

def load_yaml_config():
    """Load the config.yaml file and resolve paths."""
    config_path = os.path.join(base_dir, "src", "sleeklady", "configurations", "config.yaml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")

    # Resolve paths dynamically
    for key, relative_path in config.get("paths", {}).items():
        abs_path = os.path.abspath(os.path.join(base_dir, relative_path))
        config["paths"][key] = abs_path

    return config

def load_product_codes():
    """Load the product_codes.json file."""
    json_path = os.path.join(base_dir, "src", "sleeklady", "configurations", "product_codes.json")

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Product codes file not found: {json_path}")

    try:
        with open(json_path, 'r') as file:
            product_codes = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON file: {e}")

    return product_codes

# Load configurations
CONFIG = load_yaml_config()
PRODUCT_CODES = load_product_codes()
