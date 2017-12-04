import os,sys,thread,socket


MAX_QUEUE = 20          # Max number of connection
MAX_PKT_SIZE = 99999     # Max size of packet

def main():
    # [+] Usage  : python site_unblock.py
    # [+] Setting: set http proxy with localhost and port number 8080,
    #   other protocol should be DIRECT so that browser can load images.
    
    port = 8080
    host = ''

    try:
        # create socket & bind & listen!
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(MAX_QUEUE)

    except socket.error, (value, message):
        if s:
            s.close()
        print "Fail to open socket"
        sys.exit(1)

    # connect with web client 
    while 1:
        conn, client_addr = s.accept()
    
		# thread to handle web client and end server
		# thread.start_new_thread(func, args, kwargs=None)
        thread.start_new_thread(proxy_thread, (conn, client_addr))

    s.close()

def proxy_thread(conn, client_addr):

	# get response from web browser
    req = conn.recv(MAX_PKT_SIZE)
    """ format of req!!!!!
GET http://www.sex.com/ HTTP/1.1
Host: www.sex.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:54.0) Gecko/20100101 Firefox/54.0
	""" 
	# split first line 
    line = req.split('\n')[0] 
	# get url!! GET : [0], http://www.sex.com : [1]
    url = line.split(' ')[1] 
    http_pos = url.find("://")          # find position of ://
    if (http_pos==-1): # if it does not exist
        temp = url
    else:
        temp = url[(http_pos+3):]       # get the rest of url print temp # print the URLs!!
    # find / in url and remove it

    webserver_pos = temp.find("/")
    if webserver_pos == -1:
        webserver_pos = len(temp)
    webserver = temp[:webserver_pos]

    try:
        # create a socket to connect to the end server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect end server with port 80
        s.connect((webserver, 80))
        # put dummy behind of request
        dummyRequest = 'GET / HTTP/1.1\r\nHost: test.gilgil.net\r\n\r\n'
        req = dummyRequest + req
        # send request to end server
        s.send(req)         
        
        while 1:
            # receive data from end server
            data = s.recv(MAX_PKT_SIZE)
			# print data
            # if 404 data, ignore it
            if data.find('HTTP/1.1 404 Not Found') >= 0:
                continue
            if (len(data) > 0):
                # send to browser
                conn.send(data)
            else:
                break
        s.close()
        conn.close()
    except socket.error, (value, message):
        s.close()
        conn.close()
        sys.exit(1)

main()
