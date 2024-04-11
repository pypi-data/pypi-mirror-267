"""Aiohttp webserver used for captcha solving and email verification."""

from __future__ import annotations

import asyncio
import typing
import webbrowser

import aiohttp
from aiohttp import web

from . import client

__all__ = ["PAGES", "launch_webapp", "solve_geetest", "verify_email"]

PAGES: typing.Final[typing.Dict[typing.Literal["captcha", "verify-email", "enter-otp"], str]] = {
    "captcha": """
    <!DOCTYPE html>
    <html>
      <body></body>
      <script src="./gt.js"></script>
      <script>
        fetch("/mmt")
          .then((response) => response.json())
          .then((mmt) =>
            window.initGeetest(
              {
                gt: mmt.data.gt,
                challenge: mmt.data.challenge,
                new_captcha: mmt.data.new_captcha,
                api_server: "api-na.geetest.com",
                product: "bind",
                https: false,
                lang: "en",
              },
              (captcha) => {
                captcha.onReady(() => {
                  captcha.verify();
                });
                captcha.onSuccess(() => {
                  fetch("/send-data", {
                    method: "POST",
                    body: JSON.stringify({
                    session_id: mmt.session_id,
                    data: captcha.getValidate()
                  }),
                });
                document.body.innerHTML = "You may now close this window.";
              });
            }
          )
        );
      </script>
    </html>
    """,
    "verify-email": """
    <!DOCTYPE html>
    <html>
      <body>
        <input id="code" type="number">
        <button id="verify">Send</button>
      </body>
      <script>
        document.getElementById("verify").onclick = () => {
          fetch("/send-data", {
            method: "POST",
            body: JSON.stringify({
              code: document.getElementById("code").value
            }),
          });
          document.body.innerHTML = "You may now close this window.";
        };
      </script>
    </html>
    """,
    "enter-otp": """
    <!DOCTYPE html>
    <html>
      <body>
        <input id="code" type="number">
        <button id="verify">Send</button>
      </body>
      <script>
        document.getElementById("verify").onclick = () => {
          fetch("/send-data", {
            method: "POST",
            body: JSON.stringify({
              code: document.getElementById("code").value
            }),
          });
          document.body.innerHTML = "You may now close this window.";
        };
      </script>
    </html>
    """,
}


GT_URL = "https://raw.githubusercontent.com/GeeTeam/gt3-node-sdk/master/demo/static/libs/gt.js"


async def launch_webapp(
    page: typing.Literal["captcha", "verify-email", "enter-otp"],
    *,
    port: int = 5000,
    mmt: typing.Optional[typing.Dict[str, typing.Any]] = None,
) -> typing.Any:
    """Create and run a webapp to solve captcha or send verification code."""
    routes = web.RouteTableDef()
    future: asyncio.Future[typing.Any] = asyncio.Future()

    @routes.get("/captcha")
    async def captcha(request: web.Request) -> web.StreamResponse:
        return web.Response(body=PAGES["captcha"], content_type="text/html")

    @routes.get("/verify-email")
    async def verify_email(request: web.Request) -> web.StreamResponse:
        return web.Response(body=PAGES["verify-email"], content_type="text/html")

    @routes.get("/enter-otp")
    async def enter_otp(request: web.Request) -> web.StreamResponse:
        return web.Response(body=PAGES["enter-otp"], content_type="text/html")

    @routes.get("/gt.js")
    async def gt(request: web.Request) -> web.StreamResponse:
        async with aiohttp.ClientSession() as session:
            r = await session.get(GT_URL)
            content = await r.read()

        return web.Response(body=content, content_type="text/javascript")

    @routes.get("/mmt")
    async def mmt_endpoint(request: web.Request) -> web.Response:
        return web.json_response(mmt)

    @routes.post("/send-data")
    async def send_data_endpoint(request: web.Request) -> web.Response:
        body = await request.json()
        future.set_result(body)

        return web.Response(status=204)

    app = web.Application()
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, host="localhost", port=port)
    print(f"Opening http://localhost:{port}/{page} in browser...")  # noqa
    webbrowser.open_new_tab(f"http://localhost:{port}/{page}")

    await site.start()

    try:
        data = await future
    finally:
        await asyncio.sleep(0.3)
        await runner.shutdown()
        await runner.cleanup()

    return data


async def solve_geetest(
    mmt: typing.Dict[str, typing.Any],
    *,
    port: int = 5000,
) -> typing.Dict[str, typing.Any]:
    """Solve a geetest captcha manually."""
    return await launch_webapp("captcha", port=port, mmt=mmt)


async def verify_email(
    client: client.GeetestClient,
    ticket: typing.Dict[str, typing.Any],
    *,
    port: int = 5000,
) -> None:
    """Verify email to login via HoYoLab app endpoint."""
    data = await launch_webapp("verify-email", port=port)
    code = data["code"]

    return await client._verify_email(code, ticket)


async def enter_otp(port: int = 5000) -> str:
    """Lets user enter the OTP."""
    # The enter-otp page is the same as verify-email page.
    data = await launch_webapp("enter-otp", port=port)
    code = data["code"]
    return code
