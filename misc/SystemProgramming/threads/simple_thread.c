// Create a simple thread using pthreads in C
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
void *thread_function(void *arg) {
    int *num = (int *)arg;
    printf("Thread is running. Received number: %d\n", *num);
    sleep(1); // Simulate some work
    printf("Thread finished execution.\n");
    return NULL;
}
int main() {
    pthread_t thread;
    int number = 42;

    // Create a new thread
    if (pthread_create(&thread, NULL, thread_function, &number) != 0) {
        perror("Failed to create thread");
        return EXIT_FAILURE;
    }

    // Wait for the thread to finish
    if (pthread_join(thread, NULL) != 0) {
        perror("Failed to join thread");
        return EXIT_FAILURE;
    }

    printf("Main thread finished execution.\n");
    return EXIT_SUCCESS;
}
// Compile with: gcc -o simple_thread simple_thread.c -lpthread
// Run with: ./simple_thread
// Ensure you have the pthread library installed on your system.
// This code demonstrates the creation and execution of a simple thread using the pthreads library in C.
// It includes error handling for thread creation and joining, and simulates some work in the thread function.