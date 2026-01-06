import sqlite3


class Database:
    def __init__(self, folder: str):
        self.dir = folder

    def __create_databases(self):
        with sqlite3.connect(self.dir + "/" + "database.db") as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS users(
                    user_id INTEGER PRIMARY KEY,
                    username STRING UNIQUE NOT NULL,
                    password_hash STRING NOT NULL,
                    signed_up_at DATETIME NOT NULL
                )
                    
                CREATE TABLE IF NOT EXISTS puzzles(
                    puzzle_id INTEGER PRIMARY KEY,
                    puzzle_json STRING NOT NULL,
                    user_id INTEGER NOT NULL
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
                    
                CREATE TABLE IF NOT EXISTS answers(
                    word STRING PRIMARY KEY
                )
                    
                CREATE TABLE IF NOT EXISTS puzzle_answers (
                    puzzle_id INTEGER NOT NULL,
                    answer TEXT NOT NULL,
                    calculated_at DATETIME DEFAULT NULL,
                    found_at DATETIME DEFAULT NULL,
                    PRIMARY KEY (puzzle_id, answer),
                    FOREIGN KEY (puzzle_id) REFERENCES puzzles(puzzle_id),
                    FOREIGN KEY (answer) REFERENCES answers(word)
                );
                """
            )
