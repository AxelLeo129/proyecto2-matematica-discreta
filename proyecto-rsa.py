# PROYECTO RSA

# Importamos las librerias necesarias
import random
import pandas as pd

# En base al PDF del proyecto, se tiene que crear una función que genere primos, por lo tanto: 


# GENERAR PRIMO:
"""
Esta parte se divide en dos funciones, la primera es para verificar si un número es primo 
y la segunda es para generar un número primo en un rango especificado, tal y como se pide en el PDF del proyecto, 
si en caso no se encuentra un número primo en el rango especificado, se imprime un mensaje de error.
"""

def es_primo(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False # Si el numero es menor o igual a 1, no es primo.
    return True

def generar_primo(rango_inferior, rango_superior):
    primos = [num for num in range(rango_inferior, rango_superior + 1) if es_primo(num)]
    
    if not primos:
        return print("No se encontraron números primos en el rango especificado")
    
    return random.choice(primos)


# MCD de dos números, realizado en clase:
"""
Al igual que la primera funcion, esta se divide en dos funciones, la primera es para verificar si un número
que se ingreso es un entero positivo y la segunda es para calcular el MCD de dos números, cabe mencionar que
esta funcion es la misma que se trabajo en clase.
"""
def entero_positivo():
    x = int(input('Ingrese el número (debe ser positivo): '))
    while x <= 0:
        print("El número debe ser un entero positivo.")
        x = int(input('Ingrese nuevamente el número: '))
    return x

def mcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# INVERSO MODULAR:
"""
Como el nombre de la funcion lo indica, esta funcion se encarga de calcular el inverso modular de dos números
que se ingresen usando el algoritmo extendido de Euclides y si en caso no exista el inverso modular, se imprime un mensaje de error.
"""
def inverso_modular(e, n):
    def gcd_extended(a, b):
        if b == 0:
            return a, 1, 0 # se retorna el MCD y los valores de x=1 y y=0
        gcd, x1, y1 = gcd_extended(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

    gcd, x, _ = gcd_extended(e, n)
    if gcd != 1: # Si el MCD no es 1, no existe el inverso modular porque e y n no son coprimos 
        raise ValueError(f"El inverso modular no existe porque {e} y {n} no son coprimos.")
    return x % n


def generar_llaves(rango_inferior, rango_superior):
    # Generar dos números primos p y q
    p = generar_primo(rango_inferior, rango_superior)
    q = generar_primo(rango_inferior, rango_superior)
    while p == q:  # Asegurarse de que p y q sean distintos
        q = generar_primo(rango_inferior, rango_superior)
    
    # Calcular n y φ(n)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Elegir e tal que sea coprimo con φ(n)
    e = random.choice([x for x in range(2, phi) if mcd(x, phi) == 1])
    
    # Calcular d (inverso modular de e mod φ(n))
    try:
        d = inverso_modular(e, phi)
    except ValueError as ve:
        return None, f"Error generando llaves: {ve}"
    
    # Llave pública: (e, n), Llave privada: (d, n)
    return (e, n), (d, n)

def encriptar(mensaje, llave_publica):
    e, n = llave_publica
    if mensaje < 0 or mensaje >= n:
        raise ValueError("El mensaje debe ser un número positivo menor que n.")
    return pow(mensaje, e, n)  # mensaje^e mod n

def desencriptar(caracter_encriptado, llave_privada):
    d, n = llave_privada
    if caracter_encriptado < 0 or caracter_encriptado >= n:
        raise ValueError("El caracter encriptado debe ser un número positivo menor que n.")
    return pow(caracter_encriptado, d, n)  # caracter_encriptado^d mod n

# Modificación para permitir ingreso de límites y mensajes con programación defensiva
def main():
    try:
        # Solicitar límites para la generación de llaves con validación
        while True:
            try:
                rango_inferior = int(input("Ingrese el límite inferior del rango de búsqueda de números primos (entero positivo): "))
                rango_superior = int(input("Ingrese el límite superior del rango de búsqueda de números primos (entero positivo mayor que límite inferior): "))
                if rango_inferior > 0 and rango_superior > rango_inferior:
                    break
                else:
                    print("Los límites deben ser enteros positivos y el superior debe ser mayor al inferior.")
            except ValueError:
                print("Entrada inválida. Por favor ingrese números enteros positivos.")

        # Generar llaves
        llave_publica, llave_privada = generar_llaves(rango_inferior, rango_superior)
        if llave_publica is None or llave_privada is None:
            print("No se pudieron generar llaves válidas. Intente con un rango diferente.")
            return

        print("\nLlave pública: " + str(llave_publica))
        print("Llave privada: " + str(llave_privada) + "\n")

        # Solicitar mensajes para encriptar y desencriptar con validación
        while True:
            try:
                cantidad_mensajes = int(input("Ingrese la cantidad de mensajes que desea probar (entero positivo): "))
                if cantidad_mensajes > 0:
                    break
                else:
                    print("La cantidad de mensajes debe ser un entero positivo.")
            except ValueError:
                print("Entrada inválida. Por favor ingrese un número entero positivo.")

        mensajes = []
        for i in range(cantidad_mensajes):
            while True:
                try:
                    mensaje = int(input(f"Ingrese el mensaje {i+1} (debe ser positivo y menor que n={llave_publica[1]}): "))
                    if 0 < mensaje < llave_publica[1]:
                        mensajes.append(mensaje)
                        break
                    else:
                        print(f"El mensaje debe ser un número positivo menor que n={llave_publica[1]}.")
                except ValueError:
                    print("Entrada inválida. Por favor ingrese un número entero positivo.")

        # Proceso de encriptar y desencriptar
        resultados = []
        for mensaje in mensajes:
            try:
                # Encriptar el mensaje
                mensaje_cifrado = encriptar(mensaje, llave_publica)
                # Desencriptar el mensaje cifrado
                mensaje_descifrado = desencriptar(mensaje_cifrado, llave_privada)
                resultados.append({
                    "mensaje_original": mensaje,
                    "mensaje_cifrado": mensaje_cifrado,
                    "mensaje_descifrado": mensaje_descifrado
                })
            except Exception as e:
                print(f"Error procesando el mensaje {mensaje}: {e}")

        # Mostrar resultados
        df_resultados = pd.DataFrame(resultados)
        print("\nResultados:")
        print(df_resultados)
    except Exception as e:
        print(f"Error crítico: {e}")

# Ejecutar la función principal
main()

"""
REFERENCIAS:

1. https://www.geeksforgeeks.org/rsa-algorithm-cryptography/
2. https://www.geeksforgeeks.org/python-program-for-basic-and-extended-euclidean-algorithms/
3. https://www.geeksforgeeks.org/python-program-for-gcd-of-more-than-two-or-array-numbers/

"""