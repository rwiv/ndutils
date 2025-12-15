import asyncio

from nodriver.cdp import fetch
from nodriver.core.tab import Tab


async def setup_proxy(username: str, password: str, tab: Tab):
    async def auth_challenge_handler(event: fetch.AuthRequired):
        # Respond to the authentication challenge
        await tab.send(
            fetch.continue_with_auth(
                request_id=event.request_id,
                auth_challenge_response=fetch.AuthChallengeResponse(
                    response="ProvideCredentials",
                    username=username,
                    password=password,
                ),
            )
        )

    async def req_paused(event: fetch.RequestPaused):
        # Continue with the request
        await tab.send(fetch.continue_request(request_id=event.request_id))

    # Add handlers for fetch events
    tab.add_handler(fetch.RequestPaused, lambda event: asyncio.create_task(req_paused(event)))
    tab.add_handler(
        fetch.AuthRequired,
        lambda event: asyncio.create_task(auth_challenge_handler(event)),
    )

    # Enable fetch domain with auth requests handling
    await tab.send(fetch.enable(handle_auth_requests=True))
