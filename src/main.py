from fastapi import FastAPI

def create_app():
    app = FastAPI(
        debug=True,
        docs_url="/api/docs/",
        title="Banking App"
    )

    return app

