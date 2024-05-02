"""
* MTG Vectors Request Handling
"""
# Standard Library Imports
from contextlib import suppress
from pathlib import Path
from typing import Optional, Union

# Third Party Imports
from loguru import logger
from omnitils.api.github import gh_get_data_json, gh_download_file
from omnitils.files import mkdir_full_perms, dump_data_file
from omnitils.files.archive import unpack_zip
from requests import RequestException
import yarl

# Local Imports
from hexproof.vectors.enums import URL

"""
* Request Funcs
"""


def get_vectors_manifest(
    directory: Path,
    url: Union[yarl.URL, str, None] = None,
    header: Optional[dict] = None,
    auth_token: Optional[str] = None
) -> Optional[dict]:
    """Gets the current mtg-vectors symbol manifest.

    Args:
        directory: Directory to save manifest file.
        url: URL to fetch manifest from, uses official `mtg-vectors` repository if not provided.
        header: Header object to pass with request, uses default if not provided.
        auth_token: Optional auth token to pass with request, increases rate limits.

    Returns:
        Path to the manifest file.
    """
    url = url or URL.MANIFEST
    if not directory.is_dir():
        mkdir_full_perms(directory)
    path = directory / 'manifest.json'
    try:
        data = gh_get_data_json(
            url=url,
            header=header,
            auth_token=auth_token)
        dump_data_file(data, path)
        return data
    except RequestException:
        return logger.error('Unable to reach mtg-vectors manifest URL!')
    except FileExistsError:
        return logger.error('Unable to write new mtg-vectors manifest!')
    except (OSError, ValueError):
        return logger.error('Unable to dump data file!')


def get_vectors_package(
        directory: Path,
        url: Union[yarl.URL, str, None] = None,
        header: Optional[dict] = None,
        auth_token: Optional[str] = None,
        chunk_size: int = 1024 * 1024 * 8
) -> Optional[Path]:
    """Updates our 'Set' symbol local assets.

    Args:
        directory: Directory to save and extract the package into.
        url: URL to fetch manifest from.
        header: Header object to pass with request, uses default if not provided.
        auth_token: Optional auth token to pass with request, increases rate limits.
        chunk_size: Chunk size to use when writing package file from stream, default is 8MB.

    Returns:
        Directory the package was extracted to, if successful, otherwise None.
    """

    # Get zip
    url = url or URL.PACKAGE
    if not directory.is_dir():
        mkdir_full_perms(directory)
    path = directory / 'package.zip'
    try:
        gh_download_file(
            url=url,
            path=path,
            header=header,
            auth_token=auth_token,
            chunk_size=chunk_size)
    except RequestException:
        return logger.error('Unable to reach mtg-vectors symbol package!')
    except FileExistsError:
        return logger.error('Unable to write new mtg-vectors symbol package!')

    # Unpack zip
    try:
        unpack_zip(path)
        return directory
    except Exception as e:
        logger.exception(e)
        logger.error('Unable to unpack vectors package!')


"""
* Update Funcs
"""


def update_vectors_manifest(
    directory: Path,
    current: str,
    url: Union[yarl.URL, str, None] = None,
    force: bool = False
) -> Optional[dict]:
    """Update the mtg-vectors manifest.

    Args:
        directory: Directory to save manifest file to.
        current: Current version of vector manifest.
        url: URL to fetch manifest from.
        force: Whether to update even if metadata is already up-to-date, False by default.

    Returns:
        Metadata if successful, otherwise None.
    """

    # Request the updated manifest
    manifest = get_vectors_manifest(directory=directory, url=url)
    if not manifest:
        return

    # Check if manifest version changed
    with suppress(Exception):
        if current == manifest.get('meta', {}).get('version', '') and not force:
            return logger.info('Set symbols already up-to-date!')
        return manifest

    # General error occurred
    return logger.error("MTG Vectors updated set symbol manifest couldn't be written!")
