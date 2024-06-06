# Task 1
numbers = [10, 20, 30, 40, 50]
avg = sum(numbers) / len(numbers)
differences = [num - avg for num in numbers]
print("Differences from the average:", differences)

# Task 2
string = "hello"
array = list(string)
print("Array from string:", array)

# Task 3
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = [num for num in numbers if num % 2 == 0]
odd_numbers = [num for num in numbers if num % 2 != 0]
print("Even numbers:", even_numbers)
print("Odd numbers:", odd_numbers)

# Task 4
numbers = [12, 11, 13, 5, 6]
for i in range(1, len(numbers)):
    key = numbers[i]
    j = i - 1
    while j >= 0 and key < numbers[j]:
        numbers[j + 1] = numbers[j]
        j -= 1
    numbers[j + 1] = key
print("Sorted array:", numbers)
