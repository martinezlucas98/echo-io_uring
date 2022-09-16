CCFLAGS ?= -Wall -O2 -D_GNU_SOURCE 
all_targets = server/io_uring-echo-server server/echo-server client/echo-client-auto server/echo-server-v2

.PHONY: liburing io_uring-echo-server

all: $(all_targets)

clean:
	rm -f $(all_targets)

liburing:
	+$(MAKE) -C ./liburing

server/io_uring-echo-server:
	$(CC) server/io_uring-echo-server.c -o ./server/io_uring-echo-server  ${CCFLAGS} -luring

server/echo-server:
	$(CC) server/echo-server.c -o ./server/echo-server ${CCFLAGS} -w

server/echo-server-v2:
	$(CC) server/echo-server-v2.c -o ./server/echo-server-v2 ${CCFLAGS} -w

client/echo-client-auto:
	$(CC) client/echo-client-auto.c -o ./client/echo-client-auto ${CCFLAGS} -w