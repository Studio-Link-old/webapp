#include <sys/types.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <string.h>
#include <microhttpd.h>
#include <stdio.h>
#include <hiredis/hiredis.h>
#include <netinet/in.h>

#define PORT 8888
#define JSON "{\"INCOMING\": \"%s\"}\n"

	static int
answer_to_connection (void *cls, struct MHD_Connection *connection,
		const char *url, const char *method,
		const char *version, const char *upload_data,
		size_t *upload_data_size, void **con_cls)
{
	char *page = "{}";
	struct MHD_Response *response;
	int ret;
	int j;
	redisContext *context;
	redisReply *reply;
	struct timeval timeout = { 29, 0 }; // 29 seconds
	context = redisConnect("127.0.0.1", 6379);


	redisSetTimeout(context, timeout);

	reply = redisCommand(context, "GET baresip_status");
	if (reply->type == REDIS_REPLY_STRING) {
		printf("baresip_status) '%s'\n", reply->str);
		if (strcmp(reply->str, "INCOMING") == 0) {
			freeReplyObject(reply);
			reply = redisCommand(context, "GET baresip_peeruri");
			page = malloc(strlen(JSON) + strlen(reply->str) + 1);
			snprintf(page, strlen(JSON) + strlen(reply->str) + 1, JSON, reply->str);
			freeReplyObject(reply);
			goto out;
		}
	}
	freeReplyObject(reply);

	reply = redisCommand(context,"SUBSCRIBE baresip_call_event");
	freeReplyObject(reply);
	while(redisGetReply(context, &reply) == REDIS_OK) {
		// consume message
		if (reply->type == REDIS_REPLY_ARRAY) {
			for (j = 0; j < reply->elements; j++) {
				printf("%u) %s\n", j, reply->element[j]->str);
			}
			if (strcmp(reply->element[2]->str, "INCOMING") == 0) {
				redisCommand(context,"UNSUBSCRIBE baresip_call_event");
				reply = redisCommand(context, "GET baresip_peeruri");
				page = malloc(strlen(JSON) + strlen(reply->str) + 1);
				snprintf(page, strlen(JSON) + strlen(reply->str) + 1, JSON, reply->str);
				freeReplyObject(reply);
				goto out;
			}
		}
		freeReplyObject(reply);
	}

out:
	response =
		MHD_create_response_from_buffer (strlen (page), (void *) page, 
				MHD_RESPMEM_PERSISTENT);
	ret = MHD_queue_response (connection, MHD_HTTP_OK, response);


	MHD_destroy_response (response);
	redisFree(context);

	return ret;
}


	int
main ()
{
	struct MHD_Daemon *daemon;
	struct sockaddr_in daemon_ip_addr;
	memset (&daemon_ip_addr, 0, sizeof (struct sockaddr_in));
	daemon_ip_addr.sin_family = AF_INET;
	daemon_ip_addr.sin_port = htons (PORT);
	daemon_ip_addr.sin_addr.s_addr = htonl (INADDR_LOOPBACK);


	daemon = MHD_start_daemon (MHD_USE_THREAD_PER_CONNECTION, PORT, NULL, NULL,
			&answer_to_connection, NULL, MHD_OPTION_SOCK_ADDR,
	                &daemon_ip_addr, MHD_OPTION_END);
	if (NULL == daemon)
		return 1;

	while(1==1) {
		sleep(1);
	}

	MHD_stop_daemon (daemon);

	return 0;
}
