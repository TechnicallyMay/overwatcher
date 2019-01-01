import sqlite3


conn = sqlite3.connect('player_data.db')
crsr = conn.cursor();
command = """
SELECT *
FROM players
"""

crsr.execute(command)
print(crsr.fetchall())
# for line in crsr.execute(command):
#     print(line[0])

conn.close()
