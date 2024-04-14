import click

import zoomegastash


@click.command
@click.version_option(zoomegastash.__version__)
def main():
  print('asdasdf')


if __name__ == '__main__':
  main()
