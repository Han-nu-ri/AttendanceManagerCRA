from abc import ABC, abstractmethod


class Grade(ABC):
    @abstractmethod
    def get_grade(self):
        pass

class Gold(Grade):
    def get_grade(self):
        return "GOLD"

class Silver(Grade):
    def get_grade(self):
        return "SILVER"

class Normal(Grade):
    def get_grade(self):
        return "NORMAL"