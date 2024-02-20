import sqlite3

conn = sqlite3.connect('db_data.db')
cur = conn.cursor()

# create t_papercatelog
sql = """
CREATE TABLE IF NOT EXISTS t_papercatelog (
    id INTEGER PRIMARY KEY,
    sortedId INTEGER,
    catelogName TEXT NOT NULL UNIQUE,
    catelogDesc TEXT
);
"""
cur.execute(sql)

# create t_paper
sql = """
CREATE TABLE IF NOT EXISTS t_paper (
    id INTEGER PRIMARY KEY,
    paperName TEXT NOT NULL,
    paperCatelogId INTEGER NOT NULL,
    folderPath TEXT,
    fileName TEXT,
    title TEXT,
    author TEXT,
    abstract TEXT,
    text TEXT,
    journal TEXT,
    issue TEXT,
    volume TEXT,
    page TEXT,
    date TEXT,
    url TEXT,
    doi TEXT,
    issn TEXT,
    isReferencedByCount TEXT,
    FOREIGN KEY(paperCatelogId) REFERENCES t_papercatelog(id)
);
"""
cur.execute(sql)

# create t_api
sql = """
CREATE TABLE IF NOT EXISTS t_api (
    id INTEGER PRIMARY KEY,
    platform TEXT NOT NULL UNIQUE,
    key TEXT,
    host TEXT,
    selected INTEGER
);
"""
cur.execute(sql)

# create t_model
sql = """
CREATE TABLE IF NOT EXISTS t_model (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    apiId INTEGER,
    selected INTEGER,
    FOREIGN KEY(apiId) REFERENCES t_api(id)
);
"""
cur.execute(sql)

# create t_prompt
sql = """
CREATE TABLE IF NOT EXISTS t_prompt (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    text TEXT,
    selected INTEGER
);
"""
cur.execute(sql)


conn.commit()
conn.close()