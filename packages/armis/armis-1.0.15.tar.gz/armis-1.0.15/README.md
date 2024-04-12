# Armis Python Library

<p align="center"><strong>armis</strong> <em>- A library for interacting with the Armis cloud.</em></p>

<p align="center">
<a href="https://github.com/mmlange/armis-python/actions">
    <img src="https://github.com/mmlange/armis-python/actions/workflows/testsuite.yml/badge.svg" alt="Test Suite">
</a>
</p>

**armis** is a client library for talking to the Armis cloud.  It provides an API using **HTTP/2** by default,
falling back to **HTTP/1.1** when necessary.  Python 3.8+ is supported.

---

Install **armis** using pip:

```console
$ pip install armis
```

Now, let's get started:

```python
>>> from armis import ArmisCloud
>>> a = ArmisCloud(
        api_secret_key="your-api-secret-key-here",
        tenant_hostname="your-tenant-hostname-here.armis.com",
        fields=["id", "ipAddress", "name", "firstSeen"]
    )
>>> a.get_devices(asq='in:devices timeFrame:"10 Seconds"')
[{"id": 15, "ipAddress": "10.1.2.3", "name": "super-pc", "firstSeen": "2019-05-15T13:00:00+00:00"}]

```

## Features

**armis** gives you:

* Easy connection to the Armis cloud using an API secret key.
* A quick way to fetch devices from the cloud.
* Retries in the event the cloud times out.  This can happen with large queries that take more than 2 minutes.  This is the default for CloudFlare, which front-ends the cloud infrastructure.
* Mostly type annotated.
* Nearly 100% test coverage.


## Installation

Install with pip:

```console
$ pip install armis
```

**armis** requires Python 3.8+.

## Dependencies
**armis** relies on these excellent libraries:
* [furl](https://github.com/gruns/furl) - provides easy-to-use URL parsing and updating
* [httpx](https://github.com/encode/httpx/) - The underlying transport implementation for making HTTP requests
* [msgspec](https://github.com/jcrist/msgspec) - for lightning fast decoding of JSON
* [pendulum](https://github.com/sdispater/pendulum) - for easy date/time management
* [tenacity](https://github.com/jd/tenacity) - retry management when things fail, with great retry/backoff options


## License

`armis` is distributed under the terms of the [GPL-2.0-only](https://spdx.org/licenses/GPL-2.0-only.html) license.
