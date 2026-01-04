import json
import os


class Trie:
    def __init__(self, path: str = "media/trie.json"):
        self.path = path
        self.dictionary: dict = self.load_json()

    def load_json(self) -> dict:
        """Load the trie dictionary from a JSON file."""
        if not os.path.exists(self.path):
            return {}  # start with empty trie if file doesn't exist

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except (json.JSONDecodeError, OSError):
            pass

        return {}

    def save_json(self):
        """Save the trie dictionary to a JSON file."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.dictionary, f, indent=2)

    def _format_word(self, word: str) -> str:
        return word.strip().upper()

    def _insert(self, word: str) -> bool:
        word = self._format_word(word)
        if not word:
            return

        changed = False
        node = self.dictionary

        for letter in word:
            if letter not in node:
                node[letter] = {}
                changed = True
            node = node[letter]

        # mark the end of the word
        if "end" not in node:
            node["end"] = True
            changed = True

        return changed

    def insert(self, word: str):
        changed = self._insert(word)

        if changed:
            self.save_json()

    def bulk_insert(self, words: list[str]):
        for word in words:
            self._insert(word)

        self.save_json()

    def is_prefix(self, word: str) -> bool:
        """Check if a word is a prefix to a real word."""
        word = self._format_word(word)
        if not word:
            return False

        node = self.dictionary

        for letter in word:
            if letter not in node:
                return False
            node = node[letter]

        return True

    def search(self, word: str) -> bool:
        word = self._format_word(word)
        if not word:
            return False

        node = self.dictionary

        for letter in word:
            if letter not in node:
                return False
            node = node[letter]

        return "end" in node


trie = Trie()

with open("media/words.tsv", "r") as f:
    words = []
    for i, row in enumerate(f.readlines()):
        if i != 0:
            splitted = row.split("\t")
            if len(splitted) == 4:
                word = splitted[1]
                if len(word) > 3:
                    if all(
                        char.lower() in "abcdefghijklmnopqrstuvwxyz" for char in word
                    ):
                        words.append(word)

trie.bulk_insert(words)
