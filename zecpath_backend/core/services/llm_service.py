from django.conf import settings


class LLMService:

    def generate_questions(self, role):

        try:

            api_key = settings.OPENAI_API_KEY

            return {
                "status": "success",
                "questions": [
                    f"Tell me about your experience as a {role}",
                    f"What projects have you completed using {role}?",
                    "Explain a challenging problem you solved.",
                ],
            }

        except Exception as e:

            return {"status": "failed", "error": str(e)}
