# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints

GET '/categories'
- The API Return all of the categories as List of IDs with thier values.
- Request Arguments: None.
- Response Arguments: One json object [categories].
- Response Exapmle:
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    }
}



GET '/questions'
- The API Return all of the categories, the category that the user current choosen,
  all of the questions in the choosen category[all of the questions if no category choosed], number of the questions returned.
- Request Arguments: Two get integer parameters [page,currentCategory].
- Request Example:
http://127.0.0.1:5000/questions?page=1&currentCategory=6
- Response Arguments: One json object [categories],one json list [questions], two integers [totalQuestions,currentCategory].
- Response Example:
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "currentCategory": 6,
    "questions": [
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "totalQuestions": 2
}



DELETE '/questions/<int:question_id>'
- The API Delete a question from the database base on it ID.
- Request Arguments: One URL integer parameter [question_id].
- Request Example:
http://127.0.0.1:5000/questions/20
- Response Arguments: None.



POST '/questions'
- The API create a question in the database.
- Request Arguments: Two json strings [question,answer], Two json integers [category,difficulty]
- Request Example:
{"question":"Who is the player with the most world cup league goals?","answer":"ronaldo","category":6,"difficulty":1}
- Response Arguments: None.



POST '/questions/search'
- The API Return all the questions that include in the search term and the category the user choosen[in all of categories if user did not
choose any] and the number of the questions found.
- Request Arguments: One json strings [searchTerm], One json integers [currentCategory]
- Request Example:
{"currentCategory":null,"searchTerm":"player"}
- Response Arguments: One json list [questions], two integers [totalQuestions,currentCategory].
- Response Example:
{
    "currentCategory": null,
    "questions": [
        {
            "answer": "messi",
            "category": 6,
            "difficulty": 1,
            "id": 25,
            "question": "Who is the player with the most ballon dollar?"
        },
        {
            "answer": "ronaldo",
            "category": 6,
            "difficulty": 1,
            "id": 26,
            "question": "Who is the player with the most Champions league goal?"
        },
        {
            "answer": "ronaldo",
            "category": 6,
            "difficulty": 1,
            "id": 35,
            "question": "Who is the player with the most world cup league goals?"
        }
    ],
    "totalQuestions": 3
}



GET '/categories/<int:category_id>/questions'
- The API Return all the questions that include in the category the user choosen and the number of the questions in it.
- Request Arguments: One URL integer parameter [category_id].
- Request Example:
http://127.0.0.1:5000/categories/2/questions
- Response Arguments: One json list [questions], two integers [totalQuestions,currentCategory].
- Response Example:
{
    "currentCategory": 2,
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        }
    ],
    "totalQuestions": 2
}



POST '/quizzes'
- The API Return any random question that is not in the previous questions list and the category the user choosen[all categories if user
chossed all].
- Request Arguments: One json object [quiz_category], One json list [previous_questions].
- Request Example:
{"quiz_category":{"type": "Sports", "id": "6"},"previous_questions":[11,25]}
- Response Arguments: One json object [question].
- Response Example:
{
    "question": {
        "answer": "ronaldo",
        "category": 6,
        "difficulty": 1,
        "id": 35,
        "question": "Who is the player with the most world cup league goals?"
    }
}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```