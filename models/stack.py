# word list @ https://ucrel.lancs.ac.uk/bncfreq/lists/1_2_all_freq.txt


class Stack:
    def __init__(self, max_length: int):
        self.array = [None] * max_length  # simulate list being fixed-length
        self.top_pointer = 0  # next available index

    def __str__(self) -> str:
        return ", ".join(
            value if value and i < self.top_pointer else "_"
            for i, value in enumerate(self.array)
        )

    def __len__(self):
        return self.top_pointer

    def to_list(self) -> list[object]:
        return [self.array[i] for i in range(self.top_pointer)]

    def clear(self) -> None:
        self.__init__(len(self.array))

    def is_empty(self) -> bool:
        return self.top_pointer == 0

    def is_full(self) -> bool:
        return self.top_pointer == len(self.array)

    def peek(self, amt: int = 1) -> object:
        if self.top_pointer == 0 or amt > self.top_pointer:
            return None
        return self.array[self.top_pointer - amt]

    def pop(self) -> object:
        if self.is_empty():
            raise ValueError("Stack is empty.")
        self.top_pointer -= 1
        value = self.array[self.top_pointer]
        self.array[self.top_pointer] = None
        return value

    def push(self, value: object) -> None:
        if self.is_full():
            raise ValueError("Stack is full.")
        self.array[self.top_pointer] = value
        self.top_pointer += 1
