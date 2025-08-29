from grade import Gold, Silver, Normal


class GradeFactory:
    @staticmethod
    def creat_grade(point):
        gold_grade_threshold = 50
        silver_grade_threshold = 30
        if point >= gold_grade_threshold:
            return Gold()
        elif point >= silver_grade_threshold:
            return Silver()
        else:
            return Normal()
