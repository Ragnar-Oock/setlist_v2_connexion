from pony.orm import raw_sql


def format_order_by(orderby: list, alias='s', similarity_col='fts_col') -> str:
    """
    Make the api parameter 'order-by' into pony code.
    **Works on single table query ONLY**.

    :param orderby: parameter from the api, list of field to be used by the order by
    :param alias: table alias
    :param similarity_col: name of the column to use in case order by needs to be performed by similarity
    :return: formated code usable in a pony query
    """
    order_by = ''
    for field in orderby:
        # is field DESC ?
        if field[0] == '-':
            field = field[1:]
            pattern = 'orm.core.desc({field}),'
        else:
            pattern = '{field},'

        # is field a real entity property ?
        if field != 'similarity':
            field = '{alias}.{field}'.format(alias=alias, field=field)
        else:
            field = 'orm.raw_sql(\'similarity("s"."{}", $search)\')'.format(similarity_col)

        order_by += pattern.format(field=field)
    return order_by[:-1]


def format_similarity(field: str, search_string: str, table='s') -> raw_sql:
    """
    build a similarity where close
    :param table: table of the field
    :param field: field to perform the similarity search in
    :param search_string: value to search in the database
    """
    return raw_sql('"{table}"."{field}" %% $search_string'
                   .format(table=table, field=field)
                   )
