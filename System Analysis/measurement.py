# -*- coding: utf-8 -*-

from client import *
from random import choice, randint
import time

auth = Authenticator('http://destroctor51.pythonanywhere.com', '114110495', '12345')

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
    'Universitário', 'Velame', 'Vila Cabral']

weekly = [True, False]

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

