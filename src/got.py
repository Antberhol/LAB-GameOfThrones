from typing import List, NamedTuple
import csv
from collections import defaultdict


BatallaGOT = NamedTuple('BatallaGOT',                         
                        [
                            ('nombre', str),
                            ('rey_atacante', str),
                            ('rey_atacado', str),
                            ('gana_atacante', bool),
                            ('muertes_principales', bool),
                            ('comandantes_atacantes', list[str]),
                            ('comandantes_atacados', list[str]),
                            ('region', str),
                            ('num_atacantes', int|None),
                            ('num_atacados',int|None)
                        ])

def lee_batallas(fichero: str) -> list[BatallaGOT]:
    lista = []
    with open(fichero, 'r', encoding='utf-8') as f:
        lector = csv.reader(f)
        next(lector)
        for campos in lector:
            nombre = campos[0]
            rey_atacante = campos[1]
            rey_atacado = campos[2]
            gana_atacante = campos[3].lower() == 'win'
            muertes_principales = campos[4].lower() == 'true'
            comandantes_atacantes = campos[5].split(',')
            comandantes_atacados = campos[6].split(',')
            region = campos[7]
            num_atacantes = int(campos[8]) if campos[8] else None
            num_atacados = int(campos[9]) if campos[9] else None
            
            batalla = BatallaGOT(
                nombre, rey_atacante, rey_atacado, gana_atacante,
                muertes_principales, comandantes_atacantes, comandantes_atacados,
                region, num_atacantes, num_atacados
            )
            
            lista.append(batalla)
    
    return lista


    """
    
    recibe una lista de tuplas de tipo ``BatallaGOT`` y devuelve una tupla con dos cadenas
    correspondientes a los nombres de los reyes con el mayor y el menor ejército, 
    respectivamente, del acumulado de todas las batallas. Para estimar el tamaño 
    del ejército de un rey se deben sumar los números de atacantes o de atacados
    de todas las batallas en las que ha participado dicho rey como atacante o como atacado
    """

def reyes_ejercitos(batallas: list[BatallaGOT]) -> tuple[str, str]:
    resultado = defaultdict(int)
    for  batalla in batallas:
        if batalla.num_atacantes is not None:
            resultado[batalla.rey_atacante] += batalla.num_atacantes
        if batalla.num_atacados is not None:
            resultado[batalla.rey_atacado] += batalla.num_atacados
    rey_mayor = max(resultado.items(), key=lambda x: x[1])[0] #para todos los reyes busca el mayor num atacantes/atacados
    rey_menor = min(resultado.items(), key=lambda x: x[1])[0]
    return (rey_mayor, rey_menor)


    """
    3.	**batallas_mas_comandantes**: recibe una lista de tuplas de tipo ``BatallaGOT``, 
    un conjunto de cadenas ``regiones``, con valor por defecto ``None``, y un valor entero
    ``n`` con valor por defecto ``None``, y devuelve una lista de tuplas ``(str, int)`` con 
    los nombres y el total de comandantes participantes de aquellas n batallas con mayor
    número de comandantes participantes (tanto atacantes como atacados), llevadas a cabo en
    alguna de las regiones indicadas en el parámetro regiones. Si el parámetro ``regiones``
    es ``None`` se considerarán todas las regiones; por su parte, si el parámetro ``n`` es ``None`` 
    se devolverán las tuplas correspondientes a todas las batallas de las regiones escogidas. En todos los casos,
    la lista devuelta estará ordenada de mayor a menor número de comandantes. Por ejemplo, si la función recibe la
    lista completa de batallas contenida en el CSV, y si ``regiones`` es `{'The North', 'The Riverlands'}` y ``n`` es 
    ``4``, la función devuelve ``[('Battle of the Green Fork', 9), ('Battle of the Fords', 9),
    ('Battle of the Camps', 5), ('Sack of Winterfell', 5)]``. _(2 puntos)_
    
    """

def batallas_mas_comandantes(batallas: list[BatallaGOT], regiones: set[str]|None=None, n: int|None=None) -> list[tuple[str, int]]:
    batallas_comandantes = defaultdict(int)
    lista_resultado = []
    for batalla in batallas:
        if regiones is None or batalla.region in regiones or n is None:
            num_comandantes = len(batalla.comandantes_atacantes) + len(batalla.comandantes_atacados)
            batallas_comandantes[batalla.nombre] = num_comandantes
            
    batallas_ordenadas = sorted(batallas_comandantes.items(), key=lambda x: x[1], reverse=True)[:n]
    for nombre, total in batallas_ordenadas:
        lista_resultado.append((nombre, total))
    return lista_resultado  
    
    """
    4.recibe una lista de tuplas de tipo ``BatallaGOT`` y una cadena ``rol``, con valor por defecto ``"ambos"``, y devuelve
    el nombre del rey que acumula más victorias. Tenga en cuenta que un rey puede ganar una batalla en la que actúa como atacante,
    en cuyo caso el campo ``gana_atacante`` será ``True``, o una batalla en la que actúa como atacado, en cuyo caso el campo
    ``gana_atacante`` será ``False``. Si el parámetro ``rol`` es igual a ``"atacante"``, se devolverá el nombre del rey que
    acumula más victorias como atacante; si ``rol`` es igual a ``"atacado"``, se devolverá el nombre del rey que acumula más 
    victorias como atacado; si ``rol`` es igual a ``"ambos"``, se devolveré el nombre del rey que acumula más victorias en todas
    las batallas en las que ha participado (sumando sus victorias como atacante y como atacado). Si ningún rey acumula victorias
    del rol especificado en la lista de batallas recibida, la función devuelve ``None``. Por ejemplo, si el parámetro rol contiene
    ``"ambos"`` y la función devuelve ``"Stannis Baratheon"``, significa que dicho rey es el que ha ganado más batallas de
    la lista de batallas recibida, sumando tanto las
    victorias en batallas en las que fue atacante, como las victorias en batallas en las que fue atacado. _(2,75 puntos)_
    
    """
def rey_mas_victorias(batallas: list[BatallaGOT], rol: str="ambos") -> str|None:
    diccionario_victorias = defaultdict(int)
    for batalla in batallas:
        if rol =="atacante" or rol =="ambos":
            if batalla.gana_atacante:
                diccionario_victorias[batalla.rey_atacante] += 1
        if rol =="atacado" or rol =="ambos":
            if  not batalla.gana_atacante:
                diccionario_victorias[batalla.rey_atacado] += 1
        if rol!="atacante" and rol!="atacado" and rol!="ambos":
            return None
    if not diccionario_victorias:
        return None
    rey_ganador = max(diccionario_victorias.items(), key=lambda x: x[1])[0]
    return rey_ganador

    """
    5.	**rey_mas_victorias_por_region**: recibe una lista de tuplas de tipo ``BatallaGOT`` y una cadena ``rol``,
    con valor por defecto ``"ambos"``, y devuelve un diccionario que relaciona cada región con el nombre del
    rey que acumula más victorias en batallas ocurridas en esa región. El parámetro ``rol`` tiene el mismo
    significado que en la función anterior. Si para alguna región no hay ningún rey que haya ganado una batalla
    con el rol especificado, en el diccionario aparecerá el valor ``None`` asociado a dicha región. Puede usar la
    función ``rey_mas_victorias`` para resolver este ejercicio. 
Por ejemplo, si pasamos a la función la lista completa de batallas contenida en el CSV, y 
el parámetro ``rol`` contiene ``"ambos"``, la función devuelve un diccionario que, entre otros ítems, 
asocia la clave ``"The Stormlands"`` a ``"Joffrey Baratheon"``; esto significa que dicho rey es el que 
ganó más batallas de entre las batallas ocurridas en "The Stormlands", sumando tanto las victorias en batallas
en las que fue atacante, como las victorias en batallas en las que fue atacado. _(2 puntos)_
    """
    
def rey_mas_victorias_por_region(batallas: list[BatallaGOT], rol: str="ambos") -> dict[str, str|None]: 
    batallas_por_region= defaultdict(list)
    resultado = {} 
    for batalla in batallas: 
        batallas_por_region[batalla.region].append(batalla)
    for region, lista_batallas in batallas_por_region.items():
        rey= rey_mas_victorias(lista_batallas, rol)
        resultado[region]= rey
    return resultado