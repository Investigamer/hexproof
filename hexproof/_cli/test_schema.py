"""
* CLI Commands: Test
"""
import click

"""
* Commands: MTGJSON
"""


@click.command
def test_mtgjson_all():
    """Tests all MTGJSON schemas."""


"""
* Command Groups
"""


@click.group(
    name='sync',
    commands=dict(
        all=test_mtgjson_all
    )
)
def TestSchemaMTGJSON():
    pass



@click.group(
    commands=dict(
        mtgjson=TestSchemaMTGJSON
    )
)
def TestSchema():
    pass
