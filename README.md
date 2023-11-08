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

`curl --location 'https://jogallar-capstone-app-fd00b6e0aac4.herokuapp.com/albums' --header 'Content-Type: application/json' --header 'Authorization: Bearer theTokenGoesHere' --data '{
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
`POST '/albums/<int:albumId>/images'`

- Request to add a photo to an album.
- Request Arguments: The id of the album.
- Request Body: Image file in `form-data`
- Headers: Bearer token in `Authorization` header.
- Returns: An array with the new image.

Example:

`curl --location 'https://jogallar-capstone-app-fd00b6e0aac4.herokuapp.com/albums/7/images' --header 'Authorization: Bearer theTokenGoesHere' --form 'file=@"/Users/jogallar/Documents/nanodegree/capstone/avatar_1.jpg"'`

```json
{
    "images": [
        {
            "albumId": 7,
            "h": 900,
            "id": 9,
            "url": "https://ik.imagekit.io/ynuyx2nqou/image_clJLpxKKz.jpeg",
            "w": 900
        }
    ],
    "success": true
}
```

---

`PATCH '/albums/<int:albumId>'`

- Request to modify the name of an album.
- Request Arguments: The id of the album.
- Request Body: 
```json
{
    "newName": "newName 2.0"
}
```
- Headers: `Content-Type: application/json` and Bearer token in `Authorization` header.
- Returns: An array with the renamed album.

Example:

`curl --location --request PATCH 'https://jogallar-capstone-app-fd00b6e0aac4.herokuapp.com/albums/7' --header 'Content-Type: application/json' --header 'Authorization: Bearer theTokenGoesHere' --data '{ "newName": "newName 2.0" }'`

```json
{
    "albums": [
        {
            "id": 7,
            "name": "newName 2.0"
        }
    ],
    "success": true
}
```
---

`DELETE '/images/<int:imageId>'`

- Request to delete an image.
- Request Arguments: The id of the image.
- Headers: The Bearer token in `Authorization` header.
- Returns: An integer with the id of the image deleted.

Example:

`curl --location --request DELETE 'https://jogallar-capstone-app-fd00b6e0aac4.herokuapp.com/images/11' \
--header 'Authorization: Bearer theTokenGoesHere'`

```json
{
    "delete": 11,
    "success": true
}
```

---

`DELETE '/albums/<int:albumId>'`

- Request to delete an album.
- Request Arguments: The album id.
- Headers: The Bearer token in `Authorization` header.
- Returns: An integer with the id of the album deleted.

Example:

`curl --location --request DELETE 'https://jogallar-capstone-app-fd00b6e0aac4.herokuapp.com/albums/7' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVXdXJydm95ZUwzU0tlR29GOUdTVSJ9.eyJpc3MiOiJodHRwczovL2Rldi13enJ1dXJpMzVhNDIzcnoyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNDY1MjMxMTg5MjMzMTc0NzYyOCIsImF1ZCI6WyJjYXBzdG9uZVByb2plY3QiLCJodHRwczovL2Rldi13enJ1dXJpMzVhNDIzcnoyLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTk0NjY4NzMsImV4cCI6MTY5OTU1MzI3MywiYXpwIjoiUkVNVVVnNVNUcnpPbDF0SXhxZ01sZUxEQnNkc2tJZ1YiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFsYnVtcyIsImRlbGV0ZTppbWFnZXMiLCJwYXRjaDphbGJ1bXMiLCJwb3N0OmFsYnVtcyIsInBvc3Q6aW1hZ2VzIl19.ePnxOacbNlB4zuKUZFPoaycZuLFKEYtQrmjsrcD0pN7T7W9mipJfXy1N1qUG_T-4_thx1VFUrzuchTFdQiOn1tlFPwZyopsGI8VbB3V-QinPZNXI1H8uiGgi2jMkJUHxDkJ4PJ-ZuwlgNS6p7w-y1HhMNJ2VmqMp-hywI1vY6mtm39h-JxCf2GYMvtgPWf-MRsSWOy71xnnHgCllfL3ok9Xg80Q2A7EKwTO8smuIZtLoaJTKWcIkrcxAPsIBqCKrhMcwQf---4O7oJQktPO-ICG0R2xit56bZnsL64bKPsA-wFRNhCbKxGXCj3q9j1T7_ZS8MHCNwU2FmPfBOfXdBg'`

```json
{
    "delete": 7,
    "success": true
}
```

## Future work

---
## References


