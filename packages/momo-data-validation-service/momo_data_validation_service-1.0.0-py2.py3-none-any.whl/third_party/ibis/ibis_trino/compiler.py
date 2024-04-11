# import re
# import sqlalchemy as sa
# from ibis.backends.trino.compiler import TrinoSQLExprTranslator
# from ibis.backends.base.sql.registry import identifiers
# from sqlalchemy.sql.schema import Column
#
# _valid_name_pattern = re.compile(r"^[A-Za-z][A-Za-z_0-9]*$")
# TrinoSQLExprTranslator._valid_name_pattern = _valid_name_pattern
#
# def quote_identifier(name, quotechar='`', force=False):
#     """Add quotes to the `name` identifier if needed."""
#     if force or name.count(' ') or name in identifiers.base_identifiers:
#         return '{0}{1}{0}'.format(quotechar, name)
#     else:
#         return name
#
# def quote_name(translated, name, force=False):
#         return f'{translated} AS {quote_identifier(name, force=force)}'
#
# # def name(translated, name, force=False):
# #     # replace invalid characters in automatically generated names
# # #     if type(translated) == 'str':
# #     print('-------_valid_name_pattern: ', type(name), name)
# #
# #     tmp_name = name
# #     if isinstance(name, Column) or isinstance(name, str):
# #         tmp_name = name.name
# #         if _valid_name_pattern.match(tmp_name) is None:
# #             return f"{translated} AS `tmp_`{tmp_name}"
# #     return quote_name(translated, name, force)
#
# def name(translated: str, name: str, force=False):
#     # replace invalid characters in automatically generated names
# #     if type(translated) == 'str':
#     print('-------_valid_name_pattern: ', type(name), name)
#
#     tmp_name = name
#     if isinstance(name, Column) or isinstance(name, str):
#         tmp_name = name.name
#         if _valid_name_pattern.match(tmp_name) is None:
#             return f"{translated} AS `tmp_`{tmp_name}"
#     return f'{translated} AS {quote_identifier(name, force=force)}'
#
#
# TrinoSQLExprTranslator.name = name

import sqlalchemy as sa
from ibis.backends.trino.compiler import TrinoSQLExprTranslator


def name(translated, name, force=False):
    if isinstance(name, str):
        return  f"{translated} AS `tmp_`{name}"
    print('-------------third_party/ibis/ibis_trino/compiler.py/name: ', type(translated), translated)
    return translated.label(
        sa.sql.quoted_name(name, quote=force or self._quote_column_names)
    )

TrinoSQLExprTranslator.name = name









