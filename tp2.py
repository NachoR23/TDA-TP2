# La funcion optimizar_ataques recibe:
# x: un arreglo con la cantidad de soldados que atacaran en cada minuto
# f: un arreglo con la cantidad de soldados que se pueden eliminar lanzando un ataque

# Devuelve:
#   - total_eliminados: entero con el máximo total posible
#   - ataques: lista de minutos (1-based) en los que atacar (en orden cronológico)
#   - dp: arreglo DP (1-based) con los máximos hasta cada minuto

# Complejidad: O(n^2) tiempo, O(n) espacio.

def optimizar_ataques(x, f):
    n = len(x)
    # usar indexación 1-based para DP y claridad
    X = [0] + x[:]          # X[1..n]
    F = [0] + f[:]          # F[1..m], F[j] = f(j)
    # dp[i] = máximo hasta el minuto i
    dp = [0] * (n + 1)
    # prev[i] guarda el valor k que produce la mejor solución atacando en i
    # si prev[i] = 0 significa que lo mejor fue "no atacar en i" (heredamos dp[i-1])
    prev = [0] * (n + 1)
    
    for i in range(1, n+1):
        # opción 1: no atacar en i
        dp[i] = dp[i-1]
        prev[i] = 0
        # opción 2: atacar en i; probar todos los posibles "k" donde k indica
        # el índice inmediatamente posterior al último ataque (es decir, acumulamos
        # desde k hasta i inclusive: j = i-k+1 minutos de carga)
        for k in range(1, i+1):
            j = i - k + 1
            # Si f no define tantos j, usamos el último valor disponible (creciente)
            fj = F[j] if j < len(F) else F[-1]
            gain = dp[k-1] + min(X[i], fj)
            if gain > dp[i]:
                dp[i] = gain
                prev[i] = k
    
    # reconstrucción de la secuencia de ataques
    attacks = []
    detalles = []  # (minuto, eliminado)
    i = n
    while i > 0:
        if prev[i] == 0:
            # no atacamos en i, seguimos atrás
            i -= 1
        else:
            k = prev[i]
            j = i - k + 1
            fj = F[j] if j < len(F) else F[-1]
            killed = min(X[i], fj)
            attacks.append(i)               # atacamos en minuto i (1-based)
            detalles.append((i, killed))
            i = k - 1   # retrocedemos a lo que había antes del bloque que terminó en i

    attacks.reverse()
    detalles.reverse()
    total = dp[n]
    return total, attacks, dp, detalles