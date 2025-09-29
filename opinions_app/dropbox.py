import asyncio

import aiohttp

import json

from . import app

AUTH_HEADER = f'Bearer {app.config["DROPBOX_TOKEN"]}'
UPLOAD_LINK = 'https://content.dropboxapi.com/2/files/upload'
SHARING_LINK = ('https://api.dropboxapi.com/2/'
                'sharing/create_shared_link_with_settings')


async def async_upload_files_to_dropbox(images):
    if images is not None:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for image in images:
                tasks.append(
                    asyncio.ensure_future(
                        upload_file_and_get_url(session, image)
                    )
                )
            urls = await asyncio.gather(*tasks)
        return urls


async def upload_file_and_get_url(session, image):
    dropbox_args = json.dumps({
        'autorename': True,
        'mode': 'add',
        'path': f'/{image.filename}',
    })
    async with session.post(
        UPLOAD_LINK,
        headers={
            'Authorization': AUTH_HEADER,
            'Content-Type': 'application/octet-stream',
            'Dropbox-API-Arg': dropbox_args
        },
        data=image.read()
    ) as response:
        data = await response.json()
        path = data['path_lower']
    async with session.post(
        SHARING_LINK,
        headers={
            'Authorization': AUTH_HEADER,
            'Content-Type': 'application/json',
        },
        json={'path': path}
    ) as response:
        data = await response.json()
        if 'url' not in data:
            data = data['error']['shared_link_already_exists']['metadata']
        url = data['url']
        url = url.replace('&dl=0', '&raw=1')
    return url


# def upload_files_to_dropbox(images):
#     urls = []
#     if images is not None:
#         for image in images:
#             dropbox_args = json.dumps({
#                 'autorename': True,
#                 'path': f'/{image.filename}',
#             })
#             response = requests.post(
#                 UPLOAD_LINK,
#                 headers={
#                     'Authorization': AUTH_HEADER,
#                     'Content-Type': 'application/octet-stream',
#                     'Dropbox-API-Arg': dropbox_args
#                 },
#                 data=image.read()
#             )
#             path = response.json()['path_lower']
#             response = requests.post(
#                 SHARING_LINK,
#                 headers={
#                     'Authorization': AUTH_HEADER,
#                     'Content-Type': 'application/json',
#                 },
#                 json={'path': path}
#             )
#             data = response.json()
#             if 'url' not in data:
#                 data = data['error']['shared_link_already_exists']['metadata']
#             url = data['url']
#             url = url.replace('&dl=0', '&raw=1')
#             urls.append(url)
#     return urls

