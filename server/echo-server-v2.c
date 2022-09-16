/* 
 * echoserver.c - A simple connection-based echo server 
 * usage: echoserver <port>
 */

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define BUFSIZE 2048
#define BACKLOG 512

/*
 * error - wrapper for perror
 */
void error(char *msg) {
  perror(msg);
  exit(1);
}

int main(int argc, char **argv) {
  int listenfd; /* listening socket */
  int connfd; /* connection socket */
  int portno; /* port to listen on */
  int clientlen; /* byte size of client's address */
  struct sockaddr_in serveraddr; /* server's addr */
  struct sockaddr_in clientaddr; /* client addr */
  struct hostent *hostp; /* client host info */
  char buf[BUFSIZE]; /* message buffer */
  char *hostaddrp; /* dotted decimal host addr string */
  int optval; /* flag value for setsockopt */
  int n; /* message byte size */


  portno = 2048;

  /* socket: create a socket */
  listenfd = socket(AF_INET, SOCK_STREAM, 0);
  optval = 1;
  setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, 
	     (const void *)&optval , sizeof(int));

  /* build the server's internet address */
  bzero((char *) &serveraddr, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET; /* we are using the Internet */
  serveraddr.sin_addr.s_addr = htonl(INADDR_ANY); /* accept reqs to any IP addr */
  serveraddr.sin_port = htons((unsigned short)portno); /* port to listen on */

  /* bind: associate the listening socket with a port */
 bind(listenfd, (struct sockaddr *) &serveraddr, sizeof(serveraddr));

  /* listen: make it a listening socket ready to accept connection requests */
 listen(listenfd, BACKLOG);

  /* main loop: wait for a connection request, echo input line, 
     then close connection. */
  clientlen = sizeof(clientaddr);
  
  /* gethostbyaddr: determine who sent the message */
  hostp = gethostbyaddr((const char *)&clientaddr.sin_addr.s_addr, 
              sizeof(clientaddr.sin_addr.s_addr), AF_INET);
  hostaddrp = inet_ntoa(clientaddr.sin_addr);
  printf("server established connection with %s (%s)\n", 
      hostp->h_name, hostaddrp);
      
  /* accept: wait for a connection request */
  connfd = accept(listenfd, (struct sockaddr *) &clientaddr, &clientlen);
  while (1) {
    /* read: read input string from the client */
    bzero(buf, BUFSIZE);
    read(connfd, buf, BUFSIZE);
    write(connfd, buf, strlen(buf)+1);

  }
}