# Update HiBob time attendance

This repository documents how to inspect and update attendance using an authenticated HiBob cURL request supplied by the user. `hibob.py` validates the local `curl.secret`, shows a status table, lists projects, and can fill explicitly pending days when asked with `--action fill-time-attendance`.

See the [API reference](reference/api/README.md) for endpoint paths and observed request/response formats from the local HAR capture.

## Provide the request

1. Sign in to HiBob and open **Attendance**.
2. In browser Developer Tools, open **Network → Fetch/XHR** and select a successful attendance API request. Choose **Copy as cURL**. Do not use font, image, or `data:` requests.
3. Save the copied cURL locally as `curl.secret`, set private permissions with `chmod 600 curl.secret`, then run `python3 hibob.py`. The script checks the token expiry and validates the session against HiBob before making requests. It never replays the copied request or prints credentials. Keep `curl.secret` private; it is excluded from Git.
4. The default action is `show`, which prints only the month table without prompting. Use `--month` with a month number from 1 to 12 to choose a month in the current year. If omitted, the script shows the previous month on days 1–5 and the current month otherwise. Use `--action show-projects` to print the available attendance projects as a table. For example:

   ```sh
   python3 hibob.py --action show
   python3 hibob.py --month 10 --action show
   python3 hibob.py --action show-projects
   python3 hibob.py --action fill-time-attendance --value "08:00 - 14:00, 15:00 - 17:00"
   python3 hibob.py --action fill-time-attendance --month 10 --value "8-14,15-17"
   ```

   The table marks dates as `FILLED`, `PENDING`, or `NON-WORKING`. `NO DATA` means HiBob did not return a daily row, so the script does not guess its status.
5. For a manual attendance change, state the exact dates, desired intervals, and project. The fill action instead applies the supplied intervals to every pending, reportable date through yesterday in the selected month, using Teleworking.

`--value` accepts comma-separated 24-hour intervals in either `HH:MM - HH:MM` or `H-H` form; omitted minutes mean `:00`. The fill action resolves **Teleworking** from the live project list. It writes only dates through yesterday that HiBob reports as `PENDING`, skips filled days, weekends, holidays, time off, today, future dates, and dates with no report row, and checks the timesheet is open before writing. It backs up the target rows under the ignored `backups/` directory, rereads each date before updating it, and verifies the saved intervals and project afterward. This action changes attendance in HiBob.

The copied cURL supplies the request details and authenticated session context. Codex must inspect its method, URL, headers, and body before using it. A copied request may itself change data; never replay it blindly. Use the timezone offset from the current request/session for each target date, accounting for daylight-saving changes. Keep cookies and tokens private, and do not print or commit them.

## Update safely

1. Use the supplied request to identify the signed-in employee and the applicable attendance API. Read the current attendance entries and timesheet state before writing. If the request does not expose enough information, inspect the relevant attendance request in the browser rather than guessing an endpoint or employee ID.
2. Confirm the timesheet is editable. Resolve the requested project from HiBob data; do not guess or hard-code a project ID. Run `python3 hibob.py --action show-projects` to print each available project's name and ID. The command calls:

   ```text
   GET /api/attendance/employees/{employeeId}/projects?includeArchivedTasks=false
   ```

   Select the matching project (for example, **Teleworking**) and use its ID as `projectId` in the attendance-entry body. Do not replay a copied request if it has a request body or otherwise changes data.
3. For an attendance-entry update, treat the day's entry list as a whole. Preserve existing entry IDs, comments, reasons, breaks, and other entries that should remain. Include every intended entry in the update; omit an ID only for a new entry. Do not create entries on dates outside the user's request.
4. Save a local backup of the original entries in the ignored `backups/` directory before writing.
5. After each update, read attendance again and verify every requested date, interval, project, and worked-hours value. An HTTP success response alone does not verify the change. If the result is uncertain, read back before retrying.

## Security and session cleanup

The `.gitignore` excludes local cURL captures, session files, backups, and exports. Keep them out of commits and inspect staged files before committing. Remove local session and capture files when no longer needed. Logging out of HiBob is the user's responsibility; Codex may remind the user but must not log out automatically.

Example request to Codex:

> Use the HiBob XHR cURL I pasted to inspect current attendance. Update [dates] to [times/intervals] on [project]. Preserve already-filled days and skip weekends and holidays. Save a local backup before writing, then read back and verify each changed date. Keep credentials and attendance data out of Git.
