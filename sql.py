import sqlite3
from sqlite3 import Error
from console import Console
from typing import Union
from os.path import exists

console = Console(True)

def create_connection(db_file):
    """Create a database connection to a SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect("./data/"+db_file)
    except Error as e:
        console.error(e)
    finally:
        if conn:
            return conn

def db_check():
    """Check if the database exists, if not, create it. Also checks for the servers.db file to see if it needs updating."""
    conn = create_connection("servers.db")
    if not exists("./data/servers.db"):
        
        with conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE servers (id BIGINT PRIMARY KEY NOT NULL, news_channel BIGINT, role_id BIGINT)")
        console.info("Database created.")

    # Check if the role_id column exists, if not, add it.
    with conn:
        cur = conn.cursor()
        try: cur.execute("SELECT role_id FROM servers")
        except: pass
        if cur.fetchone() is None:
            try:
                cur.execute("ALTER TABLE servers ADD COLUMN role_id BIGINT")
                console.info("Added role_id column to servers table.")
            except sqlite3.OperationalError:
                console.error("Could not add role_id column to servers table.")


def add_server(server_id: int):
    """Add a server to the database."""
    if is_registered(server_id): return
    conn = create_connection("servers.db")
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO servers VALUES (?, ?, ?)", (server_id, None, None))

def remove_server(server_id: int):
    """Remove a server from the database."""
    conn = create_connection("servers.db")
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM servers WHERE id = ?", (str(server_id),))

def edit_server(server_id: int, channel_id: int = None, role_id: int = None):
    """Edit a server in the database."""
    conn = create_connection("servers.db")
    with conn:
        cur = conn.cursor()
        if channel_id is not None:
            cur.execute("UPDATE servers SET news_channel = ? WHERE id = ?", (channel_id, server_id))
        if role_id is not None:
            cur.execute("UPDATE servers SET role_id = ? WHERE id = ?", (role_id, server_id))
        else:
            cur.execute("UPDATE servers SET role_id = NULL WHERE id = ?", (server_id,))

def is_registered(server_id: int) -> bool:
    """Check if a server is registered."""
    conn = create_connection("servers.db")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM servers WHERE id = ?", (server_id,))
        if cur.fetchone() is None:
            return False
        else:
            return True

def get_server_id(server_id: int) -> Union[int, None]:
    """Gets the news channel for a server, if it does not have one, return None."""
    conn = create_connection("servers.db")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT news_channel FROM servers WHERE id = ?", (server_id,))
        out = cur.fetchone()
        if out is None:
            return None
        else:
            return out[0]

def get_role_id(server_id: int) -> Union[int, None]:
    """Gets the role_id for a server, if it does not have one, return None."""
    conn = create_connection("servers.db")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT role_id FROM servers WHERE id = ?", (server_id,))
        out = cur.fetchone()
        if out is None:
            return None
        else:
            return out[0]

def get_guilds() -> list:
    """Get all the guilds in the database."""
    conn = create_connection("servers.db")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM servers")
        return cur.fetchall()
