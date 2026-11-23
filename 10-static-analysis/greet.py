def greet(name):
    return "Hello, " + name + "!"

print(greet("Maya"))
try:
    print(greet(None))                   # this crashes at runtime
except TypeError as e:
    print("runtime error:", type(e).__name__ + ":", e)
