import argparse
import sys
import os
# La funcion optimizar_ataques recibe:
# x: un arreglo con la cantidad de soldados que atacaran en cada minuto
# f: un arreglo con la cantidad de soldados que se pueden eliminar lanzando un ataque
# n: cantidad de minutos

# Devuelve:
#   - total_eliminados: entero con el máximo total posible
#   - ataques: lista de minutos (1-based) en los que atacar (en orden cronológico)
#   - dp: arreglo DP (1-based) con los máximos hasta cada minuto

# Complejidad: O(n^2) tiempo

def optimizar_ataques(x, f, n):
    # usar indexación 1-based para DP y claridad
    X = [0] + x[:]          # X[1..n]
    F = [0] + f[:]          # F[1..m], F[j] = f(j)
    # dp[i] = máximo hasta el minuto i
    dp = [0] * (n + 1)
    # prev[i] guarda el valor k que produce la mejor solución atacando en i
    # si prev[i] = 0 significa que lo mejor fue "no atacar en i" 
    prev = [0] * (n + 1)
    for i in range(1, n+1):
        # opción 1: no atacar en i
        dp[i] = dp[i-1]
        prev[i] = 0
        # opción 2: atacar en i; probar todos los posibles "k" donde k indica
        # el índice inmediatamente posterior al último ataque (es decir, acumulamos desde k hasta i inclusive: j = i-k+1 minutos de carga)
        for k in range(1, i+1):
            j = i - k + 1
            # Si f no define tantos j, usamos el último valor disponible (creciente)
            fj = F[j] if j < len(F) else F[-1]
            gain = dp[k-1] + min(X[i], fj)
            if gain > dp[i]:
                dp[i] = gain
                prev[i] = k
    return reconstruir(prev,dp,n )


def reconstruir(prev, dp, n):
    decisiones = []
    i = n
    # Reconstruir hacia atrás
    while i > 0:
        if prev[i] == 0:
            decisiones.append(("Cargar", i))
            i -= 1
        else:
            k = prev[i]
            # El minuto i es de ataque
            decisiones.append(("Atacar", i))
            # Los minutos desde k hasta i-1 son de carga
            for j in range(i-1, k-1, -1):
                decisiones.append(("Cargar", j))
            i = k - 1
    # Ordenar por minuto
    decisiones.sort(key=lambda x: x[1])
    secuencia = [decision for decision, minuto in decisiones]
    total = dp[n]
    return total, secuencia

#lectura del archivo
def procesar_archivo(ruta):
    try:
        with open(ruta, "r") as archivo:
            lineas = [
                int(linea.strip())
                for linea in archivo
                if linea.strip() and not linea.strip().startswith("#")
            ]
        n = lineas[0]
        x = lineas[1:n+1]
        fx =  lineas[1+n:]
        return n, x, fx
    except FileNotFoundError:
        raise FileNotFoundError("La ruta no fue encontrada")
    except ValueError:
        raise ValueError("Error en el procesamiento del archivo")


def main():
    ruta_entrada = sys.argv[1]    
    try:
        n, dato1, dato2 = procesar_archivo(ruta_entrada)
        if dato1 and dato2:
            tropas_eliminadas, ataques = optimizar_ataques(dato1, dato2, n)
            print(f"Estrategia: {', '.join(ataques)}")
            print(f"Cantidad de tropas eliminadas: {tropas_eliminadas}")            
        else:
            print("El archivo no contiene datos válidos.")
            sys.exit(1)
    except Exception:
        sys.exit(1)
if __name__ == "__main__":
    main()