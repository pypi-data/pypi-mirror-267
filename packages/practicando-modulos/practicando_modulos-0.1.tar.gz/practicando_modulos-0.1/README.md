# Ejercicios de Programación

Este repositorio contiene una serie de ejercicios de programación resueltos en diferentes lenguajes de programación. Estos ejercicios están diseñados para practicar y mejorar tus habilidades de programación.

## Archivo `config.py`

Este archivo contiene una variable `pi` con un valor de `3.1416`.

### Contenido

```python
pi = 3.1416
```

## Archivo `cal.py`

Este archivo contiene una función `area_circulo(radio)` que calcula el área de un círculo utilizando la constante `pi` del módulo `config`.

### Contenido

```python
from modulo import config

def area_circulo(radio):
    return radio * config.pi
```

## Archivo `principal.py`

Este archivo utiliza la función `area_circulo(radio)` del módulo `cal` para calcular el área de un círculo con un radio de 5.

### Contenido

```python
from modulo import cal

radio = 5
area = cal.area_circulo(radio)
print(area)
```

## Contribuir

Si deseas contribuir con nuevos ejercicios o mejorar los existentes, ¡eres bienvenido! Simplemente haz un fork del repositorio, realiza tus cambios y envía un pull request.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).
