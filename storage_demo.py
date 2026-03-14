from random import randint, choice, uniform, sample

# Student table definition
class Student:
    def __init__(self, student_id, full_name, class_name, email, phone):
        self.student_id = student_id
        self.full_name = full_name
        self.class_name = class_name
        self.email = email
        self.phone = phone

    def __str__(self):
        return f"[STUDENT|{self.student_id}|{self.full_name}|{self.class_name}|{self.email}|{self.phone}]"

# Course table definition
class Course:
    def __init__(self, course_id, course_name, credits, dept_name):
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits
        self.dept_name = dept_name
    def __str__(self):
        return f"[COURSE|{self.course_id}|{self.course_name}|{self.credits}|{self.dept_name}]"


# Enrollment table definition
class Enrollment:
    def __init__(self, student_id, course_id, semester, score):
        self.student_id = student_id
        self.course_id = course_id
        self.semester = semester
        self.score = score
    def __str__(self):
        return f"[ENROLL|{self.student_id}|{self.course_id}|{self.semester}|{self.score}]"

students = []
courses = []
enrollments = []
# Initialize records
def init():
    # Randomize students
    for i in range(1, 21):
        classes = [f"C10{i}" for i in range(1, 6)]
        student = Student(i, f"Nguyen Van {i}", choice(classes), f"nvan{i}@gmail.com", f"0{randint(1000000000, 10000000000):09d}")
        students.append(student)

    # List courses
    global courses
    courses = [
        Course(1, "Giai tich 1", 3, "Co ban"),
        Course(2, "Giai tich 2", 3, "Co ban"),
        Course(3, "Triet hoc Mac-Lenin", 3, "Co ban"),
        Course(4, "Xac suat thong ke", 3, "Co ban"),
        Course(5, "Dien tu so", 3, "Dien tu"),
        Course(6, "Nhap mon tri tue nhan tao", 3, "Tri tue nhan tao"),
        Course(7, "Vat ly ung dung", 4, "Co ban"),
        Course(8, "Thuc tap co so", 4, "CNTT1")
            ]
    # Randomize enrollment
    for i in range(30):
        student = choice(students)
        course = choice(courses)
        year = ["2023", "2024", "2025", "2026"]
        semester = ["1", "2"]
        enrollments.append(Enrollment(student.student_id, course.course_id, choice(year)+choice(semester), f"{randint(0, 100)/10:.1f}"))
# Print records
def print_record():
    print("---Students---")
    print("student_id|full_name|class_name|email|phone")
    for student in students:
        print(student)
    print("---Courses---")
    print("course_id|course_name|credits|dept_name")
    for course in courses:
        print(course)
    print("---Enrollments---")
    print("student_id|course_id|semester|score")
    for enrollment in enrollments:
        print(enrollment)

init()
# print_record()



# Heap file implementation for student
class StudentHeapFile:
    def __init__(self):
        self.heap = []

    def insert(self, record):
        lookup_count = 0
        self.heap.append(record)
        return lookup_count
    def search(self, student_id):
        lookup_count = 0
        for record in self.heap:
            lookup_count += 1
            if record.student_id == student_id:
                return (record, lookup_count)
    def print(self):
        for record in self.heap:
            print(record)
# Demo for student heap
random_students = sample(students, k=len(students))
heap = StudentHeapFile()
def student_heap_insert(verbose=False):
    total_lookup_count = 0
    for student in random_students:
        total_lookup_count += heap.insert(student)
        verbose and print(f"Insert record {student} after {lookup_count} lookups")
    return total_lookup_count
def student_heap_search(id, verbose=False):
    verbose and print(f"Search for student with id {id}:")
    record, lookup_count = heap.search(id)
    verbose and print(f"Found record {record} after {lookup_count} lookups")
    return lookup_count

print("---Heap File---")
heap_insert_count = student_heap_insert()
print(f"Total lookup while inserting: {heap_insert_count}")
print("- Searching for id from 1 to 20...")
heap_search_count = 0
for i in range(1, 21):
    heap_search_count += student_heap_search(i)
print(f"Total lookup while searching: {heap_search_count}")



class StudentSequentialFile:
    def __init__(self):
        self.list = []
    def insert(self, record):
        lookup_count = 0
        if len(self.list) == 0:
            self.list.append(record)
        elif len(self.list) == 1:
            lookup_count += 1
            current = self.list[0]
            if (current.student_id > record.student_id): self.list.insert(0, record)
            else: self.list.append(record)
        else:
            left = 0
            right = len(self.list)-1
            while left <= right:
                mid = (left+right)//2
                current = self.list[mid]
                lookup_count += 1
                if current.student_id < record.student_id:
                    left = mid + 1
                else:
                    right = mid - 1
            self.list.insert(left, record)
        return lookup_count
    def search(self, student_id):
        lookup_count = 0
        left = 0
        right = len(self.list)-1
        while left <= right:
            mid = (left + right)//2
            current = self.list[mid]
            lookup_count += 1
            if current.student_id == student_id:
                return (current, lookup_count)
            elif current.student_id < student_id:
                left = mid + 1
            else:
                right = mid - 1
        return (None, lookup_count)

sequential_list = StudentSequentialFile()
def sequential_list_insert(verbose=False):
    total_lookup_count = 0
    for student in random_students:
        total_lookup_count += sequential_list.insert(student)
        verbose and print(f"Insert record {student} after {lookup_count} lookups")
    if verbose:
        for student in sequential_list.list:
            print(student)
    return total_lookup_count

def sequential_list_search(id, verbose=False):
    verbose and print(f"Search for student with id {id}")
    record, lookup_count = sequential_list.search(id)
    verbose and print(f"Found record {record} after {lookup_count} lookups")
    return lookup_count

print("---Sequential File---")
sequential_insert_count = sequential_list_insert()
print(f"Total lookup count while inserting: {sequential_insert_count}")
print("- Searching for id from 1 to 20...")
sequential_search_count = 0
for i in range(1, 21):
    sequential_search_count += sequential_list_search(i)
print(f"Total lookup while searching: {sequential_search_count}")
