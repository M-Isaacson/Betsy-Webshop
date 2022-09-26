from models import db, Product, UserProduct, ProductTag, Transaction, User, populate_test_database
import difflib as dl

__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


def search(term):
    mi_list = []
    mi_query = Product.select(Product.id, Product.name, Product.description)
    # iterate over the query and compare the search term with the text in the name and description field. Based on ratio add the item to the list of tuples (match, name and id).
    for mi_product in mi_query:
        s1 = dl.SequenceMatcher(None, term.lower(), mi_product.name.lower())
        s2 = dl.SequenceMatcher(None, term.lower(), mi_product.description.lower())
        if s1.ratio() >= s2.ratio():
            mi_ratio = int(s1.ratio() * 100)
        else:
            mi_ratio = int(s2.ratio() * 100)
        mi_item = (
            mi_ratio,
            f"Match: {mi_ratio}%",
            f"Product: {mi_product.name}",
            f"ID: {mi_product.id}",
        )
        mi_list.append(mi_item)
    mi_sorted_list = sorted(mi_list, key=lambda tuple: tuple[0], reverse=True)
    mi_list = []
    for item in mi_sorted_list:
        mi_index = mi_sorted_list.index(item)
        mi_tuple_list = list(item)
        mi_tuple_list[0] = mi_index + 1
        item = tuple(mi_tuple_list)
        mi_list.append(item)
    return mi_list


def list_user_products(user_id):
    query = Product.select().join(UserProduct).where(UserProduct.user == user_id)
    mi_list = []
    if len(query) == 0:
        return "No products for this user"
    else:
        for product in query:
            mi_list.append(product.name)
    return mi_list


def list_products_per_tag(tag_id):
    query = Product.select().join(ProductTag).where(ProductTag.tag == tag_id)
    mi_list = []
    if len(query) == 0:
        return "No products with this tag"
    else:
        for product in query:
            mi_list.append(product.name)
    return mi_list


def add_product_to_catalog(user_id, product):
    # Does user-id exist
    mi_user = User.get_or_none(User.id == user_id)
    if mi_user is None:
        return "User does not exist!"
    # Check if product does exist
    mi_product = Product.get_or_none(Product.name == product)
    if mi_product is None:
        return "Product does not exist!"
    mi_new = UserProduct.create(user=mi_user, product=mi_product)
    return f"Row {mi_new} is added to user's products."


def update_stock(product_id, new_quantity):
    # Check if product does exist
    mi_product = Product.get_or_none(Product.id == product_id)
    if mi_product is None:
        return "Product does not exist!"
    mi_query = Product.update(amount_in_stock=new_quantity).where(Product.id == mi_product)
    return f"{mi_query.execute()} row(s) updated."


def purchase_product(product_id, buyer_id, quantity):
    # Check if product does exist
    mi_product = Product.get_or_none(Product.id == product_id)
    if mi_product is None:
        return "Product does not exist!"
    # Does user-id exist
    mi_user = User.get_or_none(User.id == buyer_id)
    if mi_user is None:
        return "User does not exist!"
    if type(quantity) != int:
        return "Quantity must be an integer!"
    # Does quantity exceed amount in stock
    mi_stock = mi_product.amount_in_stock
    mi_price = mi_product.price_in_cents * quantity
    mi_payment_method = mi_user.payment_method
    if quantity > mi_stock:
        return "Not enough in stock!"
    mi_query = Transaction.create(
        product_id=product_id,
        user_id=buyer_id,
        amount=quantity,
        price_in_cents=mi_price,
        payment_method=mi_payment_method,
    )
    # Update stock
    new_stock = mi_stock - quantity
    update_stock(product_id, new_stock)
    return f"Row {mi_query} is added to tansactions and stock is updated."


def remove_product(product_id):
    # If row doesn't exist, it can't be deleted.
    mi_product = Product.get_or_none(Product.id == product_id)
    if mi_product is None:
        return "Product does not exist!"
    mi_row = mi_product.delete_instance()
    return f"{mi_row} product(s) deleted."


if __name__ == "__main__":
    db.connect()
    # populate_test_database()
    # print(search("pAinted prhoes"))
    # print(list_user_products(3))
    # print(list_products_per_tag(2))
    # print(add_product_to_catalog(3, "Scarf Ring"))
    # print(update_stock(2, 4))
    # print(purchase_product(3, 2, 5))
    # print(remove_product(3))
    # db.close()
