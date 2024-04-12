from posixpath import splitext
from typing import Any, Dict, List, Union

import pandas  # lazy module

from deirokay.fs import fs_factory


def read(
    data: Union[str, "pandas.DataFrame"],
    columns: List[str],
    sql: bool = False,
    **kwargs,
) -> "pandas.DataFrame":
    """Infer the file type by its extension and call the proper
    `pandas` method to parse it.

    Parameters
    ----------
    data : Union[DataFrame, dd.DataFrame, str]
        Path to file or SQL query, or DataFrame object
    columns : List[str]
        List of columns to be parsed.
    sql : bool, optional
        Whether or not `data` should be interpreted as a path to a file
        or a SQL query.
    **kwargs : dict
        Arguments to be passed to `pandas` methods when reading.


    Returns
    -------
    pandas.DataFrame
        The pandas DataFrame.
    """
    default_kwargs: Dict[str, Any] = {}

    if isinstance(data, pandas.DataFrame):
        return data[columns].copy()

    if not isinstance(data, str):
        raise TypeError(f"Unexpected type for `data` ({data.__class__})")

    if sql:
        read_ = pandas.read_sql

    else:
        file_extension = splitext(data)[1].lstrip(".").lower()

        if file_extension == "sql":
            query = fs_factory(data).read()
            return read(query, columns, sql=True, **kwargs)

        if file_extension in ("xls", "xlsx"):
            file_extension = "excel"

        if file_extension == "csv":
            default_kwargs.update(
                {
                    "dtype": str,
                    "skipinitialspace": True,
                }
            )

        read_ = getattr(pandas, f"read_{file_extension}", None)
        if read_ is None:
            raise TypeError(f'File type "{file_extension}" not supported')

    default_kwargs.update(kwargs)

    # try `columns` argument
    try:
        return read_(data, columns=columns, **default_kwargs)
    except TypeError as e:
        if "columns" not in str(e):
            raise e
    # try `usecols` argument
    try:
        return read_(data, usecols=columns, **default_kwargs)
    except TypeError as e:
        if "usecols" not in str(e):
            raise e
    # give up, read everything, filter columns later
    return read_(data, **default_kwargs)[columns]
