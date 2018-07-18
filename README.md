# Nim's Instant Messaging

Matrix.org console client in python with Urwid

## dependencies

- `urwid`
- `matrix-client`

You can install them by running `pip install -r requirements.txt`.  
In order to use experimental end-to-end encryption support, do `pip install -r requirements_e2e.txt --process-dependency-links`.

## Write a `settings.py` file:

```python
DT_FORMAT = '%H:%M:%S'
ROOM_LIST_WIDTH = 30
CMD_PREFIX = ':'

address = 'https://matrix.org'
login = 'nim65s'
passwd = '<your_password_goes_here>'
chan = '#matrix:matrix.org'  # default chan
device_id = None # specifying a device_id is important if you intend to use E2E
encryption = False # True enables automatic E2E support
```

## Enjoy

`./nim.py`

## Commands

Commands begins with a single `CMD_PREFIX` symbol.

- `n`: next room
- `p`: previous room
- `q`: quit
- `s`: go to system room

## Contribute

This clients lacks a few basic features, that are not hard to implement, like:

- shortcuts for commands
- better configuration file
- colors
- unread messages count / indicators
- group/reorder chans
- multi accounts
- other protocols

If someone opens an issue to ask for this kind of stuff, I can do it.
