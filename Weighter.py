# coding: utf-8


class Weighter(object):
    """
        Weighter

        Pondération des termes d'un corpus pour vectorisation.
    """

    def __init__(self, index):
        """
            Initialise un objet Weighter

            :param index: Index à utiliser
            :type  index: Index
        """

        self.index = index


    def getDocWeightsForDoc(self, document_id):
        """
            Retourne les poids des termes pour un document donné

            :param document: Identifiant du document à traiter
            :type  document: str
        """
        return self.index.getTfsForDoc(document_id)


    def getDocWeightsForStem(self, stem):
        """
            Retourne les poids d'un terme donné pour tous les documents

            :param stem: Terme à traiter
            :type  stem: str
        """
        return self.index.getTfsForStem(stem)


    def getWeightsForQuery(self, query):
        """
            Retourne les poids des termes d'une requête donnée pour tous les documents

            :param query: Requête à traiter
            :type  query: str
        """
        return { **dict.fromkeys(self.index.stems, 0),\
        **self.index.textRepresenter.getTextRepresentation(query) }
