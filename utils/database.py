import sqlite3
from dataclasses import dataclass
from datetime import datetime

from argon2 import PasswordHasher, exceptions

ph = PasswordHasher()


@dataclass
class User:
    id: int
    username: str
    password_hash: str
    signed_up_at: datetime

    def is_password(self, potential_password: str) -> bool:
        try:
            ph.verify(self.password_hash, potential_password)
        except exceptions.VerifyMismatchError:
            return False
        return True


@dataclass
class Puzzle:
    id: int
    puzzle_json: str
    user_id: int


@dataclass
class Answer:
    word: str


@dataclass
class PuzzleAnswer:
    puzzle_id: int
    answer: str
    calculated_at: datetime | None
    found_at: datetime | None


class Database:
    def __init__(self, folder: str):
        self.dir = folder
        self.db_dir = self.dir.rstrip("/") + "/database.db"
        self.__create_databases()

    def __create_databases(self) -> None:
        sql = """
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            signed_up_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS puzzles(
            puzzle_id INTEGER PRIMARY KEY,
            puzzle_json TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS answers(
            word TEXT PRIMARY KEY
        );

        CREATE TABLE IF NOT EXISTS puzzle_answers (
            puzzle_id INTEGER NOT NULL,
            answer TEXT NOT NULL,
            calculated_at TEXT DEFAULT NULL,
            found_at TEXT DEFAULT NULL,
            PRIMARY KEY (puzzle_id, answer),
            FOREIGN KEY (puzzle_id) REFERENCES puzzles(puzzle_id),
            FOREIGN KEY (answer) REFERENCES answers(word)
        );
        """

        with sqlite3.connect(self.db_dir) as conn:
            conn.executescript(sql)

    def add_user(self, username: str, password: str, signed_up_at: datetime) -> User:
        password_hash = ph.hash(password)
        with sqlite3.connect(self.db_dir) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password_hash, signed_up_at) VALUES (?, ?, ?)",
                (username, password_hash, signed_up_at.isoformat()),
            )
            user_id = cur.lastrowid
            return User(
                id=user_id,
                username=username,
                password_hash=password_hash,
                signed_up_at=signed_up_at,
            )

    def get_user(self, user_id: int) -> User | None:
        with sqlite3.connect(self.db_dir) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT user_id, username, password_hash, signed_up_at FROM users WHERE user_id = ?",
                (user_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            signed_up_at = datetime.fromisoformat(row[3])
            return User(
                id=row[0],
                username=row[1],
                password_hash=row[2],
                signed_up_at=signed_up_at,
            )

    def add_puzzle(self, json: str, user_id: int) -> Puzzle:
        with sqlite3.connect(self.db_dir) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO puzzles (puzzle_json, user_id) VALUES (?, ?)",
                (json, user_id),
            )
            puzzle_id = cur.lastrowid
            return Puzzle(id=puzzle_id, puzzle_json=json, user_id=user_id)

    def get_puzzle(self, puzzle_id: int) -> Puzzle | None:
        with sqlite3.connect(self.db_dir) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT puzzle_id, puzzle_json, user_id FROM puzzles WHERE puzzle_id = ?",
                (puzzle_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            return Puzzle(id=row[0], puzzle_json=row[1], user_id=row[2])

    def get_user_puzzles(self, user_id: int) -> list[Puzzle]:
        with sqlite3.connect(self.db_dir) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT puzzle_id, puzzle_json, user_id FROM puzzles WHERE user_id = ?",
                (user_id,),
            )
            rows = cur.fetchall()
            return [Puzzle(id=r[0], puzzle_json=r[1], user_id=r[2]) for r in rows]

    def add_puzzle_answer(
        self,
        puzzle_id: int,
        answer: str,
        calculated_at: datetime | None,
        found_at: datetime | None,
    ) -> PuzzleAnswer:
        with sqlite3.connect(self.db_dir) as conn:
            cur = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO answers (word) VALUES (?)", (answer,))
            cur.execute(
                "INSERT OR REPLACE INTO puzzle_answers (puzzle_id, answer, calculated_at, found_at) VALUES (?, ?, ?, ?)",
                (
                    puzzle_id,
                    answer,
                    calculated_at.isoformat() if calculated_at is not None else None,
                    found_at.isoformat() if found_at is not None else None,
                ),
            )
            return PuzzleAnswer(
                puzzle_id=puzzle_id,
                answer=answer,
                calculated_at=calculated_at,
                found_at=found_at,
            )

    def get_puzzle_answers(self, puzzle_id: int) -> list[PuzzleAnswer]:
        with sqlite3.connect(self.db_dir) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT puzzle_id, answer, calculated_at, found_at FROM puzzle_answers WHERE puzzle_id = ?",
                (puzzle_id,),
            )
            rows = cur.fetchall()
            results: list[PuzzleAnswer] = []
            for r in rows:
                calculated = datetime.fromisoformat(r[2]) if r[2] is not None else None
                found = datetime.fromisoformat(r[3]) if r[3] is not None else None
                results.append(
                    PuzzleAnswer(
                        puzzle_id=r[0],
                        answer=r[1],
                        calculated_at=calculated,
                        found_at=found,
                    )
                )
            return results

    def get_points(self, user_id: int) -> int:
        puzzles = self.get_user_puzzles(user_id)

        points = 0

        for puzzle in puzzles:
            answers = self.get_puzzle_answers(puzzle.id)
            for answer in answers:
                if answer.found_at is not None:
                    points += len(answer.answer)

        return points


database = Database("resources")

print(database.get_user(1).is_password("alighali"))
