import sqlite3

conn = sqlite3.connect("journal.db")
cursor = conn.cursor()

# Fetch everything inside the user_profile table
cursor.execute("SELECT * FROM user_profile")
rows = cursor.fetchall()

print("\n" + "="*30)
print("CURRENT SQLITE DATABASE VALUES:")
print("="*30)

for row in rows:
    print(f" Key: {row[0]:<15} | Value: {row[1]}")

print("="*30 + "\n")
conn.close()