# app/algorithms/traditional_sort.py


def bubble_sort(shipments):
    """
    Ordena los envíos utilizando Bubble Sort.

    Ordena de mayor a menor Priority_Score.

    Complejidad temporal:
        O(n²)

    Complejidad espacial:
        O(n)
    """

    shipments = shipments.copy()

    n = len(shipments)

    for i in range(n):

        swapped = False

        for j in range(0, n - i - 1):

            if (
                shipments[j]["Priority_Score"]
                < shipments[j + 1]["Priority_Score"]
            ):
                shipments[j], shipments[j + 1] = (
                    shipments[j + 1],
                    shipments[j],
                )

                swapped = True

        # Si no hubo intercambios,
        # la lista ya está ordenada.
        if not swapped:
            break

    return shipments