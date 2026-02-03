from enum import Enum


class Errors(Enum):
    APPSER_DB_INSERT_ERROR = {
        "type": "DBInsertError",
        "message": "Failed to insert record in DB",
    }
    APPSER_DB_FIND_ERROR = {
        "type": "DBFindError",
        "message": "Failed to get details from db",
    }
    APPSER_DB_UPDATE_ERROR = {
        "type": "DBUpdateError",
        "message": "Failed to update record in db",
    }
    APPSER_DB_DELETE_ERROR = {
        "type": "DBDeleteError",
        "message": "Failed to delete record from db",
    },
    APPSER_DB_ALREADY_EXISTS = {
        "type": "DBAlreadyExistsError", 
        "message": "Record already exists in db",
    }
