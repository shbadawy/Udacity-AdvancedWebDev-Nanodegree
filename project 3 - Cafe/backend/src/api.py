import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        allDrinksEntries = Drink.query.all()
        drinksShortList = []

        for drink in allDrinksEntries:
            drinksShortList.append(drink.short())

    except Exception:
        Drink.roll_back()
        abort("404")

    result = {"success": True, "drinks": drinksShortList}
    return jsonify(result)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(e):
    try:
        allDrinksEntries = Drink.query.all()
        drinksLongList = []

        for drink in allDrinksEntries:
            drinksLongList.append(drink.long())

    except Exception:
        Drink.roll_back()
        abort("404")

    result = {"success": True, "drinks": drinksLongList}
    return jsonify(result)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(e):
    try:
        body = request.get_json()
        newTitle = body['title']
        newRecipe = body['recipe']

        isExist = Drink.query.filter(Drink.title == newTitle).one_or_none()

        if isExist is not None:
            abort(422)

        newDrink = Drink(title=newTitle, recipe=newRecipe)
        newDrink.insert

        allDrinksEntries = Drink.query.all()
        drinksLongList = []

        for drink in allDrinksEntries:
            drinksLongList.append(drink.long())

    except Exception:
        Drink.roll_back()
        abort(422)

    result = {"success": True, "drinks": drinksLongList}
    return jsonify(result)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def modify_drink(e, drink_id):
    try:

        body = request.get_json()
        newTitle = body.get('title')
        newRecipe = body.get('recipe')

        drinkToModify = Drink.query.filter(Drink.id == drink_id).one_or_none()
        drinksLongList = []

        if drinkToModify is not None:
            drinkToModify.title = newTitle
            drinkToModify.recipe = newRecipe

            drinkToModify.update()

            allDrinksEntries = Drink.query.all()

            for drink in allDrinksEntries:
                drinksLongList.append(drink.long())

    except Exception:
        Drink.roll_back()
        abort(422)

    result = {"success": True, "drinks": drinksLongList}
    return jsonify(result)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(e, drink_id):
    try:
        drinkToModify = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drinkToModify is not None:
            drinkToModify.delete()

            allDrinksEntries = Drink.query.all()
            drinksLongList = []

            for drink in allDrinksEntries:
                drinksLongList.append(drink.long())

    except Exception:
        Drink.roll_back()
        abort(422)

    result = {"success": True, "delete": drink_id}
    return jsonify(result)


# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def unautherized(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response


# error handler for 500
@app.errorhandler(500)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 500,
                    "message": "Internal Server Error"
                    }), 500
