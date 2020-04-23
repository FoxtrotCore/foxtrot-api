# Clear Cache
This endpoint clears the API's local cache, forcing it to refetch all transcripts from its configured source. This endpoint requires an API token in order to use.


|    HTTP Request    |    Headers    | Parameters | Returns                                  |
|:------------------:|:-------------:|:----------:|------------------------------------------|
| POST `/clearcache` | Authorization | None       | A permanent redirect to `GET /available` |
