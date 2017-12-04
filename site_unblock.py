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
    except KeyboardInterrupt:
		s.close()
		sys.exit(1)

    # connect with web client 
    while 1:
        conn, client_addr = s.accept()
    
		# thread to handle Web Client & End Server
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
    host = req[req.find('Host:') + 6:].split('\n')[0][:-1]
# print host	

    try:
        # create a socket to connect to the End server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect End server with port 80
        s.connect((host, 80))
        # put dummy request / other website is too late
        dummyRequest = 'GET / HTTP/1.1\r\nHost: test.gilgil.net\r\n\r\n'
        req = dummyRequest + req
        # send request to end server
        s.send(req)
        
		# Receive data from end server
        while 1:
            data = s.recv(MAX_PKT_SIZE)
			# print data
            if data.find('HTTP/1.1 404 Not Found') >= 0:
                continue
            if (len(data) > 0):
                # send to browser
                conn.send(data)
            else:
                break
		#time.sleep(5)
        s.close()
        conn.close()
    except socket.error, (value, message):
        s.close()
        conn.close()
        sys.exit(1)
    except Exception as e:
	print 'Exception from the host ' + host
	print e
	s.close()
	conn.close()

	
main()
