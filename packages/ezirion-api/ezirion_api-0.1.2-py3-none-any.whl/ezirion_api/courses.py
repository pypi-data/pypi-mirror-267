class Course:

	def __init__(self, name, duration, link):
		self.name = name
		self.duration = duration
		self.link = link

	def __repr__(self):
		return f"{self.name} [{self.duration} horas] | Link: {self.link}"

courses = [
    Course("Mi primer curso", 12, "https://milink1.com"),
    Course("Mi segundo curso", 15, "https://milink2.com"),
    Course("Mi tercer curso", 16, "https://milink3.com")
]

def list_courses():
    for course in courses:
        print(course)

def search_course_by_name(name):
    not_found = 0
    for course in courses:
        if course.name == name:
            return course
        else:
            not_found = 1
    if not_found == 1:
        print("[!] Error: El curso solicitado no existe.")
