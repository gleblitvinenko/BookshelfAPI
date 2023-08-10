# Library-Service

- Api service for library written on DRF


## Features:

- JWT authenticated
- Admin panel /admin/
- Documentation is located via /api/doc/swagger/
- Managing your borrowings
- Creating, updating books(Only for staff)
- Filtering borrowings by users id(Only for staff) and active borrowing
- Notification on telegram when create new borrow
- Notification every day with information about borrowings
- Task control using the flower
- Payment using the Stripe service
- Docker app starts only when db is available ( custom command via management/commands )

## How to run:

- `git clone https://github.com/gleblitvinenko/Library-Service.git`
- `cd social_media_api`
- `python -m venv venv`
#### Windows:

`venv\Scripts\activate`

#### Linux/macOS:
`source venv/bin/activate`
- Copy .env.sample -> .env and populate with all required data
- `docker-compose up --build`
- Create admin user & Create schedule for running sync in DB

## Get TELEGRAM_CHAT_ID and connect telegram bot:

- Add the Telegram BOT to your group using name @bestlibrary_notifications_bot

## Getting access:

- Create user via /api/user/register/
- Get user token via /api/user/token/
- Authorize with it on /api/doc/swagger/ OR
- Install ModHeader extension 
- Create Request header with name: Auth | value: Bearer <Your access token>