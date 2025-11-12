from got import *
ruta = "data/battles.csv"
def test_lee_batallas():
    resultado = lee_batallas(ruta)
    print("el ultimo elemento es:", resultado[-1])
    
def test_reyes_ejercitos():
    batallas = lee_batallas(ruta)
    resultado = reyes_ejercitos(batallas)
    print("Los reyes con menor y mayor ejercito son:", resultado[1], resultado[0])
    
def test_batallas_mas_comandantes():
    batallas = lee_batallas(ruta)
    resultado = batallas_mas_comandantes(batallas, {'The North', 'The Riverlands'}, None)
    print("Las 3 batallas con mas comandantes son:", resultado)
    
def test_rey_mas_victorias():
    batallas = lee_batallas(ruta)
    resultado = rey_mas_victorias(batallas, "ambos")
    print("El rey con mas victorias es:", resultado)
    
def funcion_principal():
    #test_lee_batallas()
    #test_reyes_ejercitos()
    #test_batallas_mas_comandantes()
    test_rey_mas_victorias()
    
if __name__ == "__main__":
    funcion_principal()