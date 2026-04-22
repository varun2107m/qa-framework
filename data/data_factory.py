from faker import Faker
import random


class DataFactory:
    def __init__(self, seed=None):
        """
        If seed is provided → deterministic data
        If not → random data
        """
        self.fake = Faker()

        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)

    def get_user_data(self, overrides=None):
        data = {
            "username": self.fake.user_name(),
            "password": self.fake.password()
        }

        if overrides:
            data.update(overrides)

        return data

    def get_checkout_data(self, overrides=None):
        data = {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "postal_code": self.fake.postcode()
        }

        if overrides:
            data.update(overrides)

        return data


# -------- Convenience functions (for backward compatibility) -------- #

def get_user_data(seed=None, overrides=None):
    return DataFactory(seed).get_user_data(overrides)


def get_checkout_data(seed=None, overrides=None):
    return DataFactory(seed).get_checkout_data(overrides)

