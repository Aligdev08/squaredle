class Stack:
    def __init__(self, max_length: int):
        self.array = [None] * max_length  # simulate list being fixed-length
        self.top_pointer = 0  # next available index

    def __str__(self) -> str:
        return ", ".join(
            value if value and i < self.top_pointer else "_"
            for i, value in enumerate(self.array)
        )

    def is_empty(self) -> bool:
        return self.top_pointer == 0

    def is_full(self) -> bool:
        return self.top_pointer == len(self.array)

    def peek(self) -> object:
        return self.array[self.top_pointer - 1]

    def pop(self) -> object:
        if self.is_empty():
            raise ValueError("Stack is empty.")
        self.top_pointer -= 1
        return self.array[self.top_pointer]  # doesn't have to be replaced with None

    def push(self, value: object) -> None:
        if self.is_full():
            raise ValueError("Stack is full.")
        self.array[self.top_pointer] = value
        self.top_pointer += 1
