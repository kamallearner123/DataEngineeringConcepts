import datetime
import random

def generate_huge_log(num_entries=100000, filename="huge_test_log.txt"):
    """
    Generates a large test log file with entries following the specified format.

    Args:
        num_entries (int): The number of log entries to generate.
        filename (str): The name of the file to save the logs to.
    """
    components = [
        "NetworkManager", "DiskMonitor", "USBDriver", "FileSystem",
        "DatabaseService", "SecurityAgent", "WebServer", "APIGateway",
        "LoadBalancer", "CacheService", "AuthService", "BillingEngine"
    ]
    statuses = ["SUCCESS", "FAIL"]
    fail_errors = [1001, 1002, 1003, 2001, 2002, 2003, 3001, 3002, 3003, 4001, 4002, 5001, 5002]

    # Start from a time slightly before the current time
    # To simulate events leading up to now
    current_time = datetime.datetime.now() - datetime.timedelta(days=10) # Start 10 days ago for more variety

    print(f"Generating {num_entries} log entries. This might take a moment...")

    with open(filename, 'w') as f:
        for i in range(num_entries):
            # Increment time by a random interval (1 second to 5 minutes)
            current_time += datetime.timedelta(seconds=random.randint(1, 300))

            component = random.choice(components)
            status = random.choice(statuses)

            error_code = 0
            if status == "FAIL":
                error_code = random.choice(fail_errors)

            log_entry = (
                f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"COMPONENT:{component} "
                f"STATUS:{status} "
                f"ERROR:{error_code}\n"
            )
            f.write(log_entry)

            if (i + 1) % 10000 == 0:
                print(f"Generated {i + 1}/{num_entries} entries...")

    print(f"\nSuccessfully generated {num_entries} log entries in '{filename}'")

# Generate a log file with 100,000 entries
generate_huge_log(num_entries=100000)

# To give you a preview, I'll print the first 10 and last 10 lines
print("\n--- First 10 lines of the generated log ---")
with open("huge_test_log.txt", 'r') as f:
    for i, line in enumerate(f):
        if i < 10:
            print(line.strip())
        else:
            break

print("\n--- Last 10 lines of the generated log (approx) ---")
# For large files, reading from the end is more complex.
# We'll just read the whole file and take the last 10 for demonstration.
with open("huge_test_log.txt", 'r') as f:
    lines = f.readlines()
    for line in lines[-10:]:
        print(line.strip())