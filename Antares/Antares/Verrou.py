# -*- coding: utf-8 -*-
import os
from django.conf import settings


class Verrou:
    def __init__(self, fichier):
        self.fichier = os.path.join(settings.SITE_ROOT, 'verrous/' + fichier)
        self.fd = None
        self.pid = os.getpid()

    def ferme(self):
        try:
            self.fd = os.open(self.fichier, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.write(self.fd, "%d" % self.pid)
            return 1
        except OSError:
            self.fd = None
            return 0

    def ouvre(self):
        if not self.fd:
            return 0
        try:
            os.close(self.fd)
            os.remove(self.fichier)
            self.fd = None
            return 1
        except OSError:
            return 0

    def __del__(self):
        self.release()
