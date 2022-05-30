import multiprocessing
import re
from socket import *
import sys
from select import select
import threading



if len(sys.argv) != 3:
    print("Modo correto para executar o programa: python3 cliente.py IP num_porta")
    exit()

serverName = str(sys.argv[1])
serverPort = int(sys.argv[2])

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
flag = True

def receber():
    global flag
    while flag:
        try:
            mensagem = clientSocket.recv(2048).decode('ascii')
            if(mensagem == '##kill'):
                print("< Você será desconectado do Servidor de Mensagens!")
                flag = False
                clientSocket.close()
                sys.exit('< Você foi desconectado do Servidor de Mensagens!')
            else:
                print('< '+ mensagem)
        except:
            print("Um error ocorreu")
            clientSocket.close()
            break
    clientSocket.close()
    sys.exit()

def write():
    global flag
    while flag:
        mensagem = input('> ')
        clientSocket.send(mensagem.encode('ascii'))
    clientSocket.close()
    sys.exit()

receber_thread = threading.Thread(target=receber)
receber_thread.start()
enviar_thread = threading.Thread(target=write)
enviar_thread.start()