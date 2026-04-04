#!/usr/bin/env python3
"""Organize daily report-style summaries from ChatGPT export conversations.json."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "從 ChatGPT conversations.json 擷取最近 N 個月的每日紀錄，並輸出 Markdown/CSV。"
        )
    )
    parser.add_argument("input", type=Path, help="conversations.json 路徑")
    parser.add_argument(
        "--months", type=int, default=6, help="回溯月份數（預設 6）"
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default=dt.date.today().isoformat(),
        help="結束日期 YYYY-MM-DD（預設今天）",
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=Path("daily_reports_last_6_months.md"),
        help="Markdown 輸出檔名",
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=Path("daily_reports_last_6_months.csv"),
        help="CSV 輸出檔名",
    )
    return parser.parse_args()


def _extract_text(content: Dict[str, Any]) -> str:
    parts = content.get("parts") or []
    text_segments: List[str] = []
    for part in parts:
        if isinstance(part, str):
            text_segments.append(part)
        elif isinstance(part, dict):
            candidate = part.get("text")
            if isinstance(candidate, str):
                text_segments.append(candidate)
    joined = "\n".join([seg.strip() for seg in text_segments if seg and seg.strip()])
    if not joined:
        return ""
    return joined[:180]


def _safe_timestamp(value: Any) -> Optional[dt.datetime]:
    if value is None:
        return None
    try:
        ts = float(value)
        return dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc)
    except (TypeError, ValueError, OSError):
        return None


def _latest_assistant_preview(mapping: Dict[str, Any]) -> str:
    latest_time: Optional[dt.datetime] = None
    latest_preview = ""

    for node in mapping.values():
        message = node.get("message") if isinstance(node, dict) else None
        if not isinstance(message, dict):
            continue

        author = message.get("author") or {}
        role = author.get("role") if isinstance(author, dict) else None
        content = message.get("content") or {}
        create_time = _safe_timestamp(message.get("create_time"))
        if role != "assistant" or not create_time:
            continue

        preview = _extract_text(content)
        if not preview:
            continue

        if latest_time is None or create_time > latest_time:
            latest_time = create_time
            latest_preview = preview

    return latest_preview


def load_records(conversations: Iterable[Dict[str, Any]]) -> List[Dict[str, str]]:
    records: List[Dict[str, str]] = []

    for conv in conversations:
        create_time = _safe_timestamp(conv.get("create_time"))
        if not create_time:
            continue

        title = str(conv.get("title") or "(untitled)").strip()
        mapping = conv.get("mapping") if isinstance(conv.get("mapping"), dict) else {}
        preview = _latest_assistant_preview(mapping)

        records.append(
            {
                "date": create_time.date().isoformat(),
                "datetime_utc": create_time.isoformat(),
                "title": title,
                "preview": preview,
            }
        )

    records.sort(key=lambda x: x["datetime_utc"])
    return records


def filter_records(
    records: List[Dict[str, str]], end_date: dt.date, months: int
) -> List[Dict[str, str]]:
    start_date = end_date - dt.timedelta(days=months * 31)
    return [r for r in records if start_date <= dt.date.fromisoformat(r["date"]) <= end_date]


def write_csv(records: List[Dict[str, str]], output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=["date", "datetime_utc", "title", "preview"])
        writer.writeheader()
        writer.writerows(records)


def write_markdown(records: List[Dict[str, str]], output_path: Path, months: int) -> None:
    grouped: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for rec in records:
        grouped[rec["date"]].append(rec)

    lines: List[str] = [
        f"# ChatGPT 每日報表（最近 {months} 個月）",
        "",
        f"共 {len(records)} 筆對話紀錄",
        "",
    ]

    for day in sorted(grouped.keys()):
        lines.append(f"## {day}")
        for idx, rec in enumerate(grouped[day], start=1):
            title = rec["title"]
            preview = rec["preview"] or "(無 assistant 摘要內容)"
            lines.append(f"{idx}. **{title}**")
            lines.append(f"   - 摘要：{preview}")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    end_date = dt.date.fromisoformat(args.end_date)

    data = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("conversations.json 格式錯誤：預期最外層是 list")

    all_records = load_records(data)
    filtered = filter_records(all_records, end_date=end_date, months=args.months)

    write_csv(filtered, args.csv_output)
    write_markdown(filtered, args.markdown_output, args.months)

    print(
        f"完成：{len(filtered)} 筆，CSV -> {args.csv_output}，Markdown -> {args.markdown_output}"
    )


if __name__ == "__main__":
    main()
