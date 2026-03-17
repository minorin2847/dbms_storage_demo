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
        year = ["2023", "2024"]
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
print_record()



# I. Heap file vs Sequential file

# Heap file implementation for student
class StudentHeapFile:
    def __init__(self):
        self.heap = []

    def insert(self, record):
        lookup_count = 0
        self.heap.append(record)
        return lookup_count
    def random_search(self, student_id):
        lookup_count = 0
        for record in self.heap:
            lookup_count += 1
            if record.student_id == student_id:
                return (record, lookup_count)
    def sequential_search(self, start, end):
        total_lookup_count = 0
        records = []
        for i in range(start, end+1):
            record, lookup_count = self.random_search(i)
            total_lookup_count += lookup_count
            records.append(record)
        return (total_lookup_count, records)
    def print(self):
        for record in self.heap:
            print(record)

# Sequential file implementation for student
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
    def random_search(self, student_id):
        lookup_count = 0
        left = 0
        right = len(self.list)-1
        while left <= right:
            mid = (left + right)//2
            current = self.list[mid]
            lookup_count += 1
            if current.student_id == student_id:
                return (current, mid, lookup_count)
            elif current.student_id < student_id:
                left = mid + 1
            else:
                right = mid - 1
        return (None, 0, lookup_count)
    def sequential_search(self, start, end):
        record, index, lookup_count = self.random_search(start)
        records = self.list[index:index+end-start+1]
        return (lookup_count, records)


# Randomize student records for insertion
random_students = sample(students, k=len(students))

# Demo for student heap file
heapFile = StudentHeapFile()
def student_heap_insert(verbose=False):
    print("\n[HEAP FILE INSERT]\n")
    print("# Insert randomized student records into heap file")
    verbose and print("! VERBOSE OUTPUT")
    total_lookup_count = 0
    for student in random_students:
        lookup_count =  heapFile.insert(student)
        verbose and print(f"? Insert record {student} after {lookup_count} lookups")
        total_lookup_count += lookup_count
    if verbose:
        print("? Heap file content:")
        for student in heapFile.heap:
            print("- " + str(student))
    print(f"! Finish inserting into heap after {total_lookup_count} lookups")
def student_heap_random_search(count=5, verbose=False):
    print("\n[HEAP RANDOM SEARCH]\n")
    print(f"# Search for {count} random students:")
    verbose and print("! VERBOSE OUTPUT")
    random_search_id = sample(range(1, 21), k=count)
    total_lookup_count = 0
    records = []
    for i in random_search_id:
        record, lookup_count = heapFile.random_search(i)
        verbose and print(f"? Found record {record} after {lookup_count} lookups")
        total_lookup_count += lookup_count
        records.append(record)
    verbose and print(f"? Found records:\n- {'\n- '.join(str(i) for i in records)}")
    print(f"! Finish search after {total_lookup_count} lookups")
def student_heap_sequential_search(start=1, end=5, verbose=False):
    print("\n[HEAP SEQUENTIAL SEARCH]\n")
    print(f"# Search for students with id from {start} to {end}")
    verbose and print("! VERBOSE OUTPUT")
    total_lookup_count, records = heapFile.sequential_search(start, end)
    verbose and print(f"? Found records:\n- {'\n- '.join(str(i) for i in records)}")
    print(f"! Finish search after {total_lookup_count} lookups")

# Demo for student sequential file
sequentialFile = StudentSequentialFile()
def sequential_list_insert(verbose=False):
    print("\n[SEQUENTIAL FILE INSERT]\n")
    print("# Inserting random student records into sequential file")
    verbose and print("! VERBOSE OUTPUT")
    total_lookup_count = 0
    for student in random_students:
        lookup_count = sequentialFile.insert(student)
        verbose and print(f"? Insert record {student} after {lookup_count} lookups")
        total_lookup_count += lookup_count
    if verbose:
        print("? Sequential file content:")
        for student in sequentialFile.list:
            print("- " + str(student))
    print(f"! Finish inserting after {total_lookup_count} lookups")
def sequential_list_random_search(count=5, verbose=False):
    print("\n[SEQUENTIAL FILE RANDOM SEARCH]\n")
    print(f"# Search for {count} random students:")
    verbose and print("! VERBOSE OUTPUT")
    random_search_id = sample(range(1, 21), k=count)
    total_lookup_count = 0
    records = []
    for i in random_search_id:
        record, index, lookup_count = sequentialFile.random_search(i)
        verbose and print(f"? Found record {record} at index {index} after {lookup_count} lookups")
        total_lookup_count += lookup_count
        records.append(record)
    verbose and print(f"? Found records:\n- {'\n- '.join(str(i) for i in records)}")
    print(f"! Found records after {total_lookup_count} lookups")
def sequential_list_sequential_search(start=1, end=5, verbose=False):
    print("\n[SEQUENTIAL FILE SEQUENTIAL SEARCH]\n")
    print(f"# Search for students with id from {start} to {end}")
    verbose and print("! VERBOSE OUTPUT")
    total_lookup_count, records = sequentialFile.sequential_search(start, end)
    verbose and print(f"? Found records:\n- {'\n- '.join(str(i) for i in records)}")
    print(f"! Found records after {total_lookup_count} lookups")

# Heap file and sequential file demo run
print("---Heap File---")
student_heap_insert(verbose=True)
student_heap_random_search(verbose=True)
student_heap_sequential_search(verbose=True)
print("---Sequential File---")
sequential_list_insert(verbose=True)
sequential_list_random_search(verbose=True)
sequential_list_sequential_search(verbose=True)




# II. Multitable Clustering and Partitioning 

# Standard database with seperate Student and Enrollment tables using a heap file
class StandardDatabase:
    def __init__(self):
        self.database = {
            "students": [],
            "enrollments": []
        }
        self.tables = {
            "students": Student,
            "enrollments": Enrollment
        }
    def insert(self, table, record):
        if table not in self.database.keys():
            raise ValueError("Invalid table!")
        
        self.database[table].append(record)
    
    def search(self, table, key, value):
        if table not in self.database.keys():
            raise ValueError("Invalid table!")
        if not hasattr(self.database[table][0], key):
            raise ValueError("Invalid key!")
        lookup_count = 0
        records = []
        for i in self.database[table]:
            lookup_count += 1
            if getattr(i, key) == value:
                records.append(i)
        return (records, lookup_count)
    
    def join(self, t1, t2, key, tableName=""):
        if t1 not in self.database.keys() or t2 not in self.database.keys():
            raise ValueError("Invalid tables!")
        if not hasattr(self.database[t1][0], key) or not hasattr(self.database[t2][0], key):
            raise ValueError("Invalid key!")
        
        tableName = t1 + "_" + t2 if tableName == "" else tableName
        # Initiate tableName class
        def joinInit(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
        def joinStr(self):
            return f"[{str.upper(tableName)}|{'|'.join([str(i) for i in self.__dict__.values()])}]"
        
        joinClass = type(tableName, (object,), {
            '__init__': joinInit,
            '__str__': joinStr
        })
        self.tables[tableName] = joinClass
        # Helper dictionary to build joined tables
        results = []
        lookup_count = 0
        helper = {}
        for i in self.database[t1]:
            lookup_count += 1
            helper[getattr(i, key)] = i
        
        for i in self.database[t2]:
            lookup_count += 1
            match = helper.get(getattr(i, key))
            if match:
                results.append(joinClass(**{**match.__dict__, **i.__dict__}))
        
        self.database[tableName] = results
        return lookup_count
    


standard_database = StandardDatabase()
random_enrollments = sample(enrollments, k=len(enrollments))

def standard_database_insert(verbose=False):
    print("\n[STANDARD DATABASE INSERT]\n")
    print("# Inserting randomized students and enrollments into the database")
    for i in random_students:
        standard_database.insert("students", i)
    for i in random_enrollments:
        standard_database.insert("enrollments", i)
    if verbose:
        print("? Standard database structure:")
        print(f"? Students:\n- {'\n- '.join([str(i) for i in standard_database.database['students']])}")
        print(f"? Enrollments:\n- {'\n- '.join([str(i) for i in standard_database.database['enrollments']])}")


def standard_database_join(verbose=False):
    print("\n[STANDARD DATABASE JOIN]\n")
    print("# Joining database students and enrollments into studentEnroll table")
    lookup_count = standard_database.join("students", "enrollments", "student_id", "studentEnroll")
    if verbose:
        print(f"? New table structure:\n- {'\n- '.join([str(i) for i in standard_database.database['studentEnroll']])}")
    print(f"! Finish joining students and enrollments table after {lookup_count} lookup")

def standard_database_search(verbose=False):
    print("\n[STANDARD DATABASE SEARCH]\n")
    print("# Searching for enrollments in 20231 semester")
    records, lookup_count = standard_database.search("enrollments", "semester", "20231")
    verbose and print(f"? Found records:\n- {'\n- '.join([str(i) for i in records])}")
    print(f"! Found records after {lookup_count} lookups")
print("--- Standard Database ---")
standard_database_insert(verbose=True)
standard_database_join(verbose=True)        
standard_database_search(verbose=True)


# Clustered database with table Student and Enrollment by student_id
class ClusteredDatabase:
    def __init__(self):
        self.database = {}
        self.tables = {
            "students": Student,
            "enrollments": Enrollment
        }
    
    def insert(self, table, record):
        if table not in self.tables.keys():
            raise ValueError(f"Invalid table!")
        if not isinstance(record, self.tables[table]):
            raise ValueError(f"Invalid record for table {table}!")
        if not hasattr(record, 'student_id'):
            raise ValueError(f"Record doesn't have student_id column!")
        
        if getattr(record, 'student_id') not in self.database:
            self.database[getattr(record, 'student_id')] = [record]
        else:
            self.database[getattr(record, 'student_id')].append(record)
    
    def search(self, table, key, value):
        if table not in self.tables.keys():
            raise ValueError(f"Invalid table!")
        if key not in self.tables[table].__static_attributes__:
            raise ValueError(f"Invalid key!")
        lookup_count = 0
        records = []
        if key == 'student_id':
            for i in self.database[value]:
                lookup_count += 1
                if isinstance(i, self.tables[table]):
                    records.append(i)
        else:
            for i in self.database.values():
                for j in i:
                    lookup_count += 1
                    if isinstance(j, self.tables[table]) and getattr(j, key) == value:
                        records.append(j)
        return (records, lookup_count)

    def join(self, t1, t2, key, tableName=""):
        if t1 not in self.tables.keys() or t2 not in self.tables.keys():
            raise ValueError("Invalid tables!")
        if key not in self.tables[t1].__static_attributes__ \
        or key not in self.tables[t2].__static_attributes__:
            raise ValueError("Invalid key!")
        tableName = t1 + "_" + t2 if tableName == '' else tableName

        # Create class for joined table
        def joinInit(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
        def joinStr(self):
            return f"[{str.upper(tableName)}|{'|'.join([str(i) for i in self.__dict__.values()])}]"
        
        joinClass = type(tableName, (object,), {
            '__init__': joinInit,
            '__str__': joinStr
        })
        self.tables[tableName] = joinClass
        lookup_count = 0
        if key == 'student_id':
            parent = None
            for i in self.database.keys():
                newRecords = []
                lookup_count += 1
                for j in self.database[i]:
                    if isinstance(j, self.tables[t1]):
                        parent = j
                    elif isinstance(j, self.tables[t2]):
                        newRecords.append(joinClass(**{**parent.__dict__, **j.__dict__}))
                self.database[i].extend(newRecords)
        else:
            # Same as standard database, then put all the results into the database by student_id
            pass
        return lookup_count
    
clustered_database = ClusteredDatabase()

def clustered_database_insert(verbose=False):
    print("\n[CLUSTERED DATABASE INSERT]\n")
    print("# Inserting randomized students and enrollments into the database")
    for i in random_students:
        clustered_database.insert("students", i)
    for i in random_enrollments:
        clustered_database.insert("enrollments", i)
    if verbose:
        print("? Clustered database structure:")
        for key, value in clustered_database.database.items():
            print(f"- student_id = {key}:")
            for i in value:
                print(f"  - {str(i)}")

def clustered_database_search(verbose=False):
    print("\n[CLUSTERED DATABASE SEARCH]\n")
    print("# Searching for enrollments in 20231 semester")
    records, lookup_count = clustered_database.search("enrollments", "semester", "20231")
    verbose and print(f"? Found records:\n- {'\n- '.join([str(i) for i in records])}")
    print(f"! Found records after {lookup_count} lookups")

def clustered_database_key_search(verbose=False):
    print("\n[CLUSTERED DATABASE SEARCH WITH JOIN KEY]\n")
    print("# Searching for students with id 10")
    records, lookup_count = clustered_database.search("students", "student_id", 10)
    verbose and print(f"? Found records:\n- {'\n- '.join([str(i) for i in records])}")
    print(f"! Found records after {lookup_count} lookups")


def clustered_database_join(verbose=False):
    print("\n[CLUSTERED DATABASE JOIN]\n")
    print("# Joining database students and enrollments into studentEnroll table")
    lookup_count = clustered_database.join("students", "enrollments", "student_id", "studentEnroll")
    if verbose:
        print("? New database structure:")
        for key, value in clustered_database.database.items():
            print(f"- student_id = {key}:")
            for i in value:
                print(f"  - {str(i)}")
    print(f"! Finish joining students and enrollments table after {lookup_count} lookup")
clustered_database_insert(verbose=True)
clustered_database_search(verbose=True)
clustered_database_key_search(verbose=True)
clustered_database_join(verbose=True)
            
# Partitioned database with Student partitioned by class name, Enrollment partitioned by semester
class PartitionedDatabase:
    def __init__(self):
        self.database = {
            "students": {},
            "enrollments": {}
        }
        self.tables = {
            "students": Student,
            "enrollments": Enrollment
        }
    
    def insert(self, table, record):
        if table not in self.database.keys():
            raise ValueError("Invalid table!")
        if not isinstance(record, self.tables[table]):
            raise ValueError(f"Invalid record for table {table}!")
        if table == "students":
            # Partition by class_name
            if record.class_name not in self.database["students"].keys():
                self.database["students"][record.class_name] = [record]
            else:
                self.database["students"][record.class_name].append(record)
        elif table == "enrollments":
            # Partition by semester
            if record.semester not in self.database["enrollments"].keys():
                self.database["enrollments"][record.semester] = [record]
            else:
                self.database["enrollments"][record.semester].append(record)
    
    def search(self, table, key, value):
        if table not in self.tables.keys():
            raise ValueError(f"Invalid table!")
        if key not in self.tables[table].__static_attributes__:
            raise ValueError(f"Invalid key!")
        
        lookup_count = 0
        records = []

        if table == "students" and key == "class_name" or table == "enrollments" and key == "semester":
            records = self.database[table][value]
        else:
            for i in self.database[table].values():
                for j in i:
                    lookup_count += 1
                    if getattr(j, key) == value:
                        records.append(j)
        
        return (records, lookup_count)
    
    def join(self, t1, t2, key, tableName=""):
        if t1 not in self.database.keys() or t2 not in self.database.keys():
            raise ValueError("Invalid tables!")
        if key not in self.tables[t1].__static_attributes__ or key not in self.tables[t2].__static_attributes__:
            raise ValueError("Invalid key!")
        
        tableName = t1 + "_" + t2 if tableName == "" else tableName
        # Initiate tableName class
        def joinInit(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
        def joinStr(self):
            return f"[{str.upper(tableName)}|{'|'.join([str(i) for i in self.__dict__.values()])}]"
        
        joinClass = type(tableName, (object,), {
            '__init__': joinInit,
            '__str__': joinStr
        })
        self.tables[tableName] = joinClass

        # Helper dictionary to build joined tables
        results = []
        lookup_count = 0
        helper = {}
        if t1 == "students" and key == "class_name":
            for key, value in self.database[t1].items():
                helper[key] = self.database[t1][key]
        else:
            for i in self.database[t1].values():
                for j in i:
                    lookup_count += 1
                    helper[getattr(j, key)] = j
        if t2 == "enrollments" and key == "semester":
            for key, value in self.database[t2].items():
                match = helper[key]
                if match:
                    for i in value:
                        results.append(joinClass(**{**match.__dict__, **i.__dict__}))
        else:
            for i in self.database[t2].values():
                for j in i:
                    lookup_count += 1
                    match = helper.get(getattr(j, key))
                    if match:
                        results.append(joinClass(**{**match.__dict__, **j.__dict__}))
        self.database[tableName] = results
        return lookup_count
    
partitioned_database = PartitionedDatabase()

# --- Partitioned Database Demo Functions ---

def partitioned_database_insert_demo(verbose=True):
    print("\n[PARTITIONED DATABASE INSERT]\n")
    print("# Inserting randomized students (by class) and enrollments (by semester)")
    for s in random_students:
        partitioned_database.insert("students", s)
    for e in random_enrollments:
        partitioned_database.insert("enrollments", e)
    
    if verbose:
        print("? Partitioned Database Structure:")
        print("--- Students (Partitioned by class_name) ---")
        for class_key, s_list in partitioned_database.database["students"].items():
            print(f"Partition [{class_key}]:")
            for s in s_list:
                print(f"  - {s}")
        
        print("\n--- Enrollments (Partitioned by semester) ---")
        for sem_key, e_list in partitioned_database.database["enrollments"].items():
            print(f"Partition [{sem_key}]:")
            for e in e_list:
                print(f"  - {e}")

def partitioned_database_search_by_semester(semester="20231", verbose=False):
    print(f"\n[PARTITIONED SEARCH BY SEMESTER: {semester}]\n")
    print(f"# Querying partition key: {semester}")
    verbose and print("! VERBOSE OUTPUT")
    
    # Direct access to the dictionary key
    records, lookup_count = partitioned_database.search("enrollments", "semester", semester)
    
    if verbose:
        print(f"? Found records:")
        for r in records: print(f"  - {str(r)}")
    
    print(f"! Found {len(records)} records after {lookup_count} lookup(s)")

def partitioned_database_search_by_student_id(sid=10, verbose=False):
    print(f"\n[PARTITIONED SEARCH BY STUDENT_ID: {sid}]\n")
    print(f"# Querying non-partition key: {sid}")
    verbose and print("! VERBOSE OUTPUT")
    
    records, lookup_count = partitioned_database.search("students", "student_id", sid)
    
    if verbose:
        print(f"? Found records:")
        for r in records: print(f"  - {str(r)}")
        
    print(f"! Found {len(records)} record(s) after {lookup_count} lookup(s)")

def partitioned_database_join_demo(verbose=True):
    print("\n[PARTITIONED DATABASE JOIN]\n")
    print("# Joining Students and Enrollments by student_id")
    verbose and print("! VERBOSE OUTPUT")
    
    lookup_count = partitioned_database.join("students", "enrollments", "student_id", "studentEnroll")
    
    if verbose:
        print("--- studentEnroll Joined Table Content ---")
        for row in partitioned_database.database["studentEnroll"]:
            print(f"- {row}")
            
    print(f"! Finish joining after {lookup_count} lookups")

# --- Execution ---
partitioned_database_insert_demo(verbose=True)
partitioned_database_search_by_semester("20231", verbose=True)
partitioned_database_search_by_student_id(10, verbose=True)
partitioned_database_join_demo(verbose=True)

