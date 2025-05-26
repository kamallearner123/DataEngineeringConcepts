// Demonstrate a memory management issue in C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

void access_out_of_boundary() {
    // Allocate memory for an array of integers
    int *arr = (int *)malloc(5 * sizeof(int));
    if (arr == NULL) {
        perror("Memory allocation failed");
        return EXIT_FAILURE;
    }

    // Initialize the array
    for (int i = 0; i < 5; i++) {
        arr[i] = i * 10;
    }

    // Intentionally cause a memory management issue by accessing out of bounds
    printf("Accessing out of bounds: %d\n", arr[10]); // This will cause undefined behavior

    // Free the allocated memory
    free(arr);

    return;
}

// Function to demonstrate memory leak
void memory_leak() {
    // Allocate memory without freeing it
    char *leak = (char *)malloc(100 * sizeof(char));
    if (leak == NULL) {
        perror("Memory allocation failed");
        return;
    }

    // Use the allocated memory
    strcpy(leak, "This is a memory leak example.");
    printf("%s\n", leak);

    // Forget to free the allocated memory
    // free(leak); // Uncommenting this line would fix the leak

    return;
}

// Function to demonstrate double free
void double_free() {
    // Allocate memory
    char *data = (char *)malloc(50 * sizeof(char));
    if (data == NULL) {
        perror("Memory allocation failed");
        return;
    }

    // Use the allocated memory
    strcpy(data, "This is a double free example.");
    printf("%s\n", data);

    // Free the allocated memory
    free(data);

    // Intentionally free the same memory again
    free(data); // This will cause undefined behavior

    return;
}

// Function to demonstrate use after free
void use_after_free() {
    // Allocate memory
    int *num = (int *)malloc(sizeof(int));
    if (num == NULL) {
        perror("Memory allocation failed");
        return;
    }

    // Assign a value
    *num = 42;
    printf("Value before free: %d\n", *num);

    // Free the allocated memory
    free(num);

    // Intentionally access the freed memory
    printf("Value after free: %d\n", *num); // This will cause undefined behavior

    return;
}


// Main function to demonstrate memory management issues
int main() {
    printf("Demonstrating access out of boundary:\n");
    access_out_of_boundary();

    printf("\nDemonstrating memory leak:\n");
    memory_leak();

    printf("\nDemonstrating double free:\n");
    double_free();

    printf("\nDemonstrating use after free:\n");
    use_after_free();

    return 0;
}