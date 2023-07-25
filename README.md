# py-social-media

This Django REST framework-based API serves as a REST interface for a social media.

## How to run

---
```python
git clone https://github.com/Sebshe/py-social-media.git
cd py_social_media
python -m venv venv
source venv/bin/activate # for linux or macOS
venv\Scripts\activate # for Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Getting access

To get access to the API:

- Create a user via `/api/user/register/`.
- Obtain an access token via `/api/user/token/`.

## Features

- User Registration and Authentication
- Admin panel: `/admin/`
- Documentation is located at `/api/doc/swagger/`
- User Profile
- Follow/Unfollow
- Post Creation and Retrieval
- Filtering profiles and posts

