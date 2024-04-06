def reverse_bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

# 테스트를 위한 입력 데이터
input_list = [2, 3, 5, 4, 1]

# 역순 버블 정렬 수행
reverse_bubble_sort(input_list)

# 정렬된 리스트 출력
print(input_list)
