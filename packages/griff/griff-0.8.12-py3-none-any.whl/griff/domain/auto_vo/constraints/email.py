import re

from griff.domain.auto_vo.constraints.abstract_constraint import ValueConstraint


class Email(ValueConstraint):
    def __init__(self):
        super().__init__()
        self._error_msg = "is not a valid email"

    def check(self, value) -> bool:
        email_regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )
        if not re.fullmatch(email_regex, str(value)):
            return False
        return True
