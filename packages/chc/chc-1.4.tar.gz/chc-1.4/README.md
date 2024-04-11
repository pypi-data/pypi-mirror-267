<div align="center">
<h1>CHC</h1>
<p>Search your favorite songs/artists/playlists/genres</p>
<p>Get details and recommendations</p>
</div>


<h2>Installation:</h2>

```bash
python3 -m pip install chc
```

<h2>Examples:</h2>

<h3>Chc:</h3>

```python
from chc import Chc

# Search based on [track, artist, playlist] id
Chc.Search('Powerwolf', basedon='artist', limit=10)

# Get Details based on [track, artist, playlist] id 
Chc.GetDetails('0bUgTRe5st6TMbRCEjKezX', basedon='track')

# Get recommendation based on [track, artist, playlist] id or [genre] name
Chc.GetRecommendation('0bUgTRe5st6TMbRCEjKezX', basedon='track', limit=10)
```

<h3>Chc.sync:</h3>

```python
import asyncio
from chc.sync import Chc

async def my_test():
    # Search based on [track, artist, playlist] id
    await Chc.Search('Powerwolf', basedon='artist', limit=10)
    
    # Get Details based on [track, artist, playlist] id 
    await Chc.GetDetails('0bUgTRe5st6TMbRCEjKezX', basedon='track')
    
    # Get recommendation based on [track, artist, playlist] id or [genre] name
    await Chc.GetRecommendation('0bUgTRe5st6TMbRCEjKezX', basedon='track', limit=10)
    
asyncio.run(my_test())
```
