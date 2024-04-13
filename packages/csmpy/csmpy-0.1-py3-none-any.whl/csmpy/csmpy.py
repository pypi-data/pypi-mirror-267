import os
from .colors import color_codes, color_func
from .utils import load_custom_yaml_file_from_utils as load_custom_yaml_file, load_colors_from_utils as load_colors


class ColorSchemeManager:
    @classmethod
    def load_colors(cls, default_colors, custom_colors=None):
        if custom_colors is None:
            custom_colors = {}
        merged_colors = {**default_colors, **custom_colors}

        # Convert color names to ANSI escape codes
        for key, value in merged_colors.items():
            if value in color_codes:
                merged_colors[key] = color_codes[value]

        return merged_colors

    @staticmethod
    def load_custom_yaml_file(yaml_file_path):
        return load_custom_yaml_file(yaml_file_path)

    color_codes = color_codes
