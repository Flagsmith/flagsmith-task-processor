import os
import typing
from contextlib import suppress

from django.db import migrations


class PostgresOnlyRunSQL(migrations.RunSQL):
    @classmethod
    def from_sql_file(
        cls,
        file_path: typing.Union[str, os.PathLike],
        reverse_sql: typing.Union[str, os.PathLike] = None,
    ) -> "PostgresOnlyRunSQL":
        with open(file_path) as forward_sql:
            with suppress(FileNotFoundError, TypeError):
                with open(reverse_sql) as reverse_sql_file:
                    reverse_sql = reverse_sql_file.read()
            return cls(forward_sql.read(), reverse_sql=reverse_sql)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        if schema_editor.connection.vendor != "postgresql":
            return
        super().database_forwards(app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        if schema_editor.connection.vendor != "postgresql":
            return
        super().database_backwards(app_label, schema_editor, from_state, to_state)
