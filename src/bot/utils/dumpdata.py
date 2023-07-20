from asyncio import subprocess
from datetime import datetime
from pathlib import Path

import aiofiles
from aiocsv import AsyncWriter

from src.configuration import pwd, conf


async def dump_to_csv_writer(result, file_path):
    async with aiofiles.open(file_path, 'w', newline='') as csvfile:
        writer = AsyncWriter(csvfile)

        await writer.writerow(result.keys())
        await writer.writerows(result)


async def dump():
    file_path = Path(pwd, 'src', 'db', 'dumps', 'db.dump')
    copied_file = Path(pwd, 'src', 'db', 'dumps', f"db_{datetime.today().strftime('%d-%m-%Y')}.dump")

    command = f'PGPASSWORD=postgres pg_dump ' \
              f'--file "{file_path}" ' \
              f'--host "{conf.db.host}" ' \
              f'--port "{conf.db.port}" ' \
              f'--username "{conf.db.user}" ' \
              f'--verbose ' \
              f'--quote-all-identifiers ' \
              f'--format=c ' \
              f'--data-only "{conf.db.name}"'

    await subprocess.create_subprocess_shell(command)
    await subprocess.create_subprocess_shell(f'cp {file_path} {copied_file}')


async def restore(file='db.dump'):
    file_path = Path(pwd, 'src', 'db', 'dumps', file)

    command = f'PGPASSWORD={conf.db.passwd} pg_restore ' \
              f'--host "{conf.db.host}" ' \
              f'--port "{conf.db.port}" ' \
              f'--username "{conf.db.user}" ' \
              f'--dbname "{conf.db.name}" ' \
              f'--verbose "{file_path}"'

    await subprocess.create_subprocess_shell(command)
