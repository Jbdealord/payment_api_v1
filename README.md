# medialib

Test assessment for Just Work (https://just-work.org/)

https://drive.google.com/file/d/1Qi_gFJdAknKMhGNOHaf40GilIaTBxy3X/view

# API Calls Example

## GET /api/page/

Will give you the list of all pages. Each item in the list will have only the URL to API detail API endpoint.

Example:

```http request
GET /api/page/

HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "url": "http://0.0.0.0:8000/api/page/1/"
        },
        {
            "url": "http://0.0.0.0:8000/api/page/2/"
        },
        {
            "url": "http://0.0.0.0:8000/api/page/3/"
        },
        {
            "url": "http://0.0.0.0:8000/api/page/4/"
        },
        {
            "url": "http://0.0.0.0:8000/api/page/5/"
        }
    ]
}
```

## GET /api/page/<page_id: int>/

This is the API endpoint, responsible for detailed description of the page and content inside.

Example:

```http request
GET /api/page/4/

HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "title": "My Audios and Texts",
    "content": [
        {
            "title": "Queen - We will rock you",
            "counter": 3,
            "bitrate": 320
        },
        {
            "title": "Lyrics for Queen",
            "counter": 3,
            "text": "blah blah rock you"
        },
        {
            "title": "Metallica - So What",
            "counter": 3,
            "bitrate": 128
        },
        {
            "title": "Lyrics for Metallica",
            "counter": 6,
            "text": "blah blah so what"
        }
    ]
}
```

# TODO

0. Add more context about the task purpose and functional requirements (in this document). Add more information on
development process and available service in Docker Compose.
1. Handle possible race conditions during set of `order_nbr`.
2. Make population of `ContentOnPage` schema automatic (metaclass?) to register new content type automatically.
3. Cover unit test runner in tools like `nose`.
4. Celery tuning to avoid loose of tasks (during, for example, rough shutdown) - maybe use ack late.
5. Add reordering UI in admin to reorder content in more "human" way.
6. Connect `Page` model with templates and define landing places there. Each landing place should have an id.
And that id should be used in `order_nbr` field on `ContentOnPage` model.