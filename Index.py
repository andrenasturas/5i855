# coding: utf-8


class Index(object):
    """
        Index

        Objet construisant et conservant les index et index inversé d'un corpus textuel.
    """

    def __init__(self, name, parser, textRepresenter):
        """
            Initialise un objet Index

            :param name: Nom de l'index
            :param parser: Parseur à utiliser
            :param textRepresenter: Représentation du corpus
            :type name: str
            :type parser: Parser
            :type textRep: TextRepresenter
        """

        self.name = name
        self.docs = {}
        self.stems = {}
        self.docFrom = {}
        self.parser = parser
        self.textRep = textRepresenter

    def writeDict(self, dic):
        """
            Convertit un dictionnaire en une chaîne de caractères

            Cette fonction est utilisée lors de la sauvegarde sur disque d'un
            dictionnaire. Il est aussi possible d'écrire le dictionnaire
            directement, et de le lire ensuite à l'aide de la fonction native
            eval(), de sa version sécurisée ast.literal_eval(), ou en parsant
            le dictionnaire à l'aide du paquet json, ou encore en utilisant
            la sérialisation pickle.

            L'intér¤t de cette fonction est de proposer une sérialisation des
            dictionnaires la moins verbeuse possible, et dans un seul et m¤me
            fichier, ce qui sert l'objectif principal de performance visé ici.

            :param dic: Un dictionnaire à sérialiser
            :type dic: dict
            :return: Représentation en cha→ne de caractères du dictionnaire
            :rtype: str
        """

        return ';'.join([w + ":" + str(n) for w, n in dic.items()]).encode()

    def readDict(self, b):
        """
            Convertit une cha→ne de caractères en dictionnaire

            Convertit en dictionnaire python une cha→ne de caractères produite
            par la fonction Index.writeDict()

            .. seealso:: writeDict()

            :param b: Cha→ne à convertir
            :type b: str
            :return: Dictionnaire lu
            :rtype: dict
        """

        return {w: int(n) for w, n in [s.split(':') for s in b.decode().split(';')]}


    def indexation(self):
        """
            Effectue l'indexation du corpus
        """

        self.indexDirect()
        self.indexInversed()


    def indexDirect(self):
        """
            Effectue l'indexation normale du corpus
        """

        with open("./" + self.name + "_index", "wb") as ifile:
            ifcur = 0

            # Pour chaque document
            d = self.parser.nextDocument()
            while (d):
                # Lecture document
                id = d.getId()
                st = self.textRep.getTextRepresentation(d.getText().encode())

                # Écriture index
                ifile.write(self.writeDict(st))
                nfcur = ifile.tell()
                self.docs[id] = (ifcur, nfcur - ifcur)

                # Écriture table DocFrom
                docFrom = d.get("from").split(";")
                self.docFrom[id] = docFrom

                # Initialisation stems
                for s in st:
                    self.stems[s] = None

                # Itération
                ifcur = nfcur
                d = self.parser.nextDocument()

    def indexInversed(self):
        """
            Indexation inversée
        """

        with open("./" + self.name + "_inverted", "wb") as ifile:
            ifcur = 0

            for s in self.stems:

                # Pour chaque document
                d = self.parser.nextDocument()
                while(d):
                    st = self.textRep.getTextRepresentation(d.getText().encode())

                    c = t.count(s)
                    if c > 0:
                        ifile.write(d.getId() + ":" + c + ";")

                    # Itération
                    d = p.nextDocument()

                # Écriture index
                ifile.seek(-1, 1)   # suppression dernier point-virgule
                nfcur = ifile.tell()
                ifile.write("\n")
                self.stems[s] = (ifcur, nfcur-ifcur)

                # Itération
                ifcur = nfcur

    def getTfsForDoc(self, doc):
        """
            Retourne la représentation stem-tf d'un document depuis l'index

            Retrouve un document déjà indexé par son identifiant, et renvoie un
            dictionnaire contenant tous les stems du document respectivement
            associés à leurs nombres d'apparition dans celui-ci.

            :param doc: Identifiant du document
            :type doc: str
            :return: Représentation stem-tf
            :rtype: dict
        """
        ifile = open("./" + self.name + "_index", "rb")
        ifile.seek(self.docs[doc][0])
        return self.readDict(ifile.read1(self.docs[doc][1]))

    def getTfsForStem(self, stem):
        """
            Retourne la représentation doc-tf d'un document depuis l'index

            Pour un stem déjà indexé donné, retourne un dictionnaire contenant
            l'identifiant de tous les documents dans lequel il apparait,
            associés au nombre d'apparition du stem dans chacun de ces
            documents.

            :param stem: Stem recherché
            :type stem: str
            :return: Représentation doc-tf
            :rtype: dict
        """
        ifile = open("./" + self.name + "_inverted", "rb")
        try:
            ifile.seek(self.stems[stem][0])
            dic = self.readDict(ifile.read1(self.stems[stem][1]))
        except KeyError:
            dic = dict()
        return dic

    def getStrDoc(self, doc):
        """
            Retourne le texte brut d'un document

            Retourne le texte brut d'un document tel qu'il existe dans les
            fichiers sources indexés.

            :param doc: Document recherché
            :type doc: str
            :return: Texte brut du document
            :rtype: str
        """
        f = open(self.docFrom[0], "rb")
        f.seek(self.docFrom[1])
        return f.read1(self.docFrom[2])
