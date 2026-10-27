# Solution: Service Inventory

Category: Reconnaissance
Points: 200

## Flag

`VARE{enumeration_beyond_default_ports}`

## Write-up

Use the allocated host and port with `nmap -sV -sC -p PORT HOST` or HTTP metadata scripts. Confirm the service is HTTP and read the page title/metadata.

## Notes

This is an instructor solution. Keep it separate from the student-facing challenge files when distributing the challenge.
