class FlowManagerService:

    def get_next_question(self,questions,current_index,answer=None,role=None):

        # Adaptive Flow

        if answer:

            answer = answer.lower()

            if "0" in answer:

                return {"question":"Do you have internship experience?"}

            elif "5" in answer:

                if role == "Java Developer":

                    return {"question":"Explain JVM."}

                return {"question":"Explain Django Middleware."}

        # Normal Flow

        if current_index >= len(questions):
            return None

        return {"question":questions[current_index].question}