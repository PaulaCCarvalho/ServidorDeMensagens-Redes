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
    while True:
        mensagem = clientSocket.recv(2048).decode('ascii')
        if(mensagem == '##kill'):
            print("< Você será desconectado do Servidor de Mensagens!")
            break
        else:
            print('< '+ mensagem)
    clientSocket.close()

def write():
    while True:
        try:
            mensagem = input('> ')
            clientSocket.send(mensagem.encode('ascii'))
        except:
            break

receber_thread = threading.Thread(target=receber)
receber_thread.start()
enviar_thread = threading.Thread(target=write)
enviar_thread.start()
