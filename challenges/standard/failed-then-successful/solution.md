# Solution: Failed, Then Successful

Category: Forensics
Points: 200

## Flag

`SCSS{203.0.113.77_admin}`

## Write-up

Sort auth.log chronologically, group failures by source and username, then identify the source with at least five failures followed by a successful login.

## Verification

The expected flag is case-sensitive. Preserve the exact braces, capitalization, punctuation, and separators when submitting it to CTFd.
