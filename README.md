# Full Stack Udacity Capstone

## Introduction

The aim of this project is having a first approach to image handling in web pages.
Particularly, it consists in deploying a site to share images. Any who accesses the site will be able to see the content, but only people with right permissions will be allowed to create albums and upload images.

Even when we can store images in a database as binaries, this is not always the best thing to do. In general terms, it would be better storing the images in the disk or in the cloud and then save in the database the place where the images are. In this project, the cloud alternative is chosen.

## Overview

## Tech Stack

* Media management: [ImageKit](https://imagekit.io/).
* Authentication and authorization: [Auth0](https://auth0.com/).
* Database system: [PostgreSQL](https://www.postgresql.org/).
* Backend-Python3: [Flask](https://flask.palletsprojects.com/en/3.0.x/), [SQLAlchemy](https://www.sqlalchemy.org/), [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/).
* Fronted-Javascript: [knockout](https://knockoutjs.com/).
* Cloud platform as a service: [Heroku](https://dashboard.heroku.com/).

## Local development instructions

## Testing

## Heroku deployment instructions

## API documentation



|        | albums        | images         |
| -------| ------------- | -------------  |
| GET    | All users     | All users      |
| POST   | post:albums   | post:images    |
| PATCH  | patch:albums  | N/A |
| DELETE | delete:albums | delete:images  |

---

`GET '/albums'`

- Fetch the albums available in the app.
- Request Arguments: N/A.
- Returns: An array with all the albums.

Example:

`curl --location 'https://jogallar-capstone-app-fd00b6e0aac4.herokuapp.com/albums'`

```json
{
    "albums": [
        {
            "id": 1,
            "name": "Guanajuato de mi corazón"
        },
        {
            "id": 2,
            "name": "Perrito"
        },
        {
            "id": 3,
            "name": "Running"
        },
        {
            "id": 4,
            "name": "Wonderland trip"
        }
    ],
    "success": true
}
```

---

`GET '/albums/<int:albumId>/images'`

- Fetch the images available in an album.
- Request Arguments: The id of the album.
- Returns: An array with all the albums.

Example:

`curl --location 'https://jogallar-capstone-app-fd00b6e0aac4.herokuapp.com/albums/1/images'`

```json
{
    "images": [
        {
            "albumId": 1,
            "h": 1600,
            "id": 1,
            "url": "https://ik.imagekit.io/ynuyx2nqou/image_uHpQH7Mzr.jpeg",
            "w": 1200
        },
        {
            "albumId": 1,
            "h": 1200,
            "id": 3,
            "url": "https://ik.imagekit.io/ynuyx2nqou/image_8gFEWJ-qd-.jpeg",
            "w": 1600
        },
        {
            "albumId": 1,
            "h": 1200,
            "id": 4,
            "url": "https://ik.imagekit.io/ynuyx2nqou/image_wvs3aG7qn.jpeg",
            "w": 1600
        }
    ],
    "success": true
}
```
---
`POST '/albums'`

- Request to create a new album.
- Request Body:

```json
{
    "albumName": "New album name"
}
```
- Headers: `Content-Type: application/json` and Bearer token in `Authorization` header.
- Returns: An array with the new album.

Example:

`curl --location 'https://jogallar-capstone-app-fd00b6e0aac4.herokuapp.com/albums' --header 'Content-Type: application/json' --header 'Authorization: Bearer theToken' --data '{
    "albumName": "API Album"
}'`

```json
{
    "albums": [
        {
            "id": 6,
            "name": "API Album"
        }
    ],
    "success": true
}
```

---

## Future work

---
## References


