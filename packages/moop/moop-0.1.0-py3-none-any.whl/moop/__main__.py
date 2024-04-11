"""Console script for moop."""
import sys
import click

try:
    from . import __version__
except ImportError:
    __version__ = '0.1.0'

@click.group()
@click.help_option('-h', '--help')
@click.version_option(__version__, '-V', '--version', prog_name='Moop', message='%(prog)s: v%(version)s')
def entry():
    return 0


@entry.command()
@click.help_option('-h', '--help')
@click.option('-v', '--verbose', count=True)
def echo(verbose=None):
    """Console script for moop."""
    click.echo('Replace this message by putting your code into moop.__main__.entry')
    click.echo('See click documentation at https://click.palletsprojects.com/')


if __name__ == '__main__':
    sys.exit(entry())  # pragma: no cover
