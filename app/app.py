from main import app, db
from waitress import serve
from os import path
import main.tables
import main.routes
import main.requests

if __name__ == "__main__":
	with app.app_context():
		if not path.isfile("instance/database.sqlite3"):
			db.create_all()
	serve(app, host = "0.0.0.0", port = 5000)