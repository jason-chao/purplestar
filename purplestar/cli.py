"""
Command-line interface for the purplestar Purple Star Astrology chart generator.

Usage examples:
  purplestar generate --gender male --date 1990-03-15 --time 04:00 --timezone Asia/Taipei
  purplestar generate --gender female --date 1985-07-22 --format json --output chart.json
"""
import sys
import json
import click
from importlib.metadata import version as pkg_version
from purplestar.core.chart import generate_chart
from purplestar.output.json_schema import to_json_schema
from purplestar.output.plaintext import to_plaintext


@click.group()
@click.version_option(version=pkg_version('purplestar'), prog_name='purplestar')
def cli():
    """Purple Star Astrology natal chart generator.

    Generates Purple Star Astrology natal charts entirely offline.
    Supports JSON and plain-text output formats.
    """
    pass


@cli.command()
@click.option('--gender', '-g', required=True, type=click.Choice(['male', 'female']),
              help='Gender of the native (male/female).')
@click.option('--date', '-d', required=True, metavar='YYYY-MM-DD',
              help='Date of birth in solar calendar (e.g. 1990-03-15).')
@click.option('--time', '-t', default=None, metavar='HH:MM',
              help='Time of birth in 24-hour format (e.g. 14:30). Omit if unknown.')
@click.option('--timezone', '-z', default='UTC', metavar='TZ',
              help='Timezone of the birth location (e.g. Asia/Taipei, Europe/London). '
                   'Used for display only; the calculation uses the local solar date as given.')
@click.option('--place', '-p', default=None, metavar='PLACE',
              help='Place of birth (e.g. "London, England"). Optional.')
@click.option('--name', '-n', default=None, metavar='ID',
              help='Name or identifier for the native. Optional.')
@click.option('--format', '-f', 'fmt', default='text',
              type=click.Choice(['text', 'json']),
              help='Output format: text (plain-text) or json. Default: text.')
@click.option('--output', '-o', default=None, metavar='FILE',
              help='Output file path. Prints to stdout if omitted.')
def generate(gender, date, time, timezone, place, name, fmt, output):
    """Generate a Purple Star Astrology natal chart.

    Produces a natal chart in either plain-text or JSON format.
    The calculation is performed entirely offline using the sxtwl
    lunar calendar library.

    \b
    Examples:
      purplestar generate -g male -d 1990-03-15 -t 04:00 -z Asia/Taipei
      purplestar generate -g female -d 1975-11-08 -f json -o chart.json
    """
    try:
        chart = generate_chart(
            gender=gender,
            solar_date=date,
            time=time,
            timezone=timezone,
            place=place,
            name=name,
        )
    except Exception as exc:
        click.echo(f'Error generating chart: {exc}', err=True)
        sys.exit(1)

    if fmt == 'json':
        result = to_json_schema(chart)
    else:
        result = to_plaintext(chart)

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(result)
        click.echo(f'Chart written to {output}')
    else:
        click.echo(result)


@cli.command()
@click.argument('json_file', type=click.Path(exists=True))
def show(json_file):
    """Display a saved JSON chart as plain text.

    JSON_FILE: path to a JSON chart file produced by the generate command.
    """
    try:
        with open(json_file, encoding='utf-8') as f:
            data = json.load(f)
        # Convert schema back to internal format for display
        # For simplicity, just pretty-print key fields
        click.echo(f"Subject: {data.get('subject', {}).get('id', 'unknown')}")
        click.echo(f"Schema version: {data.get('schema_version', '')}")
        bd = data.get('birth_data', {})
        click.echo(f"Birth: {bd.get('year')}-{bd.get('month'):02d}-{bd.get('day'):02d} "
                   f"({bd.get('gender')})")
        profile = data.get('chart', {}).get('profile', {})
        click.echo(f"Five Elements: {profile.get('five_element_bureau', {})}")
        click.echo(f"Ming Palace: position {profile.get('ming_palace_position')}")
    except Exception as exc:
        click.echo(f'Error reading chart: {exc}', err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
