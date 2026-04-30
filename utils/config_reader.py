import yaml
import os

_CONFIG_CACHE = None   # ✅ renamed so it's actually used


def load_config() -> dict:
    global _CONFIG_CACHE
    if _CONFIG_CACHE is not None:      # ✅ cache hit — no disk read
        return _CONFIG_CACHE

    config_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
    )

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    env = os.getenv("ENV", config.get("env", "qa"))
    if env not in config.get("environments", {}):
        raise ValueError(f"Environment '{env}' not found in config.yaml")

    _CONFIG_CACHE = config             # ✅ write to cache
    return _CONFIG_CACHE


def get_config(key: str, default=None):
    """
    Supports dot-notation for nested keys.

    get_config("env")                        → "qa"
    get_config("browsers.default")           → "chromium"
    get_config("environments.qa.base_url")   → "https://www.saucedemo.com"
    """
    config = load_config()
    keys = key.split(".")              # ✅ traverse nested structure
    value = config
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            return default
        if value is None:
            return default
    return value


def get_base_url(env: str = None) -> str:
    """Convenience shortcut used by fixtures."""
    config = load_config()
    env = env or os.getenv("ENV", config.get("env", "qa"))
    try:
        return config["environments"][env]["base_url"]
    except KeyError:
        raise ValueError(f"base_url not found for environment '{env}' in config.yaml")


def reset_cache():
    """Test helper — lets unit tests swap configs between runs."""
    global _CONFIG_CACHE
    _CONFIG_CACHE = None
    
    


    