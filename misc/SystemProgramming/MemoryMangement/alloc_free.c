# Write simple C code to allocate and free memory using malloc and free functions
#include <stdio.h>
#include <stdlib.h>
int main() {
    // Allocate memory for an integer
    int *ptr = (int *)malloc(sizeof(int));
    
    // Check if memory allocation was successful
    if (ptr == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Assign a value to the allocated memory
    *ptr = 42;
    printf("Value: %d\n", *ptr);

    // Free the allocated memory
    free(ptr);
    
    return 0;
}

