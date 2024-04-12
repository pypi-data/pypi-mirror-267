import math

def puntoMedio(self, punto1, punto2):
    # Calcular el punto medio entre dos puntos
    medio_x = (punto1[0] + punto2[0]) / 2
    medio_y = (punto1[1] + punto2[1]) / 2
    return medio_x, medio_y
    # Calcular El caso que corresponde

def analisisRumboVeta(self, punto1, punto2):
    try:
        x1, y1, z1 = punto1
        x2, y2 = punto2
        caso = None
        titulo = None
        azimut = None
        Rv = None

        if x1 > x2 and y1 > y2  and (y1 - y2) != 0:
            Rv = math.atan((x1 - x2)/(y1 - y2))*180/math.pi
            caso = "Caso 1"
            titulo = "SW"
            azimut = (180 + Rv)
        elif x2 > x1 and y2 > y1 and (y2 - y1) != 0:
            Rv = math.atan((x2 - x1)/(y2 - y1))*180/math.pi
            caso = "Caso 1"
            titulo = "NE"
            azimut = Rv
        elif x1 > x2  and y2 > y1 and (y2 - y1) != 0:
            Rv = math.atan((x1 - x2)/(y2 - y1))*180/math.pi
            caso = "Caso 2"
            titulo = "NW"
            azimut = (360 - Rv)
        elif x2 > x1  and y1 > y2 and (y1 - y2) != 0:
            Rv = math.atan((x2 - x1)/(y1 - y2))*180/math.pi
            caso = "Caso 2"
            titulo = "SE"
            azimut = (180 - Rv)

        return {"caso": caso, "titulo": titulo, "azimut": azimut, "Rv": Rv}

    except ValueError:
        # Manejar la excepción de valor no válido (por ejemplo, cuando se ingresa texto en lugar de un número)
        print('Error: Ingrese un número válido.')
    except Exception as e:
        # Manejar otras excepciones no específicas
        print(f'Se produjo un error: {e}')
    return False   