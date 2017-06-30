# -*- coding: utf-8 -*-

from random import choice, randint, sample
from sys import stdout
from threading import Thread, Lock

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


output = open('out.csv', 'w')
output.write('queries,results,rides,net_time,process_time,bd_time\n')
lock = Lock()

def write(string):
    with lock:
        output.write(string)


class Register(Thread):
    def __init__(self, user, ride):
        Thread.__init__(self)
        self.user = user
        self.ride = ride

    def run(self):
        r, delta = self.user.request('POST', '/api/rides', json=self.ride)
        stdout.write('.' if r.status_code is 200 else 'x')

class Search(Thread):
    def __init__(self, user, query, queries, results, rides):
        Thread.__init__(self)
        self.user = user
        self.query = query

        self.queries = queries
        self.results = results
        self.rides = rides

    def run(self):
        r, delta = self.user.request('GET', '/api/rides', params=self.query)
        stdout.write('.' if r.status_code is 200 else 'x')

        if r.status_code == 200:
            json = r.json()

            write('%d,%d,%d,%s,%s,%s\n' % (
                self.queries, self.results, self.rides,
                str(delta), str(json['process_time']), str(json['bd_time'])
            ))

def execute(threads, w=50):
    for i in xrange(len(threads)/w):
        for j in xrange(w):
            threads[w*i+j].start()
        for j in xrange(w):
            threads[w*i+j].join()
    for k in xrange(w*i+j+1, len(threads)):
        threads[k].start()
    for k in xrange(w*i+j+1, len(threads)):
        threads[k].join()


def run_experiment(queries, results, rides):

    driver = create_user(114110000)
    passenger = create_user(114110001)

    query = gen_query(results)

    stdout.write('rides ')
    threads = []

    for i in xrange(results):
        ride = gen_ride(query)
        t = Register(driver, ride)
        threads.append(t)

    for i in xrange(rides-results):
        ride = gen_ride()
        t = Register(driver, ride)
        threads.append(t)

    execute(threads)
    stdout.write('\n')

    stdout.write('queries ')
    threads = []

    for i in xrange(queries):
        t = Search(passenger, query, queries, results, rides)
        threads.append(t)

    execute(threads)
    stdout.write('\n')

def repeat_experiment(queries, results, rides):
    for i in xrange(100):
        run_experiment(queries, results, rides)


repeat_experiment(1, 10, 100)
repeat_experiment(1, 10, 1000)
repeat_experiment(1, 100, 100)
repeat_experiment(1, 100, 1000)
repeat_experiment(200, 10, 100)
repeat_experiment(200, 10, 1000)
repeat_experiment(200, 100, 100)
repeat_experiment(200, 100, 1000)
