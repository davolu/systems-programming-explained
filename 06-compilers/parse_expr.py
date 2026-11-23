import re

TOKEN_SPECS = [
    ("NUMBER", r"\d+"),
    ("PLUS",   r"\+"),
    ("STAR",   r"\*"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("SKIP",   r"[ \t]+"),
]
TOKEN_RE = re.compile("|".join(f"(?P<{n}>{p})" for n, p in TOKEN_SPECS))

def lex(src):
    tokens, pos = [], 0
    for m in TOKEN_RE.finditer(src):
        if m.start() != pos:
            raise SyntaxError(f"unexpected {src[pos]!r} at {pos}")
        kind = m.lastgroup
        if kind != "SKIP":
            value = int(m.group()) if kind == "NUMBER" else m.group()
            tokens.append((kind, value))
        pos = m.end()
    if pos != len(src):
        raise SyntaxError(f"unexpected {src[pos]!r} at {pos}")
    tokens.append(("EOF", None))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens, self.i = tokens, 0
    def peek(self): return self.tokens[self.i][0]
    def eat(self, kind=None):
        tok = self.tokens[self.i]
        if kind and tok[0] != kind:
            raise SyntaxError(f"expected {kind}, got {tok}")
        self.i += 1
        return tok
    def expr(self):                       # term { "+" term }
        node = self.term()
        while self.peek() == "PLUS":
            self.eat("PLUS")
            node = ("+", node, self.term())
        return node
    def term(self):                       # factor { "*" factor }
        node = self.factor()
        while self.peek() == "STAR":
            self.eat("STAR")
            node = ("*", node, self.factor())
        return node
    def factor(self):                     # NUMBER | "(" expr ")"
        if self.peek() == "NUMBER":
            return ("num", self.eat("NUMBER")[1])
        self.eat("LPAREN"); node = self.expr(); self.eat("RPAREN")
        return node

def pretty(node, prefix="", last=True):
    kind = node[0]
    label = str(node[1]) if kind == "num" else kind
    branch = "└─ " if last else "├─ "
    print(prefix + (branch if prefix else "") + label)
    if kind != "num":
        child = prefix + ("   " if last else "│  ")
        pretty(node[1], child, False)
        pretty(node[2], child, True)

src = "2 + 3 * 4"
tokens = lex(src)
print("tokens:")
for t in tokens: print(f"  {t}")
print("tree:")
pretty(Parser(tokens).expr())
