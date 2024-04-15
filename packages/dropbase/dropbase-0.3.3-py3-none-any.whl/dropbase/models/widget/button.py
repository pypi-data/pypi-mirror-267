from typing import Annotated, List, Literal, Optional

from pydantic import BaseModel

from dropbase.models.category import PropertyCategory
from dropbase.models.common import ComponentDisplayProperties, OnEvent


class ButtonContextProperty(ComponentDisplayProperties):
    pass


class ButtonDefinedProperty(BaseModel):
    label: Annotated[str, PropertyCategory.default]
    name: Annotated[str, PropertyCategory.default]
    color: Annotated[
        Optional[
            Literal[
                "red",
                "blue",
                "green",
                "yellow",
                "gray",
                "orange",
                "purple",
                "pink",
            ]
        ],
        PropertyCategory.default,
    ]

    # events
    on_click: Annotated[Optional[OnEvent], PropertyCategory.events]

    # display rules
    display_rules: Annotated[Optional[List[dict]], PropertyCategory.display_rules]

    # internal
    component_type: Literal["button"]
