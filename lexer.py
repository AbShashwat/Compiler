import re

TOKEN_SPEC = [
    ("CREATE", r'create'),
    ("WEBPAGE", r'webpage'),
    ("ADD", r'add'),
    ("HEADER", r'header'),
    ("FILE", r'[A-Za-z0-9_\-/]+\.(png|jpg|jpeg|gif)'),
    ("IMAGE", r'image'),   
    ("LINK", r'link'),
    ("FOOTER", r'footer'),
    ("SOURCE", r'source'),
    ("ALT", r'alt'),
    ("TEXT", r'text'),
    ("URL", r'https?://[^\s]+'),
    ("STRING", r'"[^"]*"'),
    ("WORD", r'[A-Za-z]+'),
    ("NEWLINE", r'\n'),
    ("SKIP", r'[ \t]+')
]

STOPWORDS = {"a", "an", "the", "to", "with","and"}

token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)


def lexer(code):

    tokens = []

    for match in re.finditer(token_regex, code.lower()):

        kind = match.lastgroup
        value = match.group()

        if kind == "SKIP":
            continue

        if kind == "WORD" and value in STOPWORDS:
            continue

        tokens.append({
            "type": kind,
            "value": value
        })

    return tokens