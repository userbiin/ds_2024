class ListStack:
    def __init__(self):
        self.__stack = []

    def push(self, item):
        self.__stack.append(item)

    def pop(self):
        if not self.isEmpty():
            return self.__stack.pop()

    def isEmpty(self):
        return len(self.__stack) == 0

def split_and_store(string):
    stack1 = ListStack()
    stack2 = ListStack()
    
    # 스택을 채우기 위한 임시 변수
    temp = ""
    
    # 문자열을 순회하며 '$'를 기준으로 분리하여 스택에 저장
    for char in string:
        if char != '$':
            temp += char
        else:
            stack1.push(temp)
            temp = ""
    
    # 남은 문자열이 있을 경우 스택에 저장
    if temp:
        stack1.push(temp)
    
    # '$'를 기준으로 분리된 문자열을 역순으로 두 번째 스택에 저장
    while not stack1.isEmpty():
        stack2.push(stack1.pop())
    
    return stack1, stack2

def main():
    string = "abc$cba"
    stack1, stack2 = split_and_store(string)
    
    # 결과 출력
    print("First Stack:")
    while not stack1.isEmpty():
        print(stack1.pop())

    print("\nSecond Stack:")
    while not stack2.isEmpty():
        print(stack2.pop())

if __name__ == "__main__":
    main()
