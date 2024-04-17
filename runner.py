from src import create_app
from src.database import db

if __name__=="__main__":
    application = create_app(None)
    application.run()