from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from utilities.json_provider import Serializable

class Model(MappedAsDataclass, DeclarativeBase,Serializable):
    pass