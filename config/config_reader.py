import yaml

def load_config():
    with open("config/config.yaml") as f:
        env = yaml.safe_load(f)["env"]

    with open(f"config/{env}.yaml") as f:
        return yaml.safe_load(f)
    