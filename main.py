import logging

import psycopg2
from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv

load_dotenv()


API_TOKEN = "6418194041:AAGbuqweQTcEcgcW1793DttIOLCkYPB7gtw"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

class Pg:
    con = psycopg2.connect(
        dbname=os.getenv("DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        host=os.getenv("DB_HOST")
    )
    cur = con.cursor()
    query = """
        create table if not exists messanger_user(
            id serial primary key ,
            user_id bigint ,
            first_name varchar(255),
            username varchar(255)
        )
    """
    cur.execute(query)
    con.commit()

    def add(self, user_id, first_name, username):
        query = """
        insert into messanger_user (user_id, first_name , username) values (%s , %s , %s)
        """
        params = (user_id, first_name, username)
        self.cur.execute(query, params)
        self.con.commit()




@dp.message_handler(commands='start')
async def cats(message: types.Message):
    Pg().add(message.from_user.id, message.from_user.first_name, message.from_user.username)
    await message.answer("Welcome")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)