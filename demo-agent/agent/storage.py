# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import logging
import os
from tinydb import TinyDB
from pathlib import Path


class Storage:
    """
    Lightweight storage based on TinyDB.
    Ensures all data is stored in a directory named by site id
    """
    _logger = logging.getLogger(__name__)

    def __init__(self, siteId) -> None:
        self.varDir = "var-%s" % siteId
        path = os.path.join(os.getcwd(), self.varDir)
        Path(path).mkdir(parents=True, exist_ok=True)

        self.usersDB = TinyDB(self.varDir + '/users.json')
        self.allocationChunksDB = TinyDB(self.varDir + '/allocation_chunks.json')
        self.allocationsDB = TinyDB(self.varDir + '/allocations.json')
        self.projectsDB = TinyDB(self.varDir + '/projects.json')
        self.usersAccessDB = TinyDB(self.varDir + '/users_access.json')

    def dispose(self):
        self._dispose(self.usersDB)
        self._dispose(self.allocationChunksDB)
        self._dispose(self.allocationsDB)
        self._dispose(self.projectsDB)
        self._dispose(self.usersAccessDB)

    @staticmethod
    def _dispose(db):
        db.drop_tables()
        db.close()
