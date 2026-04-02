from flask import Flask, jsonify

from database.exceptions import AppError, ConflictError, DatabaseError, NotFoundError, ValidationError
from database.src import db
from sqlalchemy.exc import SQLAlchemyError


def register_error_handlers(app: Flask):

    @app.errorhandler(Exception)
    def handle_unexpected(e):
        db.session.rollback()
        return jsonify({
            "error": "InternalServerError",
            "message": "Something went wrong"
        }), 500

    @app.errorhandler(AppError)
    def handle_app_error(e: AppError):
        data, status = e.http_response()
        return jsonify(data),status

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(e):
        db.session.rollback()
        return jsonify({
            "error": "DatabaseError",
            "message": "A database error occurred"
        }), 500
