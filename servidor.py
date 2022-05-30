from socket import *
import sys
import threading


def conexao(connectionSocket):
    global flag
    mensagem = "Bem-Vindo ao Servidor de Mensagens!\n>> Informe a tag que deseja receber mensagens <<"
    connectionSocket.send(mensagem.encode('ascii'))
    while flag:
        try:
            mensagem = connectionSocket.recv(2048).decode('ascii')
            if(checkTag(mensagem, connectionSocket)):
                continue
            else:
                flag = False
        except:
            continue

def checkTag(mensagem, connectionSocket):
    if (mensagem[0] == '+'):
        for caractere in mensagem:
            if (caractere == '+'):
                continue
            elif (ord(caractere) >= 65 and ord(caractere) <= 90 ) or (ord(caractere) >= 97 and ord(caractere) <= 122 ):
                continue
            else:
                resposta  = "Tags devem ser sem números, sem pontuação e sem espaço!"
                connectionSocket.send(resposta.encode('ascii'))
                return True
        for con in dicionario_clientes.keys():
            if (con == connectionSocket):
                msg = mensagem[1:].split(' ')
                if(msg in dicionario_clientes[con]):
                    resposta = "already subscribed " + mensagem
                    connectionSocket.send(resposta.encode('ascii'))
                else:
                    dicionario_clientes[con].append(msg[0])
                    resposta = "subscribed " + mensagem
                    connectionSocket.send(resposta.encode('ascii'))
                    return True
            else: 
                continue

    elif (mensagem[0] == '-'):
        for caractere in mensagem:
            if (caractere == '-'):
                continue
            elif (ord(caractere) >= 65 and ord(caractere) <= 90 ) or (ord(caractere) >= 97 and ord(caractere) <= 122 ):
                continue
            else:
                resposta  = "Tags devem ser sem números, sem pontuação e sem espaço!"
                connectionSocket.send(resposta.encode('ascii'))
                return True
        for con in dicionario_clientes.keys():
            if (con == connectionSocket):
                msg = mensagem[1:].split(' ')
                if(msg not in dicionario_clientes[con]):
                    resposta = "not subscribed " + mensagem
                    connectionSocket.send(resposta.encode('ascii'))
                else:
                    dicionario_clientes[con].remove(msg[0])
                    resposta = "unsubscribed " + mensagem
                    connectionSocket.send(resposta.encode('ascii'))
                    return True
            else: 
                continue
    
    elif (mensagem == '##kill'):
        print("Mata todo mundo!")
        for cliente in dicionario_clientes.keys():
            cliente.send(mensagem.encode('ascii'))
            cliente.close()
            desconectar(cliente)
        return False
    else:
        tags = []
        aux = mensagem.split(' ')
        for tag in aux:
            if(tag[0] == '#'):
                tags.append(tag[1:])
            
        transmitir(mensagem, tags, connectionSocket) 
        return True

def transmitir(mensagem,tags, connectionSocket):
    print(dicionario_clientes)
    for cliente in dicionario_clientes.keys():
        if cliente != connectionSocket:
            for value in dicionario_clientes[cliente]:
                print(dicionario_clientes[cliente])
                print(value)
                if(value in tags):
                    print("Value: " + value)
                    try:
                        cliente.send(mensagem.encode('ascii'))
                        break
                    except:
                        cliente.close()
                        desconectar(cliente)

def desconectar(connectionSocket):
    if connectionSocket in dicionario_clientes.keys():
       dicionario_clientes.pop(dicionario_clientes[connectionSocket])

if len(sys.argv) != 2:
    print("Modo correto para executar o programa: python3 servidor.py num_porta")
    exit()
    
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverPort = int(sys.argv[1])
serverSocket.bind(('', serverPort))
serverSocket.listen(100)

dicionario_clientes = {}
global flag
flag = True
while flag: 
    connectionSocket, clienteAddress = serverSocket.accept()
    
    dicionario_clientes[connectionSocket] = []
    print("Cliente " + clienteAddress[0] + " conectado!")

    processo = threading.Thread(target=conexao, args=(connectionSocket,))
    processo.start()
    
connectionSocket.close()
serverSocket.close()
sys.exit()