from backend.app import app


@app.route('/api/collections')
def collections():
    return "Related Collection"




