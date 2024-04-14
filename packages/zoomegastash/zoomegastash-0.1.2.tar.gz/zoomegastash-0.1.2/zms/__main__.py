import click

import zms


@click.command
@click.version_option(zms.__version__)
def main():
  print('asdasdf')


if __name__ == '__main__':
  main()
