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

def reverse(str):
    st = ListStack()
    for i in range(len(str)):
        st.push(str[i])
    out = ""
    while not st.isEmpty():
        out+=st.pop()
    return out

def main():
    input = "subin 123 simulator"
    answer = reverse(input)
    print("Input string: ", input)
    print("Reverse Ouput string: ", answer)

if __name__ == "__main__":
    main()