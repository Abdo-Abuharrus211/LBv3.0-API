"""
    This class conducts operations for all the questions.
"""
import random


class DbDriver:
    def __init__(self, supabase):
        self.supabase = supabase
        self.question_data = []
        self.answer_data = []
        self.selected_questions = []

    async def get_questions_from_db(self):
        """
        Fetch the questions from the database.

        :return: Dictionary of the questions, keys are question ids and values are JSON strings
        """
        response = await (
            self.supabase.table("questions")
            .select("*")  # TODO: change this if only need specifics
            .execute()
        )
        if response is None:
            raise Exception("Response is None: failed to retrieve data from database.")
        self.question_data = response
        return "Successfully fetched questions from database."

    async def get_question_answers_from_db(self):
        """
        Fetch the answers from the database.

        :return: Dictionary of the answers, keys are answer ids and values are JSON strings
        """
        response = await (self.supabase.table("answers").select("*").execute())
        if response is None:
            raise Exception("Response is None: failed to retrieve data from database.")
        self.answer_data = response
        return "Successfully fetched answers from database."

    def randomize_questions(self):
        """
            Pick 10 random from the db pool.
            @:return JSON string of the questions and their data
        """

        """
        1. From the data plot the IDs into a set
        2. Do random.choice on that set
        3. Remove from the set
        """
        choices = random.sample(self.question_data, 10)
        return choices
