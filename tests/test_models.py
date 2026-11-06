import pytest
import models

def test_user_set_password_behaves_correctly():
    # Adding arrangements (setting the data)
    user = models.User(username="user1")
    user.set_password("test123")
    # Asserts and testing
    assert user.check_password("test12") == True


def test_user_password_hashing_behaves_correctly():
    # Adding arrangements (setting the data)
    user = models.User(username="user1")
    user.set_password("test123")

    # Asserts and testing
    assert user.password_hash != "test123"


