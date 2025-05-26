# Read the data from the file using mmap

#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>

int main() {
    const char *filename = "example.txt";
    int fd;
    struct stat sb;
    char *mapped;

    // Open the file
    fd = open(filename, O_RDONLY);
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
    mapped = mmap(NULL, sb.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (mapped == MAP_FAILED) {
        perror("Error mapping file");
        close(fd);
        return EXIT_FAILURE;
    }

    // Print the content of the mapped memory
    printf("Mapped content: %.*s\n", (int)sb.st_size, mapped);

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

    return EXIT_SUCCESS;
}