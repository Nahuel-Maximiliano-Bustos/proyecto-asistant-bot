from time import sleep
from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from keepSessions import *
import re
from unicodedata import normalize


filepath = '.\sources\session.txt'
driver = webdriver

def crear_sesion():
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            if cnt == 0:
                executor_url = line
            if cnt == 1:
                session_id = line
    
    def nuevo_comando(self, command, params=None):
        if command == 'newSession':
            return {'success': 0, 'Value': None, 'Sessionid': session_id}
        else:
            return org_command_execute(self, command, params)
    org_command_execute = RemoteWebDriver.execute
    RemoteWebDriver.execute = nuevo_comando

    new_driver = webdriver.Remote(command_executor= executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    RemoteWebDriver.execute = org_command_execute
    
    return new_driver

def buscar_chat():
    print('BUSCANDO CHATS')
    if len(driver.find_elements_by_class_name('_2zkCi')):
        print('CHAT ABIERTO')
        message = identificador()
        if message != None:
            return True

    chats = driver.find_elements_by_class_name('_2aBzC')
    for chat in chats:
        print('DETECTANDO MENSAJES SIN LEER')
        chats_mensajes = chat.find_elements_by_class_name('_38M1B')
        if len(chats_mensajes) == 0:
            print('CHATS ATENDIDOS')
            continue
        element_name = chat.find_elements_by_class_name('_3Dr46')
        name = element_name[0].text.upper().strip()

        print('IDENTIFICANDO CONTACTO')
        with open('./sources/contactos.txt', mode='r', encoding='utf-8') as archivo:
            contactos = [linea.rstrip() for linea in archivo]
            if name not in contactos:
                print('CONTACTO NO ENCONTRADO: ', name)
                continue
        print(name, 'AUTORIZADO PARA SER ATENDIDO POR BOT')
        chat.click()
        return True
    return False

def normalizar(message:str):
    message = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD",message), 0, re.I
    )
    return normalize('NFD', message)

def identificador():
    element_box = driver.find_elements_by_class_name('_3XpKm')
    posicion = len(element_box)-1
    color = element_box[posicion].value_of_css_property('background-color')
    
    print('COLOR UTILIZADO: ', color)
    if color == 'rgba(220, 248, 198, 1)' or color == 'rgba(5, 97, 98, 1)':
        print('CHAT ATENDIDO')
        return

    element_message = element_box[posicion].find_elements_by_class_name('_3ExzF')
    message = element_message[0].text.upper().strip()
    print('MENSAJE RECIBIDO: ', message)
    return normalizar(message)

def responder(message:str):
    print(':::::PREPARANDO RESPUESTAS:::::')
    if message.__contains__('1.¿QUE ES AJ DESING?'):
        response = '\t\t\t*****aj desing*****\n'\
            'es un pequeño emprendimiento de diseño gráfico digital en redes sociales.\n'

    elif message.__contains__('2.¿ Cual es su instagram?'):
        response = 'Podes visitarnos en: https://www.instagram.com/aj_desing134/ \n'

    elif message.__contains__('3.Quiero ir a su web site'):
        response = 'Nuestro sitio web: https://sites.google.com/view/ajdesing/inicio \n'

    elif message.__contains__('\t\t\t******Lista de comandos******\n'):
        text1 = open('./sources/mesnsajes.txt', mode='r', encoding='utf-8')
        response = text1.readlines()
        text1.close()

    elif message.__contains__('GRACIAS'):
        response = 'Por nada, ha sido un placer ayudarte\n'

    else:
        response = 'Hola, soy un sistema de respuesta automática\n'\
            'diseñado exclusivamente para responder a tus dudas\n'\
                'de manera inmediata!\n'
    
    return response

def proceso(message:str):
    chatbox = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    response = responder(message)
    chatbox.send_keys(response)

def machine():
    global driver
    driver = crear_sesion()
    while True:
        if not buscar_chat():
            sleep(10)
            continue
        message = identificador()
        if message == None:
            continue
        proceso(message)
machine()
