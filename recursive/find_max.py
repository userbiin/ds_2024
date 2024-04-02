def find_max_recursive(numbers, index, max_value):
    if index == len(numbers):
        return max_value
    if numbers[index]>max_value:
        max_value = numbers[index]
    return find_max_recursive(numbers, index+1, max_value)

numbers=[] 
for i in range(10):
    num = int(input("숫자를 입력하세요: "))
    numbers.append(num)

max_value=find_max_recursive(numbers, 0, numbers[0])
print("최댓값: ", max_value)