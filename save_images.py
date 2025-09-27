import os
import logging
from logging.handlers import RotatingFileHandler
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
from PIL import Image
from io import BytesIO


"""download-images-from-url

This script reads an Excel file with two columns (ID and URL) and downloads
each image into an output directory. It uses a requests Session with retries
and structured logging to both console and a rotating log file.

Notes:
 - The script is intentionally minimal: it keeps the same filename pattern
   used previously ("<ID>_B.jpg").
 - Logging is added to aid debugging and to record successes/failures.
"""

# Path to your Excel file (change if needed)
EXCEL_PATH = 'products.xlsx'

# Output directory for images
OUTPUT_DIR = 'downloaded_images'

# Log settings
LOG_FILE = 'download_images.log'
LOG_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
LOG_BACKUP_COUNT = 3


def setup_logging(log_file: str = LOG_FILE) -> logging.Logger:
    """Configure and return a logger.

    Creates both a console handler (INFO level) and a rotating file handler
    (DEBUG level) so that verbose debugging information is persisted to disk.
    """
    logger = logging.getLogger('download_images')
    if logger.handlers:
        # Already configured (avoid duplicate handlers when reloading)
        return logger

    logger.setLevel(logging.DEBUG)

    # Console handler for high-level information
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_fmt = logging.Formatter('%(levelname)s: %(message)s')
    ch.setFormatter(ch_fmt)
    logger.addHandler(ch)

    # Rotating file handler for detailed debug logs
    fh = RotatingFileHandler(log_file, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
    fh.setLevel(logging.DEBUG)
    fh_fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    fh.setFormatter(fh_fmt)
    logger.addHandler(fh)

    return logger


def create_session(retries: int = 3, backoff_factor: float = 0.5, status_forcelist=None) -> requests.Session:
    """Create a requests Session configured with retries and a backoff strategy.

    This reduces transient network errors when downloading many images.
    """
    session = requests.Session()
    if status_forcelist is None:
        status_forcelist = [429, 500, 502, 503, 504]

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(['GET', 'POST'])
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def download_and_save_image(session: requests.Session, url: str, filepath: str, timeout: int = 10) -> None:
    """Download an image from `url` using `session` and save it to `filepath`.

    Raises an exception on failure. The caller should handle/log exceptions.
    """
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content)).convert('RGB')
    # Ensure containing directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath, 'JPEG')


def main(excel_path: str = EXCEL_PATH, output_dir: str = OUTPUT_DIR) -> None:
    """Main entrypoint: read Excel, iterate rows, and download images.

    Expected Excel format: first column = ID, second column = URL.
    The script will coerce the first two columns into ['ID', 'URL'] regardless
    of their original names.
    """
    logger = setup_logging()
    logger.info('Starting image download run')

    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)

    # Read the Excel file into a DataFrame
    try:
        df = pd.read_excel(excel_path)
    except Exception as exc:
        logger.exception('Failed to read Excel file: %s', excel_path)
        raise

    # Normalize to exactly two columns: ID and URL
    if df.shape[1] < 2:
        logger.error('Excel file must have at least two columns (ID and URL). Found %d', df.shape[1])
        raise SystemExit(1)

    df.columns = [df.columns[0], df.columns[1]]
    df = df.rename(columns={df.columns[0]: 'ID', df.columns[1]: 'URL'})

    session = create_session()

    # Iterate rows with progress info
    total = len(df)
    logger.info('Found %d rows in %s', total, excel_path)

    for idx, row in df.iterrows():
        img_id = str(row['ID'])
        url = row['URL']
        filename = f"{img_id}_B.jpg"
        filepath = os.path.join(output_dir, filename)

        # Skip if file already exists (avoid re-downloading)
        if os.path.exists(filepath):
            logger.info('Skipping existing file for ID %s: %s', img_id, filepath)
            continue

        try:
            logger.debug('Downloading ID=%s URL=%s', img_id, url)
            download_and_save_image(session, url, filepath)
            logger.info('Saved: %s', filepath)
        except Exception:
            # Log full stack trace to file handler and a concise message to console
            logger.exception('Failed to download %s for ID %s', url, img_id)


if __name__ == '__main__':
    # Minimal CLI behavior: run with defaults. Users can import main() to customize.
    main()