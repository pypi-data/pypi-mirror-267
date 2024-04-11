import time
import random
import json
from lazysdk import lazyrequests

"""
2024-04-11 全面升级至3.0版本 https://developers.e.qq.com/v3.0/docs/api
"""


def make_nonce():
    """
    参考示例代码的生成一个随机数
    :return:
    """
    return str(time.time()) + str(random.randint(0, 999999))


def oauth_token2(
        app_id,
        app_secret,
        redirect_uri,
        grant_type='authorization_code',
        auth_code=None,
        refresh_token=None,
):
    """
    OAuth 2.0 授权
    获取/刷新token
    相关文档：https://developers.e.qq.com/docs/start/authorization
    :param auth_code:
    :param app_id:
    :param app_secret:
    :param grant_type: 请求的类型，可选值：authorization_code（授权码方式获取 token）、refresh_token（刷新 token）
    :param refresh_token:
    :param redirect_uri:
    :return:
    """
    redirect_uri = f'{redirect_uri}?app_id={app_id}'

    url = 'https://api.e.qq.com/oauth/token'
    params = {
        'client_id': app_id,
        'client_secret': app_secret,
        'grant_type': grant_type
    }
    if auth_code:
        params['authorization_code'] = auth_code
    if refresh_token:
        params['refresh_token'] = refresh_token
    if redirect_uri:
        params['redirect_uri'] = redirect_uri

    for k in params:
        if type(params[k]) is not str:
            params[k] = json.dumps(params[k])

    return lazyrequests.lazy_requests(
        method="GET",
        url=url,
        params=params
    )


def oauth_token3(
        access_token,
        app_id,
        app_secret,
        redirect_uri=None,
        grant_type='authorization_code',
        auth_code=None,
        refresh_token=None,
):
    """
    获取/刷新token
    相关文档：https://developers.e.qq.com/v3.0/docs/api/oauth/token
    :param access_token:
    :param auth_code:
    :param app_id:
    :param app_secret:
    :param grant_type: 请求的类型，可选值：authorization_code（授权码方式获取 token）、refresh_token（刷新 token）
    :param refresh_token:
    :param redirect_uri: 回调地址
    :return:
    """
    url = 'https://api.e.qq.com/v3.0/oauth/token'
    params = {
        'access_token': access_token,
        'timestamp': int(time.time()),
        'nonce': make_nonce,

        'client_id': app_id,
        'client_secret': app_secret,
        'grant_type': grant_type
    }
    if auth_code:
        params['authorization_code'] = auth_code
    if refresh_token:
        params['refresh_token'] = refresh_token
    if redirect_uri:
        redirect_uri = f'{redirect_uri}?app_id={app_id}'
        params['redirect_uri'] = redirect_uri

    # for k in params:
    #     if type(params[k]) is not str:
    #         params[k] = json.dumps(params[k])

    return lazyrequests.lazy_requests(
        method="GET",
        url=url,
        params=params
    )
