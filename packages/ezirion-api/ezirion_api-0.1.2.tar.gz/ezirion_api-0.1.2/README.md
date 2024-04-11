# Mi primera API

Esto es mi primera api creada de prueba para subir a PyPi.

## Cursos disponibles:

- Mi primer curso [12 horas]
- Mi segundo curso [15 horas]
- Mi tercer curso [16 horas]

## Instalación

Instala el paquete usando `pip3`:

```python3
pip3 install ezirion_api
```

## Notas de versión 

0.1.2 >>> Parche al llamar a la variable `courses` salía el objeto por pantalla y no sus propiedades.


## Uso básico

### Listar todos los cursos

```python
from ezirion_api import list_courses

for course in list_courses():
	print(course)
```

### Obtener un curso por nombre

```python
from ezirion_api import search_course_by_name

course = search_course_by_name("Mi primer curso")
print(course)
```

### Calcular duración total de los cursos

```python3
from ezirion_api.utils import total_duration
print(f"Duración total: {total_duration()} horas")
```
