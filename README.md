# foxtrot-api
An API for searching FTF transcripts.

# Endpoints:

### GET
***
`/search`: _Search FTF transcripts._

  **Parameters:**

  * `episode`: Integer [0 - 95] Episode to be searched.
  * `character`: String [Case insensitive] Filter by character.
  * `dialogue`: String [Case insensitive] Filter by dialogue.


**All** of these parameters are repeatable if more than one is desired.

**Exs:**

  `/search?episode=1&episode=2`
  `/search?character=jim&dialogue=rather not talk about it`

**Returns:**
```json
{
  "search_results": [],
  "missing_eps": [],
  "search_time": 0.0
}
```

*(Note: If no episodes are specified then all available episodes will be searched.)*

**(WARNING: This WILL slow down your search time.)**

***

`/available`: _Get a list of currently available transcripts._

**Returns:**
```json
{
  "available_episodes": [],
  "search_time": 0.0
}
```

***
