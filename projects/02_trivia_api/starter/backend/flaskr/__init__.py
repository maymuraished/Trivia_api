import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS,cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  cors = CORS(app, resources={r"*/api/*": {"origins": "*"}})



  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories', methods=['GET'])
  @cross_origin()
  def get_categories():
    try:
      categoriesResult = Category.query.all()
      categories = {}
      for category in categoriesResult:
        categories[category.id] = category.type
      return jsonify({
        'categories': categories

      })
    except:
      abort(404)


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

  @app.route('/questions', methods=['GET'])
  @cross_origin()
  def get_questions():
    try:
      page = request.args.get('page', 1, type=int)
      currentCategory = request.args.get('currentCategory', None, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      if currentCategory is None:
        questions = Question.query.all()
      else:
        questions = Question.query.filter(Question.category == currentCategory).all()
      categoriesResult = Category.query.all()
      categories = {}
      for category in categoriesResult:
        categories[category.id] = category.type
      formatted_questions = [q.format() for q in questions]
      return jsonify({
        'questions': formatted_questions[start:end],
        'totalQuestions': len(formatted_questions),
        'categories': categories,
        'currentCategory': currentCategory

      })
    except:
      abort(404)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=["DELETE"])
  @cross_origin()
  def delete_question(question_id):
    try:
      questions = Question.query.filter(Question.id == question_id).one_or_none()
      if questions is None:
        abort(404)
      else:
        questions.delete()
      return jsonify({'success': True})
    except:
      abort(404)


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  @cross_origin()
  def createQuestion():
    question = ''
    answer = ''
    difficulty = 0
    category = 0
    try:
      question = request.get_json()['question']
      answer = request.get_json()['answer']
      difficulty = request.get_json()['difficulty']
      category = request.get_json()['category']
    except:
      abort(422)
    try:
      questionObj = Question(question=question, answer=answer, difficulty=difficulty, category=category)
      questionObj.insert()
      return jsonify({'success': True})
    except:
      abort(400)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=["POST"])
  @cross_origin()
  def searchQuestionByTerm():
    try:
      searchTerm = request.get_json()['searchTerm']
      currentCategory = request.get_json()['currentCategory']
      search = "%{}%".format(searchTerm)
      if currentCategory is None:
        questions = Question.query.filter(Question.question.like(search)).all()
      else:
        questions = Question.query.filter(Question.category == currentCategory, Question.question.like(search)).all()
      formatted_questions = [q.format() for q in questions]
      return jsonify({
        'questions': formatted_questions,
        'totalQuestions': len(formatted_questions),
        'currentCategory': currentCategory
      })
    except:
      abort(400)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions', methods=["GET"])
  @cross_origin()
  def getQuestionsByCategories(category_id):
    try:
      questions = Question.query.filter(Question.category == category_id).all()
      formatted_questions = [q.format() for q in questions]
      return jsonify({
        'questions': formatted_questions,
        'totalQuestions': len(formatted_questions),
        'currentCategory': category_id
      })
    except:
      abort(404)

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

  @app.route('/quizzes', methods=["POST"])
  @cross_origin()
  def quiz():
    try:
      previous_questions = request.get_json()['previous_questions']
      quiz_category = request.get_json()['quiz_category']['id']
      categoryID = int(quiz_category)
      if categoryID == 0:
        questions = Question.query.all()
      else:
        questions = Question.query.filter(Question.category == categoryID).all()
      randomQuestion = None
      if len(questions) > 0:
        questionsAfterFiltertion = list(filter(lambda question: question.id not in previous_questions, questions))
        if len(questionsAfterFiltertion) > 0:
          randomQuestion = random.choice(questionsAfterFiltertion)
          randomQuestion = randomQuestion.format()

      return jsonify({
        'question': randomQuestion
      })
    except:
      abort(404)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad Request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not Found"
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "Method Not Allowed"
    }), 405

  @app.errorhandler(408)
  def request_timeout(error):
    return jsonify({
      "success": False,
      "error": 408,
      "message": "Request Timeout"
    }), 408

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable Entity"
    }), 422

  @app.errorhandler(429)
  def too_many_requests(error):
    return jsonify({
      "success": False,
      "error": 429,
      "message": "Too Many Requests"
    }), 429

  @app.errorhandler(431)
  def request_header_fields_too_large(error):
    return jsonify({
      "success": False,
      "error": 431,
      "message": "Request Header Fields Too Large"
    }), 431

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
    }), 500
  
  return app

    