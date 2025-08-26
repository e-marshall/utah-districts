# Utah bb

This is a toy CLI tool to learn about gerrymandering of congressional districts in Utah. It uses data from the [Princeton Gerrymandering Project](https://gerrymander.princeton.edu/) and [Utah Legistlative Redistricting Committee](https://citygate.utleg.gov/legdistricting/utah/comment_links). 

## Current functionality
- See the report card score of an enacted map
`uv run utah-bb see-score` (default & only implemented arg is 'Utah').

- See compactness of enacted and proposed congressional maps
`uv run utah-bb see-compactness --mtype 'proposed' ` or `uv run utah-bb see-compactness --mtype 'enacted'`

- Compare compactness of the enacted and proposed maps
`uv run utah-bb compare-compactness`

All statistics & scoring is from [Princeton Gerrymandering Project](https://gerrymander.princeton.edu/).