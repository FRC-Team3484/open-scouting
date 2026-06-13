from typing import Any

from tortoise import fields

"""
This file includes subclasses of Tortoise fields for use in the Settings model

These add the following custom fields to the Settings model:
    - display_name - The display name of the setting
    - setting_description - The description of the setting
    - section - The section of the setting
    - visible - Whether the setting is visible
"""

class StringSetting(fields.CharField[str]):
    def __init__(
        self,
        max_length: int,
        *args: Any, 
        display_name: str, 
        setting_description: str | None, 
        section: str | None, 
        visible: bool, 
        **kwargs: Any
    ):
        self.display_name: str = display_name
        self.setting_description: str | None = setting_description
        self.section: str | None = section
        self.visible: bool = visible

        super().__init__(max_length=max_length, *args, **kwargs)

class NumberSetting(fields.IntField[int]):
    def __init__(
        self, 
        *args: Any, 
        display_name: str, 
        setting_description: str | None, 
        section: str | None, 
        visible: bool, 
        **kwargs: Any
    ):
        self.display_name: str = display_name
        self.setting_description: str | None = setting_description
        self.section: str | None = section
        self.visible: bool = visible

        super().__init__(*args, **kwargs)

class BooleanSetting(fields.BooleanField[bool]):
    def __init__(
        self, 
        *args: Any, 
        display_name: str, 
        setting_description: str | None, 
        section: str | None, 
        visible: bool, 
        **kwargs: Any
    ):
        self.display_name: str = display_name
        self.setting_description: str | None = setting_description
        self.section: str | None = section
        self.visible: bool = visible

        super().__init__(*args, **kwargs)

class ArraySetting(fields.JSONField[Any]):
    def __init__(
        self, 
        *args: Any, 
        display_name: str, 
        setting_description: str | None, 
        section: str | None, 
        visible: bool, 
        **kwargs: Any
    ):
        self.display_name: str = display_name
        self.setting_description: str | None = setting_description
        self.section: str | None = section
        self.visible: bool = visible

        super().__init__(*args, **kwargs)

class JSONSetting(fields.JSONField[Any]):
    def __init__(
        self, 
        *args: Any, 
        display_name: str, 
        setting_description: str | None, 
        section: str | None, 
        visible: bool, 
        **kwargs: Any
    ):
        self.display_name: str = display_name
        self.setting_description: str | None = setting_description
        self.section: str | None = section
        self.visible: bool = visible

        super().__init__(*args, **kwargs)