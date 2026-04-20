import yaml
import os


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
    config_path = os.path.abspath(config_path)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    env = os.getenv("ENV", "qa")
    if env not in config.get("environments", {}):
        raise ValueError(f"Environment '{env}' not found in config.yaml")

    return config

    