# Available
This endpoint contains a list of the episode production numbers which represents the transcripts the API was able to successfully fetch from source, and cache locally. The production codes in this list are the whole set of episodes that can and will be searched from, scripts.

|   HTTP Request   | Parameters |                              Returns                             |
|:----------------:|:----------:|:----------------------------------------------------------------:|
| GET `/available` |    None    | A list of available transcripts by their production-code labels. |

## JSON Payload
| Name               | Type          | Description                                                               |
|--------------------|---------------|---------------------------------------------------------------------------|
| available_episodes | array\<number> | A list of episodes, by production code, that are available.               |
| missing_episodes   | array\<number> | A list of episodes, by production code, that are missing or non-existant. |
| search_time        | number        | Time in seconds it took to service the request.                           |
