class MCQ:
    def __init__(self, document, question, options, answer):
        assert len(options) == 4, "There should be exactly 4 options"
        self.document = document
        self.question = question
        answer_index = options.index(answer)
        prefixes = ["A. ", "B. ", "C. ", "D. "]
        for i in range(4):
            prefix = prefixes[i]
            if options[i].startswith(prefix):
                options[i] = options[i][len(prefix) :]
        self.options = options
        self.answer = options[answer_index]

    def __str__(self):
        return f"{self.question}\nA. {self.options[0]}\nB. {self.options[1]}\nC. {self.options[2]}\nD. {self.options[3]}\n"

    def __repr__(self):
        return f"{self.question}\nA. {self.options[0]}\nB. {self.options[1]}\nC. {self.options[2]}\nD. {self.options[3]}\n"

    def check_answer(self, answer: str):
        return answer == self.answer

    def check_answer_index(self, index: str):
        try:
            index = ord(index) - ord("A")
            return self.options[index] == self.answer
        except:
            return False

    def get_question(self):
        return self.question

    def get_options(self):
        return self.options

    def get_answer(self):
        return self.answer

    def to_json(self):
        return {
            "document": self.document,
            "question": self.question,
            "options": self.options,
            "answer": self.answer,
        }
