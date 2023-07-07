import fastapi
import mongodb

# Create a database connection
client = mongodb.MongoClient()
db = client.my_database

# Create a product model
class Product(mongodb.Document):
    name = mongodb.StringField()
    price = mongodb.FloatField()
    available_quantity = mongodb.IntField()

# Create an order model
class Order(mongodb.Document):
    timestamp = mongodb.DateTimeField()
    items = mongodb.ListField(
        mongodb.EmbeddedDocumentField(
            "Item",
            fields={
                "productId": mongodb.IntField(),
                "boughtQuantity": mongodb.IntField(),
                "totalAmount": mongodb.FloatField(),
            },
        ),
    )
    user_address = mongodb.EmbeddedDocumentField(
        "UserAddress",
        fields={
            "city": mongodb.StringField(),
            "country": mongodb.StringField(),
            "zipCode": mongodb.StringField(),
        },
    )

# Create a router
router = fastapi.APIRouter()

# API to list all available products
@router.get("/products")
def list_products():
    products = db.products.find()
    return products

# API to create a new order
@router.post("/orders")
def create_order(order: Order):
    db.orders.insert_one(order)
    return order

# API to fetch all orders from the system
@router.get("/orders")
def list_orders(limit: int = 10, offset: int = 0):
    orders = db.orders.find().skip(offset).limit(limit)
    return orders

# API to fetch a single order from the system using Order ID
@router.get("/orders/{order_id}")
def get_order(order_id: int):
    order = db.orders.find_one({"_id": order_id})
    return order

# API to update a product when updating the available quantity for the product
@router.put("/products/{product_id}")
def update_product(product_id: int, available_quantity: int):
    product = db.products.find_one({"_id": product_id})
    product["available_quantity"] = available_quantity
    db.products.save(product)
    return product

# Run the API
app = fastapi.FastAPI()
app.include_router(router)

if __name__ == "__main__":
    app.run(debug=True)
