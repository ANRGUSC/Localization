#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string>
#include "main.h"

using namespace std;

bool check_exit(const char *msg) {
	for (int i = 0; i < strlen(msg); ++i) {
		if (msg[i] == '#') 
			return true;
	}
	return false;
}

int main(int argc, char *argv[]) {
	if (argc!=2) {
		cout<<"Please pass port number!"<<endl;
		return 0;
	}
	int client, server;
	int portnum = stoi(argv[1]);
	int bufsize = 1024;
	bool isExit = false;
	char buffer[bufsize];
	socklen_t size;

	struct sockaddr_in serv_addr;

	client = socket(AF_INET, SOCK_STREAM, 0);
	if (client < 0) {
		cout << "\nERROR establishing socket...";
		exit(1);
	}

	cout << "\n--> Socket server created..\n";

	serv_addr.sin_port = htons(portnum);
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htons(INADDR_ANY);


	if (bind(client, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
		cout << "--> ERROR binding connection, the socket has already been established...\n";
		return -1;
	}


	size = sizeof(serv_addr);
	cout << "--> Looking for clients..." << endl;
	listen(client, 1);

	server = accept(client, (struct sockaddr*)&serv_addr, &size);
	if (server < 0) 
        cout << "--> Error on accepting..." << endl;

    
        while (server > 0) 
        {
	
			std::string ackStr("--> Server connected...\n");
			*(ackStr.end()) = '\0';
			strncpy(&buffer[0], ackStr.c_str(), bufsize);
            send(server, buffer, bufsize, 0);
            cout << "--> Connected to the client" << endl;
            cout << "\nEnter # to end the connection\n\n" << endl;


			do {
				
				isExit = check_exit(buffer);
				cout << "Recieved from Client: ";
				recv(server, buffer, bufsize, 0);
				cout << buffer << endl;

				std::string inStr;
				int numThr = 2800;
				inStr = invokeGPUEngine(&buffer[0], numThr);

                cout << "Server: ";
				*(inStr.end()) = '\0';
				strncpy(&buffer[0], inStr.c_str(), bufsize);
				send(server, buffer, bufsize, 0);
				
				if (check_exit(buffer)) 
						break;
            } while (!isExit);
            cout << "\nDisconnected..." << endl;
            isExit = false;
            exit(1);
        }
        return 0;
}
