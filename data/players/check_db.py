import sqlite3


conn = sqlite3.connect('player_data.db')
crsr = conn.cursor();
command = """
SELECT *
FROM players;
"""

for line in crsr.execute(command):
    print(line)

conn.close()
