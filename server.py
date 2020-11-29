#file name : server.py
import socket
import threading

host = 'localhost'
port = 9998
addr = (host, port)


def main(sock):
    while True:
        try:
            receive_Data = sock.recv(1024).decode('utf-8')
            print('받은 데이터 : ', receive_Data)
        except:
            print(str(addr_info)+"에서 연결이 중지되었습니다.")
            return

        translate = list(receive_Data)
        print(translate)
        #if ('안' in translate) or ('녕' in translate):
        #    annimal_said = '안녕! 집사야!'
        #elif ("배고" in translate) or ('배고파' in translate):
        #    annimal_said = '배고파!!'
        #elif ('졸' in translate) or ('피곤' in translate):
        #    annimal_said = '졸려,,,'
        #else:
        #    annimal_said = '잘모르겠어요.'

        if str(receive_Data).find('안') >= 0 or  str(receive_Data).find('녕') >= 0:
            annimal_said = '안녕! 집사야!'
        elif str(receive_Data).find('배고') >=0:
            annimal_said = '배고파!!'
        elif str(receive_Data).find('졸') >= 0 or str(receive_Data).find('피곤') >= 0:
            annimal_said = '졸려,,,'
        else:
            annimal_said = '잘모르겠어요.'

        print('메세지를 입력하시오 : ', annimal_said)
        sock.sendall(annimal_said.encode('utf-8'))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Winerror 10048
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(addr)
server_socket.listen(5)

print('%d번 포트로 접속 대기중...' % port)
while True:
    connection_socket, addr_info = server_socket.accept()

    print(str(addr_info), '에서 접속이 확인되었습니다.')

    server = threading.Thread(target=main, args=(connection_socket,))
    server.start()