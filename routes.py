from flask import Flask, request, jsonify, make_response, abort, Response
from flask_cors import CORS
from flask_restful import Api, Resource
from database import Database

'''
Initializing Flask and CORS
'''
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

'''
Initializing Database
'''
database = Database()
