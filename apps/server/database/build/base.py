from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from utilities.json_provider import Serializable

class Model(MappedAsDataclass, DeclarativeBase,Serializable):
    pass

db = SQLAlchemy(model_class=Model)

__all__ = "db","Model"