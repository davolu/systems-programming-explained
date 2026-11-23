import ast, sys

def lint(src, filename="<input>"):
    tree = ast.parse(src, filename=filename)
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # missing return: a function with no return and no pass-only body
            returns = [n for n in ast.walk(node) if isinstance(n, ast.Return)]
            if not returns:
                issues.append((node.lineno, f"function {node.name!r} has no return"))
            assigned, used = set(), set()
            for n in ast.walk(node):
                if isinstance(n, ast.Name):
                    if isinstance(n.ctx, ast.Store):
                        assigned.add(n.id)
                    elif isinstance(n.ctx, ast.Load):
                        used.add(n.id)
            for name in sorted(assigned - used):
                if name != "_":
                    issues.append((node.lineno, f"unused variable {name!r} in {node.name!r}"))
    return issues

SAMPLE = """
def add(a, b):
    leftover = a + b
    total = a + b
    return total

def greet(name):
    message = "Hello, " + name
"""

print("sample functions:")
print(SAMPLE)
print("linter findings:")
for lineno, msg in lint(SAMPLE, "sample.py"):
    print(f"  line {lineno}: {msg}")
