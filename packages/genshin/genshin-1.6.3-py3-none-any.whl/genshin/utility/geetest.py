"""Geetest utilities."""

import base64
import json
import typing

from ..types import Region

__all__ = ["encrypt_geetest_credentials"]


# RSA key is the same for app and web login
OS_LOGIN_KEY_CERT = b"""
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4PMS2JVMwBsOIrYWRluY
wEiFZL7Aphtm9z5Eu/anzJ09nB00uhW+ScrDWFECPwpQto/GlOJYCUwVM/raQpAj
/xvcjK5tNVzzK94mhk+j9RiQ+aWHaTXmOgurhxSp3YbwlRDvOgcq5yPiTz0+kSeK
ZJcGeJ95bvJ+hJ/UMP0Zx2qB5PElZmiKvfiNqVUk8A8oxLJdBB5eCpqWV6CUqDKQ
KSQP4sM0mZvQ1Sr4UcACVcYgYnCbTZMWhJTWkrNXqI8TMomekgny3y+d6NX/cFa6
6jozFIF4HCX5aW8bp8C8vq2tFvFbleQ/Q3CU56EWWKMrOcpmFtRmC18s9biZBVR/
8QIDAQAB
-----END PUBLIC KEY-----
"""

CN_LOGIN_KEY_CERT = b"""
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDvekdPMHN3AYhm/vktJT+YJr7
cI5DcsNKqdsx5DZX0gDuWFuIjzdwButrIYPNmRJ1G8ybDIF7oDW2eEpm5sMbL9zs
9ExXCdvqrn51qELbqj0XxtMTIpaCHFSI50PfPpTFV9Xt/hmyVwokoOXFlAEgCn+Q
CgGs52bFoYMtyi+xEQIDAQAB
-----END PUBLIC KEY-----
"""

WEB_LOGIN_HEADERS = {
    "x-rpc-app_id": "c9oqaq3s3gu8",
    "x-rpc-client_type": "4",
    # If not equal account.hoyolab.com It's will return retcode 1200 [Unauthorized]
    "Origin": "https://account.hoyolab.com",
    "Referer": "https://account.hoyolab.com/",
}

APP_LOGIN_HEADERS = {
    "x-rpc-app_id": "c9oqaq3s3gu8",
    "x-rpc-client_type": "2",
    # Passing "x-rpc-device_id" header will trigger email verification
    # (unless the device_id is already verified).
    #
    # For some reason, without this header, email verification is not triggered.
    # "x-rpc-device_id": "1c33337bd45c1bfs",
}

CN_LOGIN_HEADERS = {
    "x-rpc-app_id": "bll8iq97cem8",
    "x-rpc-client_type": "4",
    "Origin": "https://user.miyoushe.com",
    "Referer": "https://user.miyoushe.com/",
    "x-rpc-source": "v2.webLogin",
    "x-rpc-mi_referrer": "https://user.miyoushe.com/login-platform/index.html?app_id=bll8iq97cem8&theme=&token_type=4&game_biz=bbs_cn&message_origin=https%253A%252F%252Fwww.miyoushe.com&succ_back_type=message%253Alogin-platform%253Alogin-success&fail_back_type=message%253Alogin-platform%253Alogin-fail&ux_mode=popup&iframe_level=1#/login/password",  # noqa: E501
    "x-rpc-device_id": "586f2440-856a-4243-8076-2b0a12314197",
}

EMAIL_SEND_HEADERS = {
    "x-rpc-app_id": "c9oqaq3s3gu8",
    "x-rpc-client_type": "2",
}

EMAIL_VERIFY_HEADERS = {
    "x-rpc-app_id": "c9oqaq3s3gu8",
    "x-rpc-client_type": "2",
}


def encrypt_geetest_credentials(text: str, region: Region = Region.OVERSEAS) -> str:
    """Encrypt text for geetest."""
    import rsa

    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(
        OS_LOGIN_KEY_CERT if region is Region.OVERSEAS else CN_LOGIN_KEY_CERT
    )
    crypto = rsa.encrypt(text.encode("utf-8"), public_key)
    return base64.b64encode(crypto).decode("utf-8")


def get_aigis_header(session_id: str, mmt_data: typing.Dict[str, typing.Any]) -> str:
    """Get aigis header."""
    return f"{session_id};{base64.b64encode(json.dumps(mmt_data).encode()).decode()}"
