from flask.json.provider import DefaultJSONProvider
from sqlalchemy import inspect
from contextlib import suppress


class Serializable:
    def __json__(self):
        column_attrs = inspected.mapper.column_attrs if (
            inspected := inspect(self)) is not None else {}

        hidden_columns = getattr(self, "__hidden_columns__", ())
        if hidden_columns == "all":
            return ()
        return {
            col.key: getattr(self, col.key)
            for col in column_attrs
            if col not in hidden_columns
        }


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):  # pyright: ignore[reportIncompatibleMethodOverride]
        with suppress(AttributeError):
            return obj.__json__()
        return super().default(obj)
