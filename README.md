# oriyao-flask
> My personal website use flask
Update 2021/1/19

## Get git clone link
> https://github.com/oriyao/oriyao-flask

## Copy Clone HTTPS links
> https://github.com/oriyao/oriyao-flask.git


## Git clone from Github
> git clone https://github.com/oriyao/oriyao-flask.git


## Show local files
```
.
├── LICENSE
├── oriyao
│  ├── additional
│  ├── base
│  ├── data
│  ├── forms
│  ├── home
│  ├── __init__.py
│  ├── mydb
│  ├── setting.py
│  ├── tables
│  └── ui
├── oriyao.py
├── README.md
└── uploads
    └── logs
```

## Pull container image
```
# podman pull docker.io/tiangolo/uwsgi-nginx-flask
Trying to pull docker.io/tiangolo/uwsgi-nginx-flask...Getting image source signatures
Copying blob 6c33745f49b4: 48.06 MiB / 48.06 MiB [=========================] 56s
Copying blob ef072fc32a84: 7.45 MiB / 7.45 MiB [===========================] 56s
Copying blob c0afb8e68e0b: 9.53 MiB / 9.53 MiB [===========================] 56s
Copying blob d599c07d28e6: 49.43 MiB / 49.43 MiB [=========================] 56s
Copying blob f2ecc74db11a: 183.40 MiB / 183.40 MiB [=======================] 56s
Copying blob 26856d31ce86: 5.86 MiB / 5.86 MiB [===========================] 56s
Copying blob 48268e67e08d: 17.39 MiB / 17.39 MiB [=========================] 56s
Copying blob 851553cad175: 233 B / 233 B [=================================] 56s
Copying blob 6ed59c16487d: 2.04 MiB / 2.04 MiB [===========================] 56s
Copying blob 6ade896a4ee7: 1.34 KiB / 1.34 KiB [===========================] 56s
Copying blob 5ec0e37df1b6: 3.94 MiB / 3.94 MiB [===========================] 56s
Copying blob 4f6c72509119: 4.36 MiB / 4.36 MiB [===========================] 56s
Copying blob bbc02d793499: 177 B / 177 B [=================================] 56s
Copying blob 7d12e1b22bfd: 379 B / 379 B [=================================] 56s
Copying blob 7e8bb239f5d6: 1.25 MiB / 1.25 MiB [===========================] 56s
Copying blob 2d46ec561967: 369 B / 369 B [=================================] 56s
Copying blob d4b6fa41b651: 320 B / 320 B [=================================] 56s
Copying blob f48ab5bf399a: 320 B / 320 B [=================================] 56s
Copying blob c62912515bd6: 1.15 KiB / 1.15 KiB [===========================] 56s
Copying blob ece78d4ba686: 1.15 KiB / 1.15 KiB [===========================] 56s
Copying blob 6b7e6ce53520: 566 B / 566 B [=================================] 56s
Copying blob 7b582569db67: 1.83 MiB / 1.83 MiB [===========================] 56s
Copying blob 0f653a39a01a: 585 B / 585 B [=================================] 56s
Copying blob da8807674160: 1.19 KiB / 1.19 KiB [===========================] 56s
Copying blob 5ae47c5d112e: 769 B / 769 B [=================================] 56s
Copying blob 21869bc5d89b: 769 B / 769 B [=================================] 56s
Copying config 6ea734e365fb: 14.73 KiB / 14.73 KiB [========================] 0s
Writing manifest to image destination
Storing signatures
6ea734e365fb09c913c92b4be7e2b6ca397c31407334801ae6d62db5e1f07bbd
```

## Show container image
```
# podman images
REPOSITORY                                       TAG      IMAGE ID       CREATED         SIZE
docker.io/tiangolo/uwsgi-nginx-flask   latest   6ea734e365fb   13 days ago     936 MB
```

## Run mongo database container
```
podman run -it -d \
-v /home/mongodata:/data/db --privileged=true \
-p 27017:27017 \
-e MONGO_INITDB_ROOT_USERNAME=oriyao \
-e MONGO_INITDB_ROOT_PASSWORD=cnp200 \
--name mongodb \
docker.io/library/mongo
```

## Run mongo-express webclient container
```
podman run -it -d \
--name mongo-express \
-p 8081:8081 \
-e ME_CONFIG_MONGODB_PORT=27017 \
-e ME_CONFIG_MONGODB_SERVER=152.32.132.155 \
-e ME_CONFIG_MONGODB_ADMINUSERNAME=oriyao \
-e ME_CONFIG_MONGODB_ADMINPASSWORD=cnp200 \
-e ME_CONFIG_BASICAUTH_USERNAME=oriyao \
-e ME_CONFIG_BASICAUTH_PASSWORD=cnp200 \
docker.io/library/mongo-express 
```

## Run container service
```
podman run -d \
--name gentelella \
-p 1981:80 \
-v /home/flask-gentelella:/app \
--privileged=true \
-e FLASK_APP=gentelella.py \
-e FLASK_DEBUG=1 \
docker.io/tiangolo/uwsgi-nginx-flask \
flask run --host=0.0.0.0 --port=80
```

## Install requirements
```
podman exec -it gentelella bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Access Website
> Go to http://server_address:1981

# Example [oriyao](http://www.openstack.top/)

