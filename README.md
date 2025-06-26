# MySQL Schema MCP Server

A Metadata Change Proposal (MCP) server for retrieving MySQL database schema information using the [FastMCP](https://github.com/jlowin/fastmcp) framework.

## Features

- Retrieve database list
- Retrieve table list from databases
- Get table schema (columns) information
- Get table indexes information
- Get table foreign key information

## Setup

### Local Setup with uv

1. Clone this repository
2. Install [uv](https://github.com/astral-sh/uv) if you don't have it already:
   ```bash
   pip install uv
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example` with your MySQL connection details:
   ```
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=information_schema
   ```

### Local Setup with pip

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

#### Building and Running the Docker Image

1. Clone this repository
2. Build the Docker image:
   ```
   docker build -t mysql-mcp-server .
   ```
3. Run the Docker container with environment variables for MySQL connection:
   ```
   docker run -p 8000:8000 \
     -e MYSQL_HOST=host.docker.internal \
     -e MYSQL_PORT=3306 \
     -e MYSQL_USER=your_username \
     -e MYSQL_PASSWORD=your_password \
     -e MYSQL_DATABASE=information_schema \
     mysql-mcp-server
   ```

   Note: `host.docker.internal` is used to connect to the MySQL instance running on your host machine from inside the Docker container.

4. For Mac and Windows, `host.docker.internal` resolves to the host machine. For Linux, you may need to use:
   ```
   docker run -p 8000:8000 \
     --add-host=host.docker.internal:host-gateway \
     -e MYSQL_HOST=host.docker.internal \
     -e MYSQL_USER=your_username \
     -e MYSQL_PASSWORD=your_password \
     mysql-mcp-server
   ```

## Usage

### Local Usage

Start the server:
```
python main.py
```

### Docker Usage

Run the Docker container (as shown in the setup section):
```
docker run -p 8000:8000 \
  -e MYSQL_HOST=host.docker.internal \
  -e MYSQL_USER=your_username \
  -e MYSQL_PASSWORD=your_password \
  mysql-mcp-server
```

You can also create a `.env` file and mount it to the container:
```
docker run -p 8000:8000 \
  -v $(pwd)/.env:/app/.env \
  mysql-mcp-server
```

### MCP JSON Configuration

To use this MCP server with MCP-compatible clients, you'll need to configure the client with the appropriate JSON configuration. Here are examples for both local and Docker setups:

#### Local MCP Configuration

```json
{
  "mcpServers": {
    "mysql-schema": {
      "command": "python",
      "args": [
        "main.py"
      ],
      "cwd": "/path/to/mcp-first",
      "alwaysAllow": [
        "databases",
        "tables",
        "schema",
        "indexes",
        "foreign_keys"
      ]
    }
  }
}
```

#### Docker MCP Configuration

```json
{
  "mcpServers": {
    "mysql-schema": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "MYSQL_HOST=host.docker.internal",
        "-e",
        "MYSQL_USER=your_username",
        "-e",
        "MYSQL_PASSWORD=your_password",
        "mysql-mcp-server"
      ],
      "alwaysAllow": [
        "databases",
        "tables",
        "schema",
        "indexes",
        "foreign_keys"
      ]
    }
  }
}
```

### Available Tools

The server provides the following tools:
- `databases`: List all databases
- `tables`: List all tables in a database
- `schema`: Get the schema (columns, indexes, and foreign keys) for one or more tables.

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
schema = client.schema(tables=["your_table"], database="your_database")

# Get schema for multiple tables
schemas = client.schema(tables=["table1", "table2"], database="your_database")

# Get indexes for a specific table
indexes = client.indexes(table="your_table", database="your_database")

# Get foreign keys for a specific table
foreign_keys = client.foreign_keys(table="your_table", database="your_database")
```
