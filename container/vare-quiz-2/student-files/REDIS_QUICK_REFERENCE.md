# Redis command reference
Redis stores named keys and values. You are not expected to memorize its syntax.
Use the host and port shown for your own running challenge instance.

```sh
redis-cli -h HOST -p PORT
```

At the Redis prompt:

- `PING` checks whether the service responds.
- `INFO server` reports server information.
- `SCAN 0` returns a cursor and some key names. Repeat SCAN with the returned cursor until it is 0; one reply need not include all keys.
- `GET key_name` reads a string value. Replace key_name with an actual key from your results.
- `QUIT` exits.

Do not supply credentials unless the challenge explicitly gives them. Record whether a new unauthenticated connection can read internal records. Do not change/delete data.
If redis-cli is missing in Kali, ask the instructor to install the redis-tools package before the quiz.
