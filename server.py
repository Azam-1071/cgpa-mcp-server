"""MCP server for the CGPA Guider. Run: python server.py  ->  http://127.0.0.1:8000/mcp"""
import os

from fastmcp import FastMCP

from tools import (calculate_new_cgpa, calculate_semester_gpa, get_credit_hours,
                   get_remaining_credit_hours, get_semester_courses,
                   marks_to_grade_points, required_gpa_for_target, save_report)

mcp = FastMCP("cgpa")

for fn in (marks_to_grade_points, calculate_semester_gpa, calculate_new_cgpa,
           required_gpa_for_target, get_semester_courses, get_credit_hours,
           get_remaining_credit_hours, save_report):
    mcp.tool(fn)  # type hints + docstring become the description the model reads

if __name__ == "__main__":
    mcp.run(transport="http",
            host=os.getenv("HOST", "127.0.0.1"),
            port=int(os.getenv("PORT", "8000")))
