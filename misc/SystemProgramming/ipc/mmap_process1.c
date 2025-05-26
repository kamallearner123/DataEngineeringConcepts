# Write an  example of using mmap in C to read and write to a file.
#     <meta charset="UTF-8">


#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>
#include <limits.h>

int main() {
    const char *filename = "example.txt";
    int fd;
    struct stat sb;
    char *mapped;

    // Open the file
    fd = open(filename, O_RDWR);
    if (fd == -1) {
        perror("Error opening file");
        return EXIT_FAILURE;
    }
    // Get the size of the file
    if (fstat(fd, &sb) == -1) {
        perror("Error getting file size");
        close(fd);
        return EXIT_FAILURE;
    }
    // Map the file into memory
    mapped = mmap(NULL, sb.st_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (mapped == MAP_FAILED) {
        perror("Error mapping file");
        close(fd);
        return EXIT_FAILURE;
    }
    // Write to the mapped memory
    const char *text = "Hello, mmap!";
    size_t text_len = strlen(text);
    if (text_len > sb.st_size) {
        fprintf(stderr, "Text is too long for the file\n");
        munmap(mapped, sb.st_size);
        close(fd);
        return EXIT_FAILURE;
    }
    memcpy(mapped, text, text_len);
    // Print the content of the mapped memory
    printf("Mapped content: %s\n", mapped);
    // Unmap the memory
    if (munmap(mapped, sb.st_size) == -1) {
        perror("Error unmapping memory");
        close(fd);
        return EXIT_FAILURE;
    }
    // Close the file descriptor
    if (close(fd) == -1) {
        perror("Error closing file");
        return EXIT_FAILURE;
    }
    printf("File updated successfully.\n");
    return EXIT_SUCCESS;

}
// Compile with: gcc -o mmap_example mmap.c -lrt
// Run with: ./mmap_example
// Ensure the file "example.txt" exists and has some content before running the program.
