score = float(input("Enter student's score: "))

if score > 90:
    grade = "A"
elif score > 75:
    grade = "B"
elif score > 65:
    grade = "C"
else:
    grade = "F"

print("Student's grade:", grade)