# app/algorithms/merge_sort.py


def merge(left, right):
    """
    Combina dos listas ordenadas en una sola lista ordenada.

    Ordena de mayor a menor Priority_Score.
    """

    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i]["Priority_Score"] >= right[j]["Priority_Score"]:
            result.append(left[i])
            i += 1

        else:
            result.append(right[j])
            j += 1

    # Agregar elementos restantes de left
    while i < len(left):
        result.append(left[i])
        i += 1

    # Agregar elementos restantes de right
    while j < len(right):
        result.append(right[j])
        j += 1

    return result


def merge_sort(shipments):
    """
    Ordena los envíos utilizando Merge Sort.

    Divide & Conquer:
        1. Divide la lista en dos partes.
        2. Ordena recursivamente cada parte.
        3. Combina las partes ordenadas.

    Complejidad temporal:
        O(n log n)

    Complejidad espacial:
        O(n)
    """

    # Caso base:
    # Una lista de 0 o 1 elementos ya está ordenada.
    if len(shipments) <= 1:
        return shipments

    # ==========================================
    # DIVIDE
    # ==========================================

    middle = len(shipments) // 2

    left = shipments[:middle]
    right = shipments[middle:]

    # ==========================================
    # CONQUER
    # ==========================================

    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)

    # ==========================================
    # COMBINE
    # ==========================================

    return merge(left_sorted, right_sorted)