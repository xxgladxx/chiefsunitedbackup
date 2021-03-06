from typing import Dict, Sequence

from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list, inline

from .consts import CHECK, CROSS, DOCS_BASE


def format_help(self: commands.Cog, ctx: commands.Context) -> str:
    """Wrapper for format_help_for_context. **Not** currently for use outside my cogs.

    Thanks Sinbad.

    Parameters
    ----------
    self : commands.Cog
        The Cog class
    context : commands.Context
        Context

    Returns
    -------
    str
        Formatted help
    """
    docs = DOCS_BASE.format(self.qualified_name.lower())
    pre_processed = super(type(self), self).format_help_for_context(ctx)

    return (
        f"{pre_processed}\n\nAuthor: **`{self.__author__}`**\nCog Version: "
        f"**`{self.__version__}`**\n{docs}"
    )
    # adding docs link here so doesn't show up in auto generated docs


def format_info(qualified_name: str, version: str, extras: Dict[str, bool] = {}) -> str:
    """Generate simple info text about the cog. **Not** currently for use outside my cogs.

    Parameters
    ----------
    qualified_name : str
        The name you want to show, eg "BetterUptime"
    version : str
        The version of the cog
    extras : Dict[str, bool], optional
        Dict with name as the key a bool as the value, by default {}

    Returns
    -------
    str
        Simple info text.
    """
    start = f"{qualified_name} by Vexed.\n<https://github.com/Vexed01/Vex-Cogs>\n\n"
    end = f"Version: `{version}`"

    extra = ""
    for key, value in extras.items():
        extra += f"{key}: `{CHECK if value else CROSS}`\n"

    return f"{start}{extra}{end}"


# maybe think about adding to core
def inline_hum_list(items: Sequence[str], *, style: str = "standard") -> str:
    """Similar to core's humanize_list, but all items are in inline code blocks. **Can** be used
    outside my cogs.

    Strips leading and trailing whitespace.

    Does not support locale.

    Does support style (see core's docs for available styles)

    Parameters
    ----------
    items : Sequence[str]
        The items to humanize
    style : str, optional
        The style. See core's docs, by default "standard"

    Returns
    -------
    str
        Humanized inline list.
    """
    inline_list = [inline(i.strip()) for i in items]
    return humanize_list(inline_list, style=style)
