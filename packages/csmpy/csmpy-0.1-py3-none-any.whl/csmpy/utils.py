import yaml


def load_colors_from_utils(default_colors, custom_colors=None):
    if custom_colors is None:
        custom_colors = {}
    merged_colors = {**default_colors, **custom_colors}
    return merged_colors


def load_custom_yaml_file_from_utils(yaml_file_path):
    try:
        with open(yaml_file_path, 'r') as custom_settings_file:
            config = yaml.safe_load(custom_settings_file)
            if config is None:
                raise ValueError("The YAML file is empty or invalid.")
            return config.get('custom', {})
    except (FileNotFoundError, yaml.YAMLError):
        return {}
