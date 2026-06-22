import uuid
from faker import Faker
from api.account_api import UserData

fake = Faker()


def generate_unique_user() -> UserData:

    unique_suffix = uuid.uuid4().hex[:8]

    return UserData(
        name=fake.first_name(),
        email=f"qa.auto.{unique_suffix}@example.com",
        password=fake.password(length=12),
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        company=fake.company(),
        address1=fake.street_address(),
        address2=fake.secondary_address(),
        zipcode=fake.postcode(),
        city=fake.city(),
        mobile_number=fake.msisdn()[:10],
    )
