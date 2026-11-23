def greet(name: str) -> str:
    return "Hello, " + name + "!"

print(greet("Maya"))
print(greet(None))                       # mypy should flag this
