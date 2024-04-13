from . import table20240326, table20240410


def get_table_factory(table_name):
    if table_name == "table20240326":
        return table20240326
    elif table_name == "table20240410":
        return table20240410
    else:
        raise NotImplementedError(f"Not supported <{table_name=}>.")
