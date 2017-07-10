"""CLI interface for the package"""

import logging
import os

import click

from . import logging as rpmlb_logging
from .builder.base import BaseBuilder
from .downloader.base import BaseDownloader
from .recipe import Recipe
from .work import Work


@click.command()
# General options
@click.option(
    '--verbose', '-v', is_flag=True, default=False,
    help='Turn on verbose logging.',
    # Enable logging as early as possible
    is_eager=True, expose_value=False,
    callback=lambda ctx, param, verbose:
        rpmlb_logging.configure_logging(verbose),
)
@click.option(
    '--download', '-d',
    type=click.Choice('none local rhpkg custom'.split()),
    default='none',
    help='Choose a download type.',
)
@click.option(
    '--build', '-b',
    type=click.Choice('dummy mock copr custom'.split()),
    default='dummy',
    help='Choose a build type.',
)
@click.option(
    '--work-directory', '-w',
    type=click.Path(exists=True, file_okay=False, writable=True,
                    resolve_path=True),
    default=None,
    help='Specify a working directory.',
)
@click.option(
    '--custom-file', '-c',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help='Instructions for custom downloader and builder.',
)
# Download options
@click.option(
    '--branch', '-B',
    help='Git branch for downloaders that use it (rhpkg).',
)
@click.option(
    '--source-directory', '-S',
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    default=os.path.abspath(os.getcwd()),
    help='Package source directory for local downloader.',
)
# Build options
@click.option(
    '--resume', '-r',
    type=click.INT,
    help='Resume build from specified position.',
)
@click.option(
    '--mock-config', '-M',
    help='Mock configuration for mock builder.',
)
@click.option(
    '--copr-repo', '-C',
    help='Target Copr for copr builder.',
)
# Positional arguments
@click.argument(
    'recipe_file',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
)
@click.argument('recipe_name')
def run(recipe_file, recipe_name, **option_dict):
    """Download and build RPMs listed in RECIPE_FILE under RECIPE_NAME
    (such as 'python33').
    """

    log = logging.getLogger(__name__)

    # Load recipe and processing objects
    recipe = Recipe(recipe_file, recipe_name)
    recipe.verify()

    builder = BaseBuilder.get_instance(option_dict['build'])
    downloader = BaseDownloader.get_instance(option_dict['download'])

    # Prepare the working directory
    # HINT: with contextlib.closing(Work(recipe, **option_dict)) as work:
    work = Work(recipe, **option_dict)

    # Download
    log.info('Downloading...')
    downloader.run(work, **option_dict)

    # Build
    log.info('Building...')
    builder.run(work, **option_dict)

    log.info('Success!')
