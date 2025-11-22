"""
    This class conducts operations for all the questions.
"""


class Questions:
    def __init__(self):
        pass

    def get_questions_from_db(self):
        """
        Fetch the questions from the database.

        :return: Dictionary of the questions, keys are question ids and values are JSON strings
        """
        pass

    def get_question_answers_from_db(self):
        """
        Fetch the answers from the database.

        :return: Dictionary of the answers, keys are answer ids and values are JSON strings
        """
        pass

    def randomize_questions(self):
        """
            Pick 10 random from the db pool.
            @:return JSON string of the questions and their data
        """
        pass
