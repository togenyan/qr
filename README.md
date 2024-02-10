# qr.py

## Usage

```text
$ python ./qr.py TOGENYN
/TOGENYNVGMLSCQ89RL91V4LDP4MIRFQS8
```

## Format

### v1

```text
http://.../XX YYYY ZZZZZZZZZZZZZZZZZZZZZZZZZZZ
           ~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~
           ^  ^    ^
           |  |    |
           |  |    `------ hash (26 base32 chars = 130bit)
           |  `----------- variation
           `-------------- type (base36)
```

### v2

```text
http://.../XXX YYYY ZZZZZZZZZZZZZZZZZZZZZZZZZZZ
           ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~
           ^   ^    ^
           |   |    |
           |   |    `------ hash (26 base32 chars = 130bit)
           |   `----------- variation
           `--------------- type (base36)
```

## Hash calculation

```text
    "XXYYYY" or "XXXYYYY"
             ↓
        +----------+
        | HMAC-MD5 | ← key1
        +----------+
             ↓
        +----------+
        | Hexlify  |
        +----------+
             ↓
        +----------+
        | HMAC-MD5 | ← key2
        +----------+
             ↓
    +-----------------+
    | Modified Base32 |
    +-----------------+
             ↓
"ZZZZZZZZZZZZZZZZZZZZZZZZZZ"
```
