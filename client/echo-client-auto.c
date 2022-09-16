#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
 
int main() {
    printf("Starting client...");
    int socket_fd, i, port = 2048;
    struct sockaddr_in serv_addr;
    char received_str[100], send_str[100] = "Hello Server";
 
    socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    bzero(&serv_addr, sizeof serv_addr);
 
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(port);
 
    inet_pton(AF_INET, "127.0.0.1", &(serv_addr.sin_addr));
    connect(socket_fd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
 
    for(i=0; i<1000; i++) {
        bzero(received_str, 100);
        write(socket_fd, send_str, strlen(send_str)+1);
        printf("Sent: %s", send_str);
        read(socket_fd, received_str, 100);
        printf("\tReceived: %s\n", received_str);
    }
    // printf(i);
}