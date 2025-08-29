from abc import ABC, abstractmethod


class Point(ABC):
    @abstractmethod
    def get_point(self):
        pass


class MondayPoint(Point):
    def get_point(self):
        return 1


class TuesdayPoint(Point):
    def get_point(self):
        return 1


class WednesdayPoint(Point):
    def get_point(self):
        return 3


class ThursdayPoint(Point):
    def get_point(self):
        return 1


class FridayPoint(Point):
    def get_point(self):
        return 1


class SaturdayPoint(Point):
    def get_point(self):
        return 2


class SundayPoint(Point):
    def get_point(self):
        return 2
