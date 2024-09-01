from os import getenv

from dotenv import load_dotenv
from flask import Flask, render_template
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database.query import (orm_get_photos)


load_dotenv()

app = Flask(__name__)
engine = create_async_engine(getenv('DB_PSQL'))
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@app.route('/<name>')
async def index(name):
    async with session_maker() as session:
        result = await orm_get_photos(session,name)
    if not result is None:
        return render_template(template_name_or_list="index.html",data=result)


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
