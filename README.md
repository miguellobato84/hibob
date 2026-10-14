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

## Get the session

1. Sign in to HiBob in Chrome and open the Attendance page.
2. Open Chrome DevTools (`⌘`+`Option`+`I` on macOS, or `Ctrl`+`Shift`+`I` on Windows/Linux) and select **Network**. DevTools records requests while this panel is open, so reload the Attendance page if needed.
3. Select the **Fetch/XHR** filter and find a successful Attendance request. Right-click its row and choose **Copy** → **Copy as cURL**.
4. Create or open `curl.secret` in the repository root, paste the copied command as-is, and save the file. Restrict access to your account:

   ```sh
   chmod 600 curl.secret
   ```

The copied command contains session credentials, such as cookies or authorization headers. Treat `curl.secret` like a password; do not share or commit it. See the [Chrome DevTools Network reference](https://developer.chrome.com/docs/devtools/network/reference/) for the Network panel, request filters, and copy options.

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
python3 hibob.py --action fill-time-attendance --project-id PROJECT_ID --schedule "08:00 - 14:00, 15:00 - 17:00"

# Add a break interval between work intervals
python3 hibob.py --action fill-time-attendance --project-id PROJECT_ID --schedule "8-14,15-17" --break-schedule "14-15"

# The shorter hour-only form is also accepted
python3 hibob.py --action fill-time-attendance --month 10 --project-id PROJECT_ID --schedule "8-14,15-17"

# Replace existing attendance entries in the selected month
python3 hibob.py --action fill-time-attendance --month 10 --project-id PROJECT_ID --schedule "8-14,15-17" --overwrite
```

Replace `PROJECT_ID` with an ID shown by `--action show-projects`.

`--action show` is the default. If `--month` is omitted, the tool selects the previous month on days 1–5 and the current month on all other days. `--month` accepts a number from 1 to 12 and uses the current year.

The attendance table shows each date as `FILLED`, `PENDING`, `NON-WORKING`, or `NO DATA`. `NO DATA` means HiBob returned no daily row; the tool does not infer that the date is available to fill.

## Filling attendance

`--schedule` takes comma-separated 24-hour work intervals. Enter each as `HH:MM - HH:MM` or as `H-H` with omitted minutes treated as `:00`. For example, `08:00 - 14:00, 15:00 - 17:00` and `8-14,15-17` mean the same thing. `--break-schedule` takes break intervals in the same format and uses the same validation. Example: `--schedule "8-14,15-17" --break-schedule "14-15"`. Each interval must end after it starts, intervals within a schedule cannot overlap, and overnight intervals are not supported.

The fill action:

- Requires `--project-id`; it has no default. The ID must match a project returned by HiBob for the signed-in employee.
- Accepts optional `--break-schedule`; each interval is submitted as an `entryType: "break"` entry with no project ID.
- Writes only dates through yesterday that HiBob reports as `PENDING` in the selected month.
- With `--overwrite`, replaces existing attendance entries on every filled date in the selected month and also fills pending dates through yesterday.
- In the default mode, skips dates already filled, weekends, holidays, time off, dates without a report row, today, and future dates.
- Checks that the timesheet is open before writing.
- Saves a private backup under the ignored `backups/` directory, rereads each date before updating it, and reads attendance back to verify the intervals and project.

This action writes attendance to HiBob. In the default mode, if a request fails partway through, rerunning it skips dates that are already filled.

`--overwrite` is restricted to `--action fill-time-attendance`. It replaces each target date's full entry list with the requested schedule and project. Existing entries later in the selected month are included; pending dates are still filled only through yesterday. A backup of every target day's prior row is saved before writing.

## API reference

[reference/api/README.md](reference/api/README.md) describes endpoints observed in a local HiBob HAR capture, with request and response shapes and a short purpose for each endpoint. These are private web-app endpoints, not a stable public API; response formats and permissions can change.

## Protect session and attendance data

Keep `curl.secret` private. `.gitignore` excludes it, HAR captures, session files, backups, exports, and Python cache files. Do not commit credentials or attendance backups. Remove local session captures when you no longer need them, and log out of HiBob yourself when finished.
