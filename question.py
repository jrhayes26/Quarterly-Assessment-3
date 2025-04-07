class Question:
    def __init__(self, question, options, correct_answer):
        self.question = question
        self.options = options  # list of options: [A, B, C, D]
        self.correct_answer = correct_answer

    def is_correct(self, answer):
        return answer == self.correct_answer
