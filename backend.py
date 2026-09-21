import os
import pandas as pd

CSV_FILE = "students.csv"

COLUMNS = [
    "Roll No",
    "Name",
    "Class",
    "English",
    "Physics",
    "Chemistry",
    "Maths",
    "Total",
    "Percentage",
    "Grade",
    "Result"
]

# Create CSV if not exists
def create_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_FILE, index=False)



# Get all students
def get_students():
    create_csv()

    df = pd.read_csv(CSV_FILE)

    # If CSV is empty
    if df.empty:
        return pd.DataFrame(columns=COLUMNS)

    return df



# Calculate result
def calculate_result(english, physics, chemistry, maths):

    marks = [english, physics, chemistry, maths]

    total = sum(marks)
    percentage = total / 4

    # Pass condition
    if any(mark < 33 for mark in marks):
        result = "Fail"
    else:
        result = "Pass"

    # Grade
    if result == "Fail":
        grade = "F"
    elif percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B+"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"

    return total, percentage, grade, result

# Add student
def add_student(
    roll_no,
    name,
    student_class,
    english,
    physics,
    chemistry,
    maths
):

    df = get_students()

    # Check duplicate roll number
    if not df.empty:
        if str(roll_no) in df["Roll No"].astype(str).values:
            return False, "Roll No already exists!"

    total, percentage, grade, result = calculate_result(
        english,
        physics,
        chemistry,
        maths
    )

    new_student = pd.DataFrame([{
        "Roll No": roll_no,
        "Name": name,
        "Class": student_class,
        "English": english,
        "Physics": physics,
        "Chemistry": chemistry,
        "Maths": maths,
        "Total": total,
        "Percentage": round(percentage, 2),
        "Grade": grade,
        "Result": result
    }])

    df = pd.concat([df, new_student], ignore_index=True)

    df.to_csv(CSV_FILE, index=False)

    return True, "Student added successfully!"

# Delete student
def delete_student(roll_no):

    df = get_students()

    if df.empty:
        return False, "No students found."

    old_length = len(df)

    df = df[df["Roll No"].astype(str) != str(roll_no)]

    if len(df) == old_length:
        return False, "Student not found."

    df.to_csv(CSV_FILE, index=False)

    return True, "Student deleted successfully!"

# Update student
def update_student(
    roll_no,
    name,
    student_class,
    english,
    physics,
    chemistry,
    maths
):

    df = get_students()

    if df.empty:
        return False, "No students found."

    index = df[df["Roll No"].astype(str) == str(roll_no)].index

    if len(index) == 0:
        return False, "Student not found."

    total, percentage, grade, result = calculate_result(
        english,
        physics,
        chemistry,
        maths
    )

    i = index[0]

    df.loc[i, "Name"] = name
    df.loc[i, "Class"] = student_class
    df.loc[i, "English"] = english
    df.loc[i, "Physics"] = physics
    df.loc[i, "Chemistry"] = chemistry
    df.loc[i, "Maths"] = maths
    df.loc[i, "Total"] = total
    df.loc[i, "Percentage"] = round(percentage, 2)
    df.loc[i, "Grade"] = grade
    df.loc[i, "Result"] = result

    df.to_csv(CSV_FILE, index=False)

    return True, "Student updated successfully!"

# Search student
def search_students(keyword):

    df = get_students()

    if df.empty:
        return df

    keyword = str(keyword).lower()

    result = df[
        df["Name"].astype(str).str.lower().str.contains(keyword)
        |
        df["Roll No"].astype(str).str.lower().str.contains(keyword)
        |
        df["Class"].astype(str).str.lower().str.contains(keyword)
    ]

    return result

# Get topper
def get_topper():

    df = get_students()

    if df.empty:
        return None

    return df.loc[df["Percentage"].idxmax()]

# Class-wise result
def get_class_result(student_class):

    df = get_students()

    if df.empty:
        return df

    return df[
        df["Class"].astype(str) == str(student_class)
    ]

# Statistics
def get_statistics():

    df = get_students()

    if df.empty:
        return {
            "total_students": 0,
            "pass_students": 0,
            "fail_students": 0,
            "average_percentage": 0,
            "top_percentage": 0
        }

    return {
        "total_students": len(df),
        "pass_students": len(df[df["Result"] == "Pass"]),
        "fail_students": len(df[df["Result"] == "Fail"]),
        "average_percentage": round(df["Percentage"].mean(), 2),
        "top_percentage": round(df["Percentage"].max(), 2)
    }

# Save uploaded CSV
def save_uploaded_csv(uploaded_file):

    try:

        df = pd.read_csv(uploaded_file)

        # Check required columns
        required = [
            "Roll No",
            "Name",
            "Class",
            "English",
            "Physics",
            "Chemistry",
            "Maths"
        ]

        missing = [
            col for col in required
            if col not in df.columns
        ]

        if missing:
            return False, f"Missing columns: {missing}"

        # Recalculate result
        results = df.apply(
            lambda row: calculate_result(
                float(row["English"]),
                float(row["Physics"]),
                float(row["Chemistry"]),
                float(row["Maths"])
            ),
            axis=1
        )

        df["Total"] = [r[0] for r in results]
        df["Percentage"] = [round(r[1], 2) for r in results]
        df["Grade"] = [r[2] for r in results]
        df["Result"] = [r[3] for r in results]

        df = df[COLUMNS]

        df.to_csv(CSV_FILE, index=False)

        return True, "CSV uploaded successfully!"

    except Exception as e:
        return False, f"Error: {e}"