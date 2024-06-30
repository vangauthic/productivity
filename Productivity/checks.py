import aiosqlite

async def check_tables():
    # Database
    async with aiosqlite.connect('database.db') as db:
        # Creates the "teamsToDo" table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS teamsToDo (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            role STRING,
            roleID INT,
            title STRING,
            description STRING
        )
        """)

        # Creates the "urgentToDo" table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS urgentToDo (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            role STRING,
            roleID INT,
            title STRING,
            description STRING
        )
        """)
        await db.commit()