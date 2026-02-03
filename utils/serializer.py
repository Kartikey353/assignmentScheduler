from datetime import datetime
from uuid import UUID

def serialize(obj):
    if isinstance(obj, (datetime, UUID)):
        return str(obj)
    if hasattr(obj, '__dict__'):
        return {
            key: serialize(value)
            for key, value in obj.__dict__.items()
        }
    return obj
