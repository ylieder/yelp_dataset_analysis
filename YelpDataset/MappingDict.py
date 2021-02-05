from typing import Any, Tuple


class MappingDict:
    """
    A dict like object that creates a unique integer mapping of the requested items.
    """
    def __init__(self):
        self.counter = 0
        self.mapping = {}

    def __getitem__(self, item: Any) -> Tuple[int, bool]:
        """
        Adds item to dict, if not exists and return unique mapping id.

        :param item: Requested item.
        :return: Mapping id of item and bool, whether item was added to dict or already existed.
        """
        if item in self.mapping:
            return self.mapping[item], False
        else:
            self.mapping[item] = self.counter
            self.counter += 1
            return self.counter - 1, True
