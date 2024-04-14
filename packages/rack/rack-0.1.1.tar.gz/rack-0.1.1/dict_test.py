#!/usr/bin/env python
# SPDX-FileCopyrightText: 2024 Jérôme Carretero <cJ-rack@zougloub.eu> & contributors
# SPDX-License-Identifier: MIT

import logging

from .dict import PersistentDict as dict_


logger = logging.getLogger(__name__)


def test_smoke():
	with dict_(name="pouet") as d:
		d[1] = 2
		assert d[1] == 2

		assert 1 in d

		d["2"] = 3
		assert d.get("2") == 3

		d.update(a=1)

		d["2"] = 4

		logger.info("keys")
		for x in d:
			logger.info("- %s", x)

		logger.info("keys")
		for k in d.keys():
			logger.info("- k:%s", k)

		logger.info("values")
		for v in d.values():
			logger.info("- v:%s",  v)

		logger.info("items")
		for k, v in d.items():
			logger.info("- %s=%s", k, v)

		logger.info("keys2")
		for k in d:
			logger.info("- %s", k)
