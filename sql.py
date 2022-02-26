import sqlite3
from sqlite3 import Error
from console import Console
from typing import Union

console = Console(True)

def create_connection(db_file):
    """Create a database connection to a SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect("./Data/"+db_file)
    except Error as e:
        console.error(e)
    finally:
        if conn:
            return conn

def add_server(server_id: int):
    """Add a server to the database."""
    if is_registered(server_id): return
    conn = create_connection("servers.db")
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO servers VALUES (?, ?)", (server_id, None))

def remove_server(server_id: int):
    """Remove a server from the database."""
    conn = create_connection("servers.db")
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM servers WHERE id = ?", (server_id,))

def edit_server(server_id: int, channel_id: int):
    """Edit a server in the database."""
    conn = create_connection("servers.db")
    with conn:
        cur = conn.cursor()
        cur.execute("UPDATE servers SET news_channel = ? WHERE id = ?", (channel_id, server_id))

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

def get_id(server_id: int) -> Union[int, None]:
    """Gets the news channel for a server, if it does not have one, return None."""
    conn = create_connection("servers.db")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT news_channel FROM servers WHERE id = ?", (server_id,))
        return cur.fetchone()[0]