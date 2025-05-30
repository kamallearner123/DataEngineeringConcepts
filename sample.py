import sys

# sys.exit([arg]) - Terminates the interpreter.
# sys.exit(0) # Exits with a success code (0).
# sys.exit("Error: Something went wrong!") # Exits with an error message (non-zero).

# sys.getrecursionlimit() - Gets the maximum recursion depth.
print(f"Current recursion limit: {sys.getrecursionlimit()}")

# sys.setrecursionlimit(limit) - Sets the maximum recursion depth (use with caution).
# sys.setrecursionlimit(2000)
# print(f"New recursion limit: {sys.getrecursionlimit()}")

# sys.getsizeof(object[, default]) - Returns the size of an object in bytes.
my_data = [1, 'hello', 3.14]
print(f"Size of my_data: {sys.getsizeof(my_data)} bytes")

# sys.exc_info() - Returns exception information (type, value, traceback) in an except block.
try:
    result = 1 / 0
except ZeroDivisionError:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print(f"Caught exception type: {exc_type.__name__}")

