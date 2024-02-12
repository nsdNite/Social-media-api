# Social Media API 👩🏻‍💻

API for social media platform.

API allow users to create profiles, follow other users, create and retrieve posts, manage likes and comments, and
perform basic social media actions.

## Technologies

- Django Rest Framework
- Celery + Redis for scheduled post creation
- Postgres
- Docker

## How to run

Docker 🐳 should be installed first.

Copy .env-sample -> .env and populate with all required data.

```bash
docker-compose up --build
```

Note: superuser is created automatically with .env info if no users exist in database.

## Accessing API 🔓

Creating user:  
/api/user/register/

Getting access token:  
/api/user/token/

Logout:
/api/user/logout

## Features ⭐

- JWT authentication (with logout function)
- Admin panel via /admin/
- Documentation via /api/doc/swagger/
- Extended profile system for users
- Likes, comments and following system
- CRUD operations for posts, comments
- Upload media to post
- Retrieving posts by present hashtag
- Scheduled post creation
- API test included
- Auto superuser creation on first launch

## Note on JWT authentication 🪙

To access API with JWT token please install ModHeader extension:  
[ModHeader for Chrome](https://chromewebstore.google.com/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj)  
[ModHeader for Firefox](https://addons.mozilla.org/uk/firefox/addon/modheader-firefox/)

Click on extension, paste your JWT auth token with prefix word "bearer", e.g. on picture below.  
Select Authorization request header and check the box.
You can now access other parts of API.
