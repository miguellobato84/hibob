import base64
import json
import unittest
from contextlib import redirect_stderr
from datetime import date, datetime, timezone
from io import StringIO
from unittest.mock import Mock, patch

import hibob


def session_token(employee_id="12345", expiry=2_000_000_000):
    payload = (
        base64.urlsafe_b64encode(
            json.dumps({"employeeId": employee_id, "exp": expiry}).encode()
        )
        .decode()
        .rstrip("=")
    )
    return f"header.{payload}.signature"


class ParseCurlTests(unittest.TestCase):
    def test_extracts_cookie_headers_employee_and_offset(self):
        curl = (
            "curl 'https://app.hibob.com/api/attendance/report' "
            "-H 'bob-timezoneoffset: -120' "
            "-H 'Accept: application/json' "
            f"-b 'hibob={session_token()}; other=value' "
            "--data-raw '{}'"
        )

        with patch.object(hibob.time, "time", return_value=1_900_000_000):
            headers, cookies, employee_id, offset = hibob.parse_curl(curl)

        self.assertEqual(headers["accept"], "application/json")
        self.assertEqual(cookies["other"], "value")
        self.assertEqual(employee_id, "12345")
        self.assertEqual(offset, -120)

    def test_rejects_non_hibob_api_url(self):
        curl = (
            "curl 'https://example.com/api/attendance/report' "
            "-H 'bob-timezoneoffset: 0' "
            f"-b 'hibob={session_token()}'"
        )
        with self.assertRaisesRegex(
            hibob.InputError, "URL must use https://app.hibob.com"
        ):
            hibob.parse_curl(curl)


class ScheduleTests(unittest.TestCase):
    def test_parses_and_sorts_intervals(self):
        self.assertEqual(
            hibob.parse_intervals("15-17, 8:30 - 14"),
            [("08:30", "14:00"), ("15:00", "17:00")],
        )

    def test_rejects_overlap_and_overnight_ranges(self):
        with self.assertRaisesRegex(hibob.InputError, "must not overlap"):
            hibob.parse_intervals("8-12,11-14")
        with self.assertRaisesRegex(hibob.InputError, "end after it starts"):
            hibob.parse_intervals("22-6")

    def test_parses_weekday_groups_and_uniform_schedule(self):
        schedule = hibob.parse_weekday_schedule("Mon-Thu 8-13,14-17:30 Fri 8-14")

        self.assertEqual(schedule["Mon"], [("08:00", "13:00"), ("14:00", "17:30")])
        self.assertEqual(schedule["Thu"], schedule["Mon"])
        self.assertEqual(schedule["Fri"], [("08:00", "14:00")])
        self.assertEqual(schedule["Sat"], [])
        self.assertEqual(
            hibob.parse_weekday_schedule("8-14")["Fri"], [("08:00", "14:00")]
        )

    def test_weekday_schedule_requires_all_workdays_and_rejects_duplicates(self):
        with self.assertRaisesRegex(hibob.InputError, "missing Tue, Wed, Thu, Fri"):
            hibob.parse_weekday_schedule("Mon 8-14")
        with self.assertRaisesRegex(
            hibob.InputError, "Fri is specified more than once"
        ):
            hibob.parse_weekday_schedule("Mon-Fri 8-14 Fri 8-12")

    def test_grouped_break_schedule_allows_omitted_weekdays(self):
        schedule = hibob.parse_weekday_schedule(
            "Fri 12-12:30", "--break-schedule", require_workdays=False
        )

        self.assertEqual(schedule["Mon"], [])
        self.assertEqual(schedule["Fri"], [("12:00", "12:30")])


class DateAndPayloadTests(unittest.TestCase):
    def test_default_month_uses_previous_month_on_first_five_days(self):
        self.assertEqual(hibob.default_month(date(2025, 1, 5)), (2024, 12))
        self.assertEqual(hibob.default_month(date(2025, 1, 6)), (2025, 1))

    def test_day_status_skips_weekend_and_unknown_weekday(self):
        self.assertEqual(
            hibob.day_status(date(2025, 1, 11), None),
            ("NON-WORKING", "Weekend; no report row"),
        )
        self.assertEqual(
            hibob.day_status(date(2025, 1, 6), None),
            ("NO DATA", "No report row; status not inferred"),
        )

    def test_day_status_distinguishes_pending_holiday_time_off_and_filled(self):
        self.assertEqual(hibob.day_status(date(2025, 1, 6), {}), ("PENDING", ""))
        self.assertEqual(
            hibob.day_status(
                date(2025, 1, 6), {"holidayOrNonWorkingDay": "Public holiday"}
            ),
            ("NON-WORKING", "Public holiday"),
        )
        self.assertEqual(
            hibob.day_status(date(2025, 1, 6), {"timeOff": True}),
            ("NON-WORKING", "Time off"),
        )
        self.assertEqual(
            hibob.day_status(date(2025, 1, 6), {"entries": [{"entryType": "work"}]}),
            ("FILLED", ""),
        )

    def test_payload_has_work_and_break_entries_with_date_offset(self):
        target = date(2025, 7, 14)
        payload = hibob.attendance_payload(
            target,
            [("08:00", "12:00"), ("13:00", "17:00")],
            "project-7",
            hibob.date_offset(target),
            [("12:00", "13:00")],
        )

        self.assertEqual(len(payload), 3)
        self.assertEqual(payload[0]["start"], "2025-07-14T08:00")
        self.assertEqual(payload[0]["projectId"], "project-7")
        self.assertEqual(payload[0]["entryType"], "work")
        self.assertEqual(payload[2]["entryType"], "break")
        self.assertNotIn("projectId", payload[2])
        self.assertTrue(all(entry["offset"] == -120 for entry in payload))

    def test_update_verification_matches_work_project_and_breaks(self):
        row = {
            "entries": [
                {
                    "start": "2025-07-14T08:00",
                    "end": "2025-07-14T12:00",
                    "projectId": "7",
                },
                {
                    "start": "2025-07-14T12:00",
                    "end": "2025-07-14T13:00",
                    "entryType": "break",
                },
                {
                    "start": "2025-07-14T13:00",
                    "end": "2025-07-14T17:00",
                    "projectTracking": {"projectId": 7},
                },
            ]
        }
        self.assertTrue(
            hibob.matches_intervals(
                row, [("08:00", "12:00"), ("13:00", "17:00")], 7, [("12:00", "13:00")]
            )
        )
        self.assertFalse(hibob.matches_intervals(row, [("08:00", "17:00")], 7))


class RequestTests(unittest.TestCase):
    def test_post_sends_json_payload_and_accepts_empty_success(self):
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        response.read.return_value = b""
        opener = Mock()
        opener.open.return_value = response
        payload = [{"entryType": "work", "projectId": "project-7"}]

        result = hibob.request_json(
            opener, {"Accept": "application/json"}, "attendance/entries", payload
        )

        request = opener.open.call_args.args[0]
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.data, json.dumps(payload).encode("utf-8"))
        self.assertEqual(
            request.get_header("Content-type"), "application/json;charset=UTF-8"
        )
        self.assertIsNone(result)


class FillTargetTests(unittest.TestCase):
    class FrozenDateTime:
        @classmethod
        def now(cls, tz=None):
            return datetime(2025, 7, 15, tzinfo=timezone.utc)

    class StopAfterSelection(Exception):
        pass

    def selected_targets(self, overwrite):
        rows = {
            date(2025, 7, 11): {},  # pending Friday
            date(2025, 7, 12): {"entries": [{"entryType": "work"}]},  # filled weekend
            date(2025, 7, 14): {},  # pending Monday, yesterday
            date(2025, 7, 15): {},  # today
            date(2025, 7, 16): {},  # future pending day
            date(2025, 7, 17): {
                "entries": [{"entryType": "work"}]
            },  # filled later in month
        }
        cycles = [{"cycleStartDate": "2025-07-01", "cycleEndDate": "2025-07-31"}]
        selected = []

        def record_target(_cycles, target):
            selected.append(target)
            return cycles[0]

        def stop_after_selection(_cycle, _target):
            raise self.StopAfterSelection()

        with (
            patch.object(hibob, "datetime", self.FrozenDateTime),
            patch.object(hibob, "report_cycles", return_value=cycles),
            patch.object(hibob, "month_rows", return_value=rows),
            patch.object(
                hibob,
                "fetch_projects",
                return_value=[{"id": "project-7", "name": "Example"}],
            ),
            patch.object(hibob, "cycle_for_date", side_effect=record_target),
            patch.object(
                hibob, "ensure_cycle_editable", side_effect=stop_after_selection
            ),
        ):
            with self.assertRaises(self.StopAfterSelection):
                hibob.fill_month(
                    None,
                    {},
                    "12345",
                    2025,
                    7,
                    [("08:00", "17:00")],
                    "project-7",
                    overwrite,
                )
        return selected

    def test_default_targets_only_pending_weekdays_through_yesterday(self):
        self.assertEqual(
            self.selected_targets(overwrite=False),
            [date(2025, 7, 11), date(2025, 7, 14)],
        )

    def test_overwrite_includes_filled_later_days_but_pending_only_through_yesterday(
        self,
    ):
        self.assertEqual(
            self.selected_targets(overwrite=True),
            [date(2025, 7, 11), date(2025, 7, 14), date(2025, 7, 17)],
        )


class TimesheetStateTests(unittest.TestCase):
    def test_only_open_unlocked_timesheets_are_editable(self):
        target = date(2025, 7, 14)
        hibob.ensure_cycle_editable(
            {"timesheetState": {"timeSheetStatus": "Open", "locked": False}}, target
        )
        for state in (
            {"timeSheetStatus": "Open", "locked": True},
            {"timeSheetStatus": "Submitted", "locked": False},
        ):
            with (
                self.subTest(state=state),
                self.assertRaisesRegex(RuntimeError, "no entries written"),
            ):
                hibob.ensure_cycle_editable({"timesheetState": state}, target)
        with self.assertRaisesRegex(RuntimeError, "no entries written"):
            hibob.ensure_cycle_editable({}, target)


class CLIArgumentTests(unittest.TestCase):
    def test_fill_action_requires_schedule_and_project(self):
        for argv in (
            [
                "hibob.py",
                "--action",
                "fill-time-attendance",
                "--project-id",
                "project-7",
            ],
            ["hibob.py", "--action", "fill-time-attendance", "--schedule", "8-17"],
        ):
            with (
                self.subTest(argv=argv),
                patch("sys.argv", argv),
                redirect_stderr(StringIO()),
                self.assertRaises(SystemExit) as error,
            ):
                hibob.parse_args()
            self.assertEqual(error.exception.code, 2)

    def test_fill_options_are_rejected_for_show_action(self):
        with (
            patch("sys.argv", ["hibob.py", "--overwrite"]),
            redirect_stderr(StringIO()),
            self.assertRaises(SystemExit) as error,
        ):
            hibob.parse_args()
        self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
