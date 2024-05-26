import re
import string
from typing import List

from tinydb import TinyDB, where
from pathlib import Path


class User:
    DB = TinyDB(Path(__file__).parent / 'db.json', indent=4)

    def __init__(self, first_name: str, last_name: str, phone_number: str = "", address: str = ""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

    def __repr__(self):
        return f"User({self.first_name}, {self.last_name})"

    def __str__(self):
        return f"{self.full_name}\n{self.phone_number}\n{self.address}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def db_instance(self):
        return User.DB.get((where('first_name') == self.first_name) & (where('last_name') == self.last_name))

    def _check_phone_number(self):
        phone_number = re.sub(r"[+()\s]*", "", self.phone_number)
        if len(phone_number) < 10 or not phone_number.isdigit():
            raise ValueError(f"Invalid phone number {self.phone_number}.")

    def _check_names(self):
        if not self.first_name and not self.last_name:
            raise ValueError("Please enter both first_name and last_name.")

        special_characters = string.punctuation + string.digits

        for char in self.first_name + self.last_name:
            if char in special_characters:
                raise ValueError(f"Invalid character {self.full_name}.")

    def _checks(self):
        self._check_names()
        self._check_phone_number()

    def exists(self) -> bool:
        return bool(self.db_instance)

    def delete(self) -> List[int]:
        if self.exists():
            return User.DB.remove(doc_ids=[self.db_instance.doc_id])
        return []

    def save(self, validate_data: bool = False) -> int:
        if validate_data:
            self._checks()

        if self.exists():
            return -1
        else:
            return User.DB.insert(self.__dict__)


def get_all_users():
    return [User(**user) for user in User.DB.all()]


if __name__ == '__main__':
    julie = User("Julie", "Courtois")
    print(julie.delete())
