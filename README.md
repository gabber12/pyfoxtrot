## Foxtrot client

### Installation
```sh
pip install pyfoxtrot
```

### Usage

```python
from foxtrot import Foxtrot
client = Foxtrot("http://foxtrot.domain.com", auth_token="<TOKEN>")
data = client.fql("select * from test")

# Use for analysis
df = data.toPandas()
df.head()
df.describe


# Convert dot notated documents to json
df = data.toJson()
```

