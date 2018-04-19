from app import app

# def init_db():
#     db.init_app(app)
#     db.app = app
#     # db.drop_all()
#     db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
