import random
import secrets

_chars = 'abcdefghijkmnopqrstuvwxyz23456789ABCDEFGHIJKLMNPQRSTUVWXYZ'

def _char(byte):
    dx = int(byte) % 64
    if dx >= 58:
        dx = random.randint(0, 57)

    return _chars[dx]

def base58gen(n=24):
    return ''.join(map(_char, secrets.token_bytes(n)))
