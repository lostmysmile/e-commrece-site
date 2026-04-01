from typing_extensions import dataclass_transform  # pip install typing-extensions
from random import randrange, choice
from decimal import Decimal

from sqlalchemy import select
from contextlib import suppress
from typing import Any, Optional, override

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, json
# from json import JSONEncoder
from sqlalchemy.orm import Mapped, MappedAsDataclass, DeclarativeBase, mapped_column, relationship
from werkzeug.routing import BaseConverter
# from sqlalchemy.orm import relationship


class ListConverter(BaseConverter):
    def to_python(self, value):
        print(f"python, {value=}")
        return value.split("+")

    def to_url(self, value):
        print(f"url, {value=}")
        return "+".join(value)


class CustomJSONEncoder(json.provider.DefaultJSONProvider):
    def default(self, o):  # pyright: ignore[reportIncompatibleMethodOverride]
        # if isinstance(o, Decimal):
        #     return float(o)
        with suppress(AttributeError):
            return o.__json__()
        return super().default(o)


class serializable():
    from sqlalchemy import inspect

    def __json__(self):
        inspected = serializable.inspect(self)
        return {
            col.key: getattr(self, col.key)
            for col in inspected.map    per.column_attrs
        }


class Base(MappedAsDataclass, DeclarativeBase):
    pass


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json = CustomJSONEncoder(app)
app.url_map.converters["list"] = ListConverter

db = SQLAlchemy(app, model_class=Base)


class ProductCategory(serializable):
    __tablename__ = "product_category"

    product_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('product.id'), primary_key=True, init=False)
    category_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('category.id'), primary_key=True, init=False)


class User(serializable):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    username: Mapped[str] = mapped_column(
        db.String(80), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)

    password: Mapped[Password] = relationship("Password", back_populates="user", uselist=False,
                                              cascade="all, delete-orphan", init=False)


class Password(serializable):
    __tablename__ = "password"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(db.Integer,
                                         db.ForeignKey('user.id', ondelete="CASCADE"), init=False, nullable=False)
    hash: Mapped[str] = mapped_column(db.CHAR(128), nullable=False)
    salt: Mapped[str] = mapped_column(db.CHAR(32), nullable=False)

    user: Mapped["User"] = relationship(back_populates="password", init=False)


class Category(serializable):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(db.Integer, init=False, primary_key=True)
    name: Mapped[str] = mapped_column(
        db.String(50), unique=True, nullable=False, index=True)

    products: Mapped[list["Product"]] = relationship(
        secondary="product_category", back_populates="categories", init=False)


class Product(serializable):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(db.Integer, init=False, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False, index=True)

    details: Mapped[ProductDetails] = relationship('ProductDetails', back_populates='product',
                                                   uselist=False, cascade="all, delete-orphan", init=False)

    # Using 'product_category' because that is the default name for the ProductCategory class
    categories: Mapped[list[Category]] = relationship(
        'Category', secondary='product_category', back_populates='products', init=False)


class ProductDetails(serializable):
    __tablename__ = "product_details"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    product_id: Mapped[int] = mapped_column(db.Integer,
                                            db.ForeignKey('product.id', ondelete="CASCADE"), nullable=False, init=False)
    price: Mapped[Decimal] = mapped_column(
        db.Numeric(10, 2, asdecimal=False), nullable=False, default=0.00)
    description: Mapped[str] = mapped_column(db.Text, default="")

    product: Mapped[Product] = relationship(back_populates="details", init=False)


def generate_random_name(max=20):
    from string import ascii_letters
    return "".join(choice(ascii_letters) for i in range(randrange(max)))


with app.app_context():
    # ...
    db.create_all()
    # db.drop_all()


def add_user(data: dict):
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added successfully!', "data": new_user})


def add_product(data: dict):
    new_product = Product(data['name'])
    new_product.details = ProductDetails(price=data['price'])

    db.session.add(new_product)
    db.session.commit()

    # ! very important because it loads data from database?
    print(new_product, new_product.details)
    return jsonify({'message': 'Product added successfully!', 'data': (new_product.__json__())})


def get_users(limit: int | None):
    sql_query = select(User).limit(limit)

    result = db.session.execute(sql_query)
    scalars = result.scalars()
    users = scalars.all()
    return jsonify(users)


def get_user_with_integer(id: int):
    sql_query = select(User)
    sql_query = sql_query.where(User.id == id)

    result = db.session.execute(sql_query)
    scalars = result.scalars()
    user = scalars.one_or_none()
    return user


def get_user_with_string(username: str):
    sql_query = select(User)
    if "@" in username:
        sql_query = sql_query.where(User.email == username)
    else:
        sql_query = sql_query.where(User.username == username)

    result = db.session.execute(sql_query)
    scalars = result.scalars()
    user = scalars.one_or_none()

    return user


def get_products(limit: int | None):
    sql_query = select(Product).limit(limit)

    result = db.session.execute(sql_query)

    scalars = result.scalars()
    products = scalars.all()
    print(products)
    return jsonify(products)


def get_product_with_name(name):
    sql_query = select(Product).where(Product.name == name)

    result = db.session.execute(sql_query)

    scalars = result.scalars()
    products = scalars.all()
    return jsonify(products)


def get_product_with_id(id):
    sql_query = select(Product).where(Product.id == id)

    result = db.session.execute(sql_query)

    scalars = result.scalars()
    product = scalars.one_or_none()
    return jsonify(product)


@app.route('/add_user', methods=['POST'])
def add_user_api():
    return add_user(data=request.get_json()), 201


@app.route('/add_user', methods=['Get'])
def add_user_api_get():
    data = request.args or \
        {"username": generate_random_name(), "email": generate_random_name(100)}
    return add_user(data), 201


@app.route('/add_product', methods=['POST'])
def add_product_api_post():
    data = request.get_json()
    return add_product(data), 201


@app.route('/add_product', methods=['Get'])
def add_product_api_get():
    return add_product(data=request.args or {"name": generate_random_name(), "price": randrange(150)})


@app.route('/users/')
@app.route('/users/<int:limit>')
def get_users_api(limit: int | None = None):
    return get_users(limit)


@app.route('/user/<int:id>')
@app.route('/user/<string:string>')
def get_user_from_id_api(id: Optional[int] = None, string: Optional[str] = None):
    if id:
        user = (get_user_with_integer(id))
    elif string:
        user = (get_user_with_string(string))
    else:
        raise ValueError("invalid input")
    return jsonify(user), 200 if user is not None else 404


@app.route('/products/')
@app.route('/products/<int:limit>')
def get_products_api(limit=None):
    return get_products(limit)


@app.route('/product/<string:name>')
@app.route('/product/<int:id>')
def get_product_api(id: int | None = None, name: str | None = None):
    if id:
        product = get_product_with_id(id)
    elif name:
        product = get_product_with_name(name)
    else:
        raise ValueError("Invalid input")
    return jsonify(product), 200 if product else 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)
