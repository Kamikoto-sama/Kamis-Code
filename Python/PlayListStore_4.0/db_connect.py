import sqlite3

db = sqlite3.connect('data.pls')
sql = db.cursor().execute

def run():
    try:
        while True:
            query = input(">>> ").lower()
            if query == "0":
                db.close()
                return
            elif query == "commit":
                db.commit()
                continue
            answer = list(sql(query))
            if "select" in query or "pragma" in query:
                for row in answer:
                    print(row)
    except Exception as e:
        print(e)
        run()

if __name__ == "__main__":
    run()