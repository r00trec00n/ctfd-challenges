# Solution: Backup Left Behind

Category: Manual Web Assessment
Points: 300

## Flag

`VARE{backups_belong_outside_webroot}`

## Write-up

Request `/robots.txt`, follow the clue to `/maintenance-backups/`, download `portal-backup.zip`, then inspect `portal/.env` for the assessment token.

## Notes

This is an instructor solution. Keep it separate from the student-facing challenge files when distributing the challenge.
