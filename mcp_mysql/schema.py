"""Schema retrieval functions for MySQL databases."""
from typing import List, Dict, Any, Optional

from .connection import execute_query


def get_databases() -> List[Dict[str, Any]]:
    """Get a list of all databases (schemas)."""
    query = """
    SELECT
        SCHEMA_NAME,
        DEFAULT_CHARACTER_SET_NAME,
        DEFAULT_COLLATION_NAME
    FROM
        INFORMATION_SCHEMA.SCHEMATA
    ORDER BY
        SCHEMA_NAME
    """
    return execute_query(query)


def get_tables(database: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get a list of all tables in a database."""
    params = {}
    query = """
    SELECT
        TABLE_SCHEMA,
        TABLE_NAME,
        ENGINE,
        TABLE_ROWS,
        AVG_ROW_LENGTH,
        DATA_LENGTH,
        TABLE_COMMENT,
        CREATE_TIME,
        UPDATE_TIME
    FROM
        INFORMATION_SCHEMA.TABLES
    """
    
    if database:
        query += " WHERE TABLE_SCHEMA = %(database)s"
        params["database"] = database
        
    query += " ORDER BY TABLE_SCHEMA, TABLE_NAME"
    
    return execute_query(query, params)


def get_columns(table: str, database: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get columns for a specific table."""
    params = {"table": table}
    query = """
    SELECT
        TABLE_SCHEMA,
        TABLE_NAME,
        COLUMN_NAME,
        ORDINAL_POSITION,
        COLUMN_DEFAULT,
        IS_NULLABLE,
        DATA_TYPE,
        CHARACTER_MAXIMUM_LENGTH,
        NUMERIC_PRECISION,
        NUMERIC_SCALE,
        COLUMN_TYPE,
        COLUMN_KEY,
        EXTRA,
        COLUMN_COMMENT
    FROM
        INFORMATION_SCHEMA.COLUMNS
    WHERE
        TABLE_NAME = %(table)s
    """
    
    if database:
        query += " AND TABLE_SCHEMA = %(database)s"
        params["database"] = database
        
    query += " ORDER BY ORDINAL_POSITION"
    
    return execute_query(query, params)


def get_indexes(table: str, database: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get indexes for a specific table."""
    params = {"table": table}
    query = """
    SELECT
        TABLE_SCHEMA,
        TABLE_NAME,
        INDEX_NAME,
        NON_UNIQUE,
        COLUMN_NAME,
        SEQ_IN_INDEX,
        COLLATION,
        CARDINALITY,
        INDEX_TYPE
    FROM
        INFORMATION_SCHEMA.STATISTICS
    WHERE
        TABLE_NAME = %(table)s
    """
    
    if database:
        query += " AND TABLE_SCHEMA = %(database)s"
        params["database"] = database
        
    query += " ORDER BY INDEX_NAME, SEQ_IN_INDEX"
    
    return execute_query(query, params)


def get_foreign_keys(table: str, database: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get foreign keys for a specific table."""
    params = {"table": table}
    query = """
    SELECT
        kcu.CONSTRAINT_NAME,
        kcu.TABLE_SCHEMA,
        kcu.TABLE_NAME,
        kcu.COLUMN_NAME,
        kcu.REFERENCED_TABLE_SCHEMA,
        kcu.REFERENCED_TABLE_NAME,
        kcu.REFERENCED_COLUMN_NAME,
        rc.UPDATE_RULE,
        rc.DELETE_RULE
    FROM
        INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
    JOIN
        INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc
    ON
        kcu.CONSTRAINT_NAME = rc.CONSTRAINT_NAME AND
        kcu.TABLE_SCHEMA = rc.CONSTRAINT_SCHEMA
    WHERE
        kcu.TABLE_NAME = %(table)s
        AND kcu.REFERENCED_TABLE_NAME IS NOT NULL
    """
    
    if database:
        query += " AND kcu.TABLE_SCHEMA = %(database)s"
        params["database"] = database
        
    query += " ORDER BY kcu.CONSTRAINT_NAME"
    
    return execute_query(query, params)
