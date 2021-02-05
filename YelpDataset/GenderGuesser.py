from enum import Enum
from pathlib import Path
from typing import Optional, Set, Union


class Gender(Enum):
    F = 0        # Female
    M = 1        # Male
    BOTH = 2     # Female and Male
    UNKNOWN = 3  # Unknown


class GenderGuesser:
    """
    Guess the gender of a given name by looking up in a name table.
    """
    path: Optional[Union[str, Path]] = None
    female_names: Optional[Set[str]] = None
    male_names: Optional[Set[str]] = None

    def __init__(self, path: Union[str, Path], load_name_list: bool = True):
        """
        :param path: Path to CSV file with (name, gender) records.
        :param load_name_list: Whether the mname list is loaded directly.
        """
        self.path = path
        if load_name_list:
            self.load_name_list()

    def load_name_list(self) -> None:
        """
        Loads the name list and stores names into two sets (male and female names).
        """
        with open(self.path, 'r') as fd:
            names = [((items := line.split(','))[0].lower(), items[1]) for line in fd.readlines()]
            self.female_names = {name for name, gender in names if gender == 'F'}
            self.male_names = {name for name, gender in names if gender == 'M'}

    def guess(self, name: str):
        """
        Looks up name in name table. Ignores case.
        :param name: Name.
        :return: Gender.M, if name is only male name, Gender.F if name is female name only, Gender.BOTH if name is both,
        male and female name and Gender.UNKNOWN, if name is not in name table.
        """
        f = name.lower() in self.female_names
        m = name.lower() in self.male_names

        if f and m:
            return Gender.BOTH
        elif f:
            return Gender.F
        elif m:
            return Gender.M
        else:
            return Gender.UNKNOWN
