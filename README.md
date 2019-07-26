# Auth service

The main goal of this service is providing access to VPN servers for end users.

## API

For available API methods see the `src/router` module. 

API request example:
```bash
curl -X GET \
  http://127.0.0.1:5000/api/shadowsocks/key/random/3/ \
  -H 'api-key: SCRET_KEY_1'
```
Response:
```json
[
    {
        "cipher": "chacha20-ietf-poly1305",
        "created_ts": 1564131453.797555,
        "is_enabled": true,
        "key_id": "1297e2d9-8f44-461d-9c5c-4e1b29dddaec",
        "port": 9000,
        "secret": "3e0bee31-afa0-4d39-ad15-6e2bc7c6e22b",
        "user_id": "5522279d-8022-489b-8dd5-4137e8123458"
    },
    {
        "cipher": "chacha20-ietf-poly1305",
        "created_ts": 1564131453.787383,
        "is_enabled": true,
        "key_id": "1bf3b259-a669-4652-8faa-38f96551ac4c",
        "port": 9000,
        "secret": "b25b151e-b428-433a-a857-9e27e1c6768c",
        "user_id": "8d34b75b-3e71-4c17-a52b-7d4392d2ba11"
    },
    {
        "cipher": "chacha20-ietf-poly1305",
        "created_ts": 1564131453.842693,
        "is_enabled": true,
        "key_id": "483c08f3-2eb2-44d8-8274-97ef1b3bb938",
        "port": 9000,
        "secret": "b42df82c-efa7-4833-a4e5-2b2e2d61a322",
        "user_id": "bb86ad45-5d5d-4ad0-a5d4-062d5e67a3e2"
    }
]
```

## Launching as docker container

All commands below should be executed from `/src` directory.

Build docker image 
```bash
docker build -t auth_service .
```

Run docker container 
```bash
docker run --name my_auth_service -d -p 5000:5000 auth_service
```

You could configure service using `ENV` variables:
 - `API_KEYS` HTTP(s) API keys for auth_service API. default:`"YOUR_API_KEY_1;YOUR_API_KEY_2;YOUR_API_KEY_3"`
 - `ROTATE_SHADOWSOCKS_KEYS_EACH_X_SECONDS` default:`86400`                
 - `SHADOWSOCKS_KEYS_LIMIT` default:`3000`
 - `SS_KEY_PORT` default:`9000`
 - `CIPHER` default:`chacha20-ietf-poly1305`
 - `LOG_LVL` default:`INFO`                                                
 - `DEBUG` default:`0`
 - `DISABLE_API_KEY_AUTH` default:`0`  
 - ...                                    

It just overwriting variables at `.env` file (see `src/settings/.env` for details)

Example:
```bash
docker run -d \
    --name my_auth_service \
    --env DEBUG=0 \
    --env DISABLE_API_KEY_AUTH=0 \
    --env API_KEYS="SCRET_KEY_1;SECRET_KEY_2" \
    -p 127.0.0.1:5000:5000 \
    auth_service 
```

Also you would configure service using docker `volume` option and passing `.env` 
file to docker container instead of `src/settings/.env`

## Launching as docker container in `DEV` mode

Create `src/dev_run.sh` with following content:

```bash
#!/bin/bash

docker container stop dev_auth_service &>/dev/null
docker container rm --force dev_auth_service &>/dev/null
docker rmi auth_service &>/dev/null
docker build -t auth_service .
docker run -d \
    --name dev_auth_service \
    --env DEBUG=1 \
    --env DISABLE_API_KEY_AUTH=1 \
    -p 127.0.0.1:5000:5000 \
    auth_service
docker container list
```

Now you may just run `bash dev_run.sh` to rebuild image and launch container