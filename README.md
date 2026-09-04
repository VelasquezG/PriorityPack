# PriorityPack

**Priorización algorítmica de paquetes para optimizar el procesamiento de envíos.**

PriorityPack es un proyecto académico desarrollado para la asignatura **Análisis de Algoritmos**, cuyo propósito es aplicar estrategias algorítmicas para mejorar el procesamiento y la priorización de grandes volúmenes de envíos.

El sistema recibe información de envíos mediante archivos CSV, calcula un nivel de prioridad para cada paquete y utiliza algoritmos de ordenamiento para generar una lista de envíos organizada desde la mayor hasta la menor prioridad.

---

## Descripción

PriorityPack permite procesar información de envíos y generar una priorización algorítmica teniendo en cuenta diferentes características del envío, entre ellas:

- Nivel de tráfico.
- Condiciones climáticas.
- Hora del pedido.
- Tipo de área.

A partir de estas características se calcula un **Priority Score** entre 0 y 100, que posteriormente se utiliza para ordenar los envíos.

El proyecto también permite analizar experimentalmente el rendimiento de diferentes algoritmos de ordenamiento, con especial énfasis en una estrategia basada en **Divide & Conquer**.

---

## Objetivo

Desarrollar una solución capaz de priorizar paquetes de manera eficiente y analizar experimentalmente el comportamiento de diferentes algoritmos de ordenamiento al procesar grandes cantidades de registros.

El algoritmo principal utilizado para la priorización es **Merge Sort**, cuya estrategia corresponde al paradigma **Divide & Conquer**.

Como referencia experimental se utiliza **Bubble Sort**, permitiendo comparar el comportamiento de un algoritmo de complejidad `O(n log n)` frente a uno de complejidad `O(n²)`.

> **Importante:** PriorityPack busca optimizar el procesamiento computacional y la organización de los envíos. No pretende afirmar que el sistema reduzca directamente los tiempos físicos de entrega.

---

## Tecnologías

- **Python**
- **Flask**
- **Pandas**
- **HTML5**
- **CSS3**
- **JavaScript**
- **Git / GitHub**

---

## Requisitos

Para ejecutar el proyecto se necesita:

- Python 3.10 o superior.
- Git.
- pip.

Se recomienda utilizar un entorno virtual de Python para evitar conflictos entre las dependencias del proyecto y las instaladas globalmente en el equipo.

---

# Instalación

## 1. Clonar el repositorio

Desde una terminal:

```bash
git clone https://github.com/VelasquezG/PriorityPack.git
```

## Configuración del entorno

### 1. Seleccionar Python con pyenv

Comprueba las versiones disponibles e instala Python 3.14 si todavía no está instalado:

```powershell
pyenv versions
pyenv install 3.14
pyenv local 3.14
python --version
```

Si `pyenv install 3.14` no está disponible en tu instalación de pyenv-win, consulta la versión exacta disponible con `pyenv install -l`, instala una versión `3.14.x` y actualiza `.python-version` con ese valor.

### 2. Crear y activar el entorno virtual

Desde la carpeta raíz del proyecto:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Cuando el entorno esté activo, el prompt mostrará `(venv)`.

### 3. Instalar dependencias

Actualiza `pip` e instala las dependencias del proyecto:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
### 4. Ejecucion de aplicacion

Ejecuta la aplicacion con el siguiente comando:

```powershell
python run.py
```