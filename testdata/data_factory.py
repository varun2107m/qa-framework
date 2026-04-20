from faker import Faker
import random
 
fake = Faker()
 
 
def get_user_data():
    Faker.seed(123)
    random.seed(123)
    return {
        "username": fake.user_name(),
        "password": fake.password()
    }
 
 
def get_checkout_data():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "postal_code": fake.postcode()
    }
