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


def get_columns(tables: list[str], database: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get columns for specific tables."""
    if not tables:
        return []
    
    params = {}
    placeholders = ", ".join([f"%(table_{i})s" for i in range(len(tables))])
    query = f"""
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
        TABLE_NAME IN ({placeholders})
    """
    
    for i, table in enumerate(tables):
        params[f"table_{i}"] = table
    
    if database:
        query += " AND TABLE_SCHEMA = %(database)s"
        params["database"] = database
        
    query += " ORDER BY TABLE_NAME, ORDINAL_POSITION"
    
    return execute_query(query, params)


def get_indexes(tables: list[str], database: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get indexes for specific tables."""
    if not tables:
        return []

    params = {}
    placeholders = ", ".join([f"%(table_{i})s" for i in range(len(tables))])
    query = f"""
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
        TABLE_NAME IN ({placeholders})
    """
    
    for i, table in enumerate(tables):
        params[f"table_{i}"] = table

    if database:
        query += " AND TABLE_SCHEMA = %(database)s"
        params["database"] = database
        
    query += " ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX"
    
    return execute_query(query, params)


def get_foreign_keys(tables: list[str], database: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get foreign keys for specific tables."""
    if not tables:
        return []

    params = {}
    placeholders = ", ".join([f"%(table_{i})s" for i in range(len(tables))])
    query = f"""
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
        kcu.TABLE_NAME IN ({placeholders})
        AND kcu.REFERENCED_TABLE_NAME IS NOT NULL
    """
    
    for i, table in enumerate(tables):
        params[f"table_{i}"] = table

    if database:
        query += " AND kcu.TABLE_SCHEMA = %(database)s"
        params["database"] = database
        
    query += " ORDER BY kcu.TABLE_NAME, kcu.CONSTRAINT_NAME"
    
    return execute_query(query, params)


def get_table_schema(tables: list[str], database: Optional[str] = None) -> Dict[str, Any]:
    """Get the full schema for multiple tables, including columns, indexes, and foreign keys."""
    columns = get_columns(tables, database)
    indexes = get_indexes(tables, database)
    foreign_keys = get_foreign_keys(tables, database)
    
    schema_by_table = {table: {"columns": [], "indexes": [], "foreign_keys": []} for table in tables}
    
    for col in columns:
        schema_by_table[col["TABLE_NAME"]]["columns"].append(col)
        
    for idx in indexes:
        schema_by_table[idx["TABLE_NAME"]]["indexes"].append(idx)
        
    for fk in foreign_keys:
        schema_by_table[fk["TABLE_NAME"]]["foreign_keys"].append(fk)
        
    return schema_by_table
