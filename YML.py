import yaml
import os

def save_mysql_config(host, port, user, password, database):
    config_data = {
        "mysql": {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database
        }
    }

    with open("Config/MySQL.yaml", "w") as yaml_file:
        yaml.dump(config_data, yaml_file, default_flow_style=False)

def load_mysql_config():
    config_path = "Config/MySQL.yaml"

    if not os.path.exists(config_path):
        return None

    with open(config_path, "r") as yaml_file:
        try:
            config_data = yaml.safe_load(yaml_file)
            return config_data.get("mysql", None)
        except yaml.YAMLError as e:
            print(f"Loading error: {e}")
            return None