#!/usr/bin/env python3
"""Show or fill daily attendance for a selected month in HiBob.

Reads the authenticated cURL from the private curl.secret file, validates the
session with HiBob, and reads attendance data. Filling attendance writes only
dates that HiBob explicitly reports as pending unless overwrite is requested.
"""

from __future__ import annotations

import argparse
import base64
import calendar
import json
import os
import re
import shlex
import stat
import sys
import time
from datetime import date, datetime, timedelta
from http.cookiejar import Cookie, CookieJar
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPCookieProcessor, Request, build_opener
from zoneinfo import ZoneInfo


BASE_URL = "https://app.hibob.com/api"
CURL_FILE = Path(__file__).with_name("curl.secret")
TIMEZONE = ZoneInfo("Europe/Madrid")
REPORT_TYPE = "time_attendance_employee_timesheet"
REQUIRED_REPORT_FIELDS = (
    "alerts",
    "date",
    "holidayOrNonWorkingDay",
    "hoursWorked",
    "entryDisplay",
    "entryStatus",
    "entries",
    "timeOff",
    "timeOffEntries",
)
TIME_INTERVAL_PATTERN = re.compile(r"^\s*(\d{1,2})(?::([0-5]\d))?\s*-\s*(\d{1,2})(?::([0-5]\d))?\s*$")


class InputError(ValueError):
    """Raised when curl.secret is missing or is not a usable HiBob request."""


def read_curl_file() -> str:
    if not CURL_FILE.is_file():
        raise InputError(f"Required cURL file not found: {CURL_FILE}")
    if not os.access(CURL_FILE, os.R_OK):
        raise InputError(f"Cannot read {CURL_FILE}; check its permissions.")
    if os.name == "posix" and stat.S_IMODE(CURL_FILE.stat().st_mode) & 0o077:
        raise InputError(f"{CURL_FILE} must be private; run chmod 600 {CURL_FILE}.")
    try:
        content = CURL_FILE.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        raise InputError(f"Could not read {CURL_FILE} as UTF-8 text.") from None
    if not content.strip():
        raise InputError(f"{CURL_FILE} is empty.")
    return content


def parse_curl(content: str) -> tuple[dict[str, str], dict[str, str], str, int]:
    try:
        tokens = shlex.split(content, posix=True)
    except ValueError as exc:
        raise InputError(f"Could not parse {CURL_FILE.name}: {exc}") from None
    if not tokens or tokens[0].rsplit("/", 1)[-1] not in {"curl", "curl.exe"}:
        raise InputError(f"{CURL_FILE.name} must contain a copied curl command.")

    cookies: dict[str, str] = {}
    headers: dict[str, str] = {}
    target_url = ""
    index = 1
    while index < len(tokens):
        option = tokens[index]
        index += 1

        if option.startswith("https://") and not target_url:
            target_url = option
            continue

        if option in ("--url", "-b", "--cookie", "-H", "--header"):
            if index >= len(tokens):
                raise InputError(f"Missing value after {option} in {CURL_FILE.name}.")
            value = tokens[index]
            index += 1
        elif option.startswith("--url="):
            value, option = option.partition("=")[2], "--url"
        elif option.startswith("--cookie="):
            value, option = option.partition("=")[2], "--cookie"
        elif option.startswith("--header="):
            value, option = option.partition("=")[2], "--header"
        elif option.startswith("-b") and option != "-b":
            value, option = option[2:], "-b"
        elif option.startswith("-H") and option != "-H":
            value, option = option[2:], "-H"
        else:
            # The captured method/body are deliberately ignored; this script
            # never replays the user's request.
            continue

        if option == "--url":
            target_url = value
        elif option in ("-b", "--cookie"):
            add_cookie_pairs(cookies, value)
        else:
            name, separator, header_value = value.partition(":")
            if separator:
                normalized_name = name.strip().lower()
                headers[normalized_name] = header_value.strip()
                if normalized_name == "cookie":
                    add_cookie_pairs(cookies, header_value)

    parsed_url = urlsplit(target_url)
    if parsed_url.scheme != "https" or parsed_url.hostname != "app.hibob.com":
        raise InputError("The cURL URL must use https://app.hibob.com.")
    if not parsed_url.path.startswith("/api/"):
        raise InputError("The cURL URL must point to a HiBob /api/ XHR request.")
    if "hibob" not in cookies:
        raise InputError("The cURL must include a HiBob 'hibob' session cookie.")
    if "bob-timezoneoffset" not in headers:
        raise InputError("The cURL must include bob-timezoneoffset for attendance dates.")
    try:
        timezone_offset = int(headers["bob-timezoneoffset"])
    except ValueError:
        raise InputError("bob-timezoneoffset must be an integer number of minutes.") from None

    claims = decode_session_claims(cookies["hibob"])
    employee_id = str(claims.get("employeeId", ""))
    expiry = claims.get("exp")
    if not employee_id.isdigit():
        raise InputError("The session cookie does not contain a numeric employee ID.")
    if not isinstance(expiry, (int, float)) or expiry <= time.time():
        raise InputError("The session token is expired or has no valid expiry; capture a fresh cURL.")
    return headers, cookies, employee_id, timezone_offset


def add_cookie_pairs(cookies: dict[str, str], raw: str) -> None:
    for part in raw.split(";"):
        name, separator, value = part.strip().partition("=")
        if separator and name:
            cookies[name] = value.strip()


def decode_session_claims(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise InputError("The HiBob session cookie is not a JWT.")
    payload = parts[1]
    payload += "=" * (-len(payload) % 4)
    try:
        claims = json.loads(base64.urlsafe_b64decode(payload.encode("ascii")))
    except (ValueError, UnicodeError, json.JSONDecodeError):
        raise InputError("Could not read the session token claims.") from None
    if not isinstance(claims, dict):
        raise InputError("The session token claims are not a JSON object.")
    return claims


def cookie_jar(cookie_values: dict[str, str]) -> CookieJar:
    jar = CookieJar()
    for name, value in cookie_values.items():
        jar.set_cookie(
            Cookie(
                version=0,
                name=name,
                value=value,
                port=None,
                port_specified=False,
                domain="app.hibob.com",
                domain_specified=False,
                domain_initial_dot=False,
                path="/",
                path_specified=True,
                secure=True,
                expires=None,
                discard=True,
                comment=None,
                comment_url=None,
                rest={"HttpOnly": None},
                rfc2109=False,
            )
        )
    return jar


def build_client(headers: dict[str, str], cookies: dict[str, str]):
    request_headers = {
        "Accept": headers.get("accept", "application/json, text/plain, */*"),
        "Referer": headers.get("referer", "https://app.hibob.com/attendance/my-attendance"),
        "User-Agent": headers.get("user-agent", "Mozilla/5.0"),
        "X-Requested-With": "XMLHttpRequest",
        "bob-timezoneoffset": headers["bob-timezoneoffset"],
    }
    if "accept-language" in headers:
        request_headers["Accept-Language"] = headers["accept-language"]
    if "origin" in headers:
        request_headers["Origin"] = headers["origin"]
    return build_opener(HTTPCookieProcessor(cookie_jar(cookies))), request_headers


def request_json(opener, request_headers, path: str, body: dict | list | None = None):
    headers = dict(request_headers)
    data = None
    method = "GET"
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json;charset=UTF-8"
        method = "POST"
    request = Request(f"{BASE_URL}/{path.lstrip('/')}", data=data, headers=headers, method=method)
    try:
        with opener.open(request, timeout=30) as response:
            response_body = response.read()
            # HiBob's attendance-entry endpoint can accept a write with an
            # empty success body. The caller verifies the resulting state by
            # reading the report back before it treats the write as complete.
            if method == "POST" and not response_body.strip():
                return None
            return json.loads(response_body.decode("utf-8"))
    except HTTPError as exc:
        if exc.code in (401, 403):
            raise RuntimeError(
                f"HiBob returned HTTP {exc.code}; curl.secret is expired or not authorized. "
                "Capture a fresh Attendance XHR cURL."
            ) from None
        raise RuntimeError(f"HiBob returned HTTP {exc.code} for /api/{path}.") from None
    except URLError as exc:
        raise RuntimeError(f"Could not connect to HiBob: {exc.reason}") from None
    except (UnicodeError, json.JSONDecodeError):
        raise RuntimeError("HiBob returned non-JSON data; the request may have redirected to login.") from None


def validate_session(opener, request_headers, employee_id: str) -> None:
    user = request_json(opener, request_headers, "user")
    if not isinstance(user, dict) or str(user.get("id", "")) != employee_id:
        raise RuntimeError(
            "The authenticated user does not match the employee in the session token; "
            "capture a fresh cURL while signed in as the intended user."
        )


def fetch_projects(opener, request_headers, employee_id: str) -> list[dict]:
    result = request_json(
        opener,
        request_headers,
        f"attendance/employees/{employee_id}/projects?includeArchivedTasks=false",
    )
    projects = result.get("results") if isinstance(result, dict) else None
    if not isinstance(projects, list):
        raise RuntimeError("HiBob's projects response did not contain a results list.")
    return [project for project in projects if isinstance(project, dict)]


def default_month(today: date) -> tuple[int, int]:
    first_day = today.replace(day=1)
    if today.day <= 5:
        first_day -= timedelta(days=1)
    return first_day.year, first_day.month


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Show daily attendance status from a current HiBob session."
    )
    parser.add_argument(
        "--month",
        type=int,
        choices=range(1, 13),
        metavar="1-12",
        help="month number to show; defaults to the current month, or the previous month on days 1–5",
    )
    parser.add_argument(
        "--action",
        choices=("show", "show-projects", "fill-time-attendance"),
        default="show",
        help="show attendance (default), list projects, or fill attendance days",
    )
    parser.add_argument(
        "--schedule",
        help='work intervals, e.g. "08:00 - 14:00, 15:00 - 17:00" or "8-14,15-17"',
    )
    parser.add_argument(
        "--break-schedule",
        help='break intervals, e.g. "14:00 - 15:00" or "14-15"',
    )
    parser.add_argument(
        "--project-id",
        help="attendance project ID (required when filling attendance)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="replace existing attendance entries throughout the selected month",
    )
    args = parser.parse_args()
    if args.action == "fill-time-attendance":
        if args.schedule is None:
            parser.error("--schedule is required with --action fill-time-attendance")
        if args.project_id is None:
            parser.error("--project-id is required with --action fill-time-attendance")
        try:
            args.intervals = parse_intervals(args.schedule)
            args.break_intervals = (
                parse_intervals(args.break_schedule, "--break-schedule")
                if args.break_schedule is not None
                else []
            )
        except InputError as exc:
            parser.error(str(exc))
    elif args.schedule is not None or args.break_schedule is not None or args.project_id is not None or args.overwrite:
        parser.error("--schedule, --break-schedule, --project-id, and --overwrite can only be used with --action fill-time-attendance")
    return args


def parse_intervals(value: str, option_name: str = "--schedule") -> list[tuple[str, str]]:
    """Parse comma-separated 24-hour intervals, accepting optional minutes."""
    if not value.strip():
        raise InputError(f"{option_name} must contain at least one interval, such as '8-14,15-17'.")
    intervals: list[tuple[int, int, str, str]] = []
    for part in value.split(","):
        match = TIME_INTERVAL_PATTERN.fullmatch(part)
        if not match:
            raise InputError(
                f"Invalid interval {part.strip()!r} in {option_name}. Use HH:MM - HH:MM or H-H, "
                "for example '08:00 - 14:00, 15:00 - 17:00' or '8-14,15-17'."
            )
        start_hour, start_minute, end_hour, end_minute = match.groups()
        start_h, start_m = int(start_hour), int(start_minute or 0)
        end_h, end_m = int(end_hour), int(end_minute or 0)
        if start_h > 23 or end_h > 23:
            raise InputError(f"Hours must be between 0 and 23: {part.strip()!r}.")
        start_total, end_total = start_h * 60 + start_m, end_h * 60 + end_m
        if start_total >= end_total:
            raise InputError(f"Each interval must end after it starts: {part.strip()!r}.")
        intervals.append((start_total, end_total, f"{start_h:02d}:{start_m:02d}", f"{end_h:02d}:{end_m:02d}"))

    intervals.sort()
    for previous, current in zip(intervals, intervals[1:]):
        if current[0] < previous[1]:
            raise InputError("Intervals must not overlap.")
    return [(start, end) for _start, _end, start, end in intervals]


def report_cycles(opener, request_headers, employee_id: str, year: int, month: int) -> list[dict]:
    timesheets = request_json(opener, request_headers, f"attendance/employees/{employee_id}/timesheets")
    cycles = timesheets.get("employeeTimesheets", []) if isinstance(timesheets, dict) else []
    last_day = calendar.monthrange(year, month)[1]
    month_start, month_end = date(year, month, 1), date(year, month, last_day)
    matching = []
    for cycle in cycles:
        try:
            cycle_start = date.fromisoformat(str(cycle["cycleStartDate"])[:10])
            cycle_end = date.fromisoformat(str(cycle["cycleEndDate"])[:10])
        except (KeyError, TypeError, ValueError):
            continue
        if cycle_start <= month_end and cycle_end >= month_start:
            matching.append(cycle)
    if not matching:
        raise RuntimeError(f"HiBob returned no timesheet cycle covering {year:04d}-{month:02d}.")
    return matching


def month_rows(opener, request_headers, employee_id: str, year: int, month: int) -> dict[date, dict]:
    prefs = request_json(opener, request_headers, "user/prefs/time_attendance_employee_timesheet")
    configured = prefs.get("configuration", {}).get("fields", []) if isinstance(prefs, dict) else []
    fields = list(dict.fromkeys(
        [field for field in configured if isinstance(field, str)]
        + [f"/{REPORT_TYPE}/{name}" for name in REQUIRED_REPORT_FIELDS]
    ))
    rows_by_date: dict[date, dict] = {}
    for cycle in report_cycles(opener, request_headers, employee_id, year, month):
        body = {
            "instructions": [
                {"values": ["Active"], "operator": "text_equals", "fieldPath": "/internal/status"}
            ],
            "sortBy": "/root/displayName",
            "fields": fields,
            "employeeId": employee_id,
            "timesheetId": cycle["id"],
            "type": REPORT_TYPE,
        }
        result = request_json(
            opener,
            request_headers,
            "company/views/search?idsOnly=false",
            body=body,
        )
        employees = result.get("employees", []) if isinstance(result, dict) else []
        for row in employees:
            if not isinstance(row, dict) or row.get("isSummary"):
                continue
            try:
                target = date.fromisoformat(str(row.get("dateKey", ""))[:10])
            except ValueError:
                continue
            if target.year == year and target.month == month:
                data = row.get(REPORT_TYPE)
                if isinstance(data, dict):
                    rows_by_date[target] = data
    if not rows_by_date:
        raise RuntimeError("HiBob returned no daily attendance rows for the selected month.")
    return rows_by_date


def has_entries(row: dict) -> bool:
    entries = row.get("entries")
    if isinstance(entries, list) and any(isinstance(entry, dict) for entry in entries):
        return True
    display = str(row.get("entryDisplay") or "").strip()
    if display:
        return True
    worked = str(row.get("hoursWorked") or "").strip().lower()
    return bool(worked and not re.fullmatch(r"0+(?:h\s*0+m)?", worked) and worked not in {"0h 00m", "0:00"})


def has_time_off(row: dict) -> bool:
    value = row.get("timeOff")
    entries = row.get("timeOffEntries")
    return bool(value) or (isinstance(entries, list) and bool(entries))


def entry_times(row: dict) -> str:
    intervals = []
    entries = row.get("entries")
    if isinstance(entries, list):
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            if str(entry.get("entryType", "work")).lower() in {"break", "rest"}:
                continue
            start, end = entry.get("start"), entry.get("end")
            if isinstance(start, str) and isinstance(end, str):
                intervals.append(f"{start[-5:]} - {end[-5:]}")
    return ", ".join(intervals) or str(row.get("entryDisplay") or "").strip()


def day_status(target: date, row: dict | None) -> tuple[str, str]:
    if row is None:
        if target.weekday() >= 5:
            return "NON-WORKING", "Weekend; no report row"
        return "NO DATA", "No report row; status not inferred"
    if has_entries(row):
        return "FILLED", entry_times(row)
    holiday = str(row.get("holidayOrNonWorkingDay") or "").strip()
    if holiday:
        return "NON-WORKING", holiday
    if target.weekday() >= 5:
        return "NON-WORKING", "Weekend"
    if has_time_off(row):
        return "NON-WORKING", "Time off"
    return "PENDING", ""


def render_table(rows: dict[date, dict], year: int, month: int) -> None:
    print(f"Attendance status — {calendar.month_name[month]} {year}")
    columns = ("Date", "Day", "Status", "Details")
    records = []
    for day_num in range(1, calendar.monthrange(year, month)[1] + 1):
        target = date(year, month, day_num)
        status, detail = day_status(target, rows.get(target))
        records.append((target.strftime("%Y-%m-%d"), target.strftime("%A"), status, detail))
    widths = [max(len(columns[i]), *(len(row[i]) for row in records)) for i in range(len(columns))]
    print(" | ".join(columns[i].ljust(widths[i]) for i in range(len(columns))))
    print("-+-".join("-" * width for width in widths))
    for record in records:
        print(" | ".join(record[i].ljust(widths[i]) for i in range(len(columns))))


def render_projects(projects: list[dict]) -> None:
    columns = ("Project", "ID")
    records = [
        (str(project.get("name") or "(unnamed)"), str(project.get("id", "unknown")))
        for project in sorted(projects, key=lambda item: str(item.get("name", "")).casefold())
    ]
    widths = [max(len(columns[i]), *(len(row[i]) for row in records)) for i in range(len(columns))]
    print(" | ".join(columns[i].ljust(widths[i]) for i in range(len(columns))))
    print("-+-".join("-" * width for width in widths))
    for record in records:
        print(" | ".join(record[i].ljust(widths[i]) for i in range(len(columns))))


def find_project(projects: list[dict], project_id: str) -> dict:
    for project in projects:
        if str(project.get("id", "")) == project_id:
            return project
    raise RuntimeError(f"Project ID {project_id!r} is not available for this employee.")


def cycle_for_date(cycles: list[dict], target: date) -> dict:
    for cycle in cycles:
        try:
            start = date.fromisoformat(str(cycle["cycleStartDate"])[:10])
            end = date.fromisoformat(str(cycle["cycleEndDate"])[:10])
        except (KeyError, TypeError, ValueError):
            continue
        if start <= target <= end:
            return cycle
    raise RuntimeError(f"No timesheet cycle covers {target.isoformat()}.")


def ensure_cycle_editable(cycle: dict, target: date) -> None:
    state = cycle.get("timesheetState")
    if not isinstance(state, dict):
        raise RuntimeError(f"HiBob did not provide an editable state for {target.isoformat()}; no entries written.")
    status = str(state.get("timeSheetStatus", "")).casefold()
    if state.get("locked") is not False or status != "open":
        raise RuntimeError(
            f"Timesheet for {target.isoformat()} is not confirmed open "
            f"(status={state.get('timeSheetStatus')!r}, locked={state.get('locked')!r}); no entries written."
        )


def create_backup(year: int, month: int, rows: dict[date, dict], targets: list[date]) -> Path:
    backup_dir = CURL_FILE.parent / "backups"
    backup_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    stamp = datetime.now(TIMEZONE).strftime("%Y%m%d-%H%M%S")
    backup_path = backup_dir / f"{year:04d}-{month:02d}-before-fill-{stamp}.json"
    backup_content = {
        "month": f"{year:04d}-{month:02d}",
        "dates": {
            target.isoformat(): rows[target]
            for target in targets
        },
    }
    descriptor = os.open(backup_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as backup_file:
        json.dump(backup_content, backup_file, ensure_ascii=False, indent=2)
        backup_file.write("\n")
    return backup_path


def attendance_payload(target: date, intervals: list[tuple[str, str]], project_id, offset: int,
                       break_intervals: list[tuple[str, str]] | None = None) -> list[dict]:
    payload = [
        {
            "start": f"{target.isoformat()}T{start}",
            "end": f"{target.isoformat()}T{end}",
            "reason": None,
            "comment": None,
            "entryType": "work",
            "projectId": project_id,
            "reportingMethod": "startEnd",
            "offset": offset,
        }
        for start, end in intervals
    ]
    payload.extend(
        {
            "id": None,
            "start": f"{target.isoformat()}T{start}",
            "end": f"{target.isoformat()}T{end}",
            "entryType": "break",
            "reportingMethod": "startEnd",
            "offset": offset,
        }
        for start, end in (break_intervals or [])
    )
    return payload


def date_offset(target: date) -> int:
    local_midnight = datetime(target.year, target.month, target.day, tzinfo=TIMEZONE)
    utc_offset = local_midnight.utcoffset()
    if utc_offset is None:
        raise RuntimeError(f"Could not determine timezone offset for {target.isoformat()}.")
    return -int(utc_offset.total_seconds() // 60)


def matches_intervals(row: dict | None, intervals: list[tuple[str, str]], project_id,
                      break_intervals: list[tuple[str, str]] | None = None) -> bool:
    if not row or not isinstance(row.get("entries"), list):
        return False
    actual = []
    actual_breaks = []
    for entry in row["entries"]:
        if not isinstance(entry, dict):
            continue
        entry_type = str(entry.get("entryType", "work")).casefold()
        if entry_type in {"break", "rest"}:
            if entry_type == "break":
                start, end = entry.get("start"), entry.get("end")
                if not isinstance(start, str) or not isinstance(end, str):
                    return False
                actual_breaks.append((start[-5:], end[-5:]))
            continue
        start, end = entry.get("start"), entry.get("end")
        if not isinstance(start, str) or not isinstance(end, str):
            return False
        project_tracking = entry.get("projectTracking")
        actual_project_id = entry.get("projectId")
        if actual_project_id is None and isinstance(project_tracking, dict):
            actual_project_id = project_tracking.get("projectId")
        if str(actual_project_id) != str(project_id):
            return False
        actual.append((start[-5:], end[-5:]))
    return actual == intervals and actual_breaks == (break_intervals or [])


def fill_month(opener, request_headers, employee_id: str, year: int, month: int,
               intervals: list[tuple[str, str]], requested_project_id: str,
               overwrite: bool = False,
               break_intervals: list[tuple[str, str]] | None = None) -> dict[date, dict]:
    cycles = report_cycles(opener, request_headers, employee_id, year, month)
    rows = month_rows(opener, request_headers, employee_id, year, month)
    projects = fetch_projects(opener, request_headers, employee_id)
    project = find_project(projects, requested_project_id)
    project_id = project["id"]
    project_name = str(project.get("name") or "(unnamed)")
    yesterday = datetime.now(TIMEZONE).date() - timedelta(days=1)
    days = [
        date(year, month, number)
        for number in range(1, calendar.monthrange(year, month)[1] + 1)
        if date(year, month, number) <= yesterday
    ]
    pending = [day for day in days if day_status(day, rows.get(day))[0] == "PENDING"]
    if overwrite:
        # Existing entries anywhere in the selected month are replaced. Pending
        # workdays through yesterday are filled as well, matching normal fill.
        month_days = [date(year, month, number) for number in range(1, calendar.monthrange(year, month)[1] + 1)]
        targets = [day for day in month_days if day_status(day, rows.get(day))[0] == "FILLED"]
        targets.extend(pending)
        targets = sorted(set(targets))
    else:
        targets = pending
    if not targets:
        message = "attendance entries to overwrite" if overwrite else "pending attendance days through yesterday"
        print(f"No {message} for {project_name}; no entries written.")
        return rows

    # Validate every target before the first write to avoid a partial fill when
    # the selected timesheet is locked or its state is unknown.
    target_cycles = {day: cycle_for_date(cycles, day) for day in targets}
    for day, cycle in target_cycles.items():
        ensure_cycle_editable(cycle, day)

    print(f"Using project: {project_name} (ID: {project_id})")
    backup_path = create_backup(year, month, rows, targets)
    print(f"Backup saved: {backup_path}")

    for target in targets:
        # Re-read immediately before each full-list update to avoid acting on
        # stale status and entries.
        latest_rows = month_rows(opener, request_headers, employee_id, year, month)
        latest = latest_rows.get(target)
        status, _detail = day_status(target, latest)
        allowed_statuses = {"PENDING", "FILLED"} if overwrite else {"PENDING"}
        if status not in allowed_statuses:
            print(f"Skipped {target.isoformat()}: status changed to {status}.")
            rows = latest_rows
            continue
        existing = latest.get("entries") if isinstance(latest, dict) else None
        if existing and not overwrite:
            print(f"Skipped {target.isoformat()}: entries appeared before the update.")
            rows = latest_rows
            continue

        offset = date_offset(target)
        payload = attendance_payload(target, intervals, project_id, offset, break_intervals)
        request_json(
            opener,
            request_headers,
            f"attendance/employees/{employee_id}/attendance/entries?forDate={target.isoformat()}",
            body=payload,
        )
        rows = month_rows(opener, request_headers, employee_id, year, month)
        if not matches_intervals(rows.get(target), intervals, project_id, break_intervals):
            raise RuntimeError(
                f"HiBob did not verify the requested work/break intervals and project for "
                f"{target.isoformat()}; stopped before writing additional dates."
            )
        break_summary = (
            f"; breaks {', '.join(f'{start}-{end}' for start, end in break_intervals)}"
            if break_intervals else ""
        )
        print(f"Filled and verified {target.isoformat()} on {project_name} "
              f"({', '.join(f'{start}-{end}' for start, end in intervals)}{break_summary}).")
    return rows


def main() -> int:
    args = parse_args()
    today = datetime.now(TIMEZONE).date()
    try:
        headers, cookies, employee_id, _timezone_offset = parse_curl(read_curl_file())
        opener, request_headers = build_client(headers, cookies)
        validate_session(opener, request_headers, employee_id)
        print("HiBob session: valid and active.")
        if args.action == "show-projects":
            projects = fetch_projects(opener, request_headers, employee_id)
            render_projects(projects)
        elif args.action == "fill-time-attendance":
            default_year, default_number = default_month(today)
            year, month = default_year, args.month if args.month is not None else default_number
            rows = fill_month(
                opener,
                request_headers,
                employee_id,
                year,
                month,
                args.intervals,
                args.project_id,
                args.overwrite,
                args.break_intervals,
            )
            render_table(rows, year, month)
        else:
            default_year, default_number = default_month(today)
            year, month = default_year, args.month if args.month is not None else default_number
            rows = month_rows(opener, request_headers, employee_id, year, month)
            render_table(rows, year, month)
    except InputError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
