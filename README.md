# FUSIC
A file system in userspace (FUSE) based music metadata generator

### Current Usage
Currently under development, but FUSIC has a basic utility to download all of the lyrics of the tracks by user-provided artist.  
If you still want to use this feature:
1. Create a developer account on [Spotify](https://developer.spotify.com/) if you don't have one.
2. Fill the `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET` variables in `src/gui.py` with your Spotify keys.
3. Run `src/fusic.py`.
