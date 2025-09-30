def leer_gramatica(ruta):
    gramatica = {}
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if "->" in linea:
                izquierda, derecha = linea.strip().split("->")
                izquierda = izquierda.strip()
                produccion = derecha.strip().split()
                if izquierda not in gramatica:
                    gramatica[izquierda] = []
                gramatica[izquierda].append(produccion)
    return gramatica

def calcular_primeros(gramatica):
    primeros = {nt: set() for nt in gramatica}
    cambiado = True
    while cambiado:
        cambiado = False
        for nt in gramatica:
            for produccion in gramatica[nt]:
                agregar_vacio = True
                for simbolo in produccion:
                    if simbolo in gramatica:
                        antes = len(primeros[nt])
                        primeros[nt].update(x for x in primeros[simbolo] if x != "ε")
                        if "ε" not in primeros[simbolo]:
                            agregar_vacio = False
                            break
                        if len(primeros[nt]) > antes:
                            cambiado = True
                    else:
                        if simbolo != "ε":
                            if simbolo not in primeros[nt]:
                                primeros[nt].add(simbolo)
                                cambiado = True
                            agregar_vacio = False
                        else:
                            if "ε" not in primeros[nt]:
                                primeros[nt].add("ε")
                                cambiado = True
                        break
                if agregar_vacio:
                    if "ε" not in primeros[nt]:
                        primeros[nt].add("ε")
                        cambiado = True
    return primeros

def calcular_siguientes(gramatica, primeros, simbolo_inicial):
    siguientes = {nt: set() for nt in gramatica}
    siguientes[simbolo_inicial].add("$")
    cambiado = True
    while cambiado:
        cambiado = False
        for nt in gramatica:
            for produccion in gramatica[nt]:
                for i, simbolo in enumerate(produccion):
                    if simbolo in gramatica:
                        beta = produccion[i+1:]
                        if beta:
                            primeros_beta = set()
                            agregar_vacio = True
                            for s in beta:
                                if s in gramatica:
                                    primeros_beta.update(x for x in primeros[s] if x != "ε")
                                    if "ε" not in primeros[s]:
                                        agregar_vacio = False
                                        break
                                else:
                                    primeros_beta.add(s)
                                    agregar_vacio = False
                                    break
                            antes = len(siguientes[simbolo])
                            siguientes[simbolo].update(primeros_beta)
                            if len(siguientes[simbolo]) > antes:
                                cambiado = True
                            if agregar_vacio:
                                antes = len(siguientes[simbolo])
                                siguientes[simbolo].update(siguientes[nt])
                                if len(siguientes[simbolo]) > antes:
                                    cambiado = True
                        else:
                            antes = len(siguientes[simbolo])
                            siguientes[simbolo].update(siguientes[nt])
                            if len(siguientes[simbolo]) > antes:
                                cambiado = True
    return siguientes

def conjuntos_prediccion(gramatica, primeros, siguientes):
    predicciones = []
    for A in gramatica:
        for produccion in gramatica[A]:
            primeros_alpha = set()
            puede_vacio = True
            if not produccion:
                primeros_alpha.add("ε")
            else:
                for s in produccion:
                    if s in gramatica:
                        primeros_alpha.update(x for x in primeros[s] if x != "ε")
                        if "ε" in primeros[s]:
                            continue
                        else:
                            puede_vacio = False
                            break
                    else:
                        if s == "ε":
                            primeros_alpha.add("ε")
                        else:
                            primeros_alpha.add(s)
                        puede_vacio = False
                        break
            pred = set(x for x in primeros_alpha if x != "ε")
            if "ε" in primeros_alpha or puede_vacio:
                pred.update(siguientes[A])
            regla = A + " -> " + (" ".join(produccion) if produccion else "ε")
            predicciones.append((regla, pred))
    return predicciones

if __name__ == "__main__":
    ruta = "gramatica.txt"
    gramatica = leer_gramatica(ruta)
    primeros = calcular_primeros(gramatica)
    siguientes = calcular_siguientes(gramatica, primeros, simbolo_inicial="S")
    predicciones = conjuntos_prediccion(gramatica, primeros, siguientes)

    print("Conjuntos PRIMEROS:")
    for nt in gramatica:
        print(f"PRIMEROS({nt}) = {sorted(primeros[nt])}")

    print("\nConjuntos SIGUIENTES:")
    for nt in gramatica:
        print(f"SIGUIENTES({nt}) = {sorted(siguientes[nt])}")

    print("\nConjuntos de predicción:")
    for regla, conjunto in predicciones:
        print(f"{regla:<15} {sorted(conjunto)}")
