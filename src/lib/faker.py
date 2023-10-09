from faker import Faker

# Unique faker instance
_fake = Faker()


# Helper functions
def fake_username() -> str:
    return _fake.unique.user_name()


def fake_password() -> str:
    return _fake.password()
