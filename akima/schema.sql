DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS qna;
DROP TABLE IF EXISTS events;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE qna (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  event_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  event_name TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
