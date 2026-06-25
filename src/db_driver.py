"""
    This class conducts operations for all the questions.
"""
import random
import logging

logger = logging.getLogger(__name__)

class DbDriver:
    def __init__(self):
        self.question_data = []
        self.answer_data = []

    def get_questions(self, db_cursor):
        """
        Get randomized questions for client, if not fetched then query DB.

        :return: JSON string of the random questions and their data
        """
        if self.question_data:
            logger.info("returning some random stuff")
            return self.randomize_questions()
        else:
            try:
                logger.info("trying to fetch from db")
                self.fetch_questions_from_db(db_cursor)
                return self.randomize_questions()
            except Exception as e:
                logger.error(f"Error fetching questions from DB: {e}")
                return None

    def get_answers(self, q_ids, db_cursor):
        """
        Retrieve the answers for the given question IDs.
        :param q_ids: list of integers representing question IDs
        :param db_cursor: database connection
        :return: The answer data if found, else None
        """
        if self.answer_data:
            return self.find_answer_by_id(q_ids)
        else:
            try:
                logger.info("getting answers from db")
                self.fetch_answers_from_db(db_cursor)
                return self.find_answer_by_id(q_ids)
            except Exception as e:
                logger.error(f"Error fetching answers from DB: {e}")
                return None

    def fetch_questions_from_db(self, db_cursor):
        """
        Fetch the questions from the database.

        :param db_cursor: database connection
        :return: Dictionary of the questions, keys are question ids and values are JSON strings
        """
        db_cursor.execute("SELECT * FROM questions")
        response = db_cursor.fetchall()

        logger.info(f"Fetched questions from DB: {response}")
        print(f"Fetched questions from DB: {response}")
        if response is None:
            raise Exception("Response is None: failed to retrieve data from database.")
        self.question_data = getattr(response, "data", response)

    def fetch_answers_from_db(self, db_cursor):
        """
        Fetch the answers from the database.

        :return: Dictionary of the answers, keys are answer ids and values are JSON strings
        """
        db_cursor.execute("SELECT * FROM answers")
        response = db_cursor.fetchall()
        logger.info(f"Fetched answers from DB: {response}")
        print(f"Fetched answers from DB: {response}")
        if response is None:
            raise Exception("Response is None: failed to retrieve data from database.")
        self.answer_data = getattr(response, "data", response)

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
        choices = random.sample(self.question_data, min(15, len(self.question_data)))
        return choices

    def find_answer_by_id(self, q_ids: list):
        """
        Find answer objects with correlating Question IDs.

        :param q_ids: A list of question IDs to find answers for
        :return: The answer data if found, else None
        """
        answers = []
        # TODO:  Optimize this search, something more elegant than nested loops...
        for q in q_ids:
            for j, answer in enumerate(self.answer_data):
                if answer['question'] == q:
                    answers.append(answer)
        print(f"Answers by IDL: {answers}")
        return answers
