import streamlit as st
import pandas as pd

from backend import (
    get_students,
    add_student,
    delete_student,
    update_student,
    search_students,
    get_topper,
    get_class_result,
    get_statistics,
    save_uploaded_csv
)


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Student Result Management",
    page_icon="🎓",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("🎓 Student Result Management System")

st.write(
    "Manage students, marks, results, grades and class-wise performance."
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("📚 Menu")

menu = st.sidebar.radio(
    "Select Option",
    [
        "🏠 Dashboard",
        "➕ Add Student",
        "📋 Student List",
        "🔍 Search Student",
        "✏️ Update Student",
        "🗑️ Delete Student",
        "📊 Class Result",
        "🏆 Topper",
        "📤 Upload CSV",
        "📥 Download CSV"
    ]
)


# ==========================================
# DASHBOARD
# ==========================================

if menu == "🏠 Dashboard":

    st.header("📊 Dashboard")

    stats = get_statistics()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "👨‍🎓 Total Students",
        stats["total_students"]
    )

    col2.metric(
        "✅ Pass",
        stats["pass_students"]
    )

    col3.metric(
        "❌ Fail",
        stats["fail_students"]
    )

    col4.metric(
        "📈 Average %",
        stats["average_percentage"]
    )

    col5.metric(
        "🏆 Highest %",
        stats["top_percentage"]
    )

    st.divider()

    df = get_students()

    if not df.empty:

        st.subheader("📊 Percentage Chart")

        chart_data = (
            df[["Name", "Percentage"]]
            .set_index("Name")
        )

        st.bar_chart(chart_data)

        st.subheader("📋 Recent Student Data")

        st.dataframe(
            df,
            use_container_width=True
        )

    else:
        st.info("No students available.")


# ==========================================
# ADD STUDENT
# ==========================================

elif menu == "➕ Add Student":

    st.header("➕ Add Student")

    with st.form("add_student_form"):

        col1, col2 = st.columns(2)

        with col1:

            roll_no = st.text_input(
                "Roll No"
            )

            name = st.text_input(
                "Student Name"
            )

            student_class = st.text_input(
                "Class"
            )

        with col2:

            english = st.number_input(
                "English",
                min_value=0,
                max_value=100,
                value=0
            )

            physics = st.number_input(
                "Physics",
                min_value=0,
                max_value=100,
                value=0
            )

            chemistry = st.number_input(
                "Chemistry",
                min_value=0,
                max_value=100,
                value=0
            )

            maths = st.number_input(
                "Maths",
                min_value=0,
                max_value=100,
                value=0
            )

        submit = st.form_submit_button(
            "➕ Add Student"
        )

    if submit:

        if not roll_no or not name or not student_class:

            st.error(
                "Please fill all student details."
            )

        else:

            success, message = add_student(
                roll_no,
                name,
                student_class,
                english,
                physics,
                chemistry,
                maths
            )

            if success:
                st.success(message)
            else:
                st.error(message)


# ==========================================
# STUDENT LIST
# ==========================================

elif menu == "📋 Student List":

    st.header("📋 All Students")

    df = get_students()

    if df.empty:

        st.info("No students found.")

    else:

        st.dataframe(
            df,
            use_container_width=True
        )


# ==========================================
# SEARCH STUDENT
# ==========================================

elif menu == "🔍 Search Student":

    st.header("🔍 Search Student")

    keyword = st.text_input(
        "Enter Name, Roll No or Class"
    )

    if keyword:

        result = search_students(keyword)

        if result.empty:

            st.warning(
                "No student found."
            )

        else:

            st.dataframe(
                result,
                use_container_width=True
            )


# ==========================================
# UPDATE STUDENT
# ==========================================

elif menu == "✏️ Update Student":

    st.header("✏️ Update Student")

    df = get_students()

    if df.empty:

        st.info("No students available.")

    else:

        roll_no = st.selectbox(
            "Select Roll No",
            df["Roll No"].astype(str).tolist()
        )

        student = df[
            df["Roll No"].astype(str) == str(roll_no)
        ].iloc[0]

        with st.form("update_form"):

            name = st.text_input(
                "Name",
                value=str(student["Name"])
            )

            student_class = st.text_input(
                "Class",
                value=str(student["Class"])
            )

            col1, col2 = st.columns(2)

            with col1:

                english = st.number_input(
                    "English",
                    0,
                    100,
                    int(student["English"])
                )

                physics = st.number_input(
                    "Physics",
                    0,
                    100,
                    int(student["Physics"])
                )

            with col2:

                chemistry = st.number_input(
                    "Chemistry",
                    0,
                    100,
                    int(student["Chemistry"])
                )

                maths = st.number_input(
                    "Maths",
                    0,
                    100,
                    int(student["Maths"])
                )

            update = st.form_submit_button(
                "💾 Update Student"
            )

        if update:

            success, message = update_student(
                roll_no,
                name,
                student_class,
                english,
                physics,
                chemistry,
                maths
            )

            if success:
                st.success(message)
            else:
                st.error(message)


# ==========================================
# DELETE STUDENT
# ==========================================

elif menu == "🗑️ Delete Student":

    st.header("🗑️ Delete Student")

    df = get_students()

    if df.empty:

        st.info("No students available.")

    else:

        roll_no = st.selectbox(
            "Select Roll No",
            df["Roll No"].astype(str).tolist()
        )

        student = df[
            df["Roll No"].astype(str) == str(roll_no)
        ].iloc[0]

        st.warning(
            f"Delete: {student['Name']} "
            f"(Roll No: {roll_no})"
        )

        if st.button("🗑️ Delete Student"):

            success, message = delete_student(
                roll_no
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)


# ==========================================
# CLASS RESULT
# ==========================================

elif menu == "📊 Class Result":

    st.header("📊 Class-wise Result")

    df = get_students()

    if df.empty:

        st.info("No students available.")

    else:

        classes = sorted(
            df["Class"].astype(str).unique()
        )

        selected_class = st.selectbox(
            "Select Class",
            classes
        )

        result = get_class_result(
            selected_class
        )

        st.write(
            f"Students in Class {selected_class}: "
            f"**{len(result)}**"
        )

        st.dataframe(
            result,
            use_container_width=True
        )

        if not result.empty:

            st.subheader("📈 Class Performance")

            chart = (
                result[["Name", "Percentage"]]
                .set_index("Name")
            )

            st.bar_chart(chart)


# ==========================================
# TOPPER
# ==========================================

elif menu == "🏆 Topper":

    st.header("🏆 Class Topper")

    topper = get_topper()

    if topper is None:

        st.info("No students available.")

    else:

        st.success(
            f"🏆 Topper: {topper['Name']}"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Roll No",
            topper["Roll No"]
        )

        col2.metric(
            "Total",
            topper["Total"]
        )

        col3.metric(
            "Percentage",
            f"{topper['Percentage']}%"
        )

        col4.metric(
            "Grade",
            topper["Grade"]
        )

        st.dataframe(
            pd.DataFrame([topper]),
            use_container_width=True
        )


# ==========================================
# UPLOAD CSV
# ==========================================

elif menu == "📤 Upload CSV":

    st.header("📤 Upload Student CSV")

    st.write(
        "CSV must contain these columns:"
    )

    st.code(
        "Roll No, Name, Class, English, Physics, Chemistry, Maths"
    )

    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        preview = pd.read_csv(
            uploaded_file
        )

        st.subheader("Preview")

        st.dataframe(
            preview.head(),
            use_container_width=True
        )

        if st.button("📤 Import CSV"):

            uploaded_file.seek(0)

            success, message = save_uploaded_csv(
                uploaded_file
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)


# ==========================================
# DOWNLOAD CSV
# ==========================================

elif menu == "📥 Download CSV":

    st.header("📥 Download Student Data")

    df = get_students()

    if df.empty:

        st.info("No data available.")

    else:

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="students_result.csv",
            mime="text/csv"
        )

        st.dataframe(
            df,
            use_container_width=True
        )