# -*- coding: utf-8 -*-

from random import choice, randint, sample
from sys import stdout
from threading import Lock, Semaphore, Thread

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
date = [int(time()*1000) + 1*60*60, int(time()*1000) + 2*60*60]


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

window = Semaphore(64)
lock = Lock()


class Register(Thread):
    def __init__(self, user, ride):
        Thread.__init__(self)
        self.user = user
        self.ride = ride

    def run(self):
        try:
            r, delta = self.user.request('POST', '/api/rides', json=self.ride)

            if r.status_code is not 200:
                raise Exception
            stdout.write('.')

        except:
            stdout.write('x')
        window.release()

class Search(Thread):
    def __init__(self, user, query):
        Thread.__init__(self)
        self.user = user
        self.query = query
        self.result = None

    def run(self):
        try:
            r, net_time = self.user.request('GET', '/api/rides', params=self.query)

            json = r.json()
            stdout.write('.')

            with lock:
                print net_time

            self.result = {
                'net_time': net_time,
                'process_time': json['process_time'],
                'bd_time': json['bd_time']
            }

        except:
            stdout.write('x')
        window.release()

def execute(threads):
    for t in threads:
        window.acquire()
        t.start()
    for t in threads:
        t.join()


def run_experiment(queries, results, rides, rep):
    clear_database()

    driver = create_user(114110000)
    passenger = create_user(114110001)

    query = gen_query(results)

    print queries, results, rides, rep

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
        t = Search(passenger, query)
        threads.append(t)

    execute(threads)
    stdout.write('\n')

    def avg(x):
        return sum(t.result[x] for t in threads if t.result is not None) / queries

    net_time = avg('net_time')
    process_time = avg('process_time')
    bd_time = avg('bd_time')

    output.write('%d,%d,%d,%s,%s,%s\n' % (
        queries, results, rides,
        net_time, process_time, bd_time
    ))

    output.flush()

def repeat_experiment(queries, results, rides, reps=50):
    for i in xrange(reps):
        run_experiment(queries, results, rides, i)


repeat_experiment(1, 10, 100)
repeat_experiment(1, 10, 1000)
repeat_experiment(1, 100, 100)
repeat_experiment(1, 100, 1000)
repeat_experiment(200, 10, 100)
repeat_experiment(200, 10, 1000)
repeat_experiment(200, 100, 100)
repeat_experiment(200, 100, 1000)

output.close()
