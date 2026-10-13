# HiBob Attendance CLI

`hibob.py` is a command-line tool for viewing attendance, listing attendance projects, and filling pending attendance days in HiBob. It uses Python's standard library and a current HiBob browser session stored in the local `curl.secret` file.

## Requirements

- Python 3.10 or newer.
- An active HiBob session with access to Attendance.
- A successful Attendance XHR request copied from your browser as cURL.

Save the cURL command as `curl.secret` in this repository's root and restrict access to your account:

```sh
chmod 600 curl.secret
```

The script reads the cURL URL, headers, and cookies to authenticate its own requests. It does not replay the copied request or print its credentials. The session must still be valid on HiBob's servers; an unexpired token alone is not enough.

## Commands

Run these from the repository directory:

```sh
# Show the attendance table for the default month
python3 hibob.py

# Show a month number in the current year
python3 hibob.py --month 10

# List attendance projects and their IDs
python3 hibob.py --action show-projects

# Fill pending days through yesterday with split intervals
python3 hibob.py --action fill-time-attendance --value "08:00 - 14:00, 15:00 - 17:00"

# The shorter hour-only form is also accepted
python3 hibob.py --action fill-time-attendance --month 10 --value "8-14,15-17"
```

`--action show` is the default. If `--month` is omitted, the tool selects the previous month on days 1–5 and the current month on all other days. `--month` accepts a number from 1 to 12 and uses the current year.

The attendance table shows each date as `FILLED`, `PENDING`, `NON-WORKING`, or `NO DATA`. `NO DATA` means HiBob returned no daily row; the tool does not infer that the date is available to fill.

## Filling attendance

`--value` takes comma-separated 24-hour work intervals. Enter each as `HH:MM - HH:MM` or as `H-H` with omitted minutes treated as `:00`. For example, `08:00 - 14:00, 15:00 - 17:00` and `8-14,15-17` mean the same thing. Each interval must end after it starts, and intervals cannot overlap. Overnight intervals are not supported.

The fill action:

- Uses the **Teleworking** project resolved from HiBob's current project list.
- Writes only dates through yesterday that HiBob reports as `PENDING` in the selected month.
- Skips dates already filled, weekends, holidays, time off, dates without a report row, today, and future dates.
- Checks that the timesheet is open before writing.
- Saves a private backup under the ignored `backups/` directory, rereads each date before updating it, and reads attendance back to verify the intervals and project.

This action writes attendance to HiBob. If a request fails partway through, rerunning it skips dates that are already filled.

## API reference

[reference/api/README.md](reference/api/README.md) describes endpoints observed in a local HiBob HAR capture, with request and response shapes and a short purpose for each endpoint. These are private web-app endpoints, not a stable public API; response formats and permissions can change.

## Protect session and attendance data

Keep `curl.secret` private. `.gitignore` excludes it, HAR captures, session files, backups, exports, and Python cache files. Do not commit credentials or attendance backups. Remove local session captures when you no longer need them, and log out of HiBob yourself when finished.
