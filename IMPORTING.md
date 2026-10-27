# Importing Challenges into CTFd

The repository supports importing one challenge or the complete collection.

The importer uses the CTFd API, creates challenges hidden by default, adds flags and attachments, and verifies existing flags instead of silently replacing them.

## Requirements

- Python 3
- CTFd administrator API token
- CTFd URL
- For container challenges: the required container image must already exist on the Docker daemon controlled by CTFd and the containers plugin must be installed.

Never commit or paste the API token into the repository.

## 1. Create an API token

In CTFd:

1. Sign in as an administrator.
2. Open the account settings page.
3. Create an API key/token.
4. Copy it temporarily. The importer asks for it through a masked prompt.

## 2. Validate the repository first

From the repository root:

```bash
cd /home/r00trec00n/ctfd-challenges
python3 tools/import_ctfd.py --url http://127.0.0.1 --all --dry-run
```

For the second local instance:

```bash
python3 tools/import_ctfd.py --url http://127.0.0.1:8081 --all --dry-run
```

The dry run checks every `challenge.json` and every referenced attachment without contacting CTFd.

## 3. Import every challenge

Import everything into the main instance and leave it hidden:

```bash
python3 tools/import_ctfd.py \
  --url http://127.0.0.1 \
  --all
```

Import everything into the VARE instance:

```bash
python3 tools/import_ctfd.py \
  --url http://127.0.0.1:8081 \
  --all
```

The script asks for the API token and prints the CTFd ID for each imported challenge.

## 4. Import one challenge

Use the directory slug:

```bash
python3 tools/import_ctfd.py \
  --url http://127.0.0.1 \
  --challenge out-of-sight
```

Container example:

```bash
python3 tools/import_ctfd.py \
  --url http://127.0.0.1:8081 \
  --challenge service-inventory
```

You can also use the exact challenge name:

```bash
python3 tools/import_ctfd.py \
  --url http://127.0.0.1 \
  --challenge "Reverse the Recipe"
```

## 5. Publish after verification

The default behavior keeps imported challenges hidden. After checking the flag, attachment, description, and challenge settings, publish explicitly:

```bash
python3 tools/import_ctfd.py \
  --url http://127.0.0.1 \
  --challenge out-of-sight \
  --publish
```

For all challenges:

```bash
python3 tools/import_ctfd.py \
  --url http://127.0.0.1 \
  --all \
  --publish
```

Use `--publish` only after testing. Existing challenges with an unexpected flag are rejected rather than overwritten.

## Container challenge preparation

Before importing a container challenge, build its service image using the Dockerfile inside that challenge directory. For example:

```bash
cd challenges/container/service-inventory/service
docker build -t vare-quiz2-recon:1.0 .
```

The image tag must match the `image` value in that challenge's `challenge.json`.

Build the other services similarly:

```bash
cd challenges/container/backup-left-behind/service
docker build -t vare-quiz2-web:1.0 .

cd ../../internal-cache/service
docker build -t vare-quiz2-redis:1.0 .
```

Then verify that the CTFd containers plugin can access the same Docker daemon. The CTFd service normally needs access to `/var/run/docker.sock`, which is a powerful host-level permission and should only be used in an isolated, trusted CTF deployment.

`evidence-trail` is a standard file-based challenge and does not require a container image.

## What the importer does

For each challenge, the importer:

1. Loads `challenge.json`.
2. Finds an existing challenge by exact name.
3. Creates it as hidden if it does not exist.
4. Refuses to overwrite an unexpected existing flag.
5. Adds the static case-sensitive flag if missing.
6. Adds missing attachments by filename.
7. Keeps the challenge hidden unless `--publish` is supplied.

The importer is intended to be repeatable. Running it again should skip matching flags and attachments rather than create duplicates.

## Troubleshooting

`HTTP 401` or `HTTP 403`:

- Confirm the token belongs to an administrator.
- Confirm the URL points to the CTFd application, not only a reverse proxy path.
- Create a new token and retry.

`Existing challenge type differs`:

- The target already contains a challenge with the same name but a different type.
- Do not delete it automatically. Rename the source challenge or resolve the conflict manually in CTFd.

`Refusing to overwrite an unexpected existing flag`:

- The target challenge already has a different flag.
- Check whether it is the intended challenge before changing anything.

Container challenge starts but is unreachable:

- Confirm the image exists on the Docker daemon used by CTFd.
- Confirm the image tag matches `challenge.json`.
- Confirm the containers plugin is installed and configured.
- Confirm the advertised hostname is reachable by students; do not use `127.0.0.1` for remote students.
