CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    date DATE NOT NULL,
    category TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE history (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    amount REAL,
    expense_date DATE NOT NULL,
    UNIQUE (expense_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

ALTER TABLE table_name
ADD COLUMN column_name column_definition;

ALTER TABLE history
ADD COLUMN description TEXT NOT NULL;