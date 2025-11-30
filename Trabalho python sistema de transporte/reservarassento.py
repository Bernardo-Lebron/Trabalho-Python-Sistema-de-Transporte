import random

def reservar_assento_automatico(onibus):
    """Reserva um assento automaticamente. Modifica onibus e retorna assento ou None."""
    
    # lista todos os assentos livres
    livres = [n for n, livre in onibus.items() if livre]

    # se não houver nenhum retorna None
    if not livres:
        return None
    
    # escolhe um aleatório
    escolhido = random.choice(livres)

    # marca como ocupado
    onibus[escolhido] = False

    # retorna o número do assento
    return escolhido
