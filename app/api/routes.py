from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import Quotes, db, User, contact_schema, contacts_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/quotes', methods = ['POST'])
@token_required
def create_quote(current_user_token):
    quote = request.json['quote']
    author = request.json['author']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    quotes = Quotes(quote,author,user_token=user_token)

    db.session.add(quotes)
    db.session.commit()

    response = contact_schema.dump(quotes)
    return jsonify(response)

@api.route('/quotes', methods = ['GET'])
@token_required
def get_quote(current_user_token):
    a_user = current_user_token.token
    quotes = Quotes.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(quotes)
    return jsonify(response)

# Get single contact
@api.route('/quotes/<id>', methods = ['GET'])
@token_required
def get_single_quote(current_user_token, id):
    quotes = Quotes.query.get(id)
    response = contact_schema.dump(quotes)
    return jsonify(response)


@api.route('/quotes/<id>', methods = ['POST', 'PUT'])
@token_required
def update_quote(current_user_token, id):
    quotes = Quotes.query.get(id)
    quotes.quote = request.json['quote']
    quotes.author = request.json['author']
    quotes.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(quotes)
    return jsonify(response)

@api.route('/quotes/<id>', methods = ['DELETE'])
@token_required
def delete_quote(current_user_token, id):
    quotes = Quotes.query.get(id)
    db.session.delete(quotes)
    db.session.commit()
    response = contact_schema.dump(quotes)
    return jsonify(response)