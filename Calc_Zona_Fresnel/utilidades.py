import math

def truncar(numero, decimales=2):
    """
    Trunca un número sin redondearlo.
    """
    factor = 10 ** decimales
    return math.trunc(numero * factor) / factor

def convertir_numero(texto):
    """
    Convierte un texto a float.
    Acepta coma o punto decimal.
    """
    texto = texto.strip()
    if texto == "":
        raise ValueError("Campo vacío.")
    # No permitir mezclar coma y punto
    if "," in texto and "." in texto:
        raise ValueError("No mezcle coma y punto.")
    texto = texto.replace(",", ".")
    try:
        numero = float(texto)
    except:
        raise ValueError("Número inválido.")
    if numero <= 0:
        raise ValueError("El valor debe ser mayor que cero.")
    return numero

def validar_obstaculo(distancia_total, distancia_obstaculo):
    """
    Verifica que el obstáculo esté dentro del enlace.
    """
    if distancia_obstaculo >= distancia_total:
        raise ValueError(
            "El obstáculo debe estar ubicado entre ambas antenas."
        )
    return True