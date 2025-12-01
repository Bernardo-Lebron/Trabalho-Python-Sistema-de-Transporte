import random

def reservar_assento_automatico(onibus):
    """Reserva um assento automaticamente. Modifica onibus e retorna assento ou None."""
    
    livres = [n for n, livre in onibus.items() if livre]
    if not livres:
        return None
    escolhido = random.choice(livres)
    onibus[escolhido] = False

    return escolhido