#!/usr/bin/env python
# SPDX-FileCopyrightText: 2019,2024 Jérôme Carretero <cJ-rack@zougloub.eu> & contributors
# SPDX-License-Identifier: MIT

import logging
import hashlib
import marshal

import lmdb


logger = logging.getLogger(__name__)


def h(x: bytes):
	"""
	Default hasher"
	"""
	return hashlib.sha256(x).digest()

loads = marshal.loads
dumps = marshal.dumps

class PersistentDict:
	"""
	Persistent dict using LMDB database as backend
	"""
	def __init__(self, name=None, hasher=None, serdes=None):
		self._name = name
		if hasher is None:
			hasher = h
		self._h = hasher
		if serdes is None:
			self._loads = loads
			self._dumps = dumps
		else:
			self._loads, self._dumps = serdes

	def __enter__(self):
		self._env = env = lmdb.open(self._name + ".lmdb",
		 subdir=False,
		 max_dbs=4,
		 sync=False,
		 map_size=(50<<30),
		)

		self.h2n = env.open_db(b"h2n",
		 dupsort=True,
		 dupfixed=True,
		 create=True,
		)

		self.n2k = env.open_db(b"n2k",
		 create=True,
		)

		self.n2v = env.open_db(b"n2v",
		 create=True,
		)

		return self

	def __exit__(self, ext_type, exc_value, exc_tb):
		self._env.close()


	def _set(self, txn, key, value):
		k = self._dumps(key)
		v = self._dumps(value)
		h = self._h(k)

		with txn.cursor(db=self.h2n) as cur:
			res = cur.set_key(h)
			if res:
				logger.debug("Found compatible hash key")
				for n_ in cur.iternext_dup():
					d = txn.get(n_, db=self.n2k)
					if d == k:
						logger.debug("Replace %s (%d) = %s",
						 key, int.from_bytes(n_, "big"), value)
						txn.put(n_, v, db=self.n2v)
						return

			with txn.cursor(db=self.n2k) as cur:
				res = cur.last()
				if res:
					n_ = int.from_bytes(cur.key(), "big")+1
				else:
					n_ = 1
			n = n_.to_bytes(8, "big")
			logger.debug("Insert #%d", n_)
			txn.put(h, n, db=self.h2n)
			txn.put(n, k, db=self.n2k)
			txn.put(n, v, db=self.n2v)

	def __setitem__(self, key, value):
		with self._env.begin(write=True) as txn:
			self._set(txn, key, value)

	def __getitem__(self, key):
		with self._env.begin() as txn:
			k = self._dumps(key)
			h = self._h(k)

			with txn.cursor(db=self.h2n) as cur:
				res = cur.set_key(h)
				if res:
					for n_ in cur.iternext_dup():
						d = txn.get(n_, db=self.n2k)
						if d == k:
							return self._loads(txn.get(n_, db=self.n2v))

		raise KeyError(key)

	def get(self, key, default=None):
		with self._env.begin() as txn:
			k = self._dumps(key)
			h = self._h(k)

			with txn.cursor(db=self.h2n) as cur:
				res = cur.set_key(h)
				if res:
					for n_ in cur.iternext_dup():
						d = txn.get(n_, db=self.n2k)
						if d == k:
							return self._loads(txn.get(n_, db=self.n2v))

		return default

	def update(self, other=None, **kw):
		with self._env.begin(write=True) as txn:
			if other:
				for k, v in other:
					self._set(txn, k, v)

			for k, v in kw.items():
				self._set(txn, k, v)

	def __contains__(self, key):
		with self._env.begin() as txn:
			k = self._dumps(key)
			h = self._h(k)

			with txn.cursor(db=self.h2n) as cur:
				res = cur.set_key(h)
				if res:
					for n_ in cur.iternext_dup():
						d = txn.get(n_, db=self.n2k)
						if d == k:
							return True
		return False

	def __len__(self):
		"""
		:return: number of items in dict
		"""
		with self._env.begin(db=self.n2k) as txn:
			s = txn.stat()
			entries = s["entries"]
			return entries

	def keys(self):
		env = self._env
		with env.begin(db=self.n2k) as txn:
			curk = txn.cursor()
			curk.first()
			while True:
				k = curk.value()
				yield self._loads(k)
				if not curk.next():
					break

	def values(self):
		env = self._env
		with env.begin(db=self.n2v) as txn:
			curv = txn.cursor()
			curv.first()
			while True:
				v = curv.value()
				yield self._loads(v)
				if not curv.next():
					break

	def items(self):
		env = self._env
		with env.begin() as txn:
			curk = txn.cursor(db=self.n2k)
			curv = txn.cursor(db=self.n2v)
			curk.first()
			curv.first()
			while True:
				k = curk.value()
				v = curv.value()
				yield self._loads(k), self._loads(v)
				if not curk.next() and curv.next():
					break

	def __iter__(self):
		env = self._env
		with env.begin(db=self.n2k) as txn:
			cur = txn.cursor()
			cur.first()
			while True:
				v = cur.value()
				yield self._loads(v)
				if not cur.next():
					break
