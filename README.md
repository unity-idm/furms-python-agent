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

List of all allocations for site with identifier: fzj-x
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
  -c CUMULATIVE_CONSUMPTION, --cumulative-consumption CUMULATIVE_CONSUMPTION
                        value how much of an allocation should be reported as consumed
  -a ALLOCATION_ID, --allocation-id ALLOCATION_ID
                        allocation id
  -u FENIX_USER_ID, --fenix-user-id FENIX_USER_ID
                        if provided then per-user record is sent together with cumulative allocation data

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
