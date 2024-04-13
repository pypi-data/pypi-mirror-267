import urllib.request
from pathlib import Path
from tqdm import tqdm


def dl(path: Path, url: str):
    """
    Checks if a file specified by path exists. If not, downloads it from the given URL.

    Args:
        path (Path): The path to the file.
        url (str): The URL from which to download the file.
    """
    path.mkdir(parents=True, exist_ok=True)
    file_name = url.split('/')[-1]
    file_path = path / file_name
    if not file_path.exists():
        print(f"Downloading {path.name} from {url}...")
        with urllib.request.urlopen(url) as response, open(file_path, 'wb') as out_file:
            file_size = int(response.info().get('Content-Length', -1))
            chunk_size = 1024 * 1024  # 1 MB
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=file_name) as pbar:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    out_file.write(chunk)
                    pbar.update(len(chunk))
        print("Download complete!")
    else:
        print(f"Confirmed {file_path} exists")
