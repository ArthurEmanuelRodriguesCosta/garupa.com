# -*- coding: utf-8 -*-

from random import choice, randint
from time import time

from client import Authenticator
from requests import request

base_url = 'http://localhost:8000'
#base_url = 'http://destroctor51.pythonanywhere.com'

bairros = [
    'Acácio Figueiredo', 'Alto Branco', 'Bairro das Cidades', 'Bela Vista',
    'Bodocongó', 'Cachoeira', 'Castelo Branco', 'Catolé',
    'Catolé de Zé Ferreira', 'Centenário', 'Centro', 'Conjunto Cinza',
    'Dinamérica', 'Distrito de Catolé', 'Distrito Industrial', 'Estação Velha',
    'Estreito', 'Glória', 'Itararé', 'Jardim Atalaia', 'Jardim Borborema',
    'Jardim Paulistano', 'Jardim Verdejante', 'Jeremias', 'José Pinheiro',
    'Lauritzen', 'Liberdade', 'Ligeiro', 'Louzeiro', 'Malvinas', 'Mirante',
    'Monte Castelo', 'Monte Santo', 'Mutirão do Serrotão', 'Nova Brasília',
    'Novo Bodocongó', 'Palmeira', 'Pedregal', 'Prata', 'Presidente Médici',
    'Quarenta', 'Ramadinha', 'Sandra Cavalcante', 'Santa Cruz', 'Santa Rosa',
    'Santa Terezinha', 'Santo Antônio', 'São José', 'São José da Mata',
    'Serrotão', 'Sítio Estreito', 'Sítio Lucas', 'Tambor', 'Três Irmãs',
    'Universitário', 'Velame', 'Vila Cabral'
]

weekly = [True, False]

def clear_database():
    r = request('DELETE', base_url+'/api')
    print r.text

def create_user(uid=114110000):
    r = request('POST', base_url+'/api/users', json={
        'uid': uid,
        'passwd': '12345',
        'name': 'default',
        'email': 'default@email.com'
    })

    if r.status_code is 200:
        return Authenticator(base_url, uid, '12345')
    return None

'''
for i in range(100):
    r = auth.request('POST', '/api/rides', json={
        'dest': 'UFCG',
        'weekly': choice(weekly),
        'origin': 'qualquer coisa mano',
        'route': [choice(bairros), choice(bairros), choice(bairros)],
        'seats': randint(1, 4),
        'date': 1498791600000
    })

    print i, r.text
'''
