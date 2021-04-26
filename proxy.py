import sys, os, time, socket, select

#grab cache expire time from command line
try:
    cacheTime = float(sys.argv[1])
except:
    cacheTime = 120


#Create a socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setblocking(0)

#socket binded to port 8888 on localhost
serverSocket.bind(("localhost",8888))
print("server started on port 8888")
serverSocket.listen(10)
inputs = [serverSocket]
outputs = []
connections = {}
print("listening for connections...")


while inputs:
    # raises error if any connection is broken
    try:
        clients, servers, exceptions = select.select(inputs, outputs, inputs,5)
    except:
        # loop through sockets and ensure no connection is broken
        for sock in inputs:
            if (sock.fileno() == -1):
                inputs.remove(sock)
                if sock in outputs:
                    outputs.remove(sock)
                sock.close() #added
                connections.pop(sock, None)
        clients, servers, exceptions = select.select(inputs, outputs, inputs,5)

        
    for sock in clients:
        if sock is serverSocket:
            # accept incoming connections
            connection, client = sock.accept()
            connection.setblocking(0)
            inputs.append(connection)
            print("connection accepted from {}".format(client))
            connections[connection] = []
        else:
            # if sock is broken or disconnected remove and continue
            if (sock.fileno() == -1):
                inputs.remove(sock)
                if sock in outputs:
                    outputs.remove(sock)
                sock.close() #added
                connections.pop(sock, None)
                continue
            #try in case client shuts connection
            try:
                data = sock.recv(1024)
            except:
                continue
            
            if data:
                # extract file and host from request
                message = data.decode('utf-8')
                lines = message.split("\n")
                url = lines[0].split(" ")[1]
                host = url.split("/")[1]
                file = url.lstrip("/").lstrip(host)
                if file == "": file="/"
                # deal with special favicon.ico case
                if file[0]!="/": file = "/" + file 
                if host == "favicon.ico":
                    file = "/favicon.ico"
                    host = "www.cs.toronto.edu"
                # alter request so host and file are correct
                lines[0] = "GET {} HTTP/1.1\r".format(file)
                lines[1] = "Host: {}\r".format(host)
                # find "Accept_Encoding" feild and set to none so response is not compressed
                i = len(lines)-1
                while i>0:
                    if "Accept-Encoding" in lines[i]:
                        break
                    i-=1
                lines[i] = "Accept-Encoding: \r"
                # put the request back together
                newRequest = ""
                for line in lines:
                    newRequest += line + "\n"
                newRequest = newRequest[0:-1]
                connections[sock].append((host,newRequest,file))
                if sock not in outputs:
                    outputs.append(sock)
            else:
                # close connection if no data received
                if sock in outputs:
                    outputs.remove(sock)
                inputs.remove(sock)
                sock.close()
                connections.pop(sock, None)
                
        for sock in servers:
            try:
                # grab request
                host, nextRequest, file = connections[sock].pop(0)
                # create cache file, end with $ so no file extensions and all the files are the same type
                filename = "{}_{}".format(host,file)
                filename = filename.replace("/","$")
                filename += "$"
                # check if request cached and cache time not expired, else create cache file
                try:
                    if ((time.time() - os.path.getmtime(filename)) < cacheTime):
                        cacheMiss = False
                    else:
                        raise Exception("cache has expired")
                except:
                    cacheMiss = True
                # if cache miss, connect to host
                if cacheMiss:
                    webSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    webSocket.connect((host,80))
            except:
                # close connection
                if sock in outputs:
                    outputs.remove(sock)
                sock.close()
            else:
                # send request to host since cache miss
                if cacheMiss:
                    webSocket.sendall(nextRequest.encode())
                    while True:
                        try:
                            webResponse = webSocket.recv(1024)
                            respCache = webResponse
                            # Modify body to add time tag for version of page
                            if b"<body" in webResponse:
                                webResponse = webResponse.split(b"<body")
                                newResp = webResponse[0] + b'<body'
                                restResp = webResponse[1].split(b'>')
                                respCache = newResp
                                bodyTag = restResp.pop(0)
                                currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())).encode()
                                newResp +=  bodyTag + b'><p style="z-index:9999; position:fixed; top:20px; left:20px; width:200px; \
                                height:100px; background-color:yellow; padding:10px; font-weight:bold;">' \
                                + b"FRESH VERSION AT:" + currentTime +b'</p'
                                respCache +=  bodyTag + b'><p style="z-index:9999; position:fixed; top:20px; left:20px; width:200px; \
                                height:100px; background-color:yellow; padding:10px; font-weight:bold;">' \
                                + b"CACHED VERSION AS OF:" + currentTime +b'</p'
                                for s in restResp:
                                    newResp += b'>' + s
                                    respCache += b'>' + s
                                webResponse = newResp    
                            # send response back to client and write to cache 
                            if(len(webResponse)>0):
                                sock.send(webResponse)
                                with open(filename, "ab") as cache:
                                    cache.write(respCache)
                            else:
                                webSocket.close()
                                break
                        except:
                            webSocket.close()
                            break
                else:
                    # cache hit, serve up from cache
                    with open(filename, "rb") as cache:
                        while data:
                            data = cache.read(1024)
                            sock.send(data)
        for sock in exceptions:
            # close connections
            inputs.remove(sock)
            if sock in outputs:
                outputs.remove(sock)
            sock.close()
            connections.pop(sock, None)

