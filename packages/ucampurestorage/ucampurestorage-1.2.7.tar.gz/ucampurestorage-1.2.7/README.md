# UCAM PURE STORAGE
![Pure Storage](pure_storage.jpg "Pure Storage logo")

###### [Module Document](http://ifs-test-client1.srv.uis.private.cam.ac.uk:8080/index.html)

###### [Confluence Document](https://confluence.uis.cam.ac.uk/display/SYS/Pure+Storage+Automation+and+script)
### Introduction
The CLI developed in this project allows the user to interact with PureStorage using REST API.


With this CLI, you can list the existing volumes, servers, etc, on the Pure Storage, clone volumes, create snapshots, replace existing volumes with a golden image, etc. It is also able to configure system /etc/fstab and multipath when needed in some operations like volume mapping and mounting.

### Running the Application

#### Prerequisites
* [requests 2.30.0](https://pypi.org/project/requests/2.30.0/)
* [pyjwt](https://pypi.org/project/PyJWT/2.7.0/)[[crypto]](https://pypi.org/project/cryptography/40.0.2/)
* [paramiko 3.1.0](https://pypi.org/project/paramiko/3.1.0/)
* [distro 1.8.0](https://pypi.org/project/distro/1.8.0/)

Download the private key from the 1PASSWORD utilized to create the API account on the purestorage and fetch the credentials required.
1. Pure Storage Arrays [user and passowrd]
2. PureAPI information [client_id, key_id, client_name, storage, keyfile]

### Installation
To install the ucampurestorage pip package

RHEL 7
```
scl enable rh-python38 bash
pip install ucampurestorage
pip install urllib3==1.26.6
exit
export PATH=$PATH:/opt/rh/rh-python38/root/usr/local/bin:/opt/rh/rh-python38/root/usr/bin
```

RHEL 8 and 9
```
pip install ucampurestorage
```

CLI
The help shows how to use ucampurestorage.

```
    usage: __main__.py [-h] [-v] [--storage STORAGE] [--port PORT] [--client_id CLIENT_ID] [--key_id KEY_ID] [--client_name CLIENT_NAME] [--user USER] [--password PASSWORD] [--is_secure IS_SECURE]
                   [--record_config RECORD_CONFIG] [--file FILE] [--keyfile KEYFILE]
                   {tokengen,list,volume,host,snapshot} ...

    Manage Pure Storage Manager objects via REST API.

    positional arguments:
    {tokengen,list,volume,host,snapshot}
        tokengen            Generate Pure Storage API token to access objects. Example: ucampurestorage tokengen --keyfile "./key.pem"
        list                List Pure objects.
        volume              Operations with respect to volumes in the Pure objects.
        host                Operations with respect to hosts in the Pure objects.
        snapshot            Operations with respect to snapshots in the Pure objects.

    options:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit
    --storage STORAGE     Pure hostname. Default: uis-pure-wcdc1.srv.uis.private.cam.ac.uk
    --port PORT           Pure port. Default: 443
    --client_id CLIENT_ID
                            Pure Storage Client ID for API
    --key_id KEY_ID       Pure Storage Key ID for API
    --client_name CLIENT_NAME
                            Pure Storage Client Name for API
    --user USER           Pure Storage username
    --password PASSWORD   Pure Storage password
    --is_secure IS_SECURE
                            Secure connection. Default: False
    --record_config RECORD_CONFIG
                            Record multipath and file system config details. Default: False (do not record system config details)
    --file FILE           Read arguments from json file
    --keyfile KEYFILE     path to private keys inorder to generate token for the API call

```

For instance to get the list of volumes:

```

    python -m ucampurestorage  --client_id "25********************************0d" --key_id "f**************************************d" --client_nam "apitest" --user "pureuser" --password "****" --keyfile "/tmp/fa2xprivate.pem" list --object volumes
    05/15/2023 13:15:09 [INFO] List of volumes:
    ('all-cs-dev-db2/cs-dev-db2-vol1', {'name': 'all-cs-dev-db2/cs-dev-db2-vol1', 'created': 1674035421108, 'provisioned': 4398046511104, 'id': '8a92b2eb-d1e5-86ff-bae5-0b3e94a68352', 'serial': 'D11719CD15D049C4000117D1', 'subtype': 'regular', 'destroyed': False, 'connection_count': 1, 'source': {'id': None, 'name': None}, 'space': {'data_reduction': 20.207987278384994, 'shared': None, 'snapshots': 137571, 'system': None, 'thin_provisioning': 0.1090306097175926, 'total_physical': 1741547, 'total_provisioned': 4398046511104, 'total_reduction': 22.680899589580445, 'unique': 1603976, 'virtual': 3918524818432, 'unique_effective': 13794304, 'snapshots_effective': 19247104, 'total_effective': 33041408}, 'host_encryption_key_status': 'none', 'pod': {'id': None, 'name': None}, 'volume_group': {'id': '38422cf2-4b44-5446-e316-774881ac7a97', 'name': 'all-cs-dev-db2'}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    ('wcdc-unstretched::cs-dev-db2-vol2', {'name': 'wcdc-unstretched::cs-dev-db2-vol2', 'created': 1674036405359, 'provisioned': 4398046511104, 'id': '8eb257d2-932c-cc2c-6fc5-aee2c859133a', 'serial': 'D11719CD15D049C4000117D2', 'subtype': 'regular', 'destroyed': False, 'connection_count': 1, 'source': {'id': None, 'name': None}, 'space': {'data_reduction': 14.675370508125324, 'shared': None, 'snapshots': 0, 'system': None, 'thin_provisioning': 0.37564394995570183, 'total_physical': 61310655408, 'total_provisioned': 4398046511104, 'total_reduction': 23.504810287469954, 'unique': 61310655408, 'virtual': 2745946947584, 'unique_effective': 2745946947584, 'snapshots_effective': 0, 'total_effective': 2745946947584}, 'host_encryption_key_status': 'none', 'pod': {'id': 'dcc4618c-e160-2579-2670-a781a02dbecc', 'name': 'wcdc-unstretched'}, 'volume_group': {'id': None, 'name': None}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    ('TEST113', {'name': 'TEST113', 'created': 1683833793733, 'provisioned': 1099511627776, 'id': 'f7868879-0ccf-a062-3d00-fe9749244595', 'serial': 'D11719CD15D049C40003B438', 'subtype': 'regular', 'destroyed': False, 'connection_count': 1, 'source': {'id': None, 'name': None}, 'space': {'data_reduction': 20.153899533669993, 'shared': None, 'snapshots': 962, 'system': None, 'thin_provisioning': 0.9999810345470905, 'total_physical': 4727, 'total_provisioned': 1099511627776, 'total_reduction': 1062663.7618343926, 'unique': 3765, 'virtual': 20852736, 'unique_effective': 1810432, 'snapshots_effective': 1724416, 'total_effective': 3534848}, 'host_encryption_key_status': 'none', 'pod': {'id': None, 'name': None}, 'volume_group': {'id': None, 'name': None}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    ('TEST113_clone', {'name': 'TEST113_clone', 'created': 1683929188193, 'provisioned': 1099511627776, 'id': 'ab0d5603-6151-ad2e-5bbf-f225088b9d45', 'serial': 'D11719CD15D049C40003BB47', 'subtype': 'regular', 'destroyed': False, 'connection_count': 0, 'source': {'id': 'f7868879-0ccf-a062-3d00-fe9749244595', 'name': 'TEST113'}, 'space': {'data_reduction': 20.073879895763707, 'shared': None, 'snapshots': 0, 'system': None, 'thin_provisioning': 0.9999811537563801, 'total_physical': 9087, 'total_provisioned': 1099511627776, 'total_reduction': 1065139.5737316788, 'unique': 9087, 'virtual': 20721664, 'unique_effective': 1712128, 'snapshots_effective': 0, 'total_effective': 1712128}, 'host_encryption_key_status': 'none', 'pod': {'id': None, 'name': None}, 'volume_group': {'id': None, 'name': None}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    ('TEST113_1', {'name': 'TEST113_1', 'created': 1683937754712, 'provisioned': 1099511627776, 'id': 'a92df65f-c621-2ed8-f4a8-6cb14ca3b217', 'serial': 'D11719CD15D049C40003BBF1', 'subtype': 'regular', 'destroyed': False, 'connection_count': 1, 'source': {'id': 'f7868879-0ccf-a062-3d00-fe9749244595', 'name': 'TEST113'}, 'space': {'data_reduction': 20.12940592740464, 'shared': None, 'snapshots': 806, 'system': None, 'thin_provisioning': 0.9999810345470905, 'total_physical': 6032, 'total_provisioned': 1099511627776, 'total_reduction': 1061372.2763959866, 'unique': 5226, 'virtual': 20852736, 'unique_effective': 1810432, 'snapshots_effective': 1724416, 'total_effective': 3534848}, 'host_encryption_key_status': 'none', 'pod': {'id': None, 'name': None}, 'volume_group': {'id': None, 'name': None}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    05/15/2023 13:15:09 [INFO] [Command succeeded - Returns True]

```

You get prompt for client_id, key_id, client_name, storage, user, keyfile, password

```

    ucampurestorage  list --object volumes
    Username: pureuser
    Client ID: 25********************************0d
    Key ID: f**************************************d
    Client Name: apitest
    Private file location: /tmp/fa2xprivate.pem
    Password:
    05/15/2023 13:15:09 [INFO] List of volumes:
    ('all-cs-dev-db2/cs-dev-db2-vol1', {'name': 'all-cs-dev-db2/cs-dev-db2-vol1', 'created': 1674035421108, 'provisioned': 4398046511104, 'id': '8a92b2eb-d1e5-86ff-bae5-0b3e94a68352', 'serial': 'D11719CD15D049C4000117D1', 'subtype': 'regular', 'destroyed': False, 'connection_count': 1, 'source': {'id': None, 'name': None}, 'space': {'data_reduction': 20.207987278384994, 'shared': None, 'snapshots': 137571, 'system': None, 'thin_provisioning': 0.1090306097175926, 'total_physical': 1741547, 'total_provisioned': 4398046511104, 'total_reduction': 22.680899589580445, 'unique': 1603976, 'virtual': 3918524818432, 'unique_effective': 13794304, 'snapshots_effective': 19247104, 'total_effective': 33041408}, 'host_encryption_key_status': 'none', 'pod': {'id': None, 'name': None}, 'volume_group': {'id': '38422cf2-4b44-5446-e316-774881ac7a97', 'name': 'all-cs-dev-db2'}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    ('wcdc-unstretched::cs-dev-db2-vol2', {'name': 'wcdc-unstretched::cs-dev-db2-vol2', 'created': 1674036405359, 'provisioned': 4398046511104, 'id': '8eb257d2-932c-cc2c-6fc5-aee2c859133a', 'serial': 'D11719CD15D049C4000117D2', 'subtype': 'regular', 'destroyed': False, 'connection_count': 1, 'source': {'id': None, 'name': None}, 'space': {'data_reduction': 14.675370508125324, 'shared': None, 'snapshots': 0, 'system': None, 'thin_provisioning': 0.37564394995570183, 'total_physical': 61310655408, 'total_provisioned': 4398046511104, 'total_reduction': 23.504810287469954, 'unique': 61310655408, 'virtual': 2745946947584, 'unique_effective': 2745946947584, 'snapshots_effective': 0, 'total_effective': 2745946947584}, 'host_encryption_key_status': 'none', 'pod': {'id': 'dcc4618c-e160-2579-2670-a781a02dbecc', 'name': 'wcdc-unstretched'}, 'volume_group': {'id': None, 'name': None}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    ('TEST113', {'name': 'TEST113', 'created': 1683833793733, 'provisioned': 1099511627776, 'id': 'f7868879-0ccf-a062-3d00-fe9749244595', 'serial': 'D11719CD15D049C40003B438', 'subtype': 'regular', 'destroyed': False, 'connection_count': 1, 'source': {'id': None, 'name': None}, 'space': {'data_reduction': 20.153899533669993, 'shared': None, 'snapshots': 962, 'system': None, 'thin_provisioning': 0.9999810345470905, 'total_physical': 4727, 'total_provisioned': 1099511627776, 'total_reduction': 1062663.7618343926, 'unique': 3765, 'virtual': 20852736, 'unique_effective': 1810432, 'snapshots_effective': 1724416, 'total_effective': 3534848}, 'host_encryption_key_status': 'none', 'pod': {'id': None, 'name': None}, 'volume_group': {'id': None, 'name': None}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    ('TEST113_clone', {'name': 'TEST113_clone', 'created': 1683929188193, 'provisioned': 1099511627776, 'id': 'ab0d5603-6151-ad2e-5bbf-f225088b9d45', 'serial': 'D11719CD15D049C40003BB47', 'subtype': 'regular', 'destroyed': False, 'connection_count': 0, 'source': {'id': 'f7868879-0ccf-a062-3d00-fe9749244595', 'name': 'TEST113'}, 'space': {'data_reduction': 20.073879895763707, 'shared': None, 'snapshots': 0, 'system': None, 'thin_provisioning': 0.9999811537563801, 'total_physical': 9087, 'total_provisioned': 1099511627776, 'total_reduction': 1065139.5737316788, 'unique': 9087, 'virtual': 20721664, 'unique_effective': 1712128, 'snapshots_effective': 0, 'total_effective': 1712128}, 'host_encryption_key_status': 'none', 'pod': {'id': None, 'name': None}, 'volume_group': {'id': None, 'name': None}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    ('TEST113_1', {'name': 'TEST113_1', 'created': 1683937754712, 'provisioned': 1099511627776, 'id': 'a92df65f-c621-2ed8-f4a8-6cb14ca3b217', 'serial': 'D11719CD15D049C40003BBF1', 'subtype': 'regular', 'destroyed': False, 'connection_count': 1, 'source': {'id': 'f7868879-0ccf-a062-3d00-fe9749244595', 'name': 'TEST113'}, 'space': {'data_reduction': 20.12940592740464, 'shared': None, 'snapshots': 806, 'system': None, 'thin_provisioning': 0.9999810345470905, 'total_physical': 6032, 'total_provisioned': 1099511627776, 'total_reduction': 1061372.2763959866, 'unique': 5226, 'virtual': 20852736, 'unique_effective': 1810432, 'snapshots_effective': 1724416, 'total_effective': 3534848}, 'host_encryption_key_status': 'none', 'pod': {'id': None, 'name': None}, 'volume_group': {'id': None, 'name': None}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    05/15/2023 13:15:09 [INFO] [Command succeeded - Returns True]

```

The CLI can also read arguments from the a json file:

```

    {
    "client_id": "25********************************0d",
    "key_id": "f**************************************d",
    "client_name": "apitest",
    "storage": "purestorage.cam.ac.uk",
    "user": "pureuser",
    "password": "********,
    "keyfile": "/tmp/fa2xprivate.pem"
    }

```


To use a config file, use the option --file:

```

    ucampurestorage --file=./ucampurestorage/lib/secrets.json list --object volumes
    05/15/2023 13:09:11 [INFO] List of volumes:
    ('all-cs-dev-db2/cs-dev-db2-vol1', {'name': 'all-cs-dev-db2/cs-dev-db2-vol1', 'created': 1674035421108, 'provisioned': 4398046511104, 'id': '8a92b2eb-d1e5-86ff-bae5-0b3e94a68352', 'serial': 'D11719CD15D049C4000117D1', 'subtype': 'regular', 'destroyed': False, 'connection_count': 1, 'source': {'id': None, 'name': None}, 'space': {'data_reduction': 20.207987278384994, 'shared': None, 'snapshots': 137571, 'system': None, 'thin_provisioning': 0.1090306097175926, 'total_physical': 1741547, 'total_provisioned': 4398046511104, 'total_reduction': 22.680899589580445, 'unique': 1603976, 'virtual': 3918524818432, 'unique_effective': 13794304, 'snapshots_effective': 19247104, 'total_effective': 33041408}, 'host_encryption_key_status': 'none', 'pod': {'id': None, 'name': None}, 'volume_group': {'id': '38422cf2-4b44-5446-e316-774881ac7a97', 'name': 'all-cs-dev-db2'}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    ('wcdc-unstretched::cs-dev-db2-vol2', {'name': 'wcdc-unstretched::cs-dev-db2-vol2', 'created': 1674036405359, 'provisioned': 4398046511104, 'id': '8eb257d2-932c-cc2c-6fc5-aee2c859133a', 'serial': 'D11719CD15D049C4000117D2', 'subtype': 'regular', 'destroyed': False, 'connection_count': 1, 'source': {'id': None, 'name': None}, 'space': {'data_reduction': 14.675370508125324, 'shared': None, 'snapshots': 0, 'system': None, 'thin_provisioning': 0.37564394995570183, 'total_physical': 61310655408, 'total_provisioned': 4398046511104, 'total_reduction': 23.504810287469954, 'unique': 61310655408, 'virtual': 2745946947584, 'unique_effective': 2745946947584, 'snapshots_effective': 0, 'total_effective': 2745946947584}, 'host_encryption_key_status': 'none', 'pod': {'id': 'dcc4618c-e160-2579-2670-a781a02dbecc', 'name': 'wcdc-unstretched'}, 'volume_group': {'id': None, 'name': None}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    ('TEST113', {'name': 'TEST113', 'created': 1683833793733, 'provisioned': 1099511627776, 'id': 'f7868879-0ccf-a062-3d00-fe9749244595', 'serial': 'D11719CD15D049C40003B438', 'subtype': 'regular', 'destroyed': False, 'connection_count': 1, 'source': {'id': None, 'name': None}, 'space': {'data_reduction': 20.153899533669993, 'shared': None, 'snapshots': 962, 'system': None, 'thin_provisioning': 0.9999810345470905, 'total_physical': 4727, 'total_provisioned': 1099511627776, 'total_reduction': 1062663.7618343926, 'unique': 3765, 'virtual': 20852736, 'unique_effective': 1810432, 'snapshots_effective': 1724416, 'total_effective': 3534848}, 'host_encryption_key_status': 'none', 'pod': {'id': None, 'name': None}, 'volume_group': {'id': None, 'name': None}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    ('TEST113_clone', {'name': 'TEST113_clone', 'created': 1683929188193, 'provisioned': 1099511627776, 'id': 'ab0d5603-6151-ad2e-5bbf-f225088b9d45', 'serial': 'D11719CD15D049C40003BB47', 'subtype': 'regular', 'destroyed': False, 'connection_count': 0, 'source': {'id': 'f7868879-0ccf-a062-3d00-fe9749244595', 'name': 'TEST113'}, 'space': {'data_reduction': 20.073879895763707, 'shared': None, 'snapshots': 0, 'system': None, 'thin_provisioning': 0.9999811537563801, 'total_physical': 9087, 'total_provisioned': 1099511627776, 'total_reduction': 1065139.5737316788, 'unique': 9087, 'virtual': 20721664, 'unique_effective': 1712128, 'snapshots_effective': 0, 'total_effective': 1712128}, 'host_encryption_key_status': 'none', 'pod': {'id': None, 'name': None}, 'volume_group': {'id': None, 'name': None}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    ('TEST113_1', {'name': 'TEST113_1', 'created': 1683937754712, 'provisioned': 1099511627776, 'id': 'a92df65f-c621-2ed8-f4a8-6cb14ca3b217', 'serial': 'D11719CD15D049C40003BBF1', 'subtype': 'regular', 'destroyed': False, 'connection_count': 1, 'source': {'id': 'f7868879-0ccf-a062-3d00-fe9749244595', 'name': 'TEST113'}, 'space': {'data_reduction': 20.12940592740464, 'shared': None, 'snapshots': 806, 'system': None, 'thin_provisioning': 0.9999810345470905, 'total_physical': 6032, 'total_provisioned': 1099511627776, 'total_reduction': 1061372.2763959866, 'unique': 5226, 'virtual': 20852736, 'unique_effective': 1810432, 'snapshots_effective': 1724416, 'total_effective': 3534848}, 'host_encryption_key_status': 'none', 'pod': {'id': None, 'name': None}, 'volume_group': {'id': None, 'name': None}, 'requested_promotion_state': 'promoted', 'promotion_status': 'promoted', 'priority_adjustment': {'priority_adjustment_operator': '+', 'priority_adjustment_value': 0}})
    05/15/2023 13:09:11 [INFO] [Command succeeded - Returns True]

```

#### Application logging
Logs generated by cli are located in /var/log/ucampurestorage/

