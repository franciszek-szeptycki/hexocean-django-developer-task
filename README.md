## How to run on your won machine?
1. `mv .env.example .env`
2. `docker-compose up`

### Documentation
**Login**:
Provide login credentials from .env ADMIN_USERNAME and ADMIN_PASSWORD (default is *admin* and *admin*).
<img width="580" alt="Zrzut ekranu 2023-10-5 o 23 36 27" src="https://github.com/franciszek-szeptycki/hexocean-django-developer-task/assets/106173385/5da7e2d8-4130-45d2-8522-2d89a3911c30">

**From now on, set the token in *Headers* in each request**
```Authorization: Token 10f795cbb23fb2c697dc558c887aca0433dffe0c```

