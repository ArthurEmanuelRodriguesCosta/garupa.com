import re

from hashlib import md5
from os import urandom
from requests import request
from urllib import urlencode

base_url = 'http://localhost:8000'
#base_url = 'http://destroctor51.pythonanywhere.com'

class Auth(object):
	realm = None
	nonce = None
	cnonce = None
	nc = 0

	def __init__(self, user, passwd):
		self.user = user
		self.passwd = passwd

	def nc_str(self):
		return format(self.nc, '016x')

	def gen_nonce(self):
		return urandom(8).encode('hex')

	def hash_all(self, *args):
		strings = map(str, args)
		concat = ':'.join(strings)
		return md5(concat).hexdigest()

	def make_header(self, method, url, params):
		if self.realm is None:
			return None

		uri = url
		if params is not None:
			uri += '?' + urlencode(params)

		response = self.hash_all(
			self.hash_all(self.user, self.realm, self.passwd),
			self.nonce, self.nc_str(), self.cnonce, 'auth',
			self.hash_all(method, uri)
		)

		return {
			'Authorization':
				'Digest username=%s, realm=%s, nonce=%s, uri=%s, qop=auth, nc=%s, cnonce=%s, response=%s' %
				(self.user, self.realm, self.nonce, uri, self.nc_str(), self.cnonce, response)
		}

	def request(self, method, url, params=None, json=None):
		headers = self.make_header(method, url, params)
		self.nc += 1

		r = request(method, base_url+url, headers=headers, params=params, json=json)

		if r.status_code is 200:
			return r

		auth = r.headers['WWW-Authenticate']

		realm = re.search('realm="(.*?)"', auth)
		nonce = re.search('nonce="(.*?)"', auth)
		stale = re.search('stale="(.*?)"', auth)

		self.realm = realm.group(1)
		self.nonce = nonce.group(1)
		self.cnonce = self.gen_nonce()
		self.nc = 1

		if stale and stale.group(1) == 'true' or headers == None:
			return self.request(method, url, params, json)

def clear_database():
    request('DELETE', base_url+'/api')

def create_user(uid):
    r = request('POST', base_url+'/api/users', json={
        'uid': uid,
        'passwd': 'default',
        'name': 'default',
        'email': 'default@mail.com'
    })

    if r.status_code is 200:
        return Auth(uid, 'default')
    return None
