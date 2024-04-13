# QuickDL

QuickDL is a Python utility for downloading files from URLs. It checks if a file specified by a given path exists. If the file does not exist, QuickDL downloads it from the provided URL and displays a progress bar to visualize the download progress.

## Installation

You can install QuickDL using pip:

```bash
pip install quickdl
```

## Usage

```python
from quickdl import dl
from pathlib import Path

# Example usage:
dl(Path('downloads'), 'https://example.com/file.txt')
```

This code will download the file from the provided URL to the specified path. If the file already exists at the destination path, QuickDL will confirm its existence. If the file does not exist, QuickDL will download it and display a progress bar to track the download progress.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.