from asyncio import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import aiofiles
from aiocsv import AsyncWriter

from src.configuration import pwd, conf


def get_db_components():
    """
    Разбирает DATABASE_URL и возвращает словарь с параметрами подключения.
    Пример DATABASE_URL:
      postgres://user:password@host:port/dbname
    """
    parsed = urlparse(conf.db.db_url)
    return {
        "host": parsed.hostname,
        "port": parsed.port,
        "user": parsed.username,
        "password": parsed.password,
        "dbname": parsed.path.lstrip("/"),
    }


async def dump_to_csv_writer(result, file_path):
    async with aiofiles.open(file_path, 'w', newline='') as csvfile:
        writer = AsyncWriter(csvfile)

        await writer.writerow(result.keys())
        await writer.writerows(result)


async def dump():
    file_path = Path(pwd, 'src', 'db', 'dumps', 'db.dump')
    copied_file = Path(pwd, 'src', 'db', 'dumps', f"db_{datetime.today().strftime('%d-%m-%Y')}.dump")
    db = get_db_components()

    command = (
        f'PGPASSWORD={db["password"]} pg_dump '
        f'--file "{file_path}" '
        f'--host "{db["host"]}" '
        f'--port "{db["port"]}" '
        f'--username "{db["user"]}" '
        f'--verbose '
        f'--quote-all-identifiers '
        f'--format=c '
        f'--data-only "{db["dbname"]}"'
    )

    await subprocess.create_subprocess_shell(command)
    await subprocess.create_subprocess_shell(f'cp {file_path} {Path(directory, copied_file)}')


async def restore(file='db.dump'):
    file_path = Path(pwd, 'src', 'db', 'dumps', file)
    db = get_db_components()

    command = (
        f'PGPASSWORD={db["password"]} pg_restore '
        f'--host "{db["host"]}" '
        f'--port "{db["port"]}" '
        f'--username "{db["user"]}" '
        f'--dbname "{db["dbname"]}" '
        f'--verbose "{file_path}"'
    )

    await subprocess.create_subprocess_shell(command)
