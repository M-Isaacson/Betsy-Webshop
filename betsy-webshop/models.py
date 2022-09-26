from datetime import date
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    ForeignKeyField,
    TextField,
    IntegerField,
    Check,
)

# Connect to database.
db = SqliteDatabase("betsy.db")


class BaseModel(Model):
    class Meta:
        database = db


class Product(BaseModel):
    name = CharField()
    description = TextField()
    price_in_cents = IntegerField(default=0)
    amount_in_stock = IntegerField(default=0)

    class Meta:
        constraints = [Check("price_in_cents > 0"), Check("amount_in_stock >= 0")]


class Tag(BaseModel):
    name = CharField(unique=True)


class ProductTag(BaseModel):
    product = ForeignKeyField(Product, backref="tags")
    tag = ForeignKeyField(Tag, backref="products")


class User(BaseModel):
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    shipping_address = CharField(max_length=100)
    billing_address = CharField(max_length=100)
    payment_method = CharField(max_length=15)
    phone = CharField(max_length=15)
    email = CharField(max_length=30)


class Transaction(BaseModel):
    product = ForeignKeyField(Product, backref="transactions")
    user = ForeignKeyField(User, backref="transactions")
    amount = IntegerField(default=0)
    price_in_cents = IntegerField(default=0)
    trans_date = CharField(default=str(date.today()))
    payment_method = CharField()


class UserProduct(BaseModel):
    user = ForeignKeyField(User, backref="products")
    product = ForeignKeyField(Product, backref="users")


def create_tables():
    db.connect()
    with db:
        db.create_tables([Tag, Product, User, Transaction, UserProduct, ProductTag])


def drop_tables():
    db.connect()
    with db:
        db.drop_tables([Tag, Product, User, Transaction, UserProduct, ProductTag])


def populate_test_database():
    drop_tables()
    create_tables()

    user_list = [
        (
            "Thea",
            "Verdonk",
            "Klaverstraat 24, 7555 AA Hoorn, Nederland",
            "Klaverstraat 24, 7555 AA Hoorn, Nederland",
            "Bitcoin",
            "0655324444576",
            "t.verdonk@nomail.com",
        ),
        (
            "Rob",
            "Stiewert",
            "Maaskant 320, 1055 KM Apeldoorn, Nederland",
            "Mozartlaan 5, 1056 BA Apeldoorn, Nederland",
            "Ideal",
            "0653874625576",
            "rob.stiewert@spamail.com",
        ),
        (
            "Karen",
            "Jansen",
            "Brusselstraat 23, 3045 DB Assen, Nederland",
            "Brusselstraat 23, 3045 DB Assen, Nederland",
            "Ideal",
            "0452786224576",
            "karen@jansen.org",
        ),
        (
            "Sara",
            "van Oosten",
            "Kanaalweg 4, 9934 RT Harlingen, Nederland",
            "Mehrstrasse 142, 39645 Hamburg, Duitsland",
            "Cash",
            "0555837653333",
            "svoosten@gmail.com",
        ),
    ]
    with db.atomic():
        User.insert_many(
            user_list,
            fields=[
                User.first_name,
                User.last_name,
                User.shipping_address,
                User.billing_address,
                User.payment_method,
                User.phone,
                User.email,
            ],
        ).execute()

    tags_list = [
        {"name": "poncho"},
        {"name": "wool"},
        {"name": "kimono"},
        {"name": "cotton"},
        {"name": "scarf"},
        {"name": "ring"},
        {"name": "metal"},
        {"name": "vase"},
        {"name": "socks"},
        {"name": "shoes"},
        {"name": "canvas"},
    ]
    with db.atomic():
        Tag.insert_many(tags_list).execute()

    product_list = [
        ("Handmade Poncho", "Handmade Wool Poncho for Men", "7500", 34),
        ("Japanese Kimono", "Cotton Kimono for Women", "8800", 15),
        ("Painted Shoes", "Hand Painted Canvas Shoes for Women", "4500", 22),
        ("Scarf Ring", "Handmade Infinity Oval Scarf Ring", "12500", 5),
        ("Merino Wool Socks", "Hand knitted- Merino wool- Medium size 5-6", "1500", 30),
        ("Painted Vase", "Hand-Painted Floral Vase", "1500", 22),
    ]
    with db.atomic():
        Product.insert_many(
            product_list,
            fields=[
                Product.name,
                Product.description,
                Product.price_in_cents,
                Product.amount_in_stock,
            ],
        ).execute()

    product_tag_list = [
        (1, 1),
        (1, 2),
        (2, 3),
        (2, 4),
        (3, 10),
        (3, 11),
        (4, 5),
        (4, 6),
        (4, 7),
        (5, 9),
        (5, 2),
        (6, 8),
    ]
    with db.atomic():
        ProductTag.insert_many(
            product_tag_list,
            fields=[ProductTag.product, ProductTag.tag],
        ).execute()

    transaction_list = [
        (2, 3, 1, 8800, "2022-02-12", "Ideal"),
        (3, 3, 1, 4500, "2022-05-23", "Ideal"),
        (4, 4, 2, 25000, "2022-01-04", "Bitcoin"),
        (6, 3, 1, 1500, "2022-01-04", "Cash"),
        (4, 1, 1, 12500, "2022-03-15", "Bitcoin"),
    ]
    with db.atomic():
        Transaction.insert_many(
            transaction_list,
            fields=[
                Transaction.product,
                Transaction.user,
                Transaction.amount,
                Transaction.price_in_cents,
                Transaction.trans_date,
                Transaction.payment_method,
            ],
        ).execute()

    user_product_list = [
        (3, 2),
        (3, 3),
        (4, 4),
        (3, 6),
        (1, 4),
    ]
    with db.atomic():
        UserProduct.insert_many(
            user_product_list,
            fields=[
                UserProduct.user,
                UserProduct.product,
            ],
        ).execute()
