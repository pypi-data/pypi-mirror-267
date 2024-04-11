import csv
from pathlib import Path
import typing as t

from . import Qbuffer


def create_csv_dict_write_qbuffer(
    *,
    maxlen: int,
    path: Path,
    fieldnames: list[str],
    mode='w',
    encoding: t.Optional[str] = None,
    extrasaction: t.Literal['raise', 'ignore'] = 'ignore',
    newline='',
    callback: t.Optional[t.Callable[[t.Mapping[str, t.Any]], t.Any]] = None,
    flush_callback: t.Optional[t.Callable[[], t.Any]] = None,
):
    path.parent.mkdir(parents=True, exist_ok=True)
    file = path.open(mode=mode, encoding=encoding, newline=newline)
    dict_writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction=extrasaction)
    dict_writer.writeheader()
    qbuffer = Qbuffer(
        maxlen=maxlen,
        callback=callback or dict_writer.writerow,
        flush_callback=flush_callback or file.flush,
    )
    return qbuffer
