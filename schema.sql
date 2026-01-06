CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    class TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_uid TEXT UNIQUE NOT NULL,
    location TEXT,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT CHECK(status IN ('Present','Absent')),
    source TEXT CHECK(source IN ('manual','device')),
    device_id INTEGER,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, date),
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(device_id) REFERENCES devices(id)
);
