# Task 1: Find the maximum of three numbers
num1, num2, num3 = 10, 5, 8
max_number = max(num1, num2, num3)
print("Max of three numbers:", max_number)

# Task 2: Sum all the numbers in a list
numbers = [1, 2, 3, 4, 5]
sum_numbers = sum(numbers)
print("Sum of list:", sum_numbers)

# Task 3: Reverse a string
string = "hello"
reversed_string = string[::-1]
print("Reverse string:", reversed_string)

# Task 4: Count the number of upper and lower case letters in a string
string = "Hello World"
upper_count = sum(1 for char in string if char.isupper())
lower_count = sum(1 for char in string if char.islower())
print("Uppercase:", upper_count)
print("Lowercase:", lower_count)

# Task 5: Return a new list with distinct elements from the first list
my_list = [1, 2, 2, 3, 4, 4, 5]
new_list = list(set(my_list))
print("Unique elements:", new_list)
