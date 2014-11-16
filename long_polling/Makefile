default: server

server: server.c
	gcc -lhiredis -lmicrohttpd server.c -o server

clean:
	rm -f server
