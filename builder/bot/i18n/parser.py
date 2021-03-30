from typing import Dict
from builder.paths import I18N_PATH

def parse_languages() -> Dict[str, str]:
    """
    Parse all available languages and its aliases
    """

    lang_names = {}

    with open(I18N_PATH + "/" + "languages") as f:
        data = f.readlines()

    for line in data:
        language, aliases = line.split(":")

        for alias in aliases.split("|"):
            lang_names[alias.strip()] = language

    return lang_names