from dataclasses import dataclass
from psycopg2.extensions import cursor


@dataclass
class TableField:
    field_name: str
    properties: str


class Table:
    def __init__(self, cursor: cursor, table_name: str, fields: list[TableField]):
        self.table_name = table_name
        self.cursor = cursor

        self.fields = fields
        self.__initialize_table(fields)

    def insert_entry(self, *values) -> bool:
        try:
            fields_string = ",".join(
                [x.field_name for x in self.fields if x.field_name != "id"]
            )
            values_string = ",".join(["%s"] * (len(self.fields) - 1))

            self.cursor.execute(
                f"INSERT INTO {self.table_name} ({fields_string}) VALUES ({values_string})",
                (*values,),
            )
        except Exception:
            return False

        return True

    def update(self, column: str, value: str, id_column: str, id_value: str):
        self.cursor.execute(
            "UPDATE %s SET %s = (%s) WHERE %s = %s",
            (self.table_name, column, value, id_column, id_value),
        )

    def exists(self, key: str, value: str) -> bool:
        self.cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE {key} = %s", (value,)
        )
        return bool(self.cursor.fetchone())

    def fetch(self, property: str, key: str, value: str):
        self.cursor.execute(
            f"SELECT %s FROM {self.table_name} WHERE %s = %s", (property, key, value)
        )
        return self.cursor.fetchone()

    def __initialize_table(self, fields: list[TableField]):
        field_count = len(fields)

        field_string = ""
        for i, field in enumerate(fields):
            field_string += field.field_name + " " + field.properties
            if i < field_count - 1:
                field_string += ","

        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table_name} ({field_string})"
        )
