# Available
This endpoint contains a list of the episode production numbers which represents the transcripts the API was able to successfully fetch from source, and cache locally. The production codes in this list are the whole set of episodes that can and will be searched from, scripts.

|   HTTP Request   | Parameters |                              Returns                             |
|:----------------:|:----------:|:----------------------------------------------------------------:|
| GET `/available` |    None    | A list of available transcripts by their production-code labels. |
