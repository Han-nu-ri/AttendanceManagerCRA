from typing import Dict


class Player:
    def __init__(self, name, back_number):
        self.name = name
        self.back_number = back_number
        self.points = 0
        self.grade = None
        self.attendance_counts: Dict[str, int] = {'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0,
                                                  'saturday': 0, 'sunday': 0}
