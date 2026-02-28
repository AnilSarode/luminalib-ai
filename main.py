from flask import Flask
from api.books import books_bp
from api.borrowings import borrowings_bp
from api.reviews import reviews_bp

app = Flask(__name__)

app.register_blueprint(books_bp)
app.register_blueprint(borrowings_bp)
app.register_blueprint(reviews_bp)

if __name__ == "__main__":
    app.run(debug=True)
