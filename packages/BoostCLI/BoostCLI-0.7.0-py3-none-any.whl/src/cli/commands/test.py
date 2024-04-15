import click
from rich.console import Console
from typing import Optional

from src.services.lightning_service import LightningService

from ..print_value import print_value


@click.command()
@click.argument("search_term")
@click.pass_context
def test(ctx, search_term, **kwargs):
    """Display Boosts that have been received."""
    console: Console = ctx.obj["console"]
    console_error: Console = ctx.obj["console_error"]
    lighting_service: LightningService = ctx.obj["lightning_service"]
    pi_service: Optional[PodcastIndexService] = ctx.obj.get("podcast_index_service")

    console.log("test")
    pv = find_podcast_value(console, feed_service, pi_service, search_term)
    if pv is None:
        console_error.print(
            f':broken_heart: Failed to locate value by search_term="{search_term}"'
        )
        exit(1)