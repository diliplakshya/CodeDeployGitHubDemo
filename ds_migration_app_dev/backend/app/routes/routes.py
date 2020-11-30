from backend.app import app

@app.route('/api')
def home():
    return "Welcome to DataStax"
