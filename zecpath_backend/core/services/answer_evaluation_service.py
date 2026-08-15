class AnswerEvaluationService:

    def calculate_keyword_score(self, answer_text, keywords):

        answer_text = answer_text.lower()

        matches = 0

        for keyword in keywords:

            if keyword.lower() in answer_text:
                matches += 1

        if not keywords:
            return 0

        return (matches / len(keywords)) * 100

    def calculate_total_score(self, keyword_score):

        return keyword_score
