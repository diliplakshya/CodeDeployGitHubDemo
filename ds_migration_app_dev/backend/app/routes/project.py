from backend.app import app

@app.route('/api/projects')
def projects():
    return "Welcome to Projects"



