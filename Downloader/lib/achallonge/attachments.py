from achallonge import api


async def index(tournament, match, **params):
    """Retrieve a set of attachments created for a specific match."""
    return await api.fetch_and_parse(
        "GET", f"tournaments/{tournament}/matches/{match}/attachments", **params
    )


async def create(tournament, match, **params):
    """Create a new attachment for the specific match."""
    return await api.fetch_and_parse(
        "POST",
        f"tournaments/{tournament}/matches/{match}/attachments",
        "match_attachment",
        **params,
    )


async def show(tournament, match, attachment, **params):
    """Retrieve a single match attachment record."""
    return await api.fetch_and_parse(
        "GET", f"tournaments/{tournament}/matches/{match}/attachments/{attachment}", **params
    )


async def update(tournament, match, attachment, **params):
    """Update the attributes of a match attachment."""
    await api.fetch(
        "PUT",
        f"tournaments/{tournament}/matches/{match}/attachments/{attachment}",
        "match_attachment",
        **params,
    )


async def destroy(tournament, match, attachment, **params):
    """Delete a match attachment."""
    await api.fetch(
        "DELETE", f"tournaments/{tournament}/matches/{match}/attachments/{attachment}", **params
    )
