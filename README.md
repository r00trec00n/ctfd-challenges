# CTFd Challenge Repository

Reusable challenge source for the local CTFd instances. This repository contains challenge definitions, flags, student attachments, and container challenge source only. It does not contain CTFd databases, uploads from the live instances, logs, or runtime state.

## Layout

Every challenge has its own directory under `challenges/` containing:

- `challenge.json` — reusable CTFd metadata and flag
- `files/` — challenge attachments
- `solution.md` — instructor solution/write-up
- `service/` — container source where applicable

The repository currently contains 15 standard challenges and 4 VARE/container challenges.

Keep this repository private if you do not want flags and solutions exposed. The repository is currently public because it is intended as a portfolio, so all flags and write-ups are visible.
