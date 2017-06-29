from client import Authenticator

auth = Authenticator('http://destroctor51.pythonanywhere.com', '114110495', '12345')

r = auth.request('POST', '/api/rides', json={
    'dest': 'UFCG',
    'weekly': False,
    'origin': 'Minha casa poxa',
    'route': ['Bodocongo', 'Alto Branco'],
    'seats': 1,
    'date': 1498791600000
})

print r.text

r = auth.request('GET', '/api/rides', params={
    'dest': 'UFCG',
    'district': 'Bodocongo',
    'date': 1498791600000,
    'weekly': 'false',
    'page': 1
})

print r.json()
