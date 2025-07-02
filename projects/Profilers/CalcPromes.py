# my_app.py
import time
import math
import random

def calculate_primes_up_to_n(n):
    """Calculates prime numbers up to n using a basic algorithm."""
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

def process_data_items(data_size):
    """Simulates processing a list of data items."""
    data = [random.randint(1, 1000) for _ in range(data_size)]
    processed_data = []
    for item in data:
        time.sleep(0.00001) # Simulate some I/O or small delay
        processed_data.append(item * 2 + 5)
    return processed_data

def expensive_computation():
    """A function that performs a CPU-bound, expensive computation."""
    result = 0
    for i in range(10**7):
        result += i * i / (i + 1) # A slightly complex arithmetic operation
    return result

def run_application():
    """The main entry point of our simulated application."""
    print("Application started...")
    print("Step 1: Calculating primes...")
    primes = calculate_primes_up_to_n(1000) # This will be moderately slow

    print("Step 2: Processing data items...")
    processed = process_data_items(50000) # This will involve many small operations

    print("Step 3: Performing expensive computation...")
    comp_result = expensive_computation() # This will be CPU intensive

    print(f"Application finished. Found {len(primes)} primes, processed {len(processed)} items, computation result: {comp_result:.2f}")

if __name__ == "__main__":
    run_application()
