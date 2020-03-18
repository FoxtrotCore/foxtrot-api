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

**Only** one character or one dialogue is required to kick off a search but neither required for a search. The episode field is fully optional.

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

**(WARNING: This WILL slow down your search time. Usually by a factor of 10x ~ 12s avg.)**

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
