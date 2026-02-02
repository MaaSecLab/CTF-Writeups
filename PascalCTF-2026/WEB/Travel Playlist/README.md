# Challenge Writeup — Travel Playlist

## Description
This challenge involves an API endpoint intended to return JSON data based on an index value. By supplying out-of-bounds input, the application reveals that it is attempting to read files from disk. This behavior can be abused to perform a path traversal and read arbitrary files, ultimately allowing the flag to be retrieved from the filesystem.

## Initial Endpoint Behavior

The application exposes the following endpoint `POST /api/get_json` which expects JSON input containing an index value.

A valid index returns a JSON object representing a playlist entry.

![[Pasted image 20260202203013.png]]
## Out-of-Bounds Behavior

When an invalid index is supplied, such as a negative value, the server responds with an error indicating that a file was not found. This suggests the backend is likely using the index value to construct a file path on disk rather than strictly validating it.

![[Pasted image 20260202203037.png]]
## Path Traversal

Since the index value is not properly sanitized, directory traversal sequences can be supplied instead of a numeric index. By using relative path traversal, arbitrary files can be read.

The server responds with the contents of the file.

![[Pasted image 20260202203117.png]]

