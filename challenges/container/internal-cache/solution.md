# Solution: Internal Cache

Category: Manual Infrastructure Assessment
Points: 300

## Flag

`VARE{no_password_no_privacy}`

## Write-up

Connect with `redis-cli -h HOST -p PORT`, run `PING`, `SCAN 0` until the cursor is zero, then read `GET lab:internal:assessment`.

## Notes

This is an instructor solution. Keep it separate from the student-facing challenge files when distributing the challenge.
