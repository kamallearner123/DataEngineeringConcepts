// TCP server.
// Open different thread for each client connection.
// Keep all the messages in a Queue which is accessed by all threads.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <errno.h>
#define SERVER_PORT 8080
#define BUFFER_SIZE 1024
#define QUEUE_SIZE 10
#define MESSAGE_SIZE 256
typedef struct {
    char messages[QUEUE_SIZE][MESSAGE_SIZE];
    int front;
    int rear;
    pthread_mutex_t mutex;
} MessageQueue;
MessageQueue queue;
void init_queue(MessageQueue *q) {
    q->front = 0;
    q->rear = 0;
    pthread_mutex_init(&q->mutex, NULL);
}
int is_full(MessageQueue *q) {
    return (q->rear + 1) % QUEUE_SIZE == q->front;
}
int is_empty(MessageQueue *q) {
    return q->front == q->rear;
}
void enqueue(MessageQueue *q, const char *message) {
    pthread_mutex_lock(&q->mutex);
    if (!is_full(q)) {
        strncpy(q->messages[q->rear], message, MESSAGE_SIZE - 1);
        q->messages[q->rear][MESSAGE_SIZE - 1] = '\0'; // Ensure null termination
        q->rear = (q->rear + 1) % QUEUE_SIZE;
    } else {
        fprintf(stderr, "Queue is full, message not added: %s\n", message);
    }
    pthread_mutex_unlock(&q->mutex);
}
void dequeue(MessageQueue *q, char *message) {
    pthread_mutex_lock(&q->mutex);
    if (!is_empty(q)) {
        strncpy(message, q->messages[q->front], MESSAGE_SIZE - 1);
        message[MESSAGE_SIZE - 1] = '\0'; // Ensure null termination
        q->front = (q->front + 1) % QUEUE_SIZE;
    } else {
        message[0] = '\0'; // Return empty string if queue is empty
    }
    pthread_mutex_unlock(&q->mutex);
}
void *client_handler(void *arg) {
    int client_sock = *(int *)arg;
    char buffer[BUFFER_SIZE];
    ssize_t bytes_received;

    while ((bytes_received = recv(client_sock, buffer, BUFFER_SIZE - 1, 0)) > 0) {
        buffer[bytes_received] = '\0'; // Null-terminate the received string
        printf("Received message: %s\n", buffer);
        enqueue(&queue, buffer); // Add message to the queue
        send(client_sock, "Message received", 16, 0); // Acknowledge receipt
    }

    if (bytes_received < 0) {
        perror("Receive failed");
    }

    close(client_sock);
    return NULL;
}

int main() {
    int server_sock, client_sock;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len = sizeof(client_addr);
    pthread_t thread_id;

    // Initialize message queue
    init_queue(&queue);

    // Create socket
    server_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (server_sock < 0) {
        perror("Socket creation failed");
        return EXIT_FAILURE;
    }

    // Set up server address structure
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    server_addr.sin_addr.s_addr = INADDR_ANY; // Accept connections from any IP

    // Bind the socket
    if (bind(server_sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        close(server_sock);
        return EXIT_FAILURE;
    }

    // Listen for incoming connections
    if (listen(server_sock, 5) < 0) {
        perror("Listen failed");
        close(server_sock);
        return EXIT_FAILURE;
    }

    printf("Server is listening on port %d...\n", SERVER_PORT);

    while (1) {
        // Accept a new client connection
        client_sock = accept(server_sock, (struct sockaddr *)&client_addr, &addr_len);
        if (client_sock < 0) {
            perror("Accept failed");
            continue; // Continue to accept other clients
        }

        printf("Client connected.\n");

        // Create a new thread for the client
        if (pthread_create(&thread_id, NULL, client_handler, &client_sock) != 0) {
            perror("Thread creation failed");
            close(client_sock);
            continue; // Continue to accept other clients
        }

        pthread_detach(thread_id); // Detach the thread to avoid memory leaks
    }

    close(server_sock);
    return EXIT_SUCCESS;
}

// Compile with: gcc -o socket_server socket_server.c -lpthread
// Run with: ./socket_server
// Ensure you have the pthread library installed on your system.
// This code implements a simple TCP server that handles multiple client connections using threads.
// Each client connection is handled in a separate thread, and messages received from clients are stored in a shared message queue.