class ListStack:
    def __init__(self):
        self.__stack = []

    def push(self, item):
        self.__stack.append(item)

    def isEmpty(self):
       return len(self.__stack) == 0
    
    def pop(self):
        if not self.isEmpty():
            return self.__stack.pop()


def split_and_store(str):
    stack1 = ListStack()
    stack2 = ListStack()
    
    temp = ""

    for char in str:
        if char != '$':
            temp += char
        else:
            stack1.push(temp)
            temp = ""
        
    stack2.push(temp)

    return stack1, stack2

def reverse(stack):
    st = ListStack()
    while not stack.isEmpty():
        st.push(stack.pop())
    out = ""
    while not st.isEmpty():
        out += st.pop()
    return out


def check(stack1, stack2):
    while not stack1.isEmpty() and not stack2.isEmpty():
        if stack1.pop() != stack2.pop():
            return "False"
    return "True"


def main():
    input = "abc$cba"
    stack1, stack2 = split_and_store(input)
    print("Input string: ", input)
    print("Check result: ", check(stack1, stack2))

if __name__ == "__main__":
    main()