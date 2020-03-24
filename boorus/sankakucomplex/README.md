# Sankaku Complex
Downloads images and videos from Sankaku Complex.

## Prerequisites
* Python 3.6 or newer
* The requests module
    * `pip install --user requests`

## Usage
Starting the script:
`python -i sankaku_complex.py`

Searching for generic tags:
`search('Tag1+Tag2+Tag3')`

Searching for series-specific tags:
`search('Tag1+Tag2+Tag3', 'One Piece')`

Changing the timeout setting *(example for 8 second timeouts)*:
`settings.set_timeout(8)`

Disable file streaming:
`settings.set_stream(False)`

The search parameters are case-insensitive and they are not guaranteed to function well with non-ASCII characters.
The timeout setting is effective for every single request sent to the website for a total of 6 requests per file.

## Known Issues
* HTTP 429 when timeout parameter is set lower than 4 seconds.
    * This is caused by the site's ratelimiter which inhibits scripts such as this one from using up too much bandwidth.
    * The known solution for this is to:
        * Quit the downloading by spamming **CTRL + C** repeatedly.
        * Increment the timeout setting `settings.set_timeout(settings.timeout + 1)`
        * Wait a minute or two before re-running the `search` function.
* Incomplete/partially complete data.
    * This is caused by the requests library's stream parameter which is enabled by default.
    * The known solution for this is to:
        * Quit the downloading by spamming **CTRL + C** repeatedly.
        * Deleting the incomplete/partially complete data from the folder.
        * Disable data streaming with `settings.set_stream(False)`
        * Then re-run the `search` function.

## Upcoming Features
* Replacing requests with aiohttp for asyncio functionality.
* Improving the error handling of the script.
* Make the script capable of automatically mitigating **HTTP 429** errors.
* Make the script easier to use (possibly make a GUI frontend for said script).