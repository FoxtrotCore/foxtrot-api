| METHOD |           HTTP Request          |                                      Description                                     |
|:------:|:-------------------------------:|:------------------------------------------------------------------------------------:|
|   GET  |      [`/`](./endpoints.md)      | Gets the info page for Foxtrot-API.                                                  |
|   GET  |  [`/available`](./available.md) | Gets a list of episode numbers that are available and cached for Foxtrot-API         |
|  POST  | [`/clearcache`](/clearcache.md) | Force clears Foxtrot-API's cache of subtitles and re-fetches everything from source. |
|   GET  |     [`/script`](./script.md)    | Gets a singular script                                                               |
|   GET  |     [`/search`](./search.md)    | Gets a list of `Line` objects based on a parameterized search.                       |
