import random

def reservar_assento_automatico(onibus):
    """Reserva um assento automaticamente. Modifica onibus e retorna assento ou None."""
    
    livres = [n for n, livre in onibus.items() if livre] #Lista de assentos livres
    if not livres: #Se não houver assentos livres
        return None #Retorna None indicando que não foi possível reservar
    escolhido = random.choice(livres) #Escolhe um assento livre aleatoriamente
    onibus[escolhido] = False #Marca o assento como ocupado

    return escolhido #Retorna o número do assento reservado