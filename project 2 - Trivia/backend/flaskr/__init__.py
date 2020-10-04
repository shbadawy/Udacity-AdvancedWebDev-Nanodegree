import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from random import randint

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(request,selection):
    page = request.args.get('page',1,type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start+QUESTIONS_PER_PAGE
    questionList=[]
    for question in selection:
        questionList.append(question.format())
    questions= questionList[start:end]
    return questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors=CORS(app, resources ={'r/api/*' : {'origins':'*'}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE')
      return response

  '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
  @app.route('/categories',methods=['GET'])
  def get_categories():

      try:
          categories = Category.query.order_by(Category.id).all()
          data =[]

          for category in categories:
              data.append(category.format()['type'])

          result={'success':True , 'categories':data}
          return jsonify(result)

      except:
          abort (404)

  '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
  @app.route('/questions',methods=['GET'])
  def get_questions():

      allQuestions = Question.query.order_by(Question.id).all()
      allCategories = Category.query.order_by(Category.id).all()

      try:

          questions = paginate(request,allQuestions)
          allCategoriesList=[]

          for category in allCategories:
              allCategoriesList.append(category.format()['type'])

          response = {'questions':questions,'total_questions':len(allQuestions),
                      'categories':allCategoriesList,'current_category':'All'}

          return jsonify(response)

      except:
          abort (404)

  '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question (question_id):
      try:

          question = Question.query.filter(Question.id == question_id).one_or_none()
          if question is None :
              abort(422)

          question.delete()

          allQuestions = Question.query.order_by(Question.id).all()
          questions = paginate(request,allQuestions)

          return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': questions,
                'total_questions': len(Question.query.all())
          })

      except:
          abort (422)

  '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
  @app.route('/questions',methods=['POST'])
  def add_question():

      body = request.get_json()

      quesitonText=body.get('question')
      answer=body.get('answer')
      category=body.get('category')
      difficulty=body.get('difficulty')

      try:
          searchCategory = Category.query.filter(Category.id == int (category)).one_or_none()

          if searchCategory is None:
              abort (422)

          question = Question(question=quesitonText,answer=answer,
                              category=category,difficulty=difficulty)
          question.insert()

          allQuestions = Question.query.order_by(Question.id).all()
          questions = paginate(request,allQuestions)

          return jsonify({'success': True})

      except:
          abort(422)

  '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_question():
      body = request.get_json()
      search = body.get('searchTerm',None)

      if search is None:
          abort(422)
      looking_for = '%{0}%'.format(search)
      try:
          questions = Question.query.filter(Question.question.ilike(looking_for))
          totalQuestionsLen= Question.query.count()
          questionsList=[]

          for question in questions:
              questionsList.append(question.format())

          result= {'questions':questionsList,'total_questions':totalQuestionsLen,
                   'current_category':'All'}
          return jsonify(result)
      except:
          abort(422)

  '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def getQuestionsByCategory(category_id):

      try:

          category = Category.query.filter(Category.id==category_id+1).one_or_none()
          selectedQuestions=[]

          if category is None:
              abort(404)

          categoryName=category.format()['id']
          questions = Question.query.filter(Question.category==str(categoryName))

          if questions is None :
               result = {'questions':selectedQuestions,'total_questions':len(selectedQuestions)
                       ,'current_category':None}
               return jsonify (result)

          for question in questions:
              selectedQuestions.append(question.format())

          result={'questions':selectedQuestions,'total_questions':len(selectedQuestions)
                  ,'current_category':category.format()['type']}
          return jsonify(result)

      except:
          abort (404)

  '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

  @app.route ('/quizzes',methods=['POST'])
  def play():

      body = request.get_json()
      previous_questions = body.get('previous_questions')

      quiz_category_dict = body.get('quiz_category')
      quiz_category_name = quiz_category_dict['type']

      quiz_category = quiz_category_dict['id']
      question =[]

      try:

          allQuestionsLen = Question.query.count()
          if quiz_category_name == 'click':
              allQuestions = Question.query.all()

          else:
              category = Category.query.filter (Category.id == quiz_category).one_or_none()
              if category is None:
                  abort(422)
              allQuestions = Question.query.filter (Question.category == quiz_category).all()
              allQuestionsLen = Question.query.filter (Question.category == quiz_category).count()

          if ( len (previous_questions) == allQuestionsLen ) or allQuestionsLen == 0:
              result = {'question':[]}
          else :
              index = randint (0,int (allQuestionsLen)-1)
              question= allQuestions[index].format()

              while (question['question'] in previous_questions):
                  index = randint (0,int (allQuestionsLen)-1)
                  question= allQuestions[index].format()

              result = {'question':question }
          return jsonify (result)

      except:
          abort (422)

  '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  @app.errorhandler(404)
  def not_found (error):
      return jsonify({
      'success' : False,
      'error' : 404,
      'message': 'Resource not found'
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
      'success' : False,
      'error' : 422,
      'message': 'unprocessable'
      }), 422

  @app.errorhandler(400)
  def unprocessable(error):
      return jsonify({
      'success' : False,
      'error' : 400,
      'message': 'bad request'
      }), 400

  return app
