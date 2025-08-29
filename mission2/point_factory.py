from point import WednesdayPoint, SaturdayPoint, MondayPoint, TuesdayPoint, FridayPoint, ThursdayPoint, \
    SundayPoint


class PointFactory:
    @staticmethod
    def get_point(attendance_day):
        if attendance_day == "monday":
            return MondayPoint().get_point()
        elif attendance_day == "tuesday":
            return TuesdayPoint().get_point()
        elif attendance_day == "wednesday":
            return WednesdayPoint().get_point()
        elif attendance_day == "thursday":
            return ThursdayPoint().get_point()
        elif attendance_day == "friday":
            return FridayPoint().get_point()
        elif attendance_day == "saturday":
            return SaturdayPoint().get_point()
        elif attendance_day == "sunday":
            return SundayPoint().get_point()
        else:
            raise Exception("Invalid date. Input must be monday, tuesday, wednesday, thursday, friday, saturday, sunday")