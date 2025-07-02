# SimpleProfiler.py
import time

def some_function_1():
    time.sleep(0.1) # Simulate some work
    sum(range(1000000))

def some_function_2():
    time.sleep(0.05) # Simulate some other work
    [x * x for x in range(500000)]

def main_logic():
    print("Starting main logic...")
    some_function_1()
    some_function_2()
    print("Main logic finished.")

if __name__ == "__main__":
    main_logic()
