import random

def reservar_assento_automatico(onibus):
    # pega todos os assentos livres (True)
    livres = [n for n, livre in onibus.items() if livre]

    if not livres:
        return None
    
    escolhido = random.choice(livres)
    onibus[escolhido] = False
    return escolhido
