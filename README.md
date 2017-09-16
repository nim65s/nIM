# Nim's Instant Messaging

Matrix.org console client in python with Urwid

## Write a settings.py:

```python
DT_FORMAT = '%H:%M:%S'
ROOM_LIST_WIDTH = 30
CMD_PREFIX = ':'

address = 'https://matrix.org'
login = 'nim65s'
passwd = '<your_password_goes_here>'
chan = '#matrix:matrix.org'  # default chan
```

## Enjoy

`./nim.py`

## Commands

Commands begins with a single `CMD_PREFIX` symbol.

- `n`: next room
- `p`: previous room
- `q`: quit
- `s`: go to system room
