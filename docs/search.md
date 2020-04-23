# Search
This endpoint performs a parameterized search, based on the options listed below.

At least one `character` or one `dialogue` is required for a search. If neither are provided, then a `406` is returned, citing invalid arguments.

Multiple of each parameter can be provided. Adding multiple of one parameter acts as a logical OR to the search terms.

|  HTTP Request | Headers |              Parameters              | Returns                                                    |
|:-------------:|:-------:|:------------------------------------:|------------------------------------------------------------|
| GET `/search` |   None  | [ `episode`, `character`, `dialogue` ] | A list of `Line` instances matching the search parameters. |

## JSON Payload
| Name               | Type          | Description                                                               |
|--------------------|---------------|---------------------------------------------------------------------------|
| search_results | array\<Line> | A list of `Line` objects that matched the search terms.               |
| missing_episodes   | array\<number> | A list of episodes, by production code, that are missing or non-existant. |
| search_time        | number        | Time in seconds it took to service the request.                           |

## Line

The json contents of a single line:

|       Name       |    Type   |                       Description                      |
|:----------------:|:---------:|:------------------------------------------------------:|
| `episode_number` |   number  | The production code of the episode                     |
|    `timestamp`   | Timestamp | A `Timestamp` object, for start/end times of a dialogue. |
|      `name`      |   string  | The name of the actor.                                 |
|    `dialogue`    |   string  | The dialogue of the actor.                             |

## Timestamp

|  Name |  Type  |           Description           |
|:-----:|:------:|:-------------------------------:|
|  `in` | string | The start time of the dialogue. |
| `out` | string | The end time of the dialogue.   |
