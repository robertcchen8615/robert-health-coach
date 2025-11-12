from integrations.line_adapter import handle_line_event


def test_handle_line_event_basic():
    sample_event = {
        "user_id": "U123",
        "message": "generate diet",
        "replyToken": "TEST_TOKEN",
        "profile": {"calories": 2000, "name": "Tester", "preferences": ["vegan"]},
    }
    reply = handle_line_event(sample_event)
    assert isinstance(reply, dict)
    assert reply.get("replyToken") == "TEST_TOKEN"
    messages = reply.get("messages")
    assert isinstance(messages, list)
    assert len(messages) == 1
    assert messages[0]["type"] == "text"
    assert "每日總熱量" in messages[0]["text"] or "calories" in messages[0]["text"]
