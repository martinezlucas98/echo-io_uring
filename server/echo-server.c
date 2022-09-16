#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT_NUMBER         2048
#define BACKLOG             512
#define MAX_MESSAGE_LEN     2048

int main(int argc, char *argv[]) {
    char received_str[MAX_MESSAGE_LEN];
    int comm_fd, port_number = PORT_NUMBER;
    struct sockaddr_in serv_addr;

    int sock_listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    const int val = 1;
    setsockopt(sock_listen_fd, SOL_SOCKET, SO_REUSEADDR, &val, sizeof(val));

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(port_number);
    serv_addr.sin_addr.s_addr = INADDR_ANY;

    bind(sock_listen_fd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    listen(sock_listen_fd, BACKLOG);
    printf("echo server listening for connections on port: %d\n", port_number);
 
    comm_fd = accept(sock_listen_fd, (struct sockaddr*) NULL, NULL);
    
    while(1) {
        bzero(received_str, MAX_MESSAGE_LEN);
        read(comm_fd, received_str, MAX_MESSAGE_LEN);
        write(comm_fd, received_str, strlen(received_str)+1);
    }
}