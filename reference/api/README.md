# HiBob UI API reference

This reference describes private `app.hibob.com` web-app endpoints. They are not a stable or public API contract; availability and response shapes may vary by account, permissions, and application version.

Purpose descriptions summarize endpoint names and response fields. Request and response schemas use field paths and JSON types; credentials, query values, and personal field values are omitted. Dynamic path identifiers use placeholders such as `{employeeId}`, `{timesheetId}`, and `{siteId}`.

## Endpoint index

| Method | Endpoint |
|---|---|
| `GET` | `/api/attendance/employees/{employeeId}/balancesHistory` |
| `GET` | `/api/attendance/employees/{employeeId}/currentBalance` |
| `GET` | `/api/attendance/employees/{employeeId}/projects` |
| `GET` | `/api/attendance/employees/{employeeId}/settings/` |
| `GET` | `/api/attendance/employees/{employeeId}/timesheets` |
| `GET` | `/api/attendance/employees/{employeeId}/timesheets/{date}/history` |
| `GET` | `/api/attendance/employees/{employeeId}/timesheets/{timesheetId}/summary` |
| `GET` | `/api/attendance/my/clockStatus` |
| `POST` | `/api/attendance/employees/{employeeId}/attendance/entries` |
| `GET` | `/api/branding/` |
| `GET` | `/api/branding/login` |
| `GET` | `/api/company` |
| `GET` | `/api/company/ai/settings/values/globalAIEnabled` |
| `GET` | `/api/company/features` |
| `GET` | `/api/company/metadata/categories` |
| `GET` | `/api/company/metadata/lists/` |
| `GET` | `/api/company/metadata/reports/time_attendance_employee_timesheet` |
| `GET` | `/api/company/sites/details/{siteId}` |
| `GET` | `/api/company/toggles` |
| `GET` | `/api/company/views/defaults/time_attendance_employee_timesheet` |
| `GET` | `/api/employees/essentials` |
| `GET` | `/api/languages` |
| `GET` | `/api/modules/` |
| `GET` | `/api/notifications` |
| `GET` | `/api/permissions/authorizations/domains/ai` |
| `GET` | `/api/permissions/authorizations/domains/analytics` |
| `GET` | `/api/permissions/authorizations/domains/community` |
| `GET` | `/api/permissions/authorizations/domains/docs` |
| `GET` | `/api/permissions/authorizations/domains/feedback` |
| `GET` | `/api/permissions/authorizations/domains/integrations` |
| `GET` | `/api/permissions/authorizations/domains/jobCatalog` |
| `GET` | `/api/permissions/authorizations/domains/people` |
| `GET` | `/api/permissions/authorizations/domains/project` |
| `GET` | `/api/permissions/authorizations/domains/reports` |
| `GET` | `/api/permissions/authorizations/domains/reviews` |
| `GET` | `/api/permissions/authorizations/domains/settings` |
| `GET` | `/api/permissions/authorizations/domains/timeAttendance` |
| `GET` | `/api/permissions/authorizations/domains/timeoff` |
| `GET` | `/api/permissions/authorizations/domains/toDos` |
| `GET` | `/api/permissions/authorizations/domains/trainingPlatform` |
| `GET` | `/api/permissions/authorizations/domains/workflowsFolders` |
| `GET` | `/api/permissions/authorizations/domains/workforcePlanning` |
| `GET` | `/api/permissions/employees/authorized/domains/settings/resources/permissions/actions/viewAs` |
| `GET` | `/api/timeoff/outToday` |
| `GET` | `/api/timeoff/requests/pending` |
| `GET` | `/api/user` |
| `GET` | `/api/user/prefs/branding-palette-key` |
| `GET` | `/api/user/prefs/colors-state_1.1` |
| `GET` | `/api/user/prefs/isDemoDataPopFold` |
| `GET` | `/api/user/prefs/time_attendance_employee_timesheet` |
| `PUT` | `/api/user/prefs/time_attendance_employee_timesheet` |
| `HEAD` | `/api/assessment-layer/permissions/can-view-my-career` |
| `HEAD` | `/api/attendance/canViewPeoplesAttendance` |
| `HEAD` | `/api/attendance/hasPersonalAttendance` |
| `HEAD` | `/api/attendance/hasProjectOwnership` |
| `HEAD` | `/api/company/analytics/dashboards/isAllowed` |
| `HEAD` | `/api/company/analytics/diversityEquityAndInclusion/isAllowed` |
| `HEAD` | `/api/company/workforceplanning/homepage/isAllowed` |
| `HEAD` | `/api/compensation/event/compensationFeatureAllowed` |
| `HEAD` | `/api/docs/esign/templates` |
| `HEAD` | `/api/equity-vesting-schedule/isFeatureAllowed` |
| `HEAD` | `/api/import/visible` |
| `HEAD` | `/api/notifications` |
| `HEAD` | `/api/reviews/allowed` |
| `HEAD` | `/api/reviews/my-team/allowed` |
| `HEAD` | `/api/sandbox-service/login/allowed` |
| `HEAD` | `/api/sandbox/visible` |
| `HEAD` | `/api/surveys-core/surveys/visible` |
| `HEAD` | `/api/surveys-core/talent-groups` |
| `HEAD` | `/api/talent-events/allowed` |
| `HEAD` | `/api/workforceplanning/event/isAllowed` |
| `POST` | `/api/attendance/employees/{employeeId}/timesheets/{timesheetId}/details` |
| `POST` | `/api/company/views/search` |

## Endpoint reference

### `GET /api/attendance/employees/{employeeId}/balancesHistory`

### Purpose

Returns the employee attendance balance for prior cycles, with cycle dates and opening/closing balance fields.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | array |
| $[] | object |
| $[].balance | object |
| $[].balance.closingBalance | string |
| $[].balance.closingBalanceSeconds | integer |
| $[].balance.cycleBalance | string |
| $[].balance.cycleBalanceSeconds | integer |
| $[].cycle | object |
| $[].cycle.endDate | string |
| $[].cycle.startDate | string |

### `GET /api/attendance/employees/{employeeId}/currentBalance`

### Purpose

Returns the employee current-cycle balance and expected closing balance.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.cycleAdjustments | array |
| $.expectedClosingBalance | string |
| $.expectedClosingBalanceSeconds | integer |
| $.runningCycleBalance | string |
| $.runningCycleBalanceSeconds | integer |
| $.startingBalance | string |
| $.startingBalanceSeconds | integer |

### `GET /api/attendance/employees/{employeeId}/projects`

### Purpose

Lists projects and task metadata available for the employee attendance records.

### Request

#### Query parameters

| Name | Type |
| --- | --- |
| includeArchivedTasks | boolean |

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.results | array |
| $.results[] | object |
| $.results[].audienceSelector | object |
| $.results[].audienceSelector.explicitEmployees | array |
| $.results[].audienceSelector.instructions | array |
| $.results[].audienceSelector.instructions[] | object |
| $.results[].audienceSelector.instructions[].fieldPath | string |
| $.results[].audienceSelector.instructions[].operator | string |
| $.results[].audienceSelector.instructions[].values | array |
| $.results[].audienceSelector.instructions[].values[] | string |
| $.results[].billable | boolean |
| $.results[].clientId | null |
| $.results[].color | string |
| $.results[].description | null |
| $.results[].id | integer |
| $.results[].isArchived | boolean |
| $.results[].name | string |
| $.results[].projectOwners | array |
| $.results[].taskIds | array |
| $.results[].tasks | array |

### `GET /api/attendance/employees/{employeeId}/settings/`

### Purpose

Returns attendance policy and reporting settings that apply to the employee.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.approval | object |
| $.approval.approvalType | string |
| $.bankedOvertimeToTimeoffSettings | null |
| $.breakDeductionSettings | object |
| $.breakDeductionSettings.breakDeductionType | string |
| $.breakDeductionSettings.complianceTracking | object |
| $.breakDeductionSettings.complianceTracking.customBreakRules | array |
| $.breakDeductionSettings.complianceTracking.customBreakRules[] | object |
| $.breakDeductionSettings.complianceTracking.customBreakRules[].id | string |
| $.breakDeductionSettings.complianceTracking.customBreakRules[].penaltyMinutes | integer |
| $.breakDeductionSettings.complianceTracking.customBreakRules[].requirement | object |
| $.breakDeductionSettings.complianceTracking.customBreakRules[].requirement.minimumMinutes | integer |
| $.breakDeductionSettings.complianceTracking.customBreakRules[].requirement.type | string |
| $.breakDeductionSettings.complianceTracking.customBreakRules[].trigger | object |
| $.breakDeductionSettings.complianceTracking.customBreakRules[].trigger.minutesWorked | integer |
| $.breakDeductionSettings.complianceTracking.customBreakRules[].trigger.type | string |
| $.breakDeductionSettings.complianceTracking.customBreakRules[].waiverCondition | array |
| $.breakDeductionSettings.complianceTracking.guidelines | string |
| $.breakDeductionSettings.deductionByMinutesWorked | array |
| $.enforceComments | boolean |
| $.geoFenceSettings | null |
| $.timesheetReportingMethod | string |

### `GET /api/attendance/employees/{employeeId}/timesheets`

### Purpose

Lists employee timesheet cycles and their state.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.employeeTimesheets | array |
| $.employeeTimesheets[] | object |
| $.employeeTimesheets[].cycleEndDate | string |
| $.employeeTimesheets[].cycleId | integer |
| $.employeeTimesheets[].cycleStartDate | string |
| $.employeeTimesheets[].id | integer |
| $.employeeTimesheets[].timesheetState | object |
| $.employeeTimesheets[].timesheetState.lockAt | integer |
| $.employeeTimesheets[].timesheetState.locked | boolean |
| $.employeeTimesheets[].timesheetState.timeSheetStatus | string |

### `GET /api/attendance/employees/{employeeId}/timesheets/{date}/history`

### Purpose

Returns the audit history for an employee's attendance on one date. The captured response included an `editedEntries` event from the web UI, with actor, timestamp, entry details, and nested subitems.

### Request

#### Path parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `employeeId` | string | Employee identifier. |
| `date` | string | Attendance date in `YYYY-MM-DD` form. |

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.date | string |
| $.events | array |
| $.events[] | object |
| $.events[].type | string |
| $.events[].actor | object |
| $.events[].actor.employeeId | string |
| $.events[].actor.displayName | string |
| $.events[].actor.isImpersonated | boolean |
| $.events[].source | string |
| $.events[].timestamp | integer |
| $.events[].details | object |
| $.events[].details.clockIn | string |
| $.events[].details.clockOut | string |
| $.events[].details.entryDuration | string |
| $.events[].details.projectId | integer |
| $.events[].details.projectName | string |
| $.events[].subItems | array |
| $.events[].subItems[] | object |
| $.events[].subItems[].type | string |
| $.events[].subItems[].isDeleted | boolean |
| $.events[].subItems[].details | object |
| $.events[].subItems[].details.clockIn | string |
| $.events[].subItems[].details.clockOut | string |
| $.events[].subItems[].details.entryDuration | string |
| $.events[].subItems[].details.projectId | integer |
| $.events[].subItems[].details.projectName | string |

The captured event used `type: "editedEntries"` and `source: "web"`. These are observed values, not an exhaustive enum.

### `GET /api/attendance/employees/{employeeId}/timesheets/{timesheetId}/summary`

### Purpose

Returns a timesheet-cycle summary including worked time, payable time, exceptions, and submission flags.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.breakViolationCounter | integer |
| $.cycleSummary | object |
| $.cycleSummary.hoursWorkedDisplay | string |
| $.cycleSummary.nonWorkingEventsDisplay | string |
| $.cycleSummary.overUnderTime | object |
| $.cycleSummary.overUnderTime.hoursDisplay | string |
| $.cycleSummary.overUnderTime.sign | string |
| $.cycleSummary.payableDays | object |
| $.cycleSummary.payableDays.payable | integer |
| $.cycleSummary.payableDays.potential | integer |
| $.cycleSummary.payableHoursBreakdown | object |
| $.cycleSummary.payableHoursBreakdown.doubleDailyOvertimeAmount | integer |
| $.cycleSummary.payableHoursBreakdown.doubleDailyOvertimeDisplay | string |
| $.cycleSummary.payableHoursBreakdown.overtimeAmount | integer |
| $.cycleSummary.payableHoursBreakdown.overtimeDisplay | string |
| $.cycleSummary.payableHoursBreakdown.regularHoursAmount | integer |
| $.cycleSummary.payableHoursBreakdown.regularHoursDisplay | string |
| $.cycleSummary.payableHoursBreakdown.totalHoursDisplay | string |
| $.cycleSummary.potentialHours | object |
| $.cycleSummary.potentialHours.payableTimeDisplay | string |
| $.cycleSummary.potentialHours.payableTimePercentage | integer |
| $.cycleSummary.potentialHours.payableTimePercentageDisplay | string |
| $.cycleSummary.potentialHours.remainingTimeDisplay | string |
| $.cycleSummary.potentialHours.remainingTimePercentage | integer |
| $.cycleSummary.potentialHours.remainingTimePercentageDisplay | string |
| $.cycleSummary.potentialHours.summaryDisplay | string |
| $.cycleSummary.projects | array |
| $.cycleSummary.projects[] | object |
| $.cycleSummary.projects[].color | string |
| $.cycleSummary.projects[].hoursDisplay | string |
| $.cycleSummary.projects[].name | string |
| $.cycleSummary.timeOffDisplay | string |
| $.cycleSummary.unpaidBreak | object |
| $.cycleSummary.unpaidBreak.hoursDisplay | string |
| $.dailyBreakdown | object |
| $.dailyBreakdown.categories | array |
| $.dailyBreakdown.categories[] | string |
| $.dailyBreakdown.graphData | array |
| $.dailyBreakdown.graphData[] | object |
| $.dailyBreakdown.graphData[].data | array |
| $.dailyBreakdown.graphData[].data[] | null / object |
| $.dailyBreakdown.graphData[].id | string |
| $.dailyBreakdown.graphData[].name | string |
| $.dailyBreakdown.graphData[].showInLegend | boolean |
| $.dailyBreakdown.graphData[].target | array |
| $.dailyBreakdown.graphData[].target[] | null / object |
| $.enrichedExceptions | array |
| $.enrichedExceptions[] | object |
| $.enrichedExceptions[].level | string |
| $.enrichedExceptions[].message | string |
| $.enrichedExceptions[].tooltip | object |
| $.enrichedExceptions[].tooltip.header | string |
| $.enrichedExceptions[].tooltip.label | string |
| $.enrichedExceptions[].tooltip.text | array |
| $.enrichedExceptions[].tooltip.text[] | string |
| $.enrichedExceptions[].type | string |
| $.hasInvalidProjectOrTask | boolean |
| $.hasMissingEntries | boolean |
| $.hasMissingFutureEntries | boolean |
| $.hasOverlappingApprovedPaidTimeOffRequestsAndAttendance | boolean |
| $.hasPendingTimeOffRequests | boolean |
| $.isAutoSubmitTimesheet | boolean |
| $.isSubmittable | boolean |

### `POST /api/attendance/employees/{employeeId}/attendance/entries`

### Purpose

Submits attendance entries for one employee and date. The captured request sent work entries and a break entry together in one JSON array. The capture does not establish whether the server merges or replaces entries, so callers should follow the UI's submitted-list format.

### Request

#### Path parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `employeeId` | string | Employee identifier. |

#### Query parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `forDate` | string | Attendance date in `YYYY-MM-DD` form. |

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `origin`, `referer`, `x-requested-with`

#### Body

**Media type:** application/json.

An array of entries. Observed work entries contain an existing numeric `id`, `projectId`, `reason`, and `comment`. The break entry had `id: null` and omitted `projectId`, `reason`, and `comment`.

| Field path | Type | Notes |
| --- | --- | --- |
| $ | array |
| $[] | object |
| $[].id | integer / null | Existing work entries carried an ID; the new break used `null`. |
| $[].start | string | Local date-time in `YYYY-MM-DDTHH:MM` form. |
| $[].end | string | Local date-time in `YYYY-MM-DDTHH:MM` form. |
| $[].entryType | string | Captured values: `work` and `break`. |
| $[].reportingMethod | string | Captured value: `startEnd`. |
| $[].offset | integer | Time-zone offset in minutes. |
| $[].projectId | integer | Present on work entries; absent on the captured break. |
| $[].reason | null | Present on captured work entries; absent on the break. |
| $[].comment | null | Present on captured work entries; absent on the break. |

For a break, the captured shape was:

```json
{
  "id": null,
  "start": "YYYY-MM-DDTHH:MM",
  "end": "YYYY-MM-DDTHH:MM",
  "entryType": "break",
  "reportingMethod": "startEnd",
  "offset": 0
}
```

The example uses a placeholder offset. Use the offset applicable to the attendance date. The capture's successful response was HTTP 200 with an empty body (`text/plain`).

### `GET /api/attendance/my/clockStatus`

### Purpose

Returns the signed-in user clock state, current punch details, and today’s worked-time totals.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.breaksTotalMinutes | integer |
| $.comment | null |
| $.currentLocalTime | string |
| $.disabled | boolean |
| $.end | null |
| $.entries | array |
| $.entryType | null |
| $.errorMessage | null |
| $.geoFenceEnabled | boolean |
| $.minutesWorkedToday | integer |
| $.nextClockAction | string |
| $.secondsWorkedToday | integer |
| $.start | null |

### `GET /api/branding/`

### Purpose

Returns company branding assets and theme colors used by the application.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.backgrounds | object |
| $.backgrounds.homepage | string |
| $.logos | object |
| $.logos.main | string |
| $.logos.menu | null |
| $.themeSettings | object |
| $.themeSettings.linkColor | string |
| $.themeSettings.palette | object |
| $.themeSettings.palette.baseColors | array |
| $.themeSettings.palette.baseColors[] | string |
| $.themeSettings.palette.fullPalette | object |
| $.themeSettings.palette.fullPalette.color1_base | string |
| $.themeSettings.palette.fullPalette.color1_dark | string |
| $.themeSettings.palette.fullPalette.color1_darker | string |
| $.themeSettings.palette.fullPalette.color1_light | string |
| $.themeSettings.palette.fullPalette.color1_lighter | string |
| $.themeSettings.palette.fullPalette.color2_base | string |
| $.themeSettings.palette.fullPalette.color2_dark | string |
| $.themeSettings.palette.fullPalette.color2_darker | string |
| $.themeSettings.palette.fullPalette.color2_light | string |
| $.themeSettings.palette.fullPalette.color2_lighter | string |
| $.themeSettings.palette.fullPalette.color3_base | string |
| $.themeSettings.palette.fullPalette.color3_dark | string |
| $.themeSettings.palette.fullPalette.color3_darker | string |
| $.themeSettings.palette.fullPalette.color3_light | string |
| $.themeSettings.palette.fullPalette.color3_lighter | string |
| $.themeSettings.palette.fullPalette.color4_base | string |
| $.themeSettings.palette.fullPalette.color4_dark | string |
| $.themeSettings.palette.fullPalette.color4_darker | string |
| $.themeSettings.palette.fullPalette.color4_light | string |
| $.themeSettings.palette.fullPalette.color4_lighter | string |
| $.themeSettings.palette.fullPalette.color5_base | string |
| $.themeSettings.palette.fullPalette.color5_dark | string |
| $.themeSettings.palette.fullPalette.color5_darker | string |
| $.themeSettings.palette.fullPalette.color5_light | string |
| $.themeSettings.palette.fullPalette.color5_lighter | string |
| $.themeSettings.palette.fullPalette.color6_base | string |
| $.themeSettings.palette.fullPalette.color6_dark | string |
| $.themeSettings.palette.fullPalette.color6_darker | string |
| $.themeSettings.palette.fullPalette.color6_light | string |
| $.themeSettings.palette.fullPalette.color6_lighter | string |
| $.themeSettings.palette.fullPalette.color7_base | string |
| $.themeSettings.palette.fullPalette.color7_dark | string |
| $.themeSettings.palette.fullPalette.color7_darker | string |
| $.themeSettings.palette.fullPalette.color7_light | string |
| $.themeSettings.palette.fullPalette.color7_lighter | string |
| $.themeSettings.palette.fullPalette.color8_base | string |
| $.themeSettings.palette.fullPalette.color8_dark | string |
| $.themeSettings.palette.fullPalette.color8_darker | string |
| $.themeSettings.palette.fullPalette.color8_light | string |
| $.themeSettings.palette.fullPalette.color8_lighter | string |
| $.themeSettings.palette.fullPalette.color9_base | string |
| $.themeSettings.palette.fullPalette.color9_dark | string |
| $.themeSettings.palette.fullPalette.color9_darker | string |
| $.themeSettings.palette.fullPalette.color9_light | string |
| $.themeSettings.palette.fullPalette.color9_lighter | string |
| $.themeSettings.palette.id | string |
| $.themeSettings.palette.name | string |
| $.themeSettings.paletteKey | string |
| $.themeSettings.primaryButton | string |
| $.themeSettings.primaryIndication | string |
| $.themeSettings.sideMenu | string |

### `GET /api/branding/login`

### Purpose

Returns the configured login-page background asset.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.loginBackground | string |

### `GET /api/company`

### Purpose

Returns basic company profile and locale settings.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.autoGenerateId | boolean |
| $.business | string |
| $.defaultCurrency | string |
| $.defaultLanguage | string |
| $.demoData | boolean |
| $.displayDateFormat | string |
| $.incorporationDate | null |
| $.logoUrl | string |
| $.name | string |
| $.testAccount | boolean |
| $.tradingNumber | null |

### `GET /api/company/ai/settings/values/globalAIEnabled`

### Purpose

Returns whether the company-wide AI setting is enabled.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.enabled | boolean |

### `GET /api/company/features`

### Purpose

Lists company feature flags and their enabled states.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | array |
| $[] | object |
| $[].attributes | object |
| $[].attributes.isPinned | boolean |
| $[].description | string |
| $[].displayName | string |
| $[].enabled | boolean |
| $[].name | string |

### `GET /api/company/metadata/categories`

### Purpose

Returns company metadata categories, fields, and field filter operators.

### Request

#### Query parameters

| Name | Type |
| --- | --- |
| filter | string |

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.categories | array |
| $.categories[] | object |
| $.categories[].canBeDeleted | boolean |
| $.categories[].categoryName | string |
| $.categories[].custom | array |
| $.categories[].description | null |
| $.categories[].displayName | string |
| $.categories[].fields | array |
| $.categories[].fields[] | object |
| $.categories[].fields[].canBeDeleted | boolean |
| $.categories[].fields[].categoryName | string |
| $.categories[].fields[].description | null / string |
| $.categories[].fields[].immutableAttributes | object |
| $.categories[].fields[].immutableAttributes.isHistorical | boolean |
| $.categories[].fields[].immutableAttributes.isMasked | boolean |
| $.categories[].fields[].immutableAttributes.isRequired | boolean |
| $.categories[].fields[].immutableAttributes.mandatory | boolean |
| $.categories[].fields[].immutableAttributes.siteFilter | boolean |
| $.categories[].fields[].isCalculated | boolean |
| $.categories[].fields[].isDisplayable | boolean |
| $.categories[].fields[].isDynamic | boolean |
| $.categories[].fields[].isFilterable | boolean |
| $.categories[].fields[].isHistorical | boolean |
| $.categories[].fields[].isMasked | boolean |
| $.categories[].fields[].isReadOnly | boolean |
| $.categories[].fields[].isRequired | boolean |
| $.categories[].fields[].isSearchable | boolean |
| $.categories[].fields[].isTableColumn | boolean |
| $.categories[].fields[].listName | string |
| $.categories[].fields[].mandatory | boolean |
| $.categories[].fields[].name | string |
| $.categories[].fields[].operators | array |
| $.categories[].fields[].operators[] | string |
| $.categories[].fields[].path | string |
| $.categories[].fields[].siteFilter | object |
| $.categories[].fields[].siteFilter.siteIds | array |
| $.categories[].fields[].siteFilter.siteIds[] | integer |
| $.categories[].fields[].siteFilter.type | string |
| $.categories[].fields[].type | string |
| $.categories[].fields[].typeData | object |
| $.categories[].fields[].typeData.listName | string |
| $.categories[].info | array |
| $.categories[].info[] | object |
| $.categories[].info[].message | string |
| $.categories[].info[].type | string |
| $.categories[].isDynamic | boolean |
| $.categories[].isEditable | boolean |
| $.fieldsOperators | object |
| $.fieldsOperators.avatar | array |
| $.fieldsOperators.avatar[] | string |
| $.fieldsOperators.boolean | array |
| $.fieldsOperators.boolean[] | string |
| $.fieldsOperators.date | array |
| $.fieldsOperators.date[] | string |
| $.fieldsOperators.employee | array |
| $.fieldsOperators.employee[] | string |
| $.fieldsOperators.employee_id | array |
| $.fieldsOperators.employee_id[] | string |
| $.fieldsOperators.floating_number | array |
| $.fieldsOperators.floating_number[] | string |
| $.fieldsOperators.list | array |
| $.fieldsOperators.list[] | string |
| $.fieldsOperators.list_id | array |
| $.fieldsOperators.list_id[] | string |
| $.fieldsOperators.long_text | array |
| $.fieldsOperators.long_text[] | string |
| $.fieldsOperators.multi_list | array |
| $.fieldsOperators.multi_list[] | string |
| $.fieldsOperators.number | array |
| $.fieldsOperators.number[] | string |
| $.fieldsOperators.short_date | array |
| $.fieldsOperators.short_date[] | string |
| $.fieldsOperators.text | array |
| $.fieldsOperators.text[] | string |

### `GET /api/company/metadata/lists/`

### Purpose

Returns company-defined list values and their editability metadata.

### Request

#### Query parameters

| Name | Type |
| --- | --- |
| includeArchived | boolean |

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.{listName} | object |
| $.{listName}.displayName | string |
| $.{listName}.editable | boolean |
| $.{listName}.type | string |
| $.{listName}.values | array |
| $.{listName}.values[] | object |
| $.{listName}.values[].archived | boolean |
| $.{listName}.values[].canBeDeleted | boolean |
| $.{listName}.values[].children | array |
| $.{listName}.values[].children[] | object |
| $.{listName}.values[].children[].archived | boolean |
| $.{listName}.values[].children[].canBeDeleted | boolean |
| $.{listName}.values[].children[].children | array |
| $.{listName}.values[].children[].children[] | object |
| $.{listName}.values[].children[].children[].archived | boolean |
| $.{listName}.values[].children[].children[].canBeDeleted | boolean |
| $.{listName}.values[].children[].children[].children | array |
| $.{listName}.values[].children[].children[].children[] | object |
| $.{listName}.values[].children[].children[].serverId | integer |
| $.{listName}.values[].children[].children[].value | string |
| $.{listName}.values[].children[].serverId | integer |
| $.{listName}.values[].children[].value | string |
| $.{listName}.values[].serverId | integer / string |
| $.{listName}.values[].value | string |

### `GET /api/company/metadata/reports/time_attendance_employee_timesheet`

### Purpose

Returns field metadata and display capabilities for the employee timesheet report.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.aiConfig | object |
| $.aiConfig.chatbotEnabled | boolean |
| $.downloadFormats | array |
| $.downloadFormats[] | string |
| $.excludeFromColumnPicker | array |
| $.groups | null |
| $.metaData | array |
| $.metaData[] | object |
| $.metaData[].categoryName | string |
| $.metaData[].custom | array |
| $.metaData[].displayName | string |
| $.metaData[].fields | array |
| $.metaData[].fields[] | object |
| $.metaData[].fields[].categoryName | string |
| $.metaData[].fields[].dataJsonPath | string |
| $.metaData[].fields[].dataPath | string |
| $.metaData[].fields[].editable | boolean |
| $.metaData[].fields[].isConfidential | boolean |
| $.metaData[].fields[].isDisplayable | boolean |
| $.metaData[].fields[].isFilterable | boolean |
| $.metaData[].fields[].isFilterableWithPagination | boolean |
| $.metaData[].fields[].isFormulaField | boolean |
| $.metaData[].fields[].isHistoricalData | boolean |
| $.metaData[].fields[].isMasked | boolean |
| $.metaData[].fields[].isRemovableFromReport | boolean |
| $.metaData[].fields[].isRequired | boolean |
| $.metaData[].fields[].isSearchable | boolean |
| $.metaData[].fields[].isSortableWithPagination | boolean |
| $.metaData[].fields[].lockPosition | boolean |
| $.metaData[].fields[].name | string |
| $.metaData[].fields[].operators | array |
| $.metaData[].fields[].operators[] | string |
| $.metaData[].fields[].path | string |
| $.metaData[].fields[].pinned | null / string |
| $.metaData[].fields[].tooltip | null / string |
| $.metaData[].fields[].type | string |
| $.metaData[].fields[].typeData | object |
| $.metaData[].fields[].typeData.viewType | string |
| $.permittedEntityReferenceTypes | array |
| $.quickFilters | array |
| $.serverSidePaginationConfig | null |
| $.showViewOptions | boolean |
| $.supportsCategoryChangesFilter | boolean |
| $.totalCountDescription | null |
| $.unSortable | boolean |

### `GET /api/company/sites/details/{siteId}`

### Purpose

Returns site timezone, date/time display, and location details.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.addressLine1 | string |
| $.addressLine2 | null |
| $.city | string |
| $.country | string |
| $.currency | string |
| $.dateFormat | string |
| $.firstDayOfTheWeek | string |
| $.is24HoursClockFormat | boolean |
| $.isDemo | boolean |
| $.language | string |
| $.postalCode | string |
| $.siteCompanyNumber | null |
| $.siteId | integer |
| $.state | null |
| $.timezone | string |

### `GET /api/company/toggles`

### Purpose

Lists company-level application toggle names.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.toggles | array |
| $.toggles[] | string |

### `GET /api/company/views/defaults/time_attendance_employee_timesheet`

### Purpose

Returns the default configuration for the employee timesheet view.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.category | string |
| $.configuration | object |
| $.configuration.changes | null |
| $.configuration.displayPreferences | object |
| $.configuration.displayPreferences.columnWidths | object |
| $.configuration.displayPreferences.columnsProperties | array |
| $.configuration.displayPreferences.dateFormat | null |
| $.configuration.displayPreferences.exportConfiguration | null |
| $.configuration.displayPreferences.includeFlatJson | boolean |
| $.configuration.displayPreferences.includeHumanReadable | boolean |
| $.configuration.displayPreferences.supportErrorWrapping | boolean |
| $.configuration.fields | array |
| $.configuration.fields[] | string |
| $.configuration.instructions | array |
| $.configuration.instructions[] | object |
| $.configuration.instructions[].fieldPath | string |
| $.configuration.instructions[].operator | string |
| $.configuration.instructions[].values | array |
| $.configuration.instructions[].values[] | string |
| $.configuration.sortBy | string |
| $.createdBy | string |
| $.creationDate | null |
| $.description | string |
| $.modificationDate | null |
| $.name | string |
| $.type | string |

### `GET /api/employees/essentials`

### Purpose

Returns a compact employee directory with identity and work-summary fields.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | array |
| $[] | object |
| $[].about | object |
| $[].about.avatar | string |
| $[].companyId | integer |
| $[].coverImageUrl | string |
| $[].displayName | string |
| $[].email | string |
| $[].firstName | string |
| $[].id | string |
| $[].internal | object |
| $[].internal.lifecycleStatus | string |
| $[].internal.status | string |
| $[].surname | string |
| $[].work | object |
| $[].work.department | string |
| $[].work.employeeIdInCompany | integer |
| $[].work.reportsTo | null / object |
| $[].work.site | string |
| $[].work.siteId | integer |
| $[].work.title | string |

### `GET /api/languages`

### Purpose

Lists language codes and display names supported by the application.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.languages | array |
| $.languages[] | object |
| $.languages[].code | string |
| $.languages[].displayName | string |

### `GET /api/modules/`

### Purpose

Lists application module identifiers available to the signed-in session.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | array |
| $[] | string |

### `GET /api/notifications`

### Purpose

Returns notification items and their read state.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.notifications | array |
| $.notifications[] | object |
| $.notifications[].creationDate | string |
| $.notifications[].data | object |
| $.notifications[].data.actor | string |
| $.notifications[].data.actorDisplayName | string |
| $.notifications[].data.subject | string |
| $.notifications[].id | integer |
| $.notifications[].isRead | boolean |
| $.notifications[].type | string |

### `GET /api/permissions/authorizations/domains/ai`

### Purpose

Returns authorization entries for the AI domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.ai | array |
| $.permissions.ai[] | object |
| $.permissions.ai[].action | string |
| $.permissions.ai[].filter | string |
| $.permissions.ai[].resource | string |

### `GET /api/permissions/authorizations/domains/analytics`

### Purpose

Returns authorization entries for the analytics domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.analytics | array |

### `GET /api/permissions/authorizations/domains/community`

### Purpose

Returns authorization entries for the community domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.community | array |

### `GET /api/permissions/authorizations/domains/docs`

### Purpose

Returns authorization entries for the documents domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.docs | array |
| $.permissions.docs[] | object |
| $.permissions.docs[].action | string |
| $.permissions.docs[].filter | string |
| $.permissions.docs[].resource | string |

### `GET /api/permissions/authorizations/domains/feedback`

### Purpose

Returns authorization entries for the feedback domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.feedback | array |
| $.permissions.feedback[] | object |
| $.permissions.feedback[].action | string |
| $.permissions.feedback[].filter | string |
| $.permissions.feedback[].resource | string |

### `GET /api/permissions/authorizations/domains/integrations`

### Purpose

Returns authorization entries for the integrations domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.integrations | array |

### `GET /api/permissions/authorizations/domains/jobCatalog`

### Purpose

Returns authorization entries for the job catalog domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.jobCatalog | array |

### `GET /api/permissions/authorizations/domains/people`

### Purpose

Returns authorization entries for the people domain; one captured request also includes an employeeId query parameter.

### Request

#### Query parameters

| Name | Type |
| --- | --- |
| employeeId | integer |

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.people | array |
| $.permissions.people[] | object |
| $.permissions.people[].action | string |
| $.permissions.people[].filter | string |
| $.permissions.people[].resource | string |

### `GET /api/permissions/authorizations/domains/project`

### Purpose

Returns authorization entries for the project domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.project | array |

### `GET /api/permissions/authorizations/domains/reports`

### Purpose

Returns authorization entries for the reports domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.reports | array |
| $.permissions.reports[] | object |
| $.permissions.reports[].action | string |
| $.permissions.reports[].filter | string |
| $.permissions.reports[].resource | string |

### `GET /api/permissions/authorizations/domains/reviews`

### Purpose

Returns authorization entries for the reviews domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.reviews | array |

### `GET /api/permissions/authorizations/domains/settings`

### Purpose

Returns authorization entries for the settings domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.settings | array |

### `GET /api/permissions/authorizations/domains/timeAttendance`

### Purpose

Returns authorization entries for the time attendance domain; one captured request also includes an employeeId query parameter.

### Request

#### Query parameters

| Name | Type |
| --- | --- |
| employeeId | integer |

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.timeAttendance | array |
| $.permissions.timeAttendance[] | object |
| $.permissions.timeAttendance[].action | string |
| $.permissions.timeAttendance[].filter | string |
| $.permissions.timeAttendance[].resource | string |

### `GET /api/permissions/authorizations/domains/timeoff`

### Purpose

Returns authorization entries for the time-off domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.timeoff | array |
| $.permissions.timeoff[] | object |
| $.permissions.timeoff[].action | string |
| $.permissions.timeoff[].filter | string |
| $.permissions.timeoff[].resource | string |

### `GET /api/permissions/authorizations/domains/toDos`

### Purpose

Returns authorization entries for the to-dos domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.toDos | array |
| $.permissions.toDos[] | object |
| $.permissions.toDos[].action | string |
| $.permissions.toDos[].filter | string |
| $.permissions.toDos[].resource | string |

### `GET /api/permissions/authorizations/domains/trainingPlatform`

### Purpose

Returns authorization entries for the training platform domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.trainingPlatform | array |

### `GET /api/permissions/authorizations/domains/workflowsFolders`

### Purpose

Returns authorization entries for workflow folders.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.workflowsFolders | array |
| $.permissions.workflowsFolders[] | object |
| $.permissions.workflowsFolders[].action | string |
| $.permissions.workflowsFolders[].filter | string |
| $.permissions.workflowsFolders[].resource | string |

### `GET /api/permissions/authorizations/domains/workforcePlanning`

### Purpose

Returns authorization entries for the workforce planning domain.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.permissions | object |
| $.permissions.workforcePlanning | array |

### `GET /api/permissions/employees/authorized/domains/settings/resources/permissions/actions/viewAs`

### Purpose

Returns the employees authorized for the settings “view as” action.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.employees | string |

### `GET /api/timeoff/outToday`

### Purpose

Returns time-off requests and calendar events matching the requested date and filters.

### Request

#### Query parameters

| Name | Type |
| --- | --- |
| employeeId | integer |
| includeDurationZeroRequests | boolean |
| includeNonWorkingEvents | boolean |
| minimumHours | integer |
| today | date string |

#### Headers

`accept`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.events | array |
| $.requests | array |
| $.requests[] | object |
| $.requests[].dailyHours | null |
| $.requests[].dateRange | object |
| $.requests[].dateRange.endDate | null / string |
| $.requests[].dateRange.endPortion | null / string |
| $.requests[].dateRange.startDate | string |
| $.requests[].dateRange.startPortion | string |
| $.requests[].dateRange.timeZone | string |
| $.requests[].dateRange.type | string |
| $.requests[].dayPortion | null |
| $.requests[].durations | array |
| $.requests[].emoji | string |
| $.requests[].employeeId | string |
| $.requests[].endDate | null / string |
| $.requests[].endDatePortion | null / string |
| $.requests[].hours | null |
| $.requests[].isPending | boolean |
| $.requests[].percentageOfDay | null |
| $.requests[].policyRequestOverride | boolean |
| $.requests[].policyType | null / string |
| $.requests[].policyTypeClassification | string |
| $.requests[].policyTypeColorName | string |
| $.requests[].policyTypeDisplayName | string |
| $.requests[].policyTypeOrder | integer |
| $.requests[].requestId | integer |
| $.requests[].startDate | string |
| $.requests[].startDatePortion | string |
| $.requests[].timeOffRangeType | string |

### `GET /api/timeoff/requests/pending`

### Purpose

Returns pending time-off request records for the signed-in context.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | array |

### `GET /api/user`

### Purpose

Returns the signed-in user profile and account context.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.allReportees | array |
| $.avatar | string |
| $.companyId | integer |
| $.companyName | string |
| $.currency | string |
| $.cxPersonaWithRole | string |
| $.dateFormat | string |
| $.displayName | string |
| $.email | string |
| $.firstName | string |
| $.id | string |
| $.isLoggedInIntoSandbox | boolean |
| $.isManager | boolean |
| $.jobRoleDisplayName | string |
| $.language | string |
| $.lastName | string |
| $.mockedRole | boolean |
| $.paying | boolean |
| $.reportees | array |
| $.role | integer |
| $.sessionType | string |
| $.site | string |
| $.siteId | integer |
| $.state | string |
| $.surname | string |
| $.timeFormat | string |
| $.timezone | string |

### `GET /api/user/prefs/branding-palette-key`

### Purpose

Returns the user’s selected branding palette key.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | string |

### `GET /api/user/prefs/colors-state_1.1`

### Purpose

Returns the stored color-state preference for the signed-in user.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |

### `GET /api/user/prefs/isDemoDataPopFold`

### Purpose

Returns the stored preference controlling the demo-data popover state.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |

### `GET /api/user/prefs/time_attendance_employee_timesheet`

### Purpose

Returns saved user preferences for the employee timesheet report and its fields.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.category | string |
| $.configuration | object |
| $.configuration.changes | null |
| $.configuration.displayPreferences | object |
| $.configuration.displayPreferences.columnWidths | object |
| $.configuration.displayPreferences.columnsProperties | array |
| $.configuration.displayPreferences.dateFormat | null |
| $.configuration.displayPreferences.exportConfiguration | null |
| $.configuration.displayPreferences.includeFlatJson | boolean |
| $.configuration.displayPreferences.includeHumanReadable | boolean |
| $.configuration.displayPreferences.supportErrorWrapping | boolean |
| $.configuration.employeeId | string |
| $.configuration.fields | array |
| $.configuration.fields[] | string |
| $.configuration.instructions | array |
| $.configuration.instructions[] | object |
| $.configuration.instructions[].fieldPath | string |
| $.configuration.instructions[].operator | string |
| $.configuration.instructions[].values | array |
| $.configuration.instructions[].values[] | string |
| $.configuration.sortBy | string |
| $.configuration.timesheetId | integer |
| $.createdBy | string |
| $.creationDate | null |
| $.description | string |
| $.modificationDate | null |
| $.name | string |
| $.pagerConfig | object |
| $.pagerConfig.sliceMax | integer |
| $.pagerConfig.sliceSize | integer |
| $.pagerConfig.sliceStep | integer |
| $.type | string |

### `PUT /api/user/prefs/time_attendance_employee_timesheet`

### Purpose

Saves the current user's employee-timesheet report preferences. This request appeared in the same capture as the break edit; it updates report configuration and is separate from submitting attendance entries.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `origin`, `referer`, `x-requested-with`

#### Body

**Media type:** application/json.

The captured body has the same field structure as the response documented for `GET /api/user/prefs/time_attendance_employee_timesheet`.

### Response

#### Body

**Media type:** application/json.

The captured response returned the saved preference object, with the same field structure as the `GET` response.

### `HEAD /api/assessment-layer/permissions/can-view-my-career`

### Purpose

Checks whether the current session can view the user career page.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/attendance/canViewPeoplesAttendance`

### Purpose

Checks whether the session can view other people’s attendance.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/attendance/hasPersonalAttendance`

### Purpose

Checks whether personal attendance is available for the session.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/attendance/hasProjectOwnership`

### Purpose

Checks whether the session owns or is assigned attendance projects.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/company/analytics/dashboards/isAllowed`

### Purpose

Checks whether analytics dashboards are allowed for the session.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/company/analytics/diversityEquityAndInclusion/isAllowed`

### Purpose

Checks whether the diversity and inclusion analytics feature is allowed.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/company/workforceplanning/homepage/isAllowed`

### Purpose

Checks whether the workforce planning homepage is allowed.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/compensation/event/compensationFeatureAllowed`

### Purpose

Checks whether the compensation event feature is available.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/docs/esign/templates`

### Purpose

Checks whether e-signature templates are available.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/equity-vesting-schedule/isFeatureAllowed`

### Purpose

Checks whether the equity vesting schedule feature is available.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/import/visible`

### Purpose

Checks whether the import interface is visible.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/notifications`

### Purpose

Checks whether notifications are available.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/reviews/allowed`

### Purpose

Checks whether the reviews feature is available.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/reviews/my-team/allowed`

### Purpose

Checks whether team review information is available.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/sandbox-service/login/allowed`

### Purpose

Checks whether sandbox login is allowed.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/sandbox/visible`

### Purpose

Checks whether the sandbox interface is visible.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/surveys-core/surveys/visible`

### Purpose

Checks whether surveys are visible.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/surveys-core/talent-groups`

### Purpose

Checks whether talent-group survey resources are available.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/talent-events/allowed`

### Purpose

Checks whether talent event actions are allowed.

### Request

#### Query parameters

| Name | Type |
| --- | --- |
| type | string |

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `HEAD /api/workforceplanning/event/isAllowed`

### Purpose

Checks whether workforce planning events are allowed.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `referer`, `x-requested-with`

#### Body

None.

### Response

No body. The status and headers provide the response.

### `POST /api/attendance/employees/{employeeId}/timesheets/{timesheetId}/details`

### Purpose

Accepts a list of requested fields and returns matching policy details and working-pattern information for the timesheet.

### Request

#### Query parameters

None.

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `origin`, `referer`, `x-requested-with`

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.fields | array |
| $.fields[] | string |

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.policyDetails | object |
| $.policyDetails.allowEarlySubmission | boolean |
| $.policyDetails.allowFutureEntries | boolean |
| $.policyDetails.approval | object |
| $.policyDetails.approval.approvalType | string |
| $.policyDetails.breakDeductionSettings | object |
| $.policyDetails.breakDeductionSettings.breakDeductionType | string |
| $.policyDetails.breakDeductionSettings.complianceTracking | object |
| $.policyDetails.breakDeductionSettings.complianceTracking.customBreakRules | array |
| $.policyDetails.breakDeductionSettings.complianceTracking.customBreakRules[] | object |
| $.policyDetails.breakDeductionSettings.complianceTracking.customBreakRules[].id | string |
| $.policyDetails.breakDeductionSettings.complianceTracking.customBreakRules[].penaltyMinutes | integer |
| $.policyDetails.breakDeductionSettings.complianceTracking.customBreakRules[].requirement | object |
| $.policyDetails.breakDeductionSettings.complianceTracking.customBreakRules[].requirement.minimumMinutes | integer |
| $.policyDetails.breakDeductionSettings.complianceTracking.customBreakRules[].requirement.type | string |
| $.policyDetails.breakDeductionSettings.complianceTracking.customBreakRules[].trigger | object |
| $.policyDetails.breakDeductionSettings.complianceTracking.customBreakRules[].trigger.minutesWorked | integer |
| $.policyDetails.breakDeductionSettings.complianceTracking.customBreakRules[].trigger.type | string |
| $.policyDetails.breakDeductionSettings.complianceTracking.customBreakRules[].waiverCondition | array |
| $.policyDetails.breakDeductionSettings.complianceTracking.guidelines | string |
| $.policyDetails.breakDeductionSettings.deductionByMinutesWorked | array |
| $.policyDetails.cycleSettings | object |
| $.policyDetails.cycleSettings.cycleType | string |
| $.policyDetails.cycleSettings.deadline | integer |
| $.policyDetails.cycleSettings.startDay | integer |
| $.policyDetails.dailyEntryAutoFillSettings | null |
| $.policyDetails.description | null |
| $.policyDetails.enforceComment | boolean |
| $.policyDetails.geoFenceSettings | null |
| $.policyDetails.hourTypes | object |
| $.policyDetails.hourTypes.daily | array |
| $.policyDetails.hourTypes.daily[] | object |
| $.policyDetails.hourTypes.daily[].name | string |
| $.policyDetails.hourTypes.daily[].rules | array |
| $.policyDetails.hourTypes.daily[].rules[] | object |
| $.policyDetails.hourTypes.daily[].rules[].countPaidLeaveTowardsOvertimeThreshold | boolean |
| $.policyDetails.hourTypes.daily[].rules[].ruleType | string |
| $.policyDetails.hourTypes.daily[].rules[].tiers | array |
| $.policyDetails.hourTypes.daily[].rules[].tiers[] | object |
| $.policyDetails.hourTypes.daily[].type | string |
| $.policyDetails.name | string |
| $.policyDetails.overtimeSettings | object |
| $.policyDetails.overtimeSettings.allowCarryOver | boolean |
| $.policyDetails.overtimeSettings.calculateOnPaidTime | boolean |
| $.policyDetails.overtimeSettings.dailyUndertimeEnabled | boolean |
| $.policyDetails.overtimeSettings.deductExpectedHoursOnMissingDays | boolean |
| $.policyDetails.overtimeSettings.overtimeType | string |
| $.policyDetails.paidTimeSettings | object |
| $.policyDetails.paidTimeSettings.calendarBankHoliday | boolean |
| $.policyDetails.paidTimeSettings.excludePremiumInRegularHours | boolean |
| $.policyDetails.paidTimeSettings.holidayPremiumPayEnabled | boolean |
| $.policyDetails.paidTimeSettings.paidTimeOff | boolean |
| $.policyDetails.potentialHoursSettings | object |
| $.policyDetails.potentialHoursSettings.includeCalendarEvents | boolean |
| $.policyDetails.timeFormatterType | string |
| $.policyDetails.timesheetReportingMethod | string |
| $.workingPattern | object |
| $.workingPattern.days | object |
| $.workingPattern.days.friday | integer |
| $.workingPattern.days.monday | integer |
| $.workingPattern.days.saturday | integer |
| $.workingPattern.days.sunday | integer |
| $.workingPattern.days.thursday | integer |
| $.workingPattern.days.tuesday | integer |
| $.workingPattern.days.wednesday | integer |
| $.workingPattern.fte | integer |
| $.workingPattern.hoursByOrderedDays | array |
| $.workingPattern.hoursByOrderedDays[] | integer |
| $.workingPattern.hoursPerDay | integer |
| $.workingPattern.weeklyHours | integer |
| $.workingPattern.workingPatternId | integer |
| $.workingPattern.workingPatternType | string |

### `POST /api/company/views/search`

### Purpose

Runs a report search using filters, selected fields, and view settings; the captured response contains employee rows.

### Request

#### Query parameters

| Name | Type |
| --- | --- |
| idsOnly | boolean |

#### Headers

`accept`, `accept-language`, `bob-timezoneoffset`, `content-type`, `datatype`, `origin`, `referer`, `x-requested-with`

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.changes | null |
| $.displayPreferences | object |
| $.displayPreferences.columnWidths | object |
| $.displayPreferences.columnsProperties | array |
| $.displayPreferences.dateFormat | null |
| $.displayPreferences.exportConfiguration | null |
| $.displayPreferences.includeFlatJson | boolean |
| $.displayPreferences.includeHumanReadable | boolean |
| $.displayPreferences.supportErrorWrapping | boolean |
| $.employeeId | string |
| $.fields | array |
| $.fields[] | string |
| $.instructions | array |
| $.instructions[] | object |
| $.instructions[].fieldPath | string |
| $.instructions[].operator | string |
| $.instructions[].values | array |
| $.instructions[].values[] | string |
| $.sortBy | string |
| $.timesheetId | integer |
| $.type | string |

### Response

#### Body

**Media type:** application/json.

**Body schema**

| Field path | Type |
| --- | --- |
| $ | object |
| $.employees | array |
| $.employees[] | object / string |

## Conventions and safety

- `HEAD` endpoints return status and headers without a response body; they are used for capability or visibility checks.
- `POST /api/company/views/search` accepts report filters and selected fields and returns report rows.
- Treat these as private web-app endpoints. Check a copied XHR request before replaying it, and keep session credentials and personal data out of this reference and out of Git.
