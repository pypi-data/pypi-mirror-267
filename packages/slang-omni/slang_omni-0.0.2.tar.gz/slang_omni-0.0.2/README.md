## Python Library for Slang Omni

This is the python library for using Slang Omni Co-pilots

### Example

```
from omni_python.client import AsyncOmniClient
omni_client = AsyncOmniClient(
    assistant_id="<YOUR_ASSISTANT_ID>", 
    assistant_version="<YOUR_ASSISTANT_VERSION>", 
    api_key="<YOUR_API_KEY>"
)
res = omni_client.text2action("how are you", stream=True)
async for i in res:
    print(i)
```