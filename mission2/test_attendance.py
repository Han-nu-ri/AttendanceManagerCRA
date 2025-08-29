from unittest.mock import patch, mock_open
import pytest
from attendance import AttendanceCalculator
from grade import Normal, Gold
from player import Player


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
    attendance_calculator.players[back_number].grade = Normal()
    attendance_calculator.players[back_number].attendance_counts['saturday'] = 0
    attendance_calculator.players[back_number].attendance_counts['sunday'] = 0
    attendance_calculator.players[back_number].attendance_counts['wednesday'] = 0
    assert attendance_calculator.is_removed(back_number)

    attendance_calculator.players[back_number].grade = Gold()
    assert not attendance_calculator.is_removed(back_number)

def test_analyze_grade():
    attendance_calculator = AttendanceCalculator()
    back_number = attendance_calculator.get_back_number(name="Jane Doe")
    attendance_calculator.players[back_number].points = 10
    attendance_calculator.analyze_grade()
    assert attendance_calculator.players[back_number].grade.get_grade() == "NORMAL"

    attendance_calculator.get_back_number(name="SOTA")
    attendance_calculator.players[back_number].points = 30
    attendance_calculator.analyze_grade()
    assert attendance_calculator.players[back_number].grade.get_grade() == "SILVER"

    attendance_calculator.get_back_number(name="DONA")
    attendance_calculator.players[back_number].points = 50
    attendance_calculator.analyze_grade()
    assert attendance_calculator.players[back_number].grade.get_grade() == "GOLD"


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


def test_calculate_attendance_points(capteesys):
    attendance_calculator = AttendanceCalculator()
    attendance_calculator.calculate_attendance_points()
    captured = capteesys.readouterr()
    expected = """NAME : Umar, POINT : 48, GRADE : SILVER
NAME : Daisy, POINT : 45, GRADE : SILVER
NAME : Alice, POINT : 61, GRADE : GOLD
NAME : Xena, POINT : 91, GRADE : GOLD
NAME : Ian, POINT : 23, GRADE : NORMAL
NAME : Hannah, POINT : 127, GRADE : GOLD
NAME : Ethan, POINT : 44, GRADE : SILVER
NAME : Vera, POINT : 22, GRADE : NORMAL
NAME : Rachel, POINT : 54, GRADE : GOLD
NAME : Charlie, POINT : 58, GRADE : GOLD
NAME : Steve, POINT : 38, GRADE : SILVER
NAME : Nina, POINT : 79, GRADE : GOLD
NAME : Bob, POINT : 8, GRADE : NORMAL
NAME : George, POINT : 42, GRADE : SILVER
NAME : Quinn, POINT : 6, GRADE : NORMAL
NAME : Tina, POINT : 24, GRADE : NORMAL
NAME : Will, POINT : 36, GRADE : SILVER
NAME : Oscar, POINT : 13, GRADE : NORMAL
NAME : Zane, POINT : 1, GRADE : NORMAL

Removed player
==============
Bob
Zane
"""
    assert captured.out == expected

    with patch('builtins.open', side_effect=FileNotFoundError):
        attendance_calculator.calculate_attendance_points()
        captured = capteesys.readouterr()
        assert captured.out == "파일을 찾을 수 없습니다.\n"


def test_read_attendance_records_should_raise_file_not_found_error_when_file_path_is_invalid():
    attendance_calculator = AttendanceCalculator()
    with patch('builtins.open', side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            attendance_calculator.read_attendance_records()


def test_read_attendance_records_should_break_when_line_is_none():
    attendance_calculator = AttendanceCalculator()
    with patch("builtins.open", mock_open(read_data="Charlie friday\n")) as mock_file:
        attendance_calculator.read_attendance_records()
        assert len(attendance_calculator.attendance_records) == 1


def test_calculate_attendance_days_and_points_should_raise_exception_when_input_is_invalid():
    attendance_calculator = AttendanceCalculator()
    attendance_calculator.attendance_records = ["invalidinput"]
    with pytest.raises(Exception):
        attendance_calculator.calculate_attendance_days_and_points()


    attendance_calculator.attendance_records = ["chris invalid"]
    with pytest.raises(Exception):
        attendance_calculator.calculate_attendance_days_and_points()