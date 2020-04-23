# Script
This endpoint gets a raw transcript base on the single-parameter: episode specified and triggers a browser download of it.

`episode` is the only parameter searched for. If more than one `episode` field is provided, only the first occurrence will be used.


|    HTTP Request    | Parameters |                  Returns                 |
|:------------------:|:----------:|:----------------------------------------:|
| GET `/script` |    `episode`    | An x-www-form version of the transcript requested. (.i.e it starts a download of the transcript file requested). |
