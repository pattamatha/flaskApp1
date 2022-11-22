from app import app

 
@app.route('/')
def home():
    return "Faii says 'hello world!'"
