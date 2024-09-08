from typing import Union

class SettingsDescriptor:

    def __set_name__(self, owner, name: str) -> None:
        self.attribute: str = "__" + name

    def __get__(self, instance, owner) -> Union[int, str, float, list]:
        return getattr(instance, self.attribute)

    def __set__(self, instance, value) -> None:
        if not hasattr(instance, self.attribute):
            setattr(instance, self.attribute, value)