from app import app
import requests
import hashlib
from  rich import print
from rich.console import Console
from translate import Translator
console = Console()

def hash(argumento):
    m = hashlib.md5()
    m.update(argumento.encode('utf-8'))
    return m.hexdigest()

def autorizacao():
    publicKey = '1b22830f436a6bd1201071c913d073ed'
    privateKey = 'a419a90450dc4722b189cca71fbaecb49ebcbad7'
    ts = 1
    hash5 = hash(f'{ts}{privateKey}{publicKey}')
    parametros = f'?ts={ts}&apikey={publicKey}&hash={hash5}'
    return parametros

class Agente:
        def getheros(self):
            url = 'https://gateway.marvel.com/v1/public/characters'
            url += autorizacao()
            with requests.Session() as session:
                response = session.get(url)
                return response.json()['data']['results']

        def gethero(self, id):
            url = 'https://gateway.marvel.com/v1/public/characters/'+str(id)
            url += autorizacao()
            with requests.Session() as session:
                response = session.get(url)
                return response.json()['data']['results']
        def traduzir(self, text):
            translator= Translator(from_lang="en",to_lang="pt-br")
            translation = translator.translate(text)
            return translation