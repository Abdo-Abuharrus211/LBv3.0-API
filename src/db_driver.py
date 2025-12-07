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

    def get_questions(self):
        """
        Get randomized questions for client, if not fetched then query DB.

        :return: JSON string of the random questions and their data
        """
        print(self.question_data)
        if self.selected_questions:
            print("returning some random stuff")
            return self.selected_questions
        else:
            return self.randomize_questions()
            try:
                # print("trying to fetch from db")
                # await self.fetch_questions_from_db()
                return self.randomize_questions()
            except Exception as e:
                # print(f"Error fetching questions from DB: {e}")
                return None

    async def fetch_questions_from_db(self):
        """
        Fetch the questions from the database.

        :return: Dictionary of the questions, keys are question ids and values are JSON strings
        """
        response = await (
            self.supabase.table("questions")
            .select("*")  # TODO: change this if only need specifics
            .execute()
        )
        print(f"got the response's from db: {response}")
        data = getattr(response, "data", response)
        if response is None or not data:
            raise Exception("Response is None: failed to retrieve data from database.")
        print(data)
        self.question_data = data
        return "Successfully fetched questions from database."

    async def fetch_question_answers_from_db(self):
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
        # if len(self.question_data) < 10:
        #     raise Exception("Not enough questions in the database to select 10 unique questions.")
        # choices = random.sample(self.question_data, 10)
        choices = random.sample(self.question_data, min(10, len(self.question_data)))
        return choices
