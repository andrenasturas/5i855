# coding: utf-8

import time
import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)
log_format = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
log.addHandler(stream_handler)



class IRmodel(object):
    """
        IRmodel
    """

    def __init__(self, index):
        """
            Initialise un objet IRmodel

            :param index: Objet Index
            :type  index: Index
        """

        self.index = index


    def getScores(query):
        """
            Retourne les scores des documents pour une requête donnée

            :param query: Requête à traiter
            :type  query: str
        """
        return NotImplementedError


    def getRanking(query):
        """
            Retourne le scores de chacun des documents

            :param stem: Terme à traiter
            :type  stem: str
        """
        return sorted(self.getScores(query).items(), key=lambda t: t[1], reverse=True)
