# EWS cli tools
 
A set of command line utilities to interact with an exchange server, powered by the excellent [exchangelib](https://pypi.org/project/exchangelib/)
 
## Quick start
 
1. Clone the repo, create virtualenv and update configuration. On Ubuntu derivatives `python-dev` package is required.

    ``` 
    git clone git@github.com:flerro/ews-cli-tools.git ews-cli
    cd ews-cli
    python3 -m venv ./venv
    source ./venv/bin/activate
    pip install -r requirements.txt  
    ```



2. Create the `conf.yml` configuration file, you may refer to `conf.template.yml` for an exapmle) 
 
    ```yaml
    account:
      email: name.surname@domain.com
      domain: DOMAIN           
      user: USR1234
      password: PASSWORD
    ews:
      server: mail.domain.com      # OWA server
      chunk: 25                    # Batch size for each download request
    backup:
      months: 9                    # Backup messages until n months since today 
      delete: False                # Delete message after local download?

    ```

3. (optionally) Add the `bin` folder to path    
    
    `export PATH=$PATH:`pwd`/bin`
  
  
## Available Tools
 
### Backup email messages
 
`backup.sh` tool will download messages from `inbox` and `sent` folders and store them locally. 
Downloaded messages can be optionally removed from server.

Each message is saved to a self-contained `.eml` file, named after message date-time and subject. 
The backup folder is organized by folder, year and month. Messages in inbox folder are also organized by sender.

 ```shell
account
├── inbox
│   ├── 2018
│   │   ├── 02
│   │   │   ├── sender1@aaa.it
│   │   │   │   ├── 2018-02-01_0722___subject1.eml
│   │   │   │   └── 2018-02-10_1137___subject2.eml
...
│
└── sent
    ├── 2018
    │   ├── 03
    │   │   ├── 2018-03-01_0722___subject1.eml
    │   │   └── 2018-03-10_1137___subject2.eml
    ...
    └── 2019
        ├── 03
        │   ├── 2019-03-07_0722___subject1.eml
        │   └── 2019-03-11_1137___subject2.eml
        ...
```

**N.B.** `inbox` and `sent` sub-folders are currently not processed
 
Email message stored as self-contained `.eml` files. Use `google-chrome` or similar to read message content, 
`munpack` to extract attachments. 
 
 ```bash
$ sudo apt-get install mpack
$ munpack email.eml 
tempdesc.txt: File exists
image001.jpg.3 (image/jpeg) 
```


 
  