"""Main implementation."""
import uvicorn
from fastapi import FastAPI

app = FastAPI()


# todo: configure CORS

@app.get('/api/v1/hello')
def read_root():
    return {'Hello': 'World'}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8007)
