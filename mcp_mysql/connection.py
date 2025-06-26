"""MySQL database connection module for MCP server."""
import os
from typing import Dict, Any, Optional

import mysql.connector
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class MySQLConfig(BaseModel):
    """MySQL connection configuration."""
    host: str = os.getenv("MYSQL_HOST", "localhost")
    port: int = int(os.getenv("MYSQL_PORT", "3306"))
    user: str = os.getenv("MYSQL_USER", "root")
    password: str = os.getenv("MYSQL_PASSWORD", "")
    database: str = os.getenv("MYSQL_DATABASE", "information_schema")


def get_connection():
    """Get a MySQL database connection based on environment variables."""
    config = MySQLConfig()
    try:
        conn = mysql.connector.connect(
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.password,
            database=config.database,
        )
        return conn
    except mysql.connector.Error as err:
        raise ConnectionError(f"Failed to connect to MySQL: {err}")


def execute_query(query: str, params: Optional[Dict[str, Any]] = None):
    """Execute a query and return the result as a list of dictionaries."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or {})
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        raise Exception(f"Query execution failed: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
