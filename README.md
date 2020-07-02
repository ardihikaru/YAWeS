# YAWeS
**Y**et **A**nother python-based **We**b **S**ervice. 
This python-based Web Service was built based on [Asynchronous Server App Boilerplate (ASAB)](https://github.com/TeskaLabs/asab/commit/850dcc6d67d4670d8d759315246f454a202b824d).

## To dos
- [ ] Initial features
    - [ ] Sample GET request
    - [ ] Sample POST request
    - [ ] Sample POST /auth, get and save access_token into `Session`
    - [ ] Save, load, and delete Session variable
    - [ ] Sample Endpoint: Read URL variable, e.g. `/users/<username>`
    - [ ] Database Connection (MongoDB)
        - [ ] Simple connection
        - [ ] Integration with ORM / sqlalchemy / similar
        - [ ] Default CRUD
            - [ ] POST /auth/login
            - [ ] GET /auth/logout
            - [ ] POST /users
            - [ ] GET /users
            - [ ] PUT /users
            - [ ] DELETE /users
            - [ ] GET /users/register_between/<start_date>/<end_date>
    - [ ] Create routes (Cleaned codes)
    - [ ] Create Database Model
