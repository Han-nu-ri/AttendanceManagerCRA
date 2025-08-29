from grade import Grade


class BonusFactory:
    @staticmethod
    def get_bonus(attendance_counts):
        bonus_threshold = 10
        bonus_point = 10
        total_bonus = 0
        if attendance_counts['wednesday'] >= bonus_threshold:
            total_bonus += bonus_point
        if attendance_counts['saturday'] + attendance_counts['sunday'] >= bonus_threshold:
            total_bonus += bonus_point
        return total_bonus
