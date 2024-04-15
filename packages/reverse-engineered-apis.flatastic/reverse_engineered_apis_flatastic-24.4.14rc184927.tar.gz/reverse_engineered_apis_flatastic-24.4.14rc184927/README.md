# Reverse Engineered Flatastic API

This is a reverse engineered API schema for the flatastic API. It is not affiliated with flatastic in any way. The schema is not guaranteed to be stable, complete or correct and may change or break at any time. Please ensure that your use of this library complies with the current terms and conditions of the flatastic API.

## Usage

The package provides the generated API as a Python module. You can import it in your project like this:

```python
from reverse_engineered_apis.flatastic.api import some_api
from reverse_engineered_apis.flatastic.models.post_some_request import PostSomeRequest

request = PostSomeRequest()
request.abc = "def"
request.ghi = "jkl"

result = some_api.SomeApi().post_some_request(request)
```

## Authorization

Invoke the login endpoint to get a token and pass it in the 'x-api-key' header in subsequent requests.

## Fair Use

Please be respectful of the flatastic API and do not abuse it, that includes limiting your requests to a reasonable amount. Repeated abuse or overloading of the API might result in measures that make it harder or impossible for everyone to use the API.
