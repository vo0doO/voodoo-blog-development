CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  publication_time TIME NOTNULL,
  digest CHAR
(32) NOT NULL
);

CREATE TABLE titles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  txt VARCHAR NOT NULL,
  post_id INTEGER,
  FOREIGN KEY post_id REFERENCES posts.id
);

CREATE TABLE texts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  txt_en VARCHAR,
  txt_ru VARCHAR,
  post_id INTEGER NOT NULL
  FOREIGN KEY post_id REFERENCES posts.id
);

CREATE TABLE urls (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_url VARCHAR,
  author_post_url VARCHAR,
  images_url VARCHAR,
  videos_url VARCHAR,
  recomendation_url VARCHAR,
  vk_url VARCHAR,
  twitt_url VARCHAR,
  fb_url VARCHAR,
  ok_url VARCHAR,
  post_id INTEGER NOT NULL
  FOREIGN KEY post_id REFERENCES posts.id
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag VARCHAR UNIQUE,
    FOREIGN KEY post_id REFERENCES posts.id
)
CREATE UNIQUE INDEX idx_digest ON posts(digest);
CREATE INDEX idx_title_id ON titles (post_id);
CREATE INDEX idx_texts ON texts(id);
CREATE UNIQUE INDEX idx_tags ON tags (id);