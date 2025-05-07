# MySQL Schema MCP Server

A Metadata Change Proposal (MCP) server for retrieving MySQL database schema information using the [FastMCP](https://github.com/jlowin/fastmcp) framework.

## Features

- Retrieve database list
- Retrieve table list from databases
- Get table schema (columns) information
- Get table indexes information
- Get table foreign key information

## Setup

### Local Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example` with your MySQL connection details:
   ```
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=information_schema
   ```

### Docker Setup

1. Clone this repository
2. Make sure Docker and Docker Compose are installed on your system
3. Run the server with MySQL using Docker Compose:
   ```
   docker-compose up
   ```
   
   This will:
   - Build the MCP server Docker image
   - Start a MySQL container
   - Connect the MCP server to the MySQL container
   - Expose the MCP server on port 8000

4. Optionally, you can set environment variables before running Docker Compose:
   ```
   MYSQL_USER=custom_user MYSQL_PASSWORD=custom_password MYSQL_DATABASE=custom_db docker-compose up
   ```

## Usage

### Local Usage

Start the server:
```
python main.py
```

### Docker Usage

Start the server with MySQL:
```
docker-compose up
```

Start in detached mode:
```
docker-compose up -d
```

Stop the containers:
```
docker-compose down
```

### Available Tools

The server provides the following tools:
- `databases`: List all databases
- `tables`: List all tables in a database
- `schema`: Get the schema (columns) for a specific table
- `indexes`: Get the indexes for a specific table
- `foreign_keys`: Get the foreign keys for a specific table

## Example

```python
from fastmcp.client import Client

# Connect to the MCP server
client = Client("http://localhost:8000")

# List all databases
databases = client.databases()

# List tables in a specific database
tables = client.tables(database="your_database")

# Get schema for a specific table
schema = client.schema(table="your_table", database="your_database")

# Get indexes for a specific table
indexes = client.indexes(table="your_table", database="your_database")

# Get foreign keys for a specific table
foreign_keys = client.foreign_keys(table="your_table", database="your_database")
```
