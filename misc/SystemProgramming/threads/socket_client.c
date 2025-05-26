// TCP client example
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <errno.h>
#define SERVER_PORT 8080
#define BUFFER_SIZE 1024
int main() {
    int sockfd;
    struct sockaddr_in server_addr;
    char buffer[BUFFER_SIZE];

    // Create socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("Socket creation failed");
        return EXIT_FAILURE;
    }

    // Set up server address structure
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // Localhost
    // Connect to the server
    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Connection failed");
        close(sockfd);
        return EXIT_FAILURE;
    }
    // Send a message to the server
    const char *message = "Hello, Server!";
    if (send(sockfd, message, strlen(message), 0) < 0) {
        perror("Send failed");
        close(sockfd);
        return EXIT_FAILURE;
    }
    // Receive a response from the server
    ssize_t bytes_received = recv(sockfd, buffer, BUFFER_SIZE - 1, 0);
    if (bytes_received < 0) {
        perror("Receive failed");
        close(sockfd);
        return EXIT_FAILURE;
    }
    buffer[bytes_received] = '\0'; // Null-terminate the received string
    printf("Server response: %s\n", buffer);
    // Close the socket
    close(sockfd);
    return EXIT_SUCCESS;
}
// Compile with: gcc -o socket_client socket_client.c
// Run with: ./socket_client
// Ensure you have a server running on the specified port (8080) to test this client.