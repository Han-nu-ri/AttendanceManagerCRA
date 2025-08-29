import pytest
from mission2.attendance import AttendanceCalculator
from mission2.player import Player


def test_add_basic_point():
    attendance_calculator = AttendanceCalculator()
    back_number = 0
    name = "Jane Doe"
    attendance_calculator.players[back_number] = Player(back_number=back_number, name=name)
    attendance_calculator.add_basic_point(attendance_day='wednesday', back_number=back_number)
    assert attendance_calculator.players[back_number].points == 3

    attendance_calculator.players[back_number] = Player(back_number=back_number, name=name)
    attendance_calculator.add_basic_point(attendance_day='saturday', back_number=back_number)
    assert attendance_calculator.players[back_number].points == 2

    attendance_calculator.players[back_number] = Player(back_number=back_number, name=name)
    attendance_calculator.add_basic_point(attendance_day='sunday', back_number=back_number)
    assert attendance_calculator.players[back_number].points == 2

    attendance_calculator.players[back_number] = Player(back_number=back_number, name=name)
    attendance_calculator.add_basic_point(attendance_day='monday', back_number=back_number)
    assert attendance_calculator.players[back_number].points == 1

def test_get_back_number():
    attendance_calculator = AttendanceCalculator()
    name = "Jane Doe"
    expected_back_number = 1
    assert expected_back_number == attendance_calculator.get_back_number(name)
    name = "SOTA"
    expected_back_number = 2
    assert expected_back_number == attendance_calculator.get_back_number(name)

def test_is_removed():
    attendance_calculator = AttendanceCalculator()
    name = "Jane Doe"
    back_number = attendance_calculator.get_back_number(name)
    attendance_calculator.players[back_number].grade = "NORMAL"
    attendance_calculator.players[back_number].attendance_counts['saturday'] = 0
    attendance_calculator.players[back_number].attendance_counts['sunday'] = 0
    attendance_calculator.players[back_number].attendance_counts['wednesday'] = 0
    assert attendance_calculator.is_removed(back_number)

    attendance_calculator.players[back_number].grade = "GOLD"
    assert not attendance_calculator.is_removed(back_number)

def test_analyze_grade():
    attendance_calculator = AttendanceCalculator()
    back_number = attendance_calculator.get_back_number(name="Jane Doe")
    attendance_calculator.players[back_number].points = 10
    attendance_calculator.analyze_grade()
    assert attendance_calculator.players[back_number].grade == "NORMAL"

    attendance_calculator.get_back_number(name="SOTA")
    attendance_calculator.players[back_number].points = 30
    attendance_calculator.analyze_grade()
    assert attendance_calculator.players[back_number].grade == "SILVER"

    attendance_calculator.get_back_number(name="DONA")
    attendance_calculator.players[back_number].points = 50
    attendance_calculator.analyze_grade()
    assert attendance_calculator.players[back_number].grade == "GOLD"


def test_add_bonus():
    attendance_calculator = AttendanceCalculator()
    back_number = attendance_calculator.get_back_number(name="Jane Doe")
    attendance_calculator.players[back_number].points = 10
    attendance_calculator.players[back_number].attendance_counts['wednesday'] = 10
    attendance_calculator.add_bonus()
    assert attendance_calculator.players[back_number].points == 20

    back_number = attendance_calculator.get_back_number(name="SOTA")
    attendance_calculator.players[back_number].points = 8
    attendance_calculator.players[back_number].attendance_counts['saturday'] = 5
    attendance_calculator.players[back_number].attendance_counts['sunday'] = 5
    attendance_calculator.add_bonus()
    assert attendance_calculator.players[back_number].points == 18

    back_number = attendance_calculator.get_back_number(name="DONA")
    attendance_calculator.players[back_number].points = 8
    attendance_calculator.players[back_number].attendance_counts['saturday'] = 4
    attendance_calculator.players[back_number].attendance_counts['sunday'] = 5
    attendance_calculator.add_bonus()
    assert attendance_calculator.players[back_number].points == 8
