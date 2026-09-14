---
name: weekly-attendance-check-in
description: Find and submit attendance records for a requested Monash teaching week by discovering current units from the Attendance portal and matching official Moodle, Ed, and university email evidence.
---

# Weekly Attendance Check-In

Use the user's authenticated course sources to resolve one requested teaching week and complete only the matching attendance entries. Discover the current semester's units from the live Attendance portal; do not depend on a saved unit list, course identifier, or source URL.

## Authorization and scope

- Treat `submit`, `fill`, `check in`, or an equivalent direct instruction as authorization to submit the entries in the stated week and course scope. Do not ask for a redundant confirmation.
- A request only to check, find, list, or review codes is read-only. Prepare the mapping, but do not submit until the user explicitly asks.
- Resolve the target from an explicit week/date first, then a clearly selected Attendance week, otherwise the user's current local teaching week. Before submission, make the exact date range unambiguous.
- Never reuse a code from another week or retain attendance codes in a skill, repository, or memory. Use codes only for the current task and omit them from the final report unless the user asks to see them.

## Build the attendance inventory

1. Open Monash Attendance and treat its requested-week view as the authoritative inventory of current units. Enumerate every visible activity in scope and capture the date, displayed unit code and title, activity type, group, current status, and entry URL or identifier.
2. Separate entries that need a student code from entries already recorded, unavailable, cancelled, or explicitly handled by teaching staff. A presentation week or teacher-recorded activity is excluded only when an official course source says so.
3. Work from this inventory rather than assuming the user's normal timetable or a fixed number of weekly activities.

## Find and verify codes

For each unit discovered in Attendance:

1. Build search keys from the live unit code/title, current teaching period, campus, week/date, activity, and group.
2. Identify the corresponding current-semester Moodle unit from the authenticated dashboard or search results; do not reuse a stored Moodle course ID or section number.
3. Identify the corresponding active Ed course from the user's current course list; do not assume a same-named offering from another campus or semester is correct.
4. Search relevant university email using the live unit code plus the week/date or activity name.
5. Inspect the matching Moodle week, current Ed announcements, and course email as available. Let current official course communications establish which source normally carries that unit's codes; use the other sources for fallback or confirmation rather than hard-coding a unit-specific priority.

Accept a code only when the source matches all applicable fields: unit and campus, teaching week, exact date, activity type, and group/session. Inspect attached code images at readable size; ambiguous characters are not verified. If sources conflict or all official sources lack a current-week code, leave the entry untouched and mark it unresolved.

Do not infer a code from a timetable, an older post, another campus, another session, or a visually similar value.

## Submit and verify

For an authorized submission request:

1. Submit one verified entry at a time.
2. After each submission, confirm the form returned to the Attendance overview and that the entry is now recorded or no longer offers the same entry action.
3. If the form remains open or shows `Incorrect code`, stop attempts on that entry and reopen the exact official source. Retry only when a demonstrable transcription error is corrected; never cycle through guesses or older codes.
4. Continue with other independently verified entries when safe. Re-enumerate the overview at the end and leave it open for the user.

## Browser reliability

- Prefer the user's existing authenticated browser session. If a Moodle CLI or connector is unauthenticated, fall back to the authenticated browser without copying cookies or credentials.
- Reacquire tabs and accessibility state after navigation, timeout, or DOM change. Match a browser tab by its fresh numeric ID, exact title, and URL; do not rely on a stale `providerTabId` or accessibility index.
- Scope Ed searches to the relevant course and thread list. Distinguish similarly named campus and semester offerings before accepting evidence.

## Report the outcome

State the exact week/date range, how many entries were submitted and verified, which were already recorded or officially excluded, and every unresolved entry with the sources checked and reason. Treat a rejected code as unresolved, never as attendance recorded. Report an overall attendance-rate change only when it was observed on the final overview.
