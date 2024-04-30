-- These are scripts that are formatted for accesing the table, more comments can be provided as needed

select count(user_id) from absent_players where user_id = 000000 and has_passed = 1;
-- Select the number of times a user has been absent so far(replace user_ID)

select user_name, reason_ab from absent_players where date_ab = SYSDATE;
-- select users name, reason they're absent today (reoplace date with today's date)

select user_name, date_ab, reason_ab from absent_players where has_passed = 0;
-- selects all future players who are absent, the reason they are, and when they are.

delete from absent_players where user_ID = 00000 and date_ab = date and has_passed = 0;
-- deletes a future absence from the table, cannot remove older absences.