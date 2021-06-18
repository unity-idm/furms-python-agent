# Preparation of virtual environment for demo agent

## Create virtual environment if not already
```
python3 -m venv furms-agent-venv
```

## Activate virtual environment
```
source furms-agent-venv/bin/activate
```

## Setup virtual environment if not already
```
pip3 install -r requirements.txt
```

## Install the `furms` client library
The demo agent has been developed on top of the `furms` client library.
Let's install it in our venv:
## Build your library
```
python3 setup.py bdist_wheel
```

## Library installation steps
```
pip3 install dist/furms-1.0.0-py3-none-any.whl
```


# Running demo agent
The demo agent has been developed on top of the `furms` library and can be found in `demo-agent` directory.
Configure credentials by setting the following environmental variables:
```
export BROKER_HOST=<broker-host>
export BROKER_PORT=<broker-port>
export BROKER_USERNAME=<broker-username>
export BROKER_PASSWORD=<broker-password>
export BROKER_VIRTUAL_HOST=<broker-virtual-hsot>
export CA_FILE=<path to CA file in PEM format>
```
If aforementioned variables are not present a default values takes place:
* host - 127.0.0.1
* port - 4444
* password - guest
* user - guest
* virtual host - "/"
* exchange - "" - default amq exchange
* cafile - ./ca_certificate.pem
```
source furms-agent-venv/bin/activate # skip it if you already activated virtual env
cd demo-agent
./demo-agent.sh <site-id-from-furms-ui>
```

## Report consumption of allocation
The demo agent package comes with a separate command line tool to report resource consumption within particular allocation. Optionally you can also provide FENIX user Id to report consumption for given user.

The `report-usage.sh` tool requires site identifier and offers two commands to: 
* list allocations,
* push the consumption record.

### `list-allocations` command (alias: list)
This command is used to show all allocations provisioned to given site. 
```
cd demo-agent
./report-usage.sh --site SITE_ID list-allocations

List of all allocations for site with identifier: SITE_ID
[
    {
        "allocationIdentifier": "a4695995-35ec-4bb8-b38b-a44829ec94e1",
        "projectIdentifier": "5f655360-29b1-48ef-aaa1-75dd2db1e598",
        "resourceCreditIdentifier": "5e6a7b3b-0377-4c73-a73f-180d794fc12d",
        "amount": 100.0,
        "validFrom": "2021-04-23T03:22:00Z",
        "validTo": "2024-08-12T05:32:00Z"
    },
    {
        "allocationIdentifier": "b90414d9-3f39-45ec-b50e-3cdea407e906",
        "projectIdentifier": "5f655360-29b1-48ef-aaa1-75dd2db1e598",
        "resourceCreditIdentifier": "5e6a7b3b-0377-4c73-a73f-180d794fc12d",
        "amount": 200.0,
        "validFrom": "2021-04-23T03:22:00Z",
        "validTo": "2024-08-12T05:32:00Z"
    }
]

```

### `publish-usage` command (alias: pub)
This option is used to report consumption for given allocation and optionally fiven user.
```
cd demo-agent
./report-usage.sh --site SITE_ID publish-usage --help
usage: report-usage.sh publish-usage [-h] -c CUMULATIVE_CONSUMPTION -a ALLOCATION_ID [-u FENIX_USER_ID]

optional arguments:
  -h, --help            show this help message and exit
  -u FENIX_USER_ID, --fenix-user-id FENIX_USER_ID
                        when provided then only per-user record is sent

required arguments:
  -c CUMULATIVE_CONSUMPTION, --cumulative-consumption CUMULATIVE_CONSUMPTION
                        value how much of an allocation should be reported as consumed
  -a ALLOCATION_ID, --allocation-id ALLOCATION_ID
                        allocation id

./report-usage.sh --site SITE_ID publish-usage -c 10 -a a4695995-35ec-4bb8-b38b-a44829ec94e1
2021-06-14 09:50:14,557 furms.sitelistener [INFO] message published to SITE_ID-site-pub (exchange: 'SITE_ID-site-pub') payload:
{
  "header": {
    "version": 1,
    "status": "OK"
  },
  "body": {
    "CumulativeResourceUsageRecord": {
      "projectIdentifier": "5f655360-29b1-48ef-aaa1-75dd2db1e598",
      "allocationIdentifier": "a4695995-35ec-4bb8-b38b-a44829ec94e1",
      "cumulativeConsumption": 10.0,
      "probedAt": "2021-06-14T07:50:14Z"
    }
  }
}
```
## Alloation chunk update
The demo agent package comes with a separate command line tool to update particular allocation chunk.

The `chunk-update.sh` tool requires site identifier and offers two commands to: 
* list all chunks,
* push chunk update.

### `list-chunks` command (alias: list)
This command is used to show all chunks for given site. 
```
cd demo-agent
./chunk-update.sh --site SITE_ID list-chunks
List of all chunks for site with identifier: SITE_ID
[
    {
        "allocId": "16e51bd3-6cea-4566-9092-619921a3a7b9",
        "chunkId": 0,
        "amount": 1001.0,
        "validFrom": "2020-04-23T03:22:00Z",
        "validTo": "2028-04-22T03:22:00Z"
    },
    {
        "allocId": "16e51bd3-6cea-4566-9092-619921a3a7b9",
        "chunkId": 1,
        "amount": 200.0,
        "validFrom": "2022-12-17T16:27:00Z",
        "validTo": "2024-08-12T05:32:00Z"
    }
```

### `publish-update` command (alias: pub)
This option is used to publish chunk update.
```
cd demo-agent
./chunk-update.sh -s SITE_ID publish-update --help
usage: chunk-update.sh publish-update [-h] -a ALLOCATION_ID -c CHUNK_ID --amount AMOUNT [-f VALID_FROM] [-t VALID_TO]

optional arguments:
  -h, --help            show this help message and exit
  -f VALID_FROM, --valid-from VALID_FROM
                        when provided then send in a protocol in validFrom field, if not provided then current provisioned value is taken
  -t VALID_TO, --valid-to VALID_TO
                        when provided then send in a protocol in validTo field, , if not provided then current provisioned value is taken

required arguments:
  -a ALLOCATION_ID, --allocation-id ALLOCATION_ID
                        allocation id
  -c CHUNK_ID, --chunk-id CHUNK_ID
                        chunk id
  --amount AMOUNT       chunk amount to be updated in FURMS


./chunk-update.sh -s SITE_ID pub -a 16e51bd3-6cea-4566-9092-619921a3a7b9 -c 0 --amount 1001 -t 2028-04-22T03:22:00Z -f 2020-04-23T03:22:00Z
2021-06-18 12:06:04,635 furms.sitelistener [INFO] message published to SITE_ID-site-pub (exchange: 'SITE_ID-site-pub') payload:
{
  "header": {
    "version": 1,
    "messageCorrelationId": null,
    "status": "OK"
  },
  "body": {
    "ProjectResourceAllocationUpdate": {
      "allocationIdentifier": "16e51bd3-6cea-4566-9092-619921a3a7b9",
      "allocationChunkIdentifier": 0,
      "amount": 1001.0,
      "validFrom": "2020-04-23T03:22:00Z",
      "validTo": "2028-04-22T03:22:00Z"
    }
  }
}

```