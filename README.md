# CTFd Challenge Repository

Reusable challenge collection for CTFd. Each challenge is stored independently so it can be copied, reviewed, imported, or added manually without rebuilding it from memory.

This repository currently contains:

- 15 standard challenges
- 4 container/VARE challenges
- Challenge metadata and flags
- Student attachments
- Container Dockerfiles and service source
- Instructor solution/write-up for every challenge
- An API importer for one challenge or the complete collection

Important: this repository is public, so the flags and `solution.md` files are public. Do not use this repository as a student distribution package without removing or separating the instructor material.

## Repository layout

```text
challenges/
├── standard/
│   ├── out-of-sight/
│   │   ├── challenge.json
│   │   ├── files/
│   │   └── solution.md
│   └── ...
└── container/
    ├── service-inventory/
    │   ├── challenge.json
    │   ├── service/
    │   └── solution.md
    └── ...

tools/import_ctfd.py       # API importer
IMPORTING.md                # API and container import instructions
```

Each `challenge.json` contains the CTFd name, category, description, points, type, flag, and attachment list. The `files/` directory contains only student-facing attachments. The `solution.md` file is instructor material.

## Quick start: import with the script

From the repository root:

```bash
cd /home/r00trec00n/ctfd-challenges
```

Validate all challenges without contacting CTFd:

```bash
python3 tools/import_ctfd.py \
  --url http://127.0.0.1 \
  --all \
  --dry-run
```

Import all challenges into CTFd and keep them hidden:

```bash
python3 tools/import_ctfd.py \
  --url http://127.0.0.1 \
  --all
```

Import one challenge:

```bash
python3 tools/import_ctfd.py \
  --url http://127.0.0.1 \
  --challenge out-of-sight
```

After testing, publish one challenge:

```bash
python3 tools/import_ctfd.py \
  --url http://127.0.0.1 \
  --challenge out-of-sight \
  --publish
```

The script asks for the CTFd administrator API token using a masked prompt. Never place the token in Git, a shell command, or a public issue.

For complete API instructions, see [IMPORTING.md](IMPORTING.md).

## Add a challenge manually in the CTFd web interface

Use this method when you want to add only one challenge or when the API importer is not available.

### Step 1: choose the challenge

Open a challenge directory under:

```text
challenges/standard/<challenge-slug>/
```

or:

```text
challenges/container/<challenge-slug>/
```

Read `challenge.json`. Copy these fields into CTFd:

- `name` → Challenge name
- `category` → Category
- `description` → Description
- `value` → Initial points/value
- `flag` → Flag content
- `files/` → Attachments

Keep `solution.md` private. Do not upload it to CTFd as a student attachment.

### Step 2: open the CTFd administrator panel

1. Sign in to CTFd as an administrator.
2. Open the admin panel.
3. Open **Challenges**.
4. Select **Create Challenge**.
5. Choose **Standard** for a file-based challenge.
6. Choose the container/plugin challenge type for a container challenge.

The exact labels can differ slightly depending on the CTFd version and installed plugins.

### Step 3: create a standard challenge

For a challenge such as `out-of-sight`:

1. Open `challenges/standard/out-of-sight/challenge.json`.
2. Set the challenge name to the JSON `name` value.
3. Set the category to the JSON `category` value.
4. Copy the JSON `description` into the description editor.
5. Set the value/points from the JSON `value` field.
6. Set the challenge state to **Hidden** while configuring it.
7. Add a **Static** flag.
8. Copy the JSON `flag` value exactly, including `SCSS{...}` and capitalization.
9. Set the flag to case-sensitive if CTFd provides that option.
10. Open the challenge directory's `files/` folder.
11. Upload every file listed in the JSON `files` array.
12. Save the challenge.
13. Open the saved challenge again and verify the description, points, flag, and attachments.
14. Test the student solve path with a student account or preview.
15. Change the state to **Visible** only after verification.

Example:

```text
Directory: challenges/standard/out-of-sight/
Attachment: files/workspace.zip
Flag: SCSS{hidden_paths_found}
```

### Step 4: create a container challenge

Container challenges require the installed CTFd containers plugin and a Docker image available to the Docker daemon controlled by CTFd.

1. Open the selected container directory.
2. Read `challenge.json`.
3. Build the image from the `service/` directory using the tag in the JSON `image` field.
4. In CTFd, choose the container challenge type.
5. Set the name, category, description, and value from `challenge.json`.
6. Set the image name/tag exactly as shown in the JSON `image` field.
7. Set the internal port from the JSON `port` field.
8. Set the connection type from the JSON `ctype` field.
9. Leave volumes empty unless the challenge explicitly requires them.
10. Set the command required by the image/plugin configuration.
11. Add the static case-sensitive flag from the JSON `flag` field.
12. Keep the challenge hidden.
13. Start an instance and verify that the displayed host and port are reachable.
14. Test the intended student path.
15. Publish only after the instance, flag, and reset behavior work correctly.

Do not use `127.0.0.1` as the advertised host when students connect from other machines. The CTFd host must advertise a reachable lab IP or DNS name.

### Step 5: add hints manually

The current challenge JSON files contain the core challenge data. If a hint is needed, copy it from the corresponding instructor/setup material or add a short student-safe hint manually in CTFd.

Do not paste the solution path, final flag, or instructor marking notes into a public hint.

## Recommended workflow

```text
1. Create or edit one challenge directory.
2. Update challenge.json.
3. Put student attachments in files/.
4. Put the private solution in solution.md.
5. Test the attachment and solve path.
6. Run the dry-run importer.
7. Import hidden.
8. Verify the CTFd record.
9. Test as a student.
10. Publish.
11. Commit the change to Git.
```

## Safety and backup notes

This repository is a challenge-source backup, not a complete CTFd instance backup. It does not contain users, scores, solve history, CTFd settings, or the complete database.

The repository includes flags and instructor solutions. Keep a private copy if you need the material for teaching, and create a separate sanitized student repository if you want students to access the portfolio.
