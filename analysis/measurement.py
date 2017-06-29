# -*- coding: utf-8 -*-

from random import choice, randint, sample
from time import time

from client import *

district = [
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

dest = ['UFCG', 'HOME']
weekly = [True, False]
date = [1498800000000, 1498900000000]

def gen_query(limit=10):
    return {
        'date': choice(date),
        'dest': choice(dest),
        'district': choice(district),
        'limit': limit,
        'weekly': choice(weekly)
    }

def gen_ride(query=None):
    if query is None:
        return {
            'date': choice(date),
            'dest': choice(dest),
            'origin': 'default fixed origin',
            'route': sample(district, 4),
            'seats': 1,
            'weekly': choice(weekly)
        }

    return {
        'date': query['date'],
        'dest': query['dest'],
        'origin': 'default fixed origin',
        'route': [query['district']],
        'seats': 1,
        'weekly': query['weekly']
    }

clear_database()

user1 = create_user(114110000)
user2 = create_user(114110001)

query = gen_query()

ride1 = gen_ride()
ride2 = gen_ride(query)

r = user1.request('POST', '/api/rides', json=ride1)
r = user1.request('POST', '/api/rides', json=ride2)

r = user2.request('GET', '/api/rides', params=query)
print r.json()
