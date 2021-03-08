from app import created_app
app = created_app(config='config')
app.run(host='127.0.0.1')