from transliterate import translit


def transliterate(name):
    return translit(name, 'ru', reversed=True).replace(" ", "_").replace("'", "")
