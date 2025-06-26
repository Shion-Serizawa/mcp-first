"""
MySQL MCP Server
---------------
A FastMCP server for retrieving MySQL database schema information.

This server provides tools to retrieve:
- Database list
- Table list
- Table schema (columns)
- Table indexes
- Table foreign keys
"""
import os
from typing import Optional

from dotenv import load_dotenv
from fastmcp import FastMCP

from mcp_mysql.tools import (
    list_databases,
    list_tables,
    get_table_schema,
    get_table_indexes,
    get_table_foreign_keys,
)

load_dotenv()

mcp = FastMCP(
    "MySQL Schema MCP",
    description="A Metadata Change Proposal (MCP) server for retrieving MySQL schema information",
    dependencies=["mysql-connector-python", "python-dotenv", "pydantic", "fastmcp"],
)


@mcp.tool()
def databases():
    """List all databases in the MySQL server."""
    return list_databases()


@mcp.tool()
def tables(database: Optional[str] = None):
    """List all tables in a database. If no database is provided, lists tables from all databases."""
    return list_tables(database)


@mcp.tool()
def schema(tables: list[str], database: Optional[str] = None):
    """Get the schema (columns, indexes, foreign keys) for one or more tables."""
    return get_table_schema(tables, database)


@mcp.tool()
def indexes(table: str, database: Optional[str] = None):
    """Get the indexes for a specific table."""
    return get_table_indexes(table, database)


@mcp.tool()
def foreign_keys(table: str, database: Optional[str] = None):
    """Get the foreign keys for a specific table."""
    return get_table_foreign_keys(table, database)


if __name__ == "__main__":
    mcp.run()
