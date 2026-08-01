import math
from utilidades import truncar

def calcular_fresnel(distancia_total, frecuencia):
    """
    Calcula el radio de la Primera Zona de Fresnel
    usando la fórmula proporcionada en la consigna.
    """
    fresnel = 8.656 * math.sqrt(distancia_total / frecuencia)
    return truncar(fresnel)

def calcular_linea_de_vista(
        distancia_total,
        altura_antena1,
        altura_antena2,
        distancia_obstaculo):
    """
    Calcula la altura de la línea de vista
    en el punto donde se encuentra el obstáculo.
    """
    pendiente = (altura_antena2 - altura_antena1) / distancia_total
    altura = altura_antena1 + (pendiente * distancia_obstaculo)
    return truncar(altura)

def calcular_despeje(
        altura_linea,
        altura_obstaculo):
    """
    Calcula el espacio libre entre
    la línea de vista y el obstáculo.
    """
    despeje = altura_linea - altura_obstaculo
    return truncar(despeje)

def calcular_invasion(
        despeje,
        radio_fresnel):
    """
    Calcula el porcentaje de invasión
    de la Zona de Fresnel.
    """
    invasion = ((radio_fresnel - despeje) / radio_fresnel) * 100
    if invasion < 0:
        invasion = 0
    if invasion > 100:
        invasion = 100
    return truncar(invasion)

def clasificar_enlace(invasion):
    """
    Devuelve el estado del enlace.
    """
    if invasion <= 20:
        return (
            "ÓPTIMO",
            "green",
            "El obstáculo invade menos del 20 % de la Zona de Fresnel.\n"
            "El enlace debería funcionar correctamente."
        )
    elif invasion <= 40:
        return (
            "FUNCIONA",
            "#C28A00",
            "El obstáculo invade entre el 20 % y el 40 %.\n"
            "El enlace probablemente funcione,\n"
            "aunque sería recomendable elevar alguna antena."
        )
    else:
        return (
            "NO FUNCIONA",
            "red",
            "El obstáculo invade más del 40 % de la Zona de Fresnel.\n"
            "Se recomienda aumentar la altura de las antenas\n"
            "o cambiar el recorrido del enlace."
        )

def calcular_enlace(
        distancia_total,
        frecuencia,
        altura_antena1,
        altura_antena2,
        distancia_obstaculo,
        altura_obstaculo):
    """
    Realiza todos los cálculos del enlace.
    """
    d1 = distancia_obstaculo
    d2 = distancia_total - distancia_obstaculo
    fresnel = calcular_fresnel(
        distancia_total,
        frecuencia
    )
    linea = calcular_linea_de_vista(
        distancia_total,
        altura_antena1,
        altura_antena2,
        distancia_obstaculo
    )
    despeje = calcular_despeje(
        linea,
        altura_obstaculo
    )
    invasion = calcular_invasion(
        despeje,
        fresnel
    )
    estado, color, mensaje = clasificar_enlace(
        invasion
    )
    return {
        "fresnel": fresnel,
        "linea": linea,
        "despeje": despeje,
        "invasion": invasion,
        "estado": estado,
        "color": color,
        "mensaje": mensaje
    }