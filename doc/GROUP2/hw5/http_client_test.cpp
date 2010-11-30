/******************************************************************************
**  http_client_test.cpp
**
**  Created by: Lee VanGundy
**
**
**  Tests the connection ability of the client to the HTTP server.
**
******************************************************************************/

#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<netdb.h>
#include<iostream>
#include<cstring>
#include<cstdio>
#include<cstdlib>

using namespace std;

#define LOCAL_SERVER_PORT 9798

#define MAX_STR_LEN 512

void parse_url(char *url, char *hostname, int *port, char *identifier){
    char protocol[MAX_STR_LEN], temp_url[MAX_STR_LEN], *ptr=0, *nptr=0;

    strcpy(temp_url, url);
    ptr = strchr(temp_url, ':');
    if(!ptr){
	cout << "Wrong url: no protocol specified\n";
	exit(1);
    }
    strcpy(ptr, "\0");
    strcpy(protocol, temp_url);

    if(strcmp(protocol, "http")){
	cout << "Wrong protocol: " << protocol << endl;
	exit(1);
    }

    strcpy(temp_url, url);
    ptr = strstr(temp_url, "//");
    if(!ptr){
	cout << "Wrong url: no server specified\n";
	exit(1);
    }
    ptr+=2;

    strcpy(hostname, ptr);
    nptr = strchr(ptr, ':');

    if(!nptr){
        *port = 80;
        nptr = strchr(hostname, '/');
    }
    else{
        sscanf(nptr, ":%d", port);
        nptr = strchr(hostname, ':');
    }

    if(nptr){
	*nptr = '\0';
    }

    nptr = (char *)strchr(ptr, '/');

    if(!nptr){
        cout <<  "Wrong url: no file specified\n";
	exit(1);
    }

    strcpy(identifier, nptr);
}

int main(int argc, char *argv[]){
    char url[MAX_STR_LEN];
    char hostname[MAX_STR_LEN];
    int port;
    char identifier[MAX_STR_LEN];

    int sd, rc, i;
    struct sockaddr_in localAddr, servAddr;
    struct hostent *h;

    char *request=0;
    char buf[MAX_STR_LEN];

    int len, size;

    int head_flag=0, date_flag=0, default_flag=0;
    char s_time[30];

    request = buf;

    if(1==argc){
	cout << "\n Usage; client [-h] [-d <time-interval>] <URL> \n";
	exit(1);
    }

    strcpy(url,argv[1]);

    parse_url(url,hostname,&port,identifier);

    strcpy(request,"HEAD ");

    request=strcat(request,identifier);
    request=strcat(request," HTTP/1.1\r\nHOST: ");
    request=strcat(request,hostname);
    request=strcat(request,"\r\n");
    request=strcat(request,"\r\n");

    h = gethostbyname(hostname);
    cout << h << endl << request << endl;
    if(h == NULL){
	cout << "unknown host: " << hostname << endl;
	exit(1);
    }

    servAddr.sin_family = h->h_addrtype;
    memcpy((char *) &servAddr.sin_addr.s_addr, h->h_addr_list[0], h->h_length);
    servAddr.sin_port = htons(port);

    cout << "Create socket...   \n";
    sd = socket(AF_INET, SOCK_STREAM, 0);
    if(sd<0){
	cout << "cannot open socket\n";
	exit(1);
    }

    //  bind port number
    cout << "Bind port number...  \n";

    localAddr.sin_family = AF_INET;
    localAddr.sin_addr.s_addr = htonl(INADDR_ANY);
    localAddr.sin_port = htons(0);

    rc = bind(sd, (struct sockaddr *) &localAddr, sizeof(localAddr));
    if(rc<0){
	cout << argv[0] << ": cannot bind port TCP " << port << endl;
	exit(1);
    }

    // connect to server
    printf("Connect to server...\n");
    rc = connect(sd, (struct sockaddr *) &servAddr, sizeof(servAddr));
    if(rc<0){
	cout << "cannot connect ";
	exit(1);
    }

    // send request
    cout << "-- Send HTTP request:\n\n" << request;
    rc = write(sd, request, strlen(request));
    if(rc<0){
	cout << "cannot send data ";
	close(sd);
	exit(1);
    }

    cout << "-- Recieved response:\n\tfrom server:" << url << ", IP = " << inet_ntoa(servAddr.sin_addr) << endl << endl;

    cout << "Success!!\n";

    close(sd);
    return 0;

}

