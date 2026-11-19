"""CGPA Guider tools. Plain Python functions: server.py shares them over MCP.

Rules for every tool: type hints (they become the schema), a docstring that says
WHEN to use it, and bad input returns an "Error: ..." string instead of raising.
"""
import os
import re

COURSES = {
    1: [("MS-251", "Probability & Statistics", 3.0),
        ("GE-160", "Applications of ICT", 3.0),
        ("GE-169", "Applied Physics", 3.0),
        ("GE-167", "Discrete Structures", 3.0),
        ("HQ-001", "Quran Translation - I", 0.5),
        ("GE-190", "Functional English", 3.0)],
    2: [("CC-112", "Programming Fundamentals", 3.0),
        ("CC-112-L", "Programming Fundamentals Lab", 1.0),
        ("CC-110", "Digital Logic Design", 2.0),
        ("CC-110-L", "Digital Logic Design Lab", 1.0),
        ("MS-252", "Linear Algebra", 3.0),
        ("GE-191", "Expository Writing", 3.0),
        ("GE-163", "Islamic Studies", 2.0),
        ("HQ-002", "Quran Translation - II", 0.5)],
    3: [("CC-211", "Object Oriented Programming", 3.0),
        ("CC-211-L", "Object Oriented Programming Lab", 1.0),
        ("CC-215", "Database Systems", 3.0),
        ("CC-215-L", "Database Systems Lab", 1.0),
        ("CC-210", "Computer Organization & Assembly Language", 3.0),
        ("GE-162", "Calculus & Analytical Geometry", 3.0),
        ("GE-192", "Introduction to Management", 2.0),
        ("HQ-003", "Quran Translation - III", 0.5)],
    4: [("CC-213", "Data Structures", 3.0),
        ("CC-213-L", "Data Structures Lab", 1.0),
        ("CC-312", "Information Security", 3.0),
        ("CC-214", "Computer Networks", 3.0),
        ("CC-212", "Software Engineering", 3.0),
        ("DC-220", "Advanced Database Management Systems", 3.0),
        ("HQ-004", "Quran Translation - IV", 0.5)],
    5: [("CC-313", "Analysis of Algorithms", 3.0),
        ("CC-310", "Artificial Intelligence", 3.0),
        ("DC-320", "Theory of Automata and Formal Languages", 3.0),
        ("DC-321", "Human Computer Interaction", 3.0),
        ("DC-322", "Computer Architecture", 3.0),
        ("EC-330", "Web Technologies / Elective", 3.0),
        ("HQ-005", "Quran Translation - V", 0.5)],
    6: [("CC-311", "Operating Systems", 3.0),
        ("EC-333", "Mobile Application Development / Elective", 3.0),
        ("EC-324", "Software Construction & Development / Elective", 3.0),
        ("EC-335", "Machine Learning / Elective", 3.0),
        ("EC-334", "Game Design and Development / Elective", 3.0),
        ("MS-253", "Multivariable Calculus", 3.0),
        ("HQ-006", "Quran Translation - VI", 0.5)],
    7: [("CC-411", "Final Year Project - I", 2.0),
        ("DC-328", "Parallel & Distributed Computing", 3.0),
        ("EC-345", "Computer Vision / Elective", 3.0),
        ("EC-425", "Software Quality Engineering / Elective", 3.0),
        ("MS-254", "Technical and Business Writing", 3.0),
        ("GE-263", "Entrepreneurship", 2.0),
        ("GE-262", "Professional Practices", 2.0),
        ("HQ-007", "Quran Translation - VII", 0.5)],
    8: [("CC-412", "Final Year Project - II", 4.0),
        ("DC-421", "Compiler Construction", 3.0),
        ("UE-272", "Introduction to Marketing", 3.0),
        ("GE-168", "Ideology and Constitution of Pakistan", 2.0),
        ("GE-363", "Civics and Community Engagement", 2.0),
        ("HQ-008", "Quran Translation - VIII", 0.5)],
}

# (minimum marks, grade points) from the PUCIT grade bands, highest first
GRADE_BANDS = [(85, 4.0), (80, 3.7), (75, 3.3), (70, 3.0), (65, 2.7),
               (61, 2.3), (58, 2.0), (55, 1.7), (50, 1.0), (0, 0.0)]

REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")


def _semester_total(semester: int) -> float:
    return sum(ch for _, _, ch in COURSES[semester])


def marks_to_grade_points(marks: int) -> float | str:
    """Convert ONE course's marks (0-100) into PUCIT grade points (4.0 scale).
    Use this for every course before calculating a semester GPA, or when the
    student asks what grade/grade points a given mark is worth."""
    if not 0 <= marks <= 100:
        return "Error: marks must be between 0 and 100"
    for minimum, points in GRADE_BANDS:
        if marks >= minimum:
            return points
    return "Error: could not convert marks"


def calculate_semester_gpa(grade_points: list[float], credit_hours: list[float]) -> float | str:
    """Calculate one semester's credit-weighted GPA. Use this when the student
    has grade points and credit hours for the courses of a single semester.
    The two lists must be the same length, in the same course order."""
    if not grade_points or len(grade_points) != len(credit_hours):
        return "Error: grade_points and credit_hours must be non-empty lists of the same length"
    if any(not 0 <= g <= 4 for g in grade_points):
        return "Error: every grade point must be between 0 and 4"
    if any(c <= 0 for c in credit_hours):
        return "Error: every credit hour value must be greater than 0"
    total_ch = sum(credit_hours)
    return round(sum(g * c for g, c in zip(grade_points, credit_hours)) / total_ch, 2)


def calculate_new_cgpa(current_cgpa: float, completed_credit_hours: float,
                       semester_gpa: float, semester_credit_hours: float) -> float | str:
    """Project the CGPA after ONE more semester. Use this when the student gives
    their current CGPA and completed credit hours and wants to know where they
    end up after a semester with a given GPA."""
    if not 0 <= current_cgpa <= 4 or not 0 <= semester_gpa <= 4:
        return "Error: CGPA and GPA must be between 0 and 4"
    if completed_credit_hours < 0 or semester_credit_hours <= 0:
        return "Error: completed credit hours must be >= 0 and semester credit hours must be > 0"
    total = completed_credit_hours + semester_credit_hours
    return round((current_cgpa * completed_credit_hours + semester_gpa * semester_credit_hours) / total, 2)


def required_gpa_for_target(target_cgpa: float, current_cgpa: float,
                            completed_credit_hours: float, remaining_credit_hours: float) -> float | str:
    """Calculate the GPA the student must average over the remaining credit hours
    to reach a target CGPA. Use this for 'what do I need to graduate with X?'.
    The result CAN exceed 4.0, which means that horizon is impossible; the caller
    must then retry with more remaining credit hours."""
    if not 0 <= target_cgpa <= 4 or not 0 <= current_cgpa <= 4:
        return "Error: CGPA values must be between 0 and 4"
    if completed_credit_hours < 0 or remaining_credit_hours <= 0:
        return "Error: completed credit hours must be >= 0 and remaining credit hours must be > 0"
    needed = (target_cgpa * (completed_credit_hours + remaining_credit_hours)
              - current_cgpa * completed_credit_hours) / remaining_credit_hours
    return round(needed, 2)


def get_semester_courses(semester: int) -> str:
    """List the courses and credit hours of one semester (1-8) of the BS Computer
    Science scheme. Use this when the student asks what a semester contains, or
    to find the credit hours of the courses they took."""
    if semester not in COURSES:
        return "Error: semester must be between 1 and 8"
    lines = [f"{code}: {name} ({ch} credit hours)" for code, name, ch in COURSES[semester]]
    lines.append(f"Total: {_semester_total(semester)} credit hours")
    return f"Semester {semester}\n" + "\n".join(lines)


def get_credit_hours(semesters: list[int]) -> float | str:
    """Total credit hours of the given semesters, e.g. [5, 6] -> 37.0. Use this
    to build a horizon when a target CGPA is unreachable in the current semester
    alone: ask for [5], then [5, 6], then [5, 6, 7], and so on."""
    if not semesters:
        return "Error: give at least one semester"
    if any(s not in COURSES for s in semesters) or len(set(semesters)) != len(semesters):
        return "Error: semesters must be unique numbers between 1 and 8"
    return float(sum(_semester_total(s) for s in semesters))


def get_remaining_credit_hours(current_semester: int) -> float | str:
    """Total credit hours from the student's CURRENT semester through semester 8
    (current semester included). Use this to know how many graded hours are left
    when planning a graduation target."""
    if current_semester not in COURSES:
        return "Error: semester must be between 1 and 8"
    return float(sum(_semester_total(s) for s in range(current_semester, 9)))


def save_report(filename: str, content: str) -> str:
    """Save a text summary (semester GPA, projected CGPA or a target plan) and
    return a confirmation. Use ONLY after the student explicitly asks to save."""
    name = re.sub(r"[^A-Za-z0-9._-]", "_", os.path.basename(filename or ""))
    if not name or name.startswith("."):
        return "Error: filename must contain letters or numbers"
    if not name.endswith(".txt"):
        name += ".txt"
    if not content.strip():
        return "Error: content is empty"
    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(os.path.join(REPORTS_DIR, name), "w", encoding="utf-8") as f:
        f.write(content)
    return f"Saved report as {name}"
