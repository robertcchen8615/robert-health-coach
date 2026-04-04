import datetime as dt

from scripts.organize_chatgpt_daily_reports import filter_records, load_records


def test_load_records_extracts_basic_fields():
    conversations = [
        {
            "title": "Daily Check-in",
            "create_time": 1712275200,
            "mapping": {
                "node-1": {
                    "message": {
                        "author": {"role": "assistant"},
                        "create_time": 1712275300,
                        "content": {"parts": ["今日飲食控制不錯，繼續保持。"]},
                    }
                }
            },
        }
    ]

    records = load_records(conversations)

    assert len(records) == 1
    assert records[0]["date"] == "2024-04-05"
    assert records[0]["title"] == "Daily Check-in"
    assert "今日飲食控制不錯" in records[0]["preview"]


def test_filter_records_by_six_month_window():
    records = [
        {"date": "2025-08-01", "datetime_utc": "2025-08-01T00:00:00+00:00", "title": "A", "preview": ""},
        {"date": "2026-02-01", "datetime_utc": "2026-02-01T00:00:00+00:00", "title": "B", "preview": ""},
        {"date": "2026-04-04", "datetime_utc": "2026-04-04T00:00:00+00:00", "title": "C", "preview": ""},
    ]

    result = filter_records(records, end_date=dt.date(2026, 4, 4), months=6)

    titles = [r["title"] for r in result]
    assert "A" not in titles
    assert "B" in titles
    assert "C" in titles
