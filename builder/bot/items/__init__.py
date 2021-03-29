import yaml
from typing import Dict, Any
from builder.paths import ITEM_DEFINITION_PATH

class Item:
    def __init__(self, name: str, /) -> None:
        with open(ITEM_DEFINITION_PATH.format(name)) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        self.init_item(data)
        
    def init_item(self, data: Dict[str, Any], /) -> None:
        for key, value in data.items():
            setattr(self, key, value)