# HiBob attendance reference for Codex

Instructions for reading and updating your HiBob attendance through Codex, using a browser request copied as cURL as the session input. This repository contains documentation only. The local Python helper is excluded from Git.

The local `hibob_attendance.py` helper reads attendance only. Earlier entry corrections were executed by Codex with a separate Python `urllib` POST request, equivalent to a cURL POST. They were not updates performed by that helper.

## Session input and logout

1. Sign in to `https://app.hibob.com` through your normal company login, including SSO.
2. Open Developer Tools → Network → Fetch/XHR, then open Attendance.
3. Select a successful request to `https://app.hibob.com/api/...` and choose **Copy as cURL**. Font, image, and `data:` requests do not provide the required session.
4. Save the request locally under the ignored `captures/` directory. Give Codex its file path and the specific attendance operation you want. Prefer local input over pasting credentials into chat.
5. Have Codex inspect the method, URL, and body, then extract the Cookie header value from `-b` / `--cookie` into `.hibob_session`. Keep the `hibob` cookie and only the additional application or Cloudflare cookies needed for access. Store the secret with permissions `0600`; never print it or include it in commits.
6. Have Codex read current HiBob state, perform the explicitly requested operation, and read back the results.
7. **Logging out of HiBob is the user's responsibility. Codex must not log out automatically.** The user should log out when the task session is finished and remove `.hibob_session` and the credential capture when no longer needed. Future tasks require a fresh session.

A copied request may change data. Codex should inspect its operation before executing it. A JWT expiry date alone does not prove that the server still accepts the session.

Example Codex request:

> Read captures/session-request.txt. Extract the required HiBob cookies into .hibob_session with permissions 0600, without printing them. Show the current month's attendance as a table. Keep credentials and personal attendance data out of Git. Remind me to log out when finished.

## Common request settings

Base URL: `https://app.hibob.com`.

Use the session Cookie header, `Accept: application/json`, and `Content-Type: application/json;charset=UTF-8` for JSON bodies. Captured web requests also use `X-Requested-With: XMLHttpRequest` and the Attendance page as their Referer. Use the current browser's `bob-timezoneoffset`: minutes west of UTC (Europe/Madrid is `-120` in summer and `-60` in winter).

Resolve the signed-in employee ID from the session or `GET /api/user`. All examples below use placeholders. Replace numeric ID placeholders with actual numbers obtained from HiBob.

These private web API routes depend on the current application and account permissions. HTTP 401/403 requires checking the session and permissions. For HTTP 404, inspect the actual Attendance network request before changing endpoints.

## Read a month of attendance

### Find the cycle

```text
GET /api/attendance/employees/{employeeId}/timesheets
```

The response contains `employeeTimesheets[]`, including `id`, `cycleStartDate`, `cycleEndDate`, and `timesheetState`. Select cycles overlapping the requested month. The current cycle uses ID `0`; historical cycles use their returned IDs. Default to the current month/year in Europe/Madrid. If HiBob does not expose the requested cycle, report that it is unavailable.

### Read report preferences

```text
GET /api/user/prefs/time_attendance_employee_timesheet
```

`configuration.fields` lists the configured report columns. This endpoint provides preferences, not daily attendance records.

### Search the daily report

```text
POST /api/company/views/search?idsOnly=false
```

This POST reads report data. Example JSON body:

```json
{
  "instructions": [
    {"values": ["Active"], "operator": "text_equals", "fieldPath": "/internal/status"}
  ],
  "sortBy": "/root/displayName",
  "fields": [
    "/time_attendance_employee_timesheet/alerts",
    "/time_attendance_employee_timesheet/date",
    "/time_attendance_employee_timesheet/holidayOrNonWorkingDay",
    "/time_attendance_employee_timesheet/hoursWorked",
    "/time_attendance_employee_timesheet/entryDisplay",
    "/time_attendance_employee_timesheet/entries"
  ],
  "employeeId": "<EMPLOYEE_ID>",
  "timesheetId": 0,
  "type": "time_attendance_employee_timesheet"
}
```

Rows are in `employees[]`. Skip weekly summary rows where `isSummary` is true. Filter the requested month using each day's `dateKey`, then sort newest first. The nested `time_attendance_employee_timesheet` object contains:

| Field | Table use |
| --- | --- |
| `alerts` | Count of alerts in the array |
| `date` | Date display text |
| `holidayOrNonWorkingDay` | HiBob's holiday/non-working-day label |
| `hoursWorked` | Worked time display |
| `entryDisplay` | Overall clock-time display |
| `entries` | Individual intervals, IDs, comments, reasons, and project tracking |

Use actual returned rows and labels. Do not infer non-working days from weekdays or invent future entries. `entryDisplay` can span several intervals; inspect `entries` to see a split shift or gaps.

## Update attendance entries

Require an explicit instruction naming dates, desired intervals, and project. For this workflow, always use **Teleworking**. Resolve its project ID from existing entries or available projects; do not hard-code a personal ID into the repository.

Example Codex request:

> Update existing October workdays to 08:00–14:00 and 15:00–17:00 on Teleworking. Read current entries and timesheet state first. Preserve comments and reasons, save a local backup, skip days already matching, then read back and verify each individual interval and project.

### Full-day update

```text
POST /api/attendance/employees/{employeeId}/attendance/entries?forDate=YYYY-MM-DD
```

**The body is the full day's entry list, not a partial patch.** Preserve retained IDs and account for existing work and break entries before writing. Omit the ID for a new interval. Preserve reasons, comments, and the intended project. Do not create work on empty days, holidays, or dates outside the requested scope unless explicitly requested.

Example body for retaining one work entry and adding a second:

```json
[
  {
    "id": "<EXISTING_ENTRY_ID>",
    "start": "YYYY-MM-DDT08:00",
    "end": "YYYY-MM-DDT14:00",
    "reason": null,
    "comment": null,
    "entryType": "work",
    "projectId": "<TELEWORKING_PROJECT_ID>",
    "reportingMethod": "startEnd",
    "offset": -120
  },
  {
    "start": "YYYY-MM-DDT15:00",
    "end": "YYYY-MM-DDT17:00",
    "reason": null,
    "comment": null,
    "entryType": "work",
    "projectId": "<TELEWORKING_PROJECT_ID>",
    "reportingMethod": "startEnd",
    "offset": -120
  }
]
```

Replace date and ID placeholders. The `null` reason/comment values are examples; preserve original values when present. Times are local wall-clock values without a UTC suffix. Calculate each entry's `offset` for its date in Europe/Madrid, including daylight-saving changes. If both intervals already exist, preserve both IDs. If other entries exist, inspect them and construct the complete intended list.

Check timesheet lock state and editing rights before writing. Save original rows in an ignored local backup with permissions `0600`. After each write, read the report again and verify individual start/end times, project IDs, and worked hours. HTTP success alone is insufficient. If a request has an uncertain result, read back before deciding whether to retry.

## BetterBob reference and Git hygiene

[BetterBob's client](https://github.com/kevinhufnagl/betterbob/blob/d2c466ec7f6a40c3c4aab7b2974aeccb2f501dc1/Packages/BetterBobShared/Sources/BetterBobShared/Services/BobClient.swift) is the reference for the report and full-day update routes. Its [endpoint notes](https://github.com/kevinhufnagl/betterbob/blob/d2c466ec7f6a40c3c4aab7b2974aeccb2f501dc1/Docs/endpoints.md) describe the private API. Codex can implement requests using cURL or Python's standard library; this repository does not include an executable client or install BetterBob.

Commit documentation only. `.gitignore` excludes the local Python helper, sessions, credential captures, attendance backups/exports, environment files, and Python caches. Inspect staged files before pushing; never commit Cookie headers, session JWTs, personal attendance records, or backups. Logout is the user's responsibility; Codex may remind the user but must not log out automatically.
