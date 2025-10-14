from abc import abstractmethod


class SceneBase:
    def __init__(self):
        self.next = self

    @abstractmethod
    def process(self, events):
        """Process user input"""
        print("uh-oh, you didn't override this in the child class")

    @abstractmethod
    def update(self):
        print("uh-oh, you didn't override this in the child class")

    @abstractmethod
    def render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def switch_to_next_scene(self, next_scene: "SceneBase"):
        self.next = next_scene
