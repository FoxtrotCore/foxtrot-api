# Search
This endpoint gets a raw transcript base on the single-parameter: episode specified.

`episode` is the only parameter searched for. If more than one `episode` field is provided, only the first occurrence will be used.


|  HTTP Request | Headers |              Parameters              | Returns                                                    |
|:-------------:|:-------:|:------------------------------------:|------------------------------------------------------------|
| GET `/search` |   None  | [`episode`, `character`, `dialogue`] | A list of `Line` instances matching the search parameters. |


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
