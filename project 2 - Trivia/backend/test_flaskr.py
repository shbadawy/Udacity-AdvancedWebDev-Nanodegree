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
        self.database_name = 'trivia_test'
        self.database_path = os.environ.get('DATABASE')

        setup_db(self.app, self.database_path)

        self.new_question={
         'question' : 'How many wonders are there in the world',
         'answer' : '7',
         'category' : '2',
         'difficulty' : '1'
        }

        self.searchTerm={'searchTerm' : 'What'}

        self.new_quiz={'previous_questions':[],
        'quiz_category':{'id':'3', 'type':'History'}
        }
        self.new_question_fail= {'question':'What is the capital of Egypt',
                                 'answer' : 'Kuwait City',
                                 'category' : '10000',
                                 'difficulty' : '1'}

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
    def test_show_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_show_all_quesitons(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])

    def test_delete_quesiton (self):

        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['deleted'],2)
        self.assertTrue(data['total_questions'])
        self.assertEqual(question,None)

    def test_422_fail_delete_quesiton (self):

        res = self.client().delete('/questions/100000000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],422)
        self.assertEqual(data['message'],'unprocessable')


    def test_add_new_quesiton(self):

        res = self.client().post('/questions',json=self.new_question)
        print ("In Normal Test")
        data = json.loads(res.data)
        question = self.new_question['question']
        found = Question.query.filter(Question.question == question).all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(found)

    def test_422_fail_add_new_quesiton(self):

        res = self.client().post('/questions',json= self.new_question_fail)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],422)
        self.assertEqual(data['message'],'unprocessable')

    def test_search_quesitons(self):

        res = self.client().post('/questions/search',json=self.searchTerm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_422_fail_search_quesitons (self):

         res = self.client().post('/questions/search', json= {'searchTerm':None})

         data = json.loads(res.data)

         self.assertEqual(res.status_code, 422)
         self.assertEqual(data['success'],False)
         self.assertEqual(data['error'],422)
         self.assertEqual(data['message'],'unprocessable')

    def test_show_topic_quesitons(self):

        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_fail_show_topic_quesitons (self):

        res = self.client().get ('/categories/10000000/questions')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],'Resource not found')

    def test_play_quizz(self):

        res = self.client().post('/quizzes' , json=self.new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_422_fail_Play_quiz (self):

        res = self.client().post ('/quizzes', json={'previous_questions':None,
                                  'quiz_category':{'id':10000, 'type':'Hoppies'}})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],422)
        self.assertEqual(data['message'],'unprocessable')

     # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
