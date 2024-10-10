from grh.celery import app

@app.task()
def somme(x, y):
    return x  + y