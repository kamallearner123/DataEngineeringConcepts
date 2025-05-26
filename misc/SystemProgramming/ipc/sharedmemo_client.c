// Shared memory client example
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <errno.h>
#define SHM_SIZE 1024 // Size of shared memory segment
int main() {
    int shm_id;
    char *shm_ptr;

    // Create a unique key for the shared memory segment
    key_t key = ftok("shmfile", 65);
    if (key == -1) {
        perror("ftok failed");
        return EXIT_FAILURE;
    }

    // Create the shared memory segment
    shm_id = shmget(key, SHM_SIZE, 0666 | IPC_CREAT);
    if (shm_id == -1) {
        perror("shmget failed");
        return EXIT_FAILURE;
    }

    // Attach the shared memory segment
    shm_ptr = shmat(shm_id, NULL, 0);
    if (shm_ptr == (char *)(-1)) {
        perror("shmat failed");
        return EXIT_FAILURE;
    }

    // Read data from the shared memory
    printf("Data read from shared memory: %s\n", shm_ptr);

    // Detach the shared memory segment
    if (shmdt(shm_ptr) == -1) {
        perror("shmdt failed");
        return EXIT_FAILURE;
    }

    // Optionally, remove the shared memory segment
    if (shmctl(shm_id, IPC_RMID, NULL) == -1) {
        perror("shmctl failed");
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}

// Compile with: gcc -o sharedmemo_client sharedmemo_client.c
// Run with: ./sharedmemo_client
// Ensure you have a shared memory segment created by a corresponding server process.
// This code demonstrates a simple client that reads data from a shared memory segment.
// It creates a unique key for the shared memory, attaches to it, reads data, and then detaches and removes the segment.