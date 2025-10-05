from flask import Flask

app = Flask(__name__)
import junya_flask.main

from junya_flask import db

db.create_books_table()
