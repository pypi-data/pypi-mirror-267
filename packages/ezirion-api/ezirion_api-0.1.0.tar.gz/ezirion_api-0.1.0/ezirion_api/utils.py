from .courses import courses

#En este script quiero utilizar la lista de objetos courses del módulo courses.py

def total_duration():

	return sum(course.duration for course in courses)
