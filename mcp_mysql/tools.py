"""FastMCP tools for MySQL schema retrieval."""
from typing import List, Dict, Any, Optional

from pydantic import BaseModel, Field

from .schema import (
    get_databases,
    get_tables,
    get_columns,
    get_indexes,
    get_foreign_keys,
    get_table_schema as get_table_schema_from_db,
)


class DatabaseInfo(BaseModel):
    """Database information model."""
    schema_name: str
    character_set: str
    collation: str

    @classmethod
    def from_db_row(cls, row: Dict[str, Any]) -> "DatabaseInfo":
        """Create a DatabaseInfo from a database row."""
        return cls(
            schema_name=row["SCHEMA_NAME"],
            character_set=row["DEFAULT_CHARACTER_SET_NAME"],
            collation=row["DEFAULT_COLLATION_NAME"],
        )


class TableInfo(BaseModel):
    """Table information model."""
    schema: str
    name: str
    engine: Optional[str] = None
    rows: Optional[int] = None
    avg_row_length: Optional[int] = None
    data_length: Optional[int] = None
    comment: Optional[str] = None
    create_time: Optional[str] = None
    update_time: Optional[str] = None

    @classmethod
    def from_db_row(cls, row: Dict[str, Any]) -> "TableInfo":
        """Create a TableInfo from a database row."""
        return cls(
            schema=row["TABLE_SCHEMA"],
            name=row["TABLE_NAME"],
            engine=row["ENGINE"],
            rows=row["TABLE_ROWS"],
            avg_row_length=row["AVG_ROW_LENGTH"],
            data_length=row["DATA_LENGTH"],
            comment=row["TABLE_COMMENT"],
            create_time=row["CREATE_TIME"].isoformat() if row["CREATE_TIME"] else None,
            update_time=row["UPDATE_TIME"].isoformat() if row["UPDATE_TIME"] else None,
        )


class ColumnInfo(BaseModel):
    """Column information model."""
    schema: str
    table: str
    name: str
    position: int
    default: Optional[str] = None
    is_nullable: str
    data_type: str
    max_length: Optional[int] = None
    numeric_precision: Optional[int] = None
    numeric_scale: Optional[int] = None
    column_type: str
    column_key: str
    extra: str
    comment: str

    @classmethod
    def from_db_row(cls, row: Dict[str, Any]) -> "ColumnInfo":
        """Create a ColumnInfo from a database row."""
        return cls(
            schema=row["TABLE_SCHEMA"],
            table=row["TABLE_NAME"],
            name=row["COLUMN_NAME"],
            position=row["ORDINAL_POSITION"],
            default=row["COLUMN_DEFAULT"],
            is_nullable=row["IS_NULLABLE"],
            data_type=row["DATA_TYPE"],
            max_length=row["CHARACTER_MAXIMUM_LENGTH"],
            numeric_precision=row["NUMERIC_PRECISION"],
            numeric_scale=row["NUMERIC_SCALE"],
            column_type=row["COLUMN_TYPE"],
            column_key=row["COLUMN_KEY"],
            extra=row["EXTRA"],
            comment=row["COLUMN_COMMENT"],
        )


class IndexInfo(BaseModel):
    """Index information model."""
    schema: str
    table: str
    name: str
    non_unique: int
    column_name: str
    seq_in_index: int
    collation: Optional[str] = None
    cardinality: Optional[int] = None
    index_type: str

    @classmethod
    def from_db_row(cls, row: Dict[str, Any]) -> "IndexInfo":
        """Create an IndexInfo from a database row."""
        return cls(
            schema=row["TABLE_SCHEMA"],
            table=row["TABLE_NAME"],
            name=row["INDEX_NAME"],
            non_unique=row["NON_UNIQUE"],
            column_name=row["COLUMN_NAME"],
            seq_in_index=row["SEQ_IN_INDEX"],
            collation=row["COLLATION"],
            cardinality=row["CARDINALITY"],
            index_type=row["INDEX_TYPE"],
        )


class ForeignKeyInfo(BaseModel):
    """Foreign key information model."""
    constraint_name: str
    schema: str
    table: str
    column: str
    referenced_schema: str
    referenced_table: str
    referenced_column: str
    update_rule: str
    delete_rule: str

    @classmethod
    def from_db_row(cls, row: Dict[str, Any]) -> "ForeignKeyInfo":
        """Create a ForeignKeyInfo from a database row."""
        return cls(
            constraint_name=row["CONSTRAINT_NAME"],
            schema=row["TABLE_SCHEMA"],
            table=row["TABLE_NAME"],
            column=row["COLUMN_NAME"],
            referenced_schema=row["REFERENCED_TABLE_SCHEMA"],
            referenced_table=row["REFERENCED_TABLE_NAME"],
            referenced_column=row["REFERENCED_COLUMN_NAME"],
            update_rule=row["UPDATE_RULE"],
            delete_rule=row["DELETE_RULE"],
        )


def list_databases() -> List[DatabaseInfo]:
    """List all databases in the MySQL server."""
    db_list = get_databases()
    return [DatabaseInfo.from_db_row(db) for db in db_list]


def list_tables(database: Optional[str] = Field(None, description="Database name")) -> List[TableInfo]:
    """List all tables in a database. If no database is provided, lists tables from all databases."""
    table_list = get_tables(database)
    return [TableInfo.from_db_row(table) for table in table_list]


def get_table_schema(
    tables: list[str] = Field(..., description="List of table names"),
    database: Optional[str] = Field(None, description="Database name"),
) -> Dict[str, "TableSchema"]:
    """Get the full schema for multiple tables."""
    schema_data = get_table_schema_from_db(tables, database)
    
    result = {}
    for table_name, data in schema_data.items():
        result[table_name] = TableSchema(
            columns=[ColumnInfo.from_db_row(col) for col in data["columns"]],
            indexes=[IndexInfo.from_db_row(idx) for idx in data["indexes"]],
            foreign_keys=[ForeignKeyInfo.from_db_row(fk) for fk in data["foreign_keys"]],
        )
    return result


def get_table_indexes(
    table: str = Field(..., description="Table name"),
    database: Optional[str] = Field(None, description="Database name"),
) -> List[IndexInfo]:
    """Get the indexes for a specific table."""
    indexes = get_indexes(table, database)
    return [IndexInfo.from_db_row(idx) for idx in indexes]


def get_table_foreign_keys(
    table: str = Field(..., description="Table name"),
    database: Optional[str] = Field(None, description="Database name"),
) -> List[ForeignKeyInfo]:
    """Get the foreign keys for a specific table."""
    foreign_keys = get_foreign_keys(table, database)
    return [ForeignKeyInfo.from_db_row(fk) for fk in foreign_keys]
