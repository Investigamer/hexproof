"""
* MTG Vectors Request Handling
"""
# Standard Library Imports
from pathlib import Path
from typing import Optional, Union

# Third Party Imports
from loguru import logger
from omnitils.api.github import gh_get_data_json, gh_download_file
from omnitils.files import mkdir_full_perms
from omnitils.files.archive import unpack_zip
from requests import RequestException
import yarl

# Local Imports
from hexproof.vectors.enums import VectorURL
from hexproof.vectors import schema as VectorSchema

"""
* Request Funcs
"""


def get_vectors_manifest(
    url: Union[yarl.URL, str, None] = None,
    header: Optional[dict] = None,
    auth_token: Optional[str] = None
) -> Optional[VectorSchema.Manifest]:
    """Gets the current mtg-vectors symbol manifest and returns it as a 'Manifest' object.

    Args:
        url: URL to fetch manifest from, uses official `mtg-vectors` repository if not provided.
        header: Header object to pass with request, uses default if not provided.
        auth_token: Optional auth token to pass with request, increases rate limits.

    Returns:
        A mtg-vectors 'Manifest' object.
    """
    try:
        data = gh_get_data_json(
            url=url or VectorURL.Manifest,
            header=header,
            auth_token=auth_token)
        return VectorSchema.Manifest(**data)
    except RequestException:
        return logger.error('Unable to reach mtg-vectors manifest URL!')
    except FileExistsError:
        return logger.error('Unable to write new mtg-vectors manifest!')
    except (OSError, ValueError):
        return logger.error('Unable to dump data file!')


"""
* Download Funcs
"""


def cache_vectors_manifest(
    path: Path,
    url: Union[yarl.URL, str, None] = None,
    header: Optional[dict] = None,
    auth_token: Optional[str] = None
) -> Optional[Path]:
    """Gets the current mtg-vectors symbol manifest.

    Args:
        path: Path to save the manifest file.
        url: URL to fetch manifest from, uses official `mtg-vectors` repository if not provided.
        header: Header object to pass with request, uses default if not provided.
        auth_token: Optional auth token to pass with request, increases rate limits.

    Returns:
        Path to the manifest file.
    """
    try:
        _path = gh_download_file(
            url=url or VectorURL.Manifest,
            path=path,
            header=header,
            auth_token=auth_token)
        return _path
    except RequestException:
        return logger.error('Unable to reach mtg-vectors manifest URL!')
    except FileExistsError:
        return logger.error('Unable to write new mtg-vectors manifest!')
    except (OSError, ValueError):
        return logger.error('Unable to dump data file!')


def cache_vectors_package(
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
    url = url or VectorURL.Package
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
