import os
import aiosqlite

DB_PATH = os.path.join(os.getcwd(), "user_states.db")

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_state (
                tgid INTEGER PRIMARY KEY,
                state TEXT,
                xml TEXT,
                paid INTEGER DEFAULT 0,
                comment TEXT
            )
        """)
        await db.commit()

async def set_user_state(tgid, state=None, xml=None, paid=None, comment=None):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT tgid FROM user_state WHERE tgid=?", (tgid,))
        exists = await cur.fetchone()
        if exists:
            if state is not None:
                await db.execute("UPDATE user_state SET state=? WHERE tgid=?", (state, tgid))
            if xml is not None:
                await db.execute("UPDATE user_state SET xml=? WHERE tgid=?", (xml, tgid))
            if paid is not None:
                await db.execute("UPDATE user_state SET paid=? WHERE tgid=?", (int(paid), tgid))
            if comment is not None:
                await db.execute("UPDATE user_state SET comment=? WHERE tgid=?", (comment, tgid))
        else:
            await db.execute("INSERT INTO user_state (tgid, state, xml, paid, comment) VALUES (?, ?, ?, ?, ?)", (tgid, state or '', xml or '', int(paid) if paid is not None else 0, comment or ''))
        await db.commit()

async def get_user_state(tgid):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT state, xml, paid, comment FROM user_state WHERE tgid=?", (tgid,))
        row = await cur.fetchone()
        if row:
            return {"state": row[0], "xml": row[1], "paid": bool(row[2]), "comment": row[3]}
        return None
