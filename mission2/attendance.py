from typing import Dict
from mission2.player import Player


class AttendanceCalculator:
    def __init__(self):
        self.attendance_records = []
        self.name_and_back_number = {}
        self.max_back_number = 0
        self.players: Dict[int, Player] = {}

    def add_basic_point(self, attendance_day, back_number):
        wednesday_point = 3
        weekend_point = 2
        basic_point = 1
        if attendance_day == "wednesday":
            self.players[back_number].points += wednesday_point
        elif attendance_day == "saturday" or attendance_day == "sunday":
            self.players[back_number].points += weekend_point
        else:
            self.players[back_number].points += basic_point

    def get_back_number(self, name):
        if name not in self.name_and_back_number:
            self.max_back_number += 1
            self.name_and_back_number[name] = self.max_back_number
            self.players[self.max_back_number] = Player(name, self.max_back_number)
        return self.name_and_back_number[name]

    def calculate_attendance_points(self):
        try:
            self.read_attendance_records()
            self.calculate_attendance_days_and_points()
            self.add_bonus()
            self.analyze_grade()
            self.print_grades()
            self.print_removed_players()
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
        except Exception as exception:
            print(f"{exception}")

    def print_removed_players(self):
        print("\nRemoved player")
        print("==============")
        for back_number in range(1, self.max_back_number + 1):
            if self.is_removed(back_number):
                print(self.players[back_number].name)

    def is_removed(self, back_number):
        return self.players[back_number].grade == "NORMAL" and (
                self.players[back_number].attendance_counts['saturday']
                + self.players[back_number].attendance_counts['sunday']) == 0 and \
            self.players[back_number].attendance_counts['wednesday'] == 0

    def analyze_grade(self):
        gold_grade_threshold = 50
        silver_grade_threshold = 30
        for back_number in range(1, self.max_back_number + 1):
            if self.players[back_number].points >= gold_grade_threshold:
                self.players[back_number].grade = "GOLD"
            elif self.players[back_number].points >= silver_grade_threshold:
                self.players[back_number].grade = "SILVER"
            else:
                self.players[back_number].grade = "NORMAL"

    def add_bonus(self):
        bonus_threshold = 10
        bonus_point = 10
        for back_number in range(1, self.max_back_number + 1):
            if self.players[back_number].attendance_counts['wednesday'] >= bonus_threshold:
                self.players[back_number].points += bonus_point
            if self.players[back_number].attendance_counts['saturday'] + self.players[back_number].attendance_counts[
                'sunday'] >= bonus_threshold:
                self.players[back_number].points += bonus_point

    def print_grades(self):
        for back_number in range(1, self.max_back_number + 1):
            print(f"NAME : {self.players[back_number].name}, POINT : {self.players[back_number].points}, GRADE : ",
                  end="")
            print(self.players[back_number].grade)

    def read_attendance_records(self):
        attendance_records_file = "attendance_weekday_500.txt"
        with open(attendance_records_file, encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                self.attendance_records.append(line)

    def calculate_attendance_days_and_points(self):
        for each_line in self.attendance_records:
            name_and_day = each_line.strip().split()
            if len(name_and_day) == 2:
                name = name_and_day[0]
                attendance_day = name_and_day[1]
                back_number = self.get_back_number(name)
                self.add_basic_point(attendance_day, back_number)
                self.players[back_number].attendance_counts[attendance_day] += 1
            else:
                raise Exception(
                    f"Invalid Inputs. Each line must contain two str separated by space, But input is {each_line}")
