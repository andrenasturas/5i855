import TextRepresenter, Index, ParserCACM, pickle

p = ParserCACM.ParserCACM()
t = TextRepresenter.PorterStemmer()
i = Index.Index("Index", p, t, "cacm/cacm.txt")

i.indexation()

with open('Index', 'wb') as f:
    pick = pickle.Pickler(f)
    pick.dump(i)