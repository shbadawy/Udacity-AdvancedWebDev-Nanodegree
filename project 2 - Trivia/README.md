# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Tasks

There are `TODO` comments throughout project. Start by reading the READMEs in:

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

We recommend following the instructions in those files in order. This order will look familiar from our prior work in the course.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup.

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency.

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API.

[View the README.md within ./frontend for more details.](./frontend/README.md)

This is the public repository for Udacity's Full-Stack Nanodegree program.

## How to run the project

### Backend
* Change directory to backend folder
* Open the terminal and run the following :
  * export DATABASE=postgresql://USERNAME:PASSWORD@localhost:5432/trivia
  * export FLASK_ENV=development
  * export FLASK_APP=flaskr
  * Navigate to localhost:5000 (the link provided in the terminal)
  
### Frontend
* Change direcory to the frontend folder 
* Open a new terminal
* Run "npm start"

### Tests 
* Change directory to backend folder
* Open the terminal and run the following :
  * export DATABASE=postgresql://USERNAME:PASSWORD@localhost:5432/trivia_test
  * python3 test_flaskr.py

## API Endpoints

* **'/categories'**
  * **Method = 'GET'**
  * **Response body**
    * 'success'
    * 'categories'
    
  * Sample response <br>
  ` {
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "success": true
  } `

* **'/questions'**
  * **Method = 'GET'**
  * **Response body**
    * 'questions'
    * 'total_questions'
    * 'categories'
    * 'current_category'

  * Sample response <br>
  ` {
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": "All", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ], 
  "total_questions": 19
  } `
  
* **'/categories/<int:category_id>/questions'**
  * **Method = 'GET'**
  * **Response body**
    * 'questions'
    * 'total_questions'
    * 'current_category'
    
  * Sample response <br>
  ` {
  "current_category": "Sports", 
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
  "total_questions": 2
  } `
  
* **'/questions/<int:question_id>'**
  * **Method = 'DELETE'**
  * **Response body**
    * 'success'
    * 'deleted'
    * 'questions'
    * 'total_questions'
    
  * Sample response <br>
    ` {
        'success': True,
        'deleted': 1,
        'questions':[
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 3, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    } 
    ],
        'total_questions': len(Question.query.all())
    } `
    
* **'/questions'**
  * **Method = 'POST'**
  * **Request parameters**
    * 'question'
    * 'answer'
    * 'category'
    * 'difficulty'
  * **Response body**
    * 'success'
    
  * Sample request <br>
  ` {
  "question":"How many days are there in the week",
  "answer":7,
  "category":'History',
  "difficulty":1
  } `
  
  * Sample response <br>
  ` {
  "success":True
  } `
  
* **'/questions/search'**
  * **Method = 'POST'**
  * **Request parameters**
    * 'searchTerm'
  * **Response body**
    * 'questions'
    * 'total_questions'
    * 'current_category'
    
  * Sample request <br>
  ` {
  "searchTerm":"days"
  } `
  
  * Sample response <br>
  ` {
  "questions":[
  "How many days are there in the week"
  ],
  "total_questions":1,
  "current_category":"History"
  } `

* **'/quizzes'**
  * **Method = 'POST'**
  * **Request parameters**
    * 'previous_questions'
    * 'quiz_category'
  * **Response body**
    * 'question'
    
  * Sample request <br>
  ` {
  "previous_questions":[
  "How many days are there in the week",
  "What is the capital of Egypt"
  ],
  "quiz_category":"History"
  } `
  
  * Sample response <br>
  ` {
  "question":[
  "Who is the current CEO of Apple"
  ]
  } `
