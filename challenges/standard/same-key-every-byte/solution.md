# Solution: Same Key, Every Byte

Category: Crypto
Points: 200

## Flag

`SCSS{known_plaintext_breaks_xor}`

## Write-up

Use the known plaintext prefix to derive the repeating eight-byte XOR key, decrypt report.enc.txt, and read the flag from the plaintext.

## Verification

The expected flag is case-sensitive. Preserve the exact braces, capitalization, punctuation, and separators when submitting it to CTFd.
