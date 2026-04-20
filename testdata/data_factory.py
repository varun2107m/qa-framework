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
