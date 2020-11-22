import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://postgres:Gofran_333@localhost:5432/trivia_test'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


    def test_GetCategoriesSuccessfully(self):
        res = self.client().get('/categories')
        JsonResult = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(JsonResult['categories']), 6)
        self.assertEqual(JsonResult['categories']['1'], 'Science')



    def test_GetCategories405Error(self):
        res = self.client().post('/categories')
        JsonResult = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertTrue(JsonResult['error'])
        self.assertTrue(JsonResult['message'])



    def test_GetQuestionsForCategorySuccessfully(self):
        res = self.client().get('/questions?page=1&currentCategory=2')
        JsonResult = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(JsonResult['categories']), 6)
        self.assertEqual(int(JsonResult['currentCategory']) , 2)
        self.assertEqual(len(JsonResult['questions']) , 4)
        self.assertEqual(int(JsonResult['totalQuestions']) , 4)



    def test_GetQuestionsForCategoryWrongCategoryError(self):
        res = self.client().get('/questions?page=1&currentCategory=7')
        JsonResult = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(JsonResult['categories']), 6)
        self.assertEqual(int(JsonResult['currentCategory']), 7)
        self.assertTrue(len(JsonResult['questions']) == 0)
        self.assertTrue(int(JsonResult['totalQuestions']) == 0)



    def test_DeleteQuestionSuccessfully(self):
        res = self.client().delete('/questions/20')
        questions = Question.query.filter(Question.id == 20).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(questions, None)



    def test_DeleteQuestion405Error(self):
        res = self.client().delete('/questions/1000')
        questions = Question.query.filter(Question.id == 1000).one_or_none()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(questions, None)

    def test_CreateQuestionSuccessfully(self):
        res = self.client().post('/questions', json={'question':'What is the name of best football player?',
                                                     'answer':'Messi','category':6,'difficulty':3})
        questions = Question.query.filter(Question.answer == 'Messi').one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(questions.answer, 'Messi')

    def test_CreateQuestion422Error(self):
        res = self.client().post('/questions', json={'question':'Who is the player that played for three different clubs?',
                                                     'answer':'CRonaldo','category':6})

        self.assertEqual(res.status_code, 422)

    def test_SearchQuestionSuccessfully(self):
        res = self.client().post('/questions/search', json={'currentCategory':None,'searchTerm':'beetle'})
        JsonResult = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(JsonResult['currentCategory'], None)
        self.assertTrue(len(JsonResult['questions']) == 1)
        self.assertTrue(int(JsonResult['totalQuestions']) == 1)

    def test_SearchQuestion400Error(self):
        res = self.client().post('/questions/search', json={'currentCategory':None})

        self.assertEqual(res.status_code, 400)

    def test_GetCategoriesQuestionsSuccessfully(self):
        res = self.client().get('/categories/2/questions')
        JsonResult = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(JsonResult['currentCategory']), 2)
        self.assertEqual(len(JsonResult['questions']), 4)
        self.assertEqual(int(JsonResult['totalQuestions']), 4)

    def test_GetCategoriesQuestionsWrongCategory(self):
        res = self.client().get('/categories/7/questions')
        JsonResult = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(JsonResult['currentCategory']), 7)
        self.assertEqual(len(JsonResult['questions']), 0)
        self.assertEqual(int(JsonResult['totalQuestions']), 0)

    def test_GetNextQuizQuestionSuccessfully(self):
        res = self.client().post('/quizzes', json={"quiz_category":{"type": "Art", "id": "2"},"previous_questions":[18,19]})
        JsonResult = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(JsonResult['question'])

    def test_GetNextQuizQuestion404Error(self):
        res = self.client().post('/quizzes', json={"previous_questions":[18,19]})
        JsonResult = json.loads(res.data)

        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()