import glob
import os

import aiomysql

async def getMySqlPool():
    return await aiomysql.create_pool(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DATABASE"),
        autocommit=True
    )

async def createTableIfNeccessary(pool):
    workDirectory = os.getcwd()
    print(f"현재 작업 디렉토리: {workDirectory}")
    pass


    # async with pool.acquire() as conn:
    #     async with conn.cursor() as cursor:
    #         for filePath in sqlFileList:
    #             with open(filePath, 'r') as file:
    #                 sql = file.read()
    #                 print(f"Executing SQL from {filePath}")
    #                 await cursor.execute(sql)   
            
    #         await conn.commit()