# MCPサーバー改善計画：複数テーブルのスキーマ一括取得

## 1. 目的

`main.py`で定義されている`schema`ツールを改善し、単一のAPIコールで複数のテーブルのスキーマ情報を効率的に取得できるようにする。

## 2. 背景

現在の`schema`ツールは、引数として単一のテーブル名 (`table: str`) を受け取る設計になっている。そのため、複数のテーブルのスキーマを取得したい場合、テーブルごとにツールを呼び出す必要があり、非効率である。

この計画では、`schema`ツールがテーブル名のリストを受け付けられるように変更し、バックエンドのデータ取得処理もそれに合わせて最適化する。

## 3. 提案する変更計画

主要な変更は、`main.py`のインターフェース部分、`mcp_mysql/tools.py`のビジネスロジック、そして`mcp_mysql/schema.py`のデータアクセス部分にまたがる。

### 3.1. `main.py` の変更

- **`schema`関数のシグネチャ変更**:
  - 現在: `def schema(table: str, database: Optional[str] = None):`
  - 変更後: `def schema(tables: list[str], database: Optional[str] = None):`
- **docstringの更新**:
  - 引数が単一のテーブルからテーブル名のリストに変更されたことを反映させる。
- **関数の実装変更**:
  - 変更後の`mcp_mysql.tools.get_table_schema`関数を、新しい`tables`引数で呼び出すように修正する。

### 3.2. `mcp_mysql/tools.py` の変更

- **`get_table_schema`関数の変更**:
  - この関数が、`mcp_mysql/schema.py`内の新しい複数テーブル対応版の関数を呼び出すようにロジックを修正する。
  - 現在: `def get_table_schema(table: str, ...)`
  - 変更後: `def get_table_schema(tables: list[str], ...)`
  - 内部で`schema.py`の`get_table_schema`を呼び出し、結果をそのまま返す。

### 3.3. `mcp_mysql/schema.py` の変更 (中心的な作業)

パフォーマンスを維持するため、テーブルごとにクエリを発行するのではなく、`IN`句を使って一度のクエリで全テーブルの情報を取得する。

- **`get_columns`, `get_indexes`, `get_foreign_keys` 関数の修正**:
  - 3つの関数すべてで、引数を `table: str` から `tables: list[str]` に変更する。
  - SQLクエリの`WHERE`句を `WHERE TABLE_NAME = %(table)s` から `WHERE TABLE_NAME IN (...)` に変更する。
    - `mysql-connector-python`では`IN`句のプレースホルダ展開が直接サポートされていないため、動的にプレースホルダ (`%s`) を生成する必要がある。
    - 例: `placeholders = ', '.join(['%s'] * len(tables))`
    - SQLインジェクションを避けるため、パラメータは適切に渡す。
- **`get_table_schema` 関数の修正**:
  - 引数を `table: str` から `tables: list[str]` に変更する。
  - 変更された`get_columns`, `get_indexes`, `get_foreign_keys`を`tables`リストで呼び出す。
  - 各関数から返されるのは、指定された全テーブルの情報が混在した単一のリストになる。
  - このリストを、テーブル名をキーとする辞書に再構成する。これにより、APIの応答がテーブルごとに整理される。
  - 期待される戻り値の構造:
    ```json
    {
      "table1_name": {
        "columns": [...],
        "indexes": [...],
        "foreign_keys": [...]
      },
      "table2_name": {
        "columns": [...],
        "indexes": [...],
        "foreign_keys": [...]
      }
    }
    ```

### 3.4. `README.md` のドキュメント更新

- `schema`ツールの使い方に関するセクションを更新する。
- 新しい使用方法として、複数のテーブルをリストで指定する例を追加する。
  - 例: `mcp schema --tables '["users", "products"]'`

## 4. 実装スコープ外

このタスクでは、上記計画のドキュメント (`prove_plan.md`) 作成のみを行い、実際のコード実装は行わない。
