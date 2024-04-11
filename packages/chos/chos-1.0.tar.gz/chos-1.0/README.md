<div align="center">
<h1>Chos</h1>
<p>Search your favorite songs/artists/playlists/genres</p>
<p>Get details and recommendations</p>
</div>


<h2>Installation:</h2>

```bash
python3 -m pip install chos
```

<h2>Examples:</h2>

<h3>chos:</h3>

```python
from chos import Chos

# Search based on [track, artist, playlist] id
Chos.Search('Powerwolf', basedon='artist', limit=10)

# Get Details based on [track, artist, playlist] id 
Chos.GetDetails('0bUgTRe5st6TMbRCEjKezX', basedon='track', limit=10)

# Get recommendation based on [track, artist, playlist] id or [genre] name
Chos.GetRecommendation('0bUgTRe5st6TMbRCEjKezX', basedon='track', limit=10)
```

<h3>chos.sync:</h3>

```python
import asyncio
from chos.sync import Chos

async def my_test():
    # Search based on [track, artist, playlist] id
    await Chos.Search('Powerwolf', basedon='artist', limit=10)
    
    # Get Details based on [track, artist, playlist] id 
    await Chos.GetDetails('0bUgTRe5st6TMbRCEjKezX', basedon='track', limit=10)
    
    # Get recommendation based on [track, artist, playlist] id or [genre] name
    await Chos.GetRecommendation('0bUgTRe5st6TMbRCEjKezX', basedon='track', limit=10)
    
asyncio.run(my_test())
```
