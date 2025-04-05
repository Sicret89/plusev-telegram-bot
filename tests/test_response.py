from main import handle_response

def test_handle_response_hello():
    assert handle_response("hello") == "Hi there!"

def test_handle_response_unknown():
    assert handle_response("unknown_message") == "I do not understand what do you want..."