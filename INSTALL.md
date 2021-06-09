INSTALL ACACIA
==============

Acacia setup requires GitHub CLI. On Ubuntu this can be installed
with

```
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

For more details see https://cli.github.com/


Acacia is a Python 3 based application which uses
SQLite3 for intermediate data storage. You can
install it using Python's pip and the
requirements.txt file.

```shell
    python3 -m pip install -r requirements.txt
```


