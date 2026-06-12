from core.models.question_template import (QuestionTemplate)


class QuestionEngineService:

    def get_questions(self,role):

        return QuestionTemplate.objects.filter(role=role).order_by('id')