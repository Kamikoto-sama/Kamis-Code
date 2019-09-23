from sqlite3 import connect

class SQLTerminal:
    def __init__(self, db_name):
            db = connect(db_name)
            self.query = db.cursor().execute
            self.commit = db.commit

            self.cursor = "List"
            self.out = "list"

    def init(self):
        while True:
            try:
                query = input(self.cursor + "=> ")
                commands = query.split()
                if commands[0] in ("exit", "q"):
                    break
                if len(commands) == 0:
                    continue
                if commands[0][0] == "+":
                    self.commit()
                    continue

                response = self.get_response(query)
                if commands[0].lower() == "select":
                    self.output(response)
            except Exception as e:
                print(e)

    def get_response(self, query):
            response = self.query(query)
            return response

    def output(self, response):
        if self.out == "list":
            print(list(response))

if __name__ == "__main__":
	db_name = input("Db name: ")
	SQLTerminal(":memory:" if len(db_name) == 0 else db_name).init()