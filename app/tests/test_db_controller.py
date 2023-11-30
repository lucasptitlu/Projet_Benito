from faker import Faker
from pytest import fixture
from app.Database.clients import Clients

faker = Faker()


@fixture
def name():
    return faker.name()


@fixture
def email():
    return faker.email()


@fixture
def bonito():
    return faker.pyint()


@fixture
def balance():
    return faker.pyint()


def test_with_real_db_connection(faker, name, email, bonito, balance):
    bd = Clients()

    # print(bd.get_entry_by_id(2))
    print(bd.get_all_table())
    bd.add_client(name, email, bonito, balance)
    all_db = bd.get_all_table()

    assert all_db is not None
    assert name == all_db[-1].get("name")
