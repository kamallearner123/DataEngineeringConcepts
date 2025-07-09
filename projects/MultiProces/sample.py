import multiprocessing
import time

def square_number(n):
    """Function to compute the square of a number"""
    time.sleep(1)  # Simulate a time-consuming task
    return n * n

def main():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    
    # Sequential processing
    # start_time = time.time()
    # sequential_results = [square_number(n) for n in numbers]
    # sequential_time = time.time() - start_time
    # print(f"Sequential results: {sequential_results}")
    # print(f"Sequential time: {sequential_time:.2f} seconds\n")
    
    # input("Please enter to continue....!!!!")
    # # Parallel processing with multiprocessing
    # start_time = time.time()    

    # with multiprocessing.Pool(processes=4) as pool:  # Use 4 processes
    #     parallel_results = pool.map(square_number, numbers) # [1,2]

    # parallel_time = time.time() - start_time
    # print(f"Parallel results: {parallel_results}")
    # print(f"Parallel time: {parallel_time:.2f} seconds")

    p1 = multiprocessing.Process(square_number, args=(numbers[0:2],))
    p1.start()
    p1.join()

if __name__ == "__main__":
    main()