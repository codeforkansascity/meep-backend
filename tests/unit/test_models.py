

def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hash are defined correctly
    """
    assert new_user.email == 'evan@aol.com'