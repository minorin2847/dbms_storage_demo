from random import seed, randint, choice, sample

seed(1)

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
    global students, courses, enrollments
    students = []
    courses = []
    enrollments = []
    # Randomize students
    for i in range(1, 21):
        classes = [f"C10{i}" for i in range(1, 6)]
        student = Student(i, f"Nguyen Van {i}", choice(classes), f"nvan{i}@gmail.com", f"0{randint(1000000000, 10000000000):09d}")
        students.append(student)

    # List courses
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
random_students = sample(students, k=len(students))
random_enrollments = sample(enrollments, k=len(enrollments))

# =================================================================
# I. Heap file vs Sequential file
# =================================================================

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

# =================================================================
# II. Multitable Clustering and Partitioning 
# =================================================================

class StandardDatabase:
    def __init__(self):
        self.database = {"students": [], "enrollments": []}
        self.tables = {"students": Student, "enrollments": Enrollment}
    def insert(self, table, record):
        self.database[table].append(record)
    def search(self, table, key, value):
        lookup_count = 0
        records = []
        for i in self.database[table]:
            lookup_count += 1
            if getattr(i, key) == value:
                records.append(i)
        return (records, lookup_count)
    def join(self, t1, t2, key, tableName=""):
        tableName = t1 + "_" + t2 if tableName == "" else tableName
        def joinInit(self, **kwargs):
            for k, v in kwargs.items(): setattr(self, k, v)
        def joinStr(self):
            return f"[{str.upper(tableName)}|{'|'.join([str(i) for i in self.__dict__.values()])}]"
        joinClass = type(tableName, (object,), {'__init__': joinInit, '__str__': joinStr})
        self.tables[tableName] = joinClass
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

class ClusteredDatabase:
    def __init__(self):
        self.database = {}
        self.tables = {"students": Student, "enrollments": Enrollment}
    def insert(self, table, record):
        if getattr(record, 'student_id') not in self.database:
            self.database[getattr(record, 'student_id')] = [record]
        else:
            self.database[getattr(record, 'student_id')].append(record)
    def search(self, table, key, value):
        lookup_count = 0
        records = []
        if key == 'student_id':
            for i in self.database.get(value, []):
                lookup_count += 1
                if isinstance(i, self.tables[table]): records.append(i)
        else:
            for i in self.database.values():
                for j in i:
                    lookup_count += 1
                    if isinstance(j, self.tables[table]) and getattr(j, key) == value:
                        records.append(j)
        return (records, lookup_count)
    def join(self, t1, t2, key, tableName=""):
        tableName = t1 + "_" + t2 if tableName == '' else tableName
        def joinInit(self, **kwargs):
            for k, v in kwargs.items(): setattr(self, k, v)
        def joinStr(self):
            return f"[{str.upper(tableName)}|{'|'.join([str(i) for i in self.__dict__.values()])}]"
        joinClass = type(tableName, (object,), {'__init__': joinInit, '__str__': joinStr})
        self.tables[tableName] = joinClass
        lookup_count = 0
        if key == 'student_id':
            for i in self.database.keys():
                newRecords = []
                lookup_count += 1
                parent = None
                for j in self.database[i]:
                    if isinstance(j, self.tables[t1]): parent = j
                    elif isinstance(j, self.tables[t2]) and parent:
                        newRecords.append(joinClass(**{**parent.__dict__, **j.__dict__}))
                self.database[i].extend(newRecords)
        return lookup_count

class PartitionedDatabase:
    def __init__(self):
        self.database = {"students": {}, "enrollments": {}}
        self.tables = {"students": Student, "enrollments": Enrollment}
    def insert(self, table, record):
        if table == "students":
            if record.class_name not in self.database["students"]: self.database["students"][record.class_name] = [record]
            else: self.database["students"][record.class_name].append(record)
        elif table == "enrollments":
            if record.semester not in self.database["enrollments"]: self.database["enrollments"][record.semester] = [record]
            else: self.database["enrollments"][record.semester].append(record)
    def search(self, table, key, value):
        lookup_count = 0
        records = []
        if (table == "students" and key == "class_name") or (table == "enrollments" and key == "semester"):
            records = self.database[table].get(value, [])
        else:
            for i in self.database[table].values():
                for j in i:
                    lookup_count += 1
                    if getattr(j, key) == value: records.append(j)
        return (records, lookup_count)
    def join(self, t1, t2, key, tableName=""):
        tableName = t1 + "_" + t2 if tableName == "" else tableName
        def joinInit(self, **kwargs):
            for k, v in kwargs.items(): setattr(self, k, v)
        def joinStr(self):
            return f"[{str.upper(tableName)}|{'|'.join([str(i) for i in self.__dict__.values()])}]"
        joinClass = type(tableName, (object,), {'__init__': joinInit, '__str__': joinStr})
        self.tables[tableName] = joinClass
        results = []
        lookup_count = 0
        helper = {}
        if t1 == "students" and key == "class_name":
            for k, v in self.database[t1].items(): helper[k] = v
        else:
            for i in self.database[t1].values():
                for j in i:
                    lookup_count += 1
                    helper[getattr(j, key)] = j
        if t2 == "enrollments" and key == "semester":
            for k, v in self.database[t2].items():
                match = helper.get(k)
                if match:
                    for i in v: results.append(joinClass(**{**match.__dict__, **i.__dict__}))
        else:
            for i in self.database[t2].values():
                for j in i:
                    lookup_count += 1
                    match = helper.get(getattr(j, key))
                    if match: results.append(joinClass(**{**match.__dict__, **j.__dict__}))
        self.database[tableName] = results
        return lookup_count

# =================================================================
# EXECUTION DEMO: COMPARING STORAGE STRATEGIES
# =================================================================

def demo_phase_1(verbose=True):
    print("\n" + "="*60)
    print("PHASE 1: FILE ORGANIZATION PERFORMANCE (Heap vs Sequential)")
    print("="*60)
    heapFile = StudentHeapFile()
    sequentialFile = StudentSequentialFile()
    
    # --- INSERT BATTLE ---
    print("\n[HEAP FILE INSERT]")
    print("# Insert randomized student records into heap file")
    verbose and print("! VERBOSE OUTPUT")
    total_hc = 0
    for s in random_students:
        hc = heapFile.insert(s)
        verbose and print(f"? Insert record {s} after {hc} lookups")
        total_hc += hc
    if verbose:
        print("? Heap file content:")
        for s in heapFile.heap: print("- " + str(s))
    print(f"! Finish inserting into heap after {total_hc} lookups")
    
    print("\n[SEQUENTIAL FILE INSERT]")
    print("# Inserting random student records into sequential file")
    verbose and print("! VERBOSE OUTPUT")
    total_sc = 0
    for s in random_students:
        sc = sequentialFile.insert(s)
        verbose and print(f"? Insert record {s} after {sc} lookups")
        total_sc += sc
    if verbose:
        print("? Sequential file content:")
        for s in sequentialFile.list: print("- " + str(s))
    print(f"! Finish inserting into sequential after {total_sc} lookups")

    # --- RANDOM SEARCH BATTLE ---
    random_search_id = sample(range(1, 21), k=5)
    
    print(f"\n[HEAP RANDOM SEARCH]")
    print(f"# Search for 5 random students: {random_search_id}")
    verbose and print("! VERBOSE OUTPUT")
    total_hc = 0
    records_heap = []
    for i in random_search_id:
        record, hc = heapFile.random_search(i)
        verbose and print(f"? Found record {record} after {hc} lookups")
        total_hc += hc
        records_heap.append(record)
    verbose and print(f"? Found records:\n- {'\n- '.join(str(i) for i in records_heap)}")
    print(f"! Finish heap search after {total_hc} lookups")

    print(f"\n[SEQUENTIAL FILE RANDOM SEARCH]")
    print(f"# Search for 5 random students: {random_search_id}")
    verbose and print("! VERBOSE OUTPUT")
    total_sc = 0
    records_seq = []
    for i in random_search_id:
        record, index, sc = sequentialFile.random_search(i)
        verbose and print(f"? Found record {record} at index {index} after {sc} lookups")
        total_sc += sc
        if record: records_seq.append(record)
    verbose and print(f"? Found records:\n- {'\n- '.join(str(i) for i in records_seq)}")
    print(f"! Finish sequential search after {total_sc} lookups")

    # --- SEQUENTIAL / RANGE SEARCH BATTLE ---
    start, end = 5, 10
    
    print(f"\n[HEAP SEQUENTIAL SEARCH]")
    print(f"# Search for students with id from {start} to {end}")
    verbose and print("! VERBOSE OUTPUT")
    hc, records_heap = heapFile.sequential_search(start, end)
    verbose and print(f"? Found records:\n- {'\n- '.join(str(i) for i in records_heap)}")
    print(f"! Finish heap search after {hc} lookups")

    print(f"\n[SEQUENTIAL FILE SEQUENTIAL SEARCH]")
    print(f"# Search for students with id from {start} to {end}")
    verbose and print("! VERBOSE OUTPUT")
    sc, records_seq = sequentialFile.sequential_search(start, end)
    verbose and print(f"? Found records:\n- {'\n- '.join(str(i) for i in records_seq)}")
    print(f"! Finish sequential search after {sc} lookups")

def demo_phase_2(verbose=True):
    print("\n" + "="*60)
    print("PHASE 2: CLUSTERING & LOCALITY (Standard vs Clustered)")
    print("="*60)
    standard_db = StandardDatabase()
    clustered_db = ClusteredDatabase()

    # --- INSERT ---
    print("\n[STANDARD DATABASE INSERT]")
    print("# Inserting randomized students and enrollments into the database")
    for s in random_students: standard_db.insert("students", s)
    for e in random_enrollments: standard_db.insert("enrollments", e)
    if verbose:
        print("? Standard database structure:")
        print(f"? Students:\n- {'\n- '.join([str(i) for i in standard_db.database['students']])}")
        print(f"? Enrollments:\n- {'\n- '.join([str(i) for i in standard_db.database['enrollments']])}")

    print("\n[CLUSTERED DATABASE INSERT]")
    print("# Inserting randomized students and enrollments into the database")
    for s in random_students: clustered_db.insert("students", s)
    for e in random_enrollments: clustered_db.insert("enrollments", e)
    if verbose:
        print("? Clustered database structure:")
        for key, value in clustered_db.database.items():
            print(f"- student_id = {key}:")
            for i in value: print(f"  - {str(i)}")

    # --- JOIN ---
    print("\n[STANDARD DATABASE JOIN]")
    print("# Joining database students and enrollments into studentEnroll table")
    sc = standard_db.join("students", "enrollments", "student_id", "studentEnroll")
    if verbose:
        print(f"? New table structure:\n- {'\n- '.join([str(i) for i in standard_db.database['studentEnroll']])}")
    print(f"! Finish Standard join after {sc} lookups")

    print("\n[CLUSTERED DATABASE JOIN]")
    print("# Joining database students and enrollments into studentEnroll table")
    cc = clustered_db.join("students", "enrollments", "student_id", "studentEnroll")
    if verbose:
        print("? New database structure:")
        for key, value in clustered_db.database.items():
            print(f"- student_id = {key}:")
            for i in value: print(f"  - {str(i)}")
    print(f"! Finish Clustered join after {cc} lookups")

def demo_phase_3(verbose=True):
    print("\n" + "="*60)
    print("PHASE 3: PARTITION PRUNING vs FULL SCAN (Partitioned)")
    print("="*60)
    part_db = PartitionedDatabase()

    print("\n[PARTITIONED DATABASE INSERT]")
    print("# Inserting randomized students (by class) and enrollments (by semester)")
    for s in random_students: part_db.insert("students", s)
    for e in random_enrollments: part_db.insert("enrollments", e)
    
    if verbose:
        print("? Partitioned Database Structure:")
        print("--- Students (Partitioned by class_name) ---")
        for class_key, s_list in part_db.database["students"].items():
            print(f"Partition [{class_key}]:")
            for s in s_list: print(f"  - {s}")
        
        print("\n--- Enrollments (Partitioned by semester) ---")
        for sem_key, e_list in part_db.database["enrollments"].items():
            print(f"Partition [{sem_key}]:")
            for e in e_list: print(f"  - {e}")

    print("\n[PARTITIONED SEARCH BY SEMESTER: 20231]")
    print(f"# Querying partition key: 20231")
    verbose and print("! VERBOSE OUTPUT")
    records, lookup_count = part_db.search("enrollments", "semester", "20231")
    if verbose:
        print(f"? Found records:")
        for r in records: print(f"  - {str(r)}")
    print(f"! Found {len(records)} records after {lookup_count} lookup(s)")

    print("\n[PARTITIONED SEARCH BY STUDENT_ID: 10]")
    print(f"# Querying non-partition key: 10")
    verbose and print("! VERBOSE OUTPUT")
    records, lookup_count = part_db.search("students", "student_id", 10)
    if verbose:
        print(f"? Found records:")
        for r in records: print(f"  - {str(r)}")
    print(f"! Found {len(records)} record(s) after {lookup_count} lookup(s)")

    print("\n[PARTITIONED DATABASE JOIN]")
    print("# Joining Students and Enrollments by student_id")
    verbose and print("! VERBOSE OUTPUT")
    lookup_count = part_db.join("students", "enrollments", "student_id", "studentEnroll")
    if verbose:
        print("--- studentEnroll Joined Table Content ---")
        for row in part_db.database["studentEnroll"]: print(f"- {row}")
    print(f"! Finish joining after {lookup_count} lookups")

def demo_phase_4(verbose=True):
    print("\n" + "="*60)
    print("PHASE 4: CLUSTERING VS PARTITIONING COMPARISON")
    print("="*60)
    
    # Khởi tạo dữ liệu sạch cho demo
    c_db = ClusteredDatabase()
    p_db = PartitionedDatabase()
    
    print("\n[PREPARING DATA]")
    for s in random_students:
        c_db.insert("students", s)
        p_db.insert("students", s)
    for e in random_enrollments:
        c_db.insert("enrollments", e)
        p_db.insert("enrollments", e)
    print("! Data loaded into both Clustered and Partitioned systems.")

    # --- SCENARIO A: JOIN ---
    print("\n[SCENARIO A: JOIN BATTLE (By student_id)]")
    print("# Task: Join 'students' and 'enrollments' tables on 'student_id'")
    verbose and print("! VERBOSE OUTPUT")

    # Clustered Join
    c_join_count = c_db.join("students", "enrollments", "student_id", "c_joined")
    if verbose:
        print("? Clustered DB Join Results (Sample):")
        # In thử 3 dòng đầu tiên của kết quả join
        sample_data = []
        for v in c_db.database.values():
            for item in v:
                if "C_JOINED" in str(item): sample_data.append(item)
        for row in sample_data[:3]: print(f"  - {row}")
    print(f"! Clustered Join finished after {c_join_count} lookups")

    # Partitioned Join
    p_join_count = p_db.join("students", "enrollments", "student_id", "p_joined")
    if verbose:
        print("? Partitioned DB Join Results (Sample):")
        for row in p_db.database["p_joined"][:3]: print(f"  - {row}")
    print(f"! Partitioned Join finished after {p_join_count} lookups")


    print("\n" + "-"*30)

    # --- SCENARIO B: SEARCH ---
    target_sem = "20231"
    print(f"\n[SCENARIO B: SEARCH BATTLE (By semester '{target_sem}')]")
    print(f"# Task: Find all enrollment records for semester {target_sem}")
    verbose and print("! VERBOSE OUTPUT")

    # Clustered Search
    c_records, c_search_count = c_db.search("enrollments", "semester", target_sem)
    if verbose:
        print(f"? Clustered Search found {len(c_records)} records:")
        for r in c_records[:3]: print(f"  - {r}")
        print("  ... (full scan performed across all student buckets)")
    print(f"! Clustered Search finished after {c_search_count} lookups")

    # Partitioned Search
    p_records, p_search_count = p_db.search("enrollments", "semester", target_sem)
    if verbose:
        print(f"? Partitioned Search found {len(p_records)} records:")
        for r in p_records[:3]: print(f"  - {r}")
        print(f"  ... (jumped directly to partition '{target_sem}')")
    print(f"! Partitioned Search finished after {p_search_count} lookups")


# --- CẬP NHẬT MENU CHÍNH ---
def main_menu():
    while True:
        print("\n" + "*"*50)
        print("Demo DBMS - Phân tích chiến lược lưu trữ")
        print("*"*50)
        print("1. Phase 1: Heap vs Sequential (File Org)")
        print("2. Phase 2: Standard vs Clustered (Locality)")
        print("3. Phase 3: Partitioning (Pruning Search)")
        print("4. Phase 4: Clustering vs Partitioning (Comparison)")
        print("Gõ 'q' để thoát")
        
        choice = input("\nChọn chức năng (1/2/3/4/q): ").strip().lower()
        
        if choice == '1':
            demo_phase_1(verbose=True)
        elif choice == '2':
            demo_phase_2(verbose=True)
        elif choice == '3':
            demo_phase_3(verbose=True)
        elif choice == '4':
            demo_phase_4(verbose=True)
        elif choice == 'q':
            print("Đang thoát chương trình. Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    main_menu()
