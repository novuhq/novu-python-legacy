<p align="center">
  <a href="https://notifire.co">
    <img width="200" src="https://notifire.co/img/logo.png">
  </a>
</p>

<h1 align="center">Notifire Python Wrapper</h1>

<div align="center">

A python wrapper for the Notifire API

</div>

## ✨ Features

- 🌈 Trigger new notifications from python
- 📦 Easy to setup and integrate
- 🛡 Written with Pydantic for data validation.

## 📦 Install

```bash
mkdir .notifire && cd .notifire && git clone git@github.com:notifirehq/python.git
```

## 🔨 Usage

```python
from .notifire.python.wrapper import Notifire
import os

notifire = Notifire(os.process.env.NOTIFIRE_API_KEY)
notifire.trigger(
    '<REPLACE_WITH_EVENT_NAME>',
    '<USER_IDENTIFIER>',
    first_name='<FIRST_USER_NAME>' # first_name, last_name, email and channels are optional
    custom_attribute='<CUSTOM_ATTRIBUTE_VALUE>' # use custom attributes from each event here
)

```

## 🔗 Links

- [Home page](https://notifire.co/)