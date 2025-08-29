from typing import Dict

from bonus_factory import BonusFactory
from grade_factory import GradeFactory
from player import Player
from point_factory import PointFactory


class AttendanceCalculator:
    def __init__(self):
        self.attendance_records = []
        self.name_and_back_number = {}
        self.max_back_number = 0
        self.players: Dict[int, Player] = {}

    def add_basic_point(self, attendance_day, back_number):
        self.players[back_number].points += PointFactory.get_point(attendance_day)


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
        return self.players[back_number].grade.get_grade() == "NORMAL" and (
                self.players[back_number].attendance_counts['saturday']
                + self.players[back_number].attendance_counts['sunday']) == 0 and \
            self.players[back_number].attendance_counts['wednesday'] == 0

    def analyze_grade(self):
        for back_number in range(1, self.max_back_number + 1):
            self.players[back_number].grade = GradeFactory.creat_grade(self.players[back_number].points)

    def add_bonus(self):
        for back_number in range(1, self.max_back_number + 1):
            self.players[back_number].points += BonusFactory.get_bonus(self.players[back_number].attendance_counts)

    def print_grades(self):
        for back_number in range(1, self.max_back_number + 1):
            print(f"NAME : {self.players[back_number].name}, POINT : {self.players[back_number].points}, GRADE : ",
                  end="")
            print(self.players[back_number].grade.get_grade())

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
