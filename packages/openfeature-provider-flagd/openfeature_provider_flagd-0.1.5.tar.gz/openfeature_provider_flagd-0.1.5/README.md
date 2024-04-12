# flagd Provider for OpenFeature

This provider is designed to use flagd's [evaluation protocol](https://github.com/open-feature/schemas/blob/main/protobuf/schema/v1/schema.proto).

## Installation

```
pip install openfeature-provider-flagd
```

## Configuration and Usage

Instantiate a new FlagdProvider instance and configure the OpenFeature SDK to use it:

```python
from openfeature import api
from openfeature.contrib.provider.flagd import FlagdProvider

api.set_provider(FlagdProvider())
```

To use in-process evaluation in offline mode with a file as source:

```python
from openfeature import api
from openfeature.contrib.provider.flagd import FlagdProvider
from openfeature.contrib.provider.flagd.config import ResolverType

api.set_provider(FlagdProvider(
    resolver_type=ResolverType.IN_PROCESS,
    offline_flag_source_path="my-flag.json",
))
```

### Configuration options

The default options can be defined in the FlagdProvider constructor.

| Option name    | Type & Values | Default   |
|----------------|---------------|-----------|
| host           | str           | localhost |
| port           | int           | 8013      |
| schema         | str           | http      |
| timeout        | int           | 2         |

## License

Apache 2.0 - See [LICENSE](./LICENSE) for more information.
