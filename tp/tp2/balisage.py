def sep_ligne(txt):
    with open(txt+".txt", 'r') as reader:
        text = reader.read()
        text.split(".")
    print(text)

sep_ligne("textes/caillou")
sep_ligne("textes/chataignes")
sep_ligne("textes/hamsasung")
