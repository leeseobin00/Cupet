#file name: chatServer.py
import socketserver
import threading

HOST = ''
PORT = 9009
lock = threading.Lock()  # syncronized


class UserManager:

    def __init__(self):
        self.users = {}  # user's register information

    def addUser(self, username, conn, addr):
        if username in self.users:  # if already registered user
            conn.send('이미 등록된 사용자입니다.\n'.encode())
            return None

        #new user
        lock.acquire()
        self.users[username] = (conn, addr)
        lock.release()

        self.sendMessageToAll('*알림*[%s]님이 입장했습니다.' % username)
        print('+++ 대화 참여자 수 [%d]' % len(self.users))

        return username

    def removeUser(self, username):  # user remove
        if username not in self.users:
            return

        lock.acquire()
        del self.users[username]
        lock.release()

        self.sendMessageToAll('*알림*[%s]님이 퇴장했습니다.' % username)
        print('--- 대화 참여자 수 [%d]' % len(self.users))

    def messageHandler(self, username, msg):
        if msg[0] != '/':
            self.sendMessageToAll('[%s] : %s' % (username, msg))
            return

        if msg.strip() == '/quit':  # 'quit'
            self.removeUser(username)
            return -1

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())


class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()

    def handle(self):  # client access -> address
        print('[%s] 연결됨' % self.client_address[0])

        try:
            username = self.registerUsername()
            msg = self.request.recv(1024)
            while msg:
                print(msg.decode())
                if self.userman.messageHandler(username, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)

        except Exception as e:
            print(e)

        print('[%s] 접속종료' % self.client_address[0])
        self.userman.removeUser(username)

    def registerUsername(self):
        while True:
            username = self.request.recv(1024)
            username = username.decode().strip()
            if self.userman.addUser(username, self.request, self.client_address):
                return username


class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def runServer():
    print('+++ 채팅 서버를 시작합니다.')
    print('+++ 채텅 서버를 끝내려면 Ctrl-C를 누르세요.')

    try:
        server = ChatingServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('--- 채팅 서버를 종료합니다.')
        server.shutdown()
        server.server_close()


runServer()