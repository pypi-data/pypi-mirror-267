<!-- PROJECT LOGO -->
<br />
<p align="center">
  <!-- <a href="https://github.com/agentsea/skillpacks">
    <img src="https://project-logo.png" alt="Logo" width="80">
  </a> -->

  <div style="display: flex; align-items: center; justify-content: center;">
    <h1>OpenCredit</h1>
      <img src="https://icons.iconarchive.com/icons/ph03nyx/super-mario/256/Retro-Coin-icon.png" alt="SurfDino Logo" width="50" height="50" style="border-radius: 20px; margin-left: 10px; margin-bottom: 20px;">
  </div>
  <p align="center">
    Credit management for pay-per-use applications
    <br />
    <a href="https://github.com/agentsea/opencredit"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/agentsea/opencredit">View Demo</a>
    ·
    <a href="https://github.com/agentsea/opencredit/issues">Report Bug</a>
    ·
    <a href="https://github.com/agentsea/opencredit/issues">Request Feature</a>
  </p>
  <br>
</p>

## Installation

```python
pip install opencredit
```

## Usage

### Connect

Get an API key

```sh
opencredit login https://foo.bar
```

Connect the Python client

```python
import os
from opencredit import Client

client = Client(addr="https://foo.bar", api_key=os.getenv("OPENCREDIT_API_KEY"))
```

### Define a credit type

Define a credit type for your application.

```python
client.create_credit(
        name="MyAppCredit",
        description="Credit for my awesome application"
        user_minimum=-20.00,
        user_maximum=10000.00,
        user_start=10.00,
    )
```

`user_minimum` is the default minimum credit a user can have.  
`user_maximum` is the default maximum credit a user can have.  
`user_start` is the default starting credit a user has.

### Per user configuration

Add credits for a user

```python
client.add_user_credit(credit="MyAppCredit", email="dolores@agentsea.ai", amount=100.00)
```

Set per user limits

```python
client.set_user_limits(
        credit="MyAppCredit",
        email="dolores@agentsea.ai",
        user_minimum=-20.00,
        user_maximum=10000.00,
        user_start=200.00
    )
```

Set automatic top up

```python
client.set_user_topup(
        credit="MyAppCredit",
        email="dolores@agentsea.ai",
        min_balance=5.00,
        topup_amount=10.00
    )
```

### Use credits

See how many credits the user currently has

```python
client.get_balance(credit="MyAppCredit", email="dolores@agentsea.ai")
```

Create a meter to charge credits based on type of usage

```python
client.create_meter(
        credit="MyAppCredit",
        name="llm_tokens",
        unit="token",
        cost=0.0004,
        description="LLM generated tokens"
    )
```

Tik the meter to use credits

```python
client.tik_meter(name="llm_tokens", amount=200, email="dolores@agentsea.ai")
```

### Reporting

Get a report of credit usage

```python
client.get_report(
        credit="MyAppCredit",
        email="dolores@agentsea.ai",
        start="2020-01-01",
        end="2020-01-31"
    )
```

## Hosting a credit server

Run locally

```python
from opencredit import Server

server = Server(backend="postgres")

server.serve()
```

Run on Kubernetes

```sh
helm install open-credit-server --set backend=postgres open-credit
```
