# site_unblock
Detouring "warning.or.kr" redirection <br />
웹 클라이언트로부터 HTTP Request를 받으면 Dummy HTTP Request를 붙여서 전송한다.<br />
웹 서버로부터 HTTP Response를 받으면 첫번째 HTTP Response를 빼고 클라이언트로 전송한다.<br />
proxy는 웹 클라이언트로부터의 multi connection 요청을 처리할 수 있어야 한다. 이를 위해 thread를 사용할 것인지, epoll을 사용할 것인지 iocp를 사용할 것인지는 알아서 할 것.
