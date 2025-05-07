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
