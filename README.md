## Algoritmos_De_Prediccion

Este proyecto implementa en Python los algoritmos para calcular los conjuntos PRIMEROS, SIGUIENTES y la tabla de predicción de una gramática libre de contexto.
El objetivo es facilitar la construcción de analizadores sintácticos predictivos (LL(1)), que utilizan estos conjuntos para decidir qué regla aplicar durante el análisis.

#### Leer la gramática:

```python
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
```

### Algoritmo de Primeros:

```python
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
```

***Funciones relevantes***

leer_gramatica(ruta)
Lee el archivo gramatica.txt y guarda cada producción en un diccionario.

calcular_primeros(gramatica)

Recorre cada no terminal.

Para cada producción, añade el primer símbolo terminal encontrado.

Si un símbolo puede derivar en ε (vacío), se avanza al siguiente de la producción.

Si toda la producción puede vaciarse, se agrega ε.

Se repite hasta que los conjuntos no cambien más.

**Resultado**: un diccionario con los conjuntos PRIMEROS de cada no terminal.

### Algoritmos de Siguientes:

```python
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
```

Los conjuntos SIGUIENTES(A) contienen los símbolos que pueden aparecer inmediatamente a la derecha de un no terminal A en alguna derivación.

***Funciones relevantes***

calcular_siguientes(gramatica, primeros, simbolo_inicial)

Inicializa el conjunto del símbolo inicial con $.

Recorre cada producción buscando ocurrencias de no terminales.

Aplica las reglas:

Si A -> αBβ, entonces PRIMEROS(β) – {ε} ⊆ SIGUIENTES(B).

Si A -> αBβ y β ⇒* ε, entonces SIGUIENTES(A) ⊆ SIGUIENTES(B).

Itera hasta que no haya cambios.

**Resultado**: un diccionario con los conjuntos SIGUIENTES de cada no terminal.

### Conjunto de Predicciones:

```python
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
```
Los conjuntos de predicción se utilizan para construir la tabla LL(1). Cada producción A -> α tiene un conjunto de predicción que indica en qué casos aplicar esa regla.

***Funciones relevantes***

conjuntos_prediccion(gramatica, primeros, siguientes)

Calcula PRIMEROS(α) para el lado derecho de cada producción.

Si ε ∈ PRIMEROS(α), también se añaden los símbolos de SIGUIENTES(A).

Devuelve una lista con cada producción y su conjunto de predicción asociado.

**Resultado**: una lista de reglas junto con los terminales que disparan su aplicación.

### Salida esperada

*Gramática 1 de ejemplo*

<pre>S -> A B
S -> a b c
A -> a B S
A -> ε
B -> b
B -> ε</pre>

*Salida*

