def find_max_iterative(numbers):
    max_value=numbers[0]
    for i in range(10):
        if numbers[i] > max_value:
            max_value = numbers[i]

    return max_value


numbers = []
for i in range(10):
    num = int(input("숫자를 입력하세요: "))
    numbers.append(num)

max_value = find_max_iterative(numbers)
print("최댓값2: ", max_value)