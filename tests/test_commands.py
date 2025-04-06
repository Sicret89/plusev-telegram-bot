from main import user_data, get_user_data

def setup_function():
    user_data.clear()  # clear shared state before each test

def test_get_user_data_creates_new_user():
    user = get_user_data(12345)
    assert user["balance"] == 0.0
    assert user["debt"] == 0.0
    assert user["max_debt"] == 100.0

def test_get_user_data_returns_existing_user():
    get_user_data(12345)["balance"] = 42
    user = get_user_data(12345)
    assert user["balance"] == 42