from datetime import datetime
import os
from pathlib import Path
import zipfile
from datoso.helpers import downloader, show_progress
from datoso.configuration.folder_helper import Folders
from datoso.helpers import FileUtils
from datoso_seed_tdc import __preffix__



def download_dats(folder_helper: Folders):
    href = 'http://www.totaldoscollection.org/nugnugnug/tdc_daily_paths.zip'
    filename = Path(href).name
    local_filename = os.path.join(folder_helper.dats, filename)
    print(f'Downloading {filename}')
    downloader(url=href, destination=local_filename, reporthook=show_progress)

    with zipfile.ZipFile(local_filename, 'r') as zip_ref:
        zip_ref.extractall(folder_helper.dats)
    backup_daily_name = f'tdc-{datetime.now().strftime("%Y-%m-%d")}.zip'

    FileUtils.move(local_filename, os.path.join(folder_helper.backup, backup_daily_name))

def fetch():
    folder_helper = Folders(seed=__preffix__)
    folder_helper.clean_dats()
    folder_helper.create_all()
    download_dats(folder_helper)
