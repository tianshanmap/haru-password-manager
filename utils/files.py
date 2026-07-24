from pathlib import Path
import anyio

def exists(path):
    return Path(path).exists()

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)

def write_export_file(export_folder,name, content):
    data_folder = Path(export_folder) / name
    with open(data_folder, 'w') as f:
        f.write(content)
    return data_folder

async def file_chunk_generator(file_path: str, chunk_size: int = 4096):
    async with await anyio.open_file(file_path, mode="rb") as f:
        while True:
            chunk = await f.read(chunk_size)
            if not chunk:
                break
            yield chunk