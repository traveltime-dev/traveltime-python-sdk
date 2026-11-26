import json
import os
from typing import IO, Any, Dict, List, Optional, Union

FORMAT_VERSION = 1

PathLike = Union[str, "os.PathLike[str]"]


class Checkpoint:
    """Append-only JSONL file of finished searches.

    The first line identifies the matrix inputs, every later line holds one finished
    search. Lines are flushed as they're written, so after a crash at most the last line
    is incomplete, and it's skipped on load.
    """

    def __init__(self, path: PathLike, fingerprint: str):
        self._path = path
        self._fingerprint = fingerprint
        self._file: Optional[IO[bytes]] = None

    def load(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self._path) or os.path.getsize(self._path) == 0:
            return []

        with open(self._path, "rb") as file:
            lines = file.read().splitlines()

        header = _parse(lines[0])
        if header is None or header.get("fingerprint") != self._fingerprint:
            raise ValueError(
                f"Checkpoint {os.fspath(self._path)} was written for a different "
                "matrix. Use a different checkpoint path or delete the file."
            )
        records = (_parse(line) for line in lines[1:])
        return [record for record in records if record is not None]

    def open(self) -> None:
        self._file = open(self._path, "ab+")
        size = self._file.tell()
        if size == 0:
            self.append({"version": FORMAT_VERSION, "fingerprint": self._fingerprint})
        else:
            self._file.seek(size - 1)
            if self._file.read(1) != b"\n":
                self._file.write(b"\n")

    def close(self) -> None:
        if self._file is not None:
            self._file.close()

    def append(self, record: Dict[str, Any]) -> None:
        assert self._file is not None
        self._file.write(json.dumps(record, separators=(",", ":")).encode() + b"\n")
        self._file.flush()


def _parse(line: bytes) -> Optional[Dict[str, Any]]:
    try:
        record = json.loads(line)
    except ValueError:
        return None
    return record if isinstance(record, dict) else None
