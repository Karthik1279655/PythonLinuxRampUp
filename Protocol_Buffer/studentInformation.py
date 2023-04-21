from student_pb2 import StudentList, StudentResult

# Create a StudentList object
students = StudentList()

# Set the values for student_id and student_name
students.student_id = 1
students.student_name = "John Doe"

# Create a StudentDetails object and set its values
student_details = students.student.add()
student_details.result = StudentResult.PASS
student_details.total_marks = 100
student_details.marks_obtain = 90

# Serialize the object to a bytes string
serialized_data = students.SerializeToString()
print(type(serialized_data))

# Print the serialized data
print("\nSerialized Byte String : \t", serialized_data, "\n\n")

# Parse the bytes string back to the StudentList object
parsed_data = StudentList.FromString(serialized_data)

# Print the parsed data
print(type(parsed_data), "\n\n")
print(parsed_data)
