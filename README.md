# Twitch IRC Data collection tool
A Python based tool for connecting to Twitch IRC servers, capturing messages, and 
providing REST API access to stored information for analytics and research purposes

This is a research project.

## Info

This is a personal learning project focused on gaining practical experience with:
- IRC protocol implementation and socket programming
- OAuth2 authentication flows
- Database design and Repository pattern
- RESTful API development with Flask
- Real-time data processing and storage
- Python software architecture

**Project goal:** Build a functional tool that collects Twitch chat data for use in future data analytics and machine learning experiments

## Features
- IRC client and real-time data collection
- message parsing
- SQL database (sqlite)
- RESTful API (Flask)

## Project-Structure
```
project/
├──config                   # Application configuration
│
│
├──database                 # database folder
│
├──keyz                     # Authentication credentials
│
├──logs                     # Error logs
│
├──src
│   │
│   ├──authentication       # OAUTH
│   │
│   ├──api                  # Flask REST Api
│   │   │
│   │   ├──models           # Database utilities for Flask
│   │   │
│   │   ├──routes           # API endpoint definitions
│   │   │
│   │   └──utils            # utility functions
│   │
│   ├──db                   # Database layer
│   │   │
│   │   ├──repositories     # Data access layer
│   │   │
│   │   └──services         # Business logic layer
│   │
│   └──parsers              # IRC message parsing
│       │
│       └──tags             # message type handlers
│   
├──tests                    # Tests (outdated)
│
├──client.py
│
└──run_api.py

```

## Tech-Stack
- Backend: Python 3.14+
- Web Framework: Flask
- Database: SQLite3
- Architecture Patterns: Factory, Repository, Service Layer

## Installation

### Prerequisites
- Python 3.14+
- Twitch account

### 1. clone repository

```Shell
git clone https://github.com/kneive/irc-chatbot
```

### 2. create virtual environment

```Shell
cd irc-chatbot
python3 -m venv venv-name
```

activate virtual environment (Linux)
```Shell
source venv-name/bin/activate
```
or
activate virtual environment (Windows)
```Shell
venv\Scripts\activate
```

### install dependencies

```Shell
pip install -r requirements.txt
```

or

```Shell
pip install Flask==3.0.0 flask-cors==4.0.0 python-dotenv==1.0.0 requests
```

## Configuration

### 1 Twitch OAuth Credentials (keyz/credentials.key)

Create Twitch App to obtain OAuth credentials

1. visit https://dev.twitch.tv/console
2. click 'Register Application'
3. set OAuth Redirect URL e.g. http://localhost:3000
4. Add Client ID and Client secret to `keyz/credentials.template`
5. rename `keyz/credentials.template` to `keyz/credentials.key`

requested Scopes:
```
chat:read
chat:edit
```

### 2 Login information (keyz/logins.key)

1. Add the username and password of the Twitch account the tool uses to `keyz/logins.key`
2. rename `keyz/logins.template` to `keyz/logins.key`

### 3 Channel configuration (config/config.json)

1. Add your nickname to `config/config.template`
2. Add the channels you want to autojoin to the channels list in `config/config.template`
3. rename `config/config.template` to `config/config.json`

### 4 Database configuration

Automatically created on the first run

### 5 API configuration

Flask API settings:

```
Host: 0.0.0.0
Port: 5000
```

in `src/api/App.py`:

```Python
app.run(
    debug=False,
    host='0.0.0.0',
    port=5000
)
```

## Usage

### 1. Run the IRC client


```Shell
python client.py
```
- On the first run the client will setup the database

- On disconnects the client should automatically reconnect

**Commands**:
```
# join a channel (client appends # if omitted)
join #channelname

# send a message
say #channel <message>

# client status
status

# disconnect from the server
quit
```

### 2. Run the Flask API

```Shell
python run_api.py
```
- By default the api will be available at `http://localhost:5000`

**Sample queries**
```Shell
# recent messages
curl "http://localhost:5000/api/messages?limit=10"

# specific user
curl "http://localhost:5000/api/messages?user-name=username"

# specific channel
curl "http://localhost:5000/api/messages?room-name=channel"

# specific date range
curl "http://localhost:5000/api/messages?start-date=2024-01-01&end-date=2024-01-31"
```
- a web browser simply open the url


## API Documentation (subject to change)

### Base URL

Default: `http://localhost:5000`

### API Endpoints


#### 1. Root: /
```JSON
{
  "message": "Saltmine API",
  "version": "1.0.0",
  "endpoints": {}
}
```

#### 2. Health check: /api/health

```Shell
curl http://localhost:5000/api/health
```

Response:
```JSON
{
  "status": "ok"
}
```

#### 3. Announcements: /api/announcements

Example request:
```shell
curl "http://localhost:5000/api/announcements?room-name=channel"
```

Example response:
```JSON
{
  "announcements": [
    {
      "room_name": "channel",
      "display_name": "username",
      "msg_content": "message content",
      "timestamp": "2024-01-15T14:00:00"
    }
  ],
  "count": 1
}
```

#### 4. Bits: /api/bits (not implemented yet)

Example request
```Shell
curl "http://localhost:5000/api/bits?room-name=channel"
```
Example response
```JSON
```

#### 5. Mystery subgifts: /api/gifts

Example request:
```Shell
curl "http://localhost:5000/api/mysterygifts?room-name=channel"
```

Example response:
```JSON
{
  "mystery_gifts": [
    {
      "display_name": "username",
      "room_name": "channel",
      "sub_plan": "1000",
      "mass_gift_count": 50,
      "timestamp": "2024-01-15T16:00:00"
    }
  ],
  "count": 1
}
```

#### 6. Chat messages: /api/messages

Example request:
```Shell
curl "http://localhost:5000/api/messages?user-name=username&room-name=channel"

curl "http://localhost:5000/api/messages?start-date=2024-01-01&end-date=2024-01-31"
```

Example response:
```JSON
{
  "messages": [
    {
      "display_name": "username",
      "room_name": "channel",
      "msg_content": "message content",
      "reply_msg_body": null,
      "timestamp": "2024-01-15T14:30:00"
    }
  ],
  "count": 1
}
```

#### 7. Rooms: /api/rooms

Example request:
```Shell
curl "http://localhost:5000/api/rooms?room-name=channel"
```

Example response:
```JSON
{
  "room_id": "12345678",
  "room_name": "channel"
}
```

#### 8. Channel subscriptions: /api/subs

Example request:
```Shell
curl "http://localhost:5000/api/subscriptions?room-name=channel&start-date=2024-01-01"
```

Example response:
```JSON
{
  "subscriptions": [
    {
      "display_name": "username",
      "room_name": "channel",
      "sub_plan": "1000",
      "timestamp": "2024-01-15T15:30:00"
    }
  ],
  "count":
}
```

### Status Codes
- 200 - Success
- 400 - malformed request
- 404 - requested ressource does not exist
- 500 - internal server error

#### 400
```JSON
{
    "error": "Bad request",
    "message": "The request is invalid or malformed",
}
```

#### 404
```JSON
{
    "error": "Not found",
    "message": "The requested resource does not exist"
}
```
#### 500
```JSON
{
    "error": "Internal server error",
    "message": "Something went wrong"
}
```

### common query parameters
```SQL
╔═════════════╦═════════╦════════════════════════╗
║  Parameter  ║  Type   ║ Description            ║
╠═════════════╬═════════╬════════════════════════╣
║  user-name  ║ string  ║ Filter by user-name    ║
║  user-id    ║ integer ║ Filter by user-id      ║
║  room-name  ║ string  ║ Filter by room-name    ║
║  room-id    ║ integer ║ Filter by room-id      ║
║  start-date ║ string  ║ Filter by date (start) ║
║  end-date   ║ string  ║ Filter by date (end)   ║
╚═════════════╩═════════╩════════════════════════╝
```

### Supported Dateformats

- `YYYY-MM-DD` (e.g., `2024-01-15`)
- `DD.MM.YYYY` (e.g., `15.01.2024`)
- `DD/MM/YYYY` (e.g., `15/01/2024`)
- `MM-DD-YYYY` (e.g., `01-15-2024`)

## Database Schema

Database schema is based on the message types and structure of these types documented in the twitch API https://dev.twitch.tv/docs/api/. Additional fields and tables were added based on message samples. 

### user Table

Stores general user information
```SQL
╔════════════════╦═══════════╦═══════════════════════════╦══════════════════════════════════════╗
║ Column         ║ Type      ║ Constraints               ║ Description                          ║
╠════════════════╬═══════════╬═══════════════════════════╬══════════════════════════════════════╣
║ `user_id`      ║ TEXT      ║ PRIMARY KEY               ║ Twitch user ID                       ║
║ `login`        ║ TEXT      ║ DEFAULT ''                ║ Username (lowercase)                 ║
║ `display_name` ║ TEXT      ║ DEFAULT ''                ║ Display name (with capitalization)   ║
║ `user_type`    ║ TEXT      ║ DEFAULT ''                ║ User type (staff, admin, etc.)       ║
║ `turbo`        ║ INTEGER   ║ DEFAULT 0                 ║ Turbo status (0=no, 1=yes)           ║
║ `created`      ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Record creation time                 ║
╚════════════════╩═══════════╩═══════════════════════════╩══════════════════════════════════════╝
```
### room Table

Stores channel ids and names
```SQL
╔═════════════╦═══════════╦═══════════════════════════╦══════════════════════════════╗
║ Column      ║ Type      ║ Constraints               ║ Description                  ║
╠═════════════╬═══════════╬═══════════════════════════╬══════════════════════════════╣
║ `room_id`   ║ TEXT      ║ PRIMARY KEY               ║ Twitch channel ID            ║
║ `room_name` ║ TEXT      ║ DEFAULT '#UNKNOWN'        ║ Channel name (with # prefix) ║
║ `created`   ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Record creation time         ║
╚═════════════╩═══════════╩═══════════════════════════╩══════════════════════════════╝
```

### user-in-room table

Stores user information specific to a given room

```SQL
╔══════════════╦═══════════╦════════════════════╦═══════════════════════════════╗
║ Column       ║ Type      ║ Constraints        ║ Description                   ║
╠══════════════╬═══════════╬════════════════════╬═══════════════════════════════╣
║ `timestamp`  ║ TIMESTAMP ║ PRIMARY KEY        ║ When user was seen in room    ║
║ `user_id`    ║ TEXT      ║ FOREIGN KEY → user ║ User reference                ║
║ `room_id`    ║ TEXT      ║ FOREIGN KEY → room ║ Room reference                ║
║ `badges`     ║ TEXT      ║ DEFAULT ''         ║ User badges (comma-separated) ║
║ `badge_info` ║ TEXT      ║ DEFAULT ''         ║ Badge metadata                ║
║ `subscriber` ║ INTEGER   ║ DEFAULT 0          ║ Subscriber status             ║
║ `sub_streak` ║ INTEGER   ║ DEFAULT 0          ║ Subscription streak months    ║
║ `vip`        ║ INTEGER   ║ DEFAULT 0          ║ VIP status                    ║
║ `mod`        ║ INTEGER   ║ DEFAULT 0          ║ Moderator status              ║
╚══════════════╩═══════════╩═══════════════════════════╩════════════════════════╝
```

### privmsg table:

Stores chat messages

```SQL
╔═════════════════════╦═══════════╦═══════════════════════════╦═══════════════════════════════════════╗
║ Column              ║ Type      ║ Constraints               ║ Description                           ║
╠═════════════════════╬═══════════╬═══════════════════════════╬═══════════════════════════════════════╣
║ `serial`            ║ INTEGER   ║ PRIMARY KEY AUTOINCREMENT ║ Unique message ID                     ║
║ `timestamp`         ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Message time                          ║
║ `tmi_sent_ts`       ║ TEXT      ║ NOT NULL                  ║ Twitch timestamp                      ║
║ `message_id`        ║ TEXT      ║ NOT NULL                  ║ Twitch message ID                     ║
║ `source_message_id` ║ TEXT      ║                           ║ Original message ID (for shared chat) ║
║ `room_id`           ║ TEXT      ║ FOREIGN KEY → room        ║ Channel where sent                    ║
║ `source_room_id`    ║ TEXT      ║ DEFAULT 'NULL'            ║ Original channel (for shared chat)    ║
║ `user_id`           ║ TEXT      ║ FOREIGN KEY → user        ║ Message author                        ║
║ `color`             ║ TEXT      ║ DEFAULT ''                ║ Username color hex code               ║
║ `returning_chatter` ║ INTEGER   ║ DEFAULT 0                 ║ Returning chatter flag                ║
║ `first_msg`         ║ INTEGER   ║ DEFAULT 0                 ║ First message flag                    ║
║ `flags`             ║ TEXT      ║ DEFAULT ''                ║ Message flags                         ║
║ `emotes`            ║ TEXT      ║ DEFAULT ''                ║ Emote data                            ║
║ `msg_content`       ║ TEXT      ║ DEFAULT ''                ║ Message text                          ║
║ `reply_user_id`     ║ TEXT      ║ FOREIGN KEY → user        ║ Reply target user                     ║
║ `reply_msg_id`      ║ TEXT      ║                           ║ Reply target message ID               ║
║ `reply_msg_body`    ║ TEXT      ║                           ║ Reply target message text             ║
║ `thread_user_id`    ║ TEXT      ║ FOREIGN KEY → user        ║ Thread parent user                    ║
║ `thread_msg_id`     ║ TEXT      ║                           ║ Thread parent message ID              ║
╚═════════════════════╩═══════════╩═══════════════════════════╩═══════════════════════════════════════╝
```

### announcement table

Stores information about channel announcements

```SQL
╔════════════════╦═══════════╦═══════════════════════════╦═════════════════════════╗
║ Column         ║ Type      ║ Constraints               ║ Description             ║
╠════════════════╬═══════════╬═══════════════════════════╬═════════════════════════╣
║ `serial`       ║ INTEGER   ║ PRIMARY KEY AUTOINCREMENT ║ Unique ID               ║
║ `room_id`      ║ TEXT      ║ FOREIGN KEY → room        ║ Channel                 ║
║ `user_id`      ║ TEXT      ║ FOREIGN KEY → user        ║ Announcer               ║
║ `display_name` ║ TEXT      ║                           ║ Announcer display name  ║
║ `timestamp`    ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Announcement time       ║
║ `msg_content`  ║ TEXT      ║                           ║ Announcement text       ║
╚════════════════╩═══════════╩═══════════════════════════╩═════════════════════════╝
```

### subscription table

Stores information about channel subscriptions (sub, resub)

```SQL
╔═══════════════════════╦═══════════╦═══════════════════════════╦═══════════════════════════════════╗
║ Column                ║ Type      ║ Constraints               ║ Description                       ║
╠═══════════════════════╬═══════════╬═══════════════════════════╬═══════════════════════════════════╣
║ `serial`              ║ INTEGER   ║ PRIMARY KEY AUTOINCREMENT ║ Unique ID                         ║
║ `user_id`             ║ TEXT      ║ FOREIGN KEY → user        ║ Subscriber                        ║
║ `room_id`             ║ TEXT      ║ FOREIGN KEY → room        ║ Channel                           ║
║ `timestamp`           ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Sub time                          ║
║ `tmi_sent_ts`         ║ TEXT      ║ NOT NULL                  ║ Twitch timestamp                  ║
║ `msg_id`              ║ TEXT      ║ NOT NULL                  ║ Message ID                        ║
║ `source_msg_id`       ║ TEXT      ║                           ║ Source message ID                 ║
║ `cumulative_months`   ║ INTEGER   ║ DEFAULT 0                 ║ Total months subscribed           ║
║ `months`              ║ INTEGER   ║ DEFAULT 0                 ║ Current streak months             ║
║ `multimonth_duration` ║ INTEGER   ║ DEFAULT 0                 ║ Multi-month purchase duration     ║
║ `multimonth_tenure`   ║ INTEGER   ║ DEFAULT 0                 ║ Multi-month tenure                ║
║ `should_share_streak` ║ INTEGER   ║ DEFAULT 0                 ║ Share streak flag                 ║
║ `sub_plan_name`       ║ TEXT      ║                           ║ Plan name                         ║
║ `sub_plan`            ║ TEXT      ║ NOT NULL                  ║ Plan tier (1000/2000/3000/Prime)  ║
║ `was_gifted`          ║ TEXT      ║ NOT NULL                  ║ Gift status                       ║
║ `system_msg`          ║ TEXT      ║                           ║ System message                    ║
╚═══════════════════════╩═══════════╩═══════════════════════════╩═══════════════════════════════════╝
```

### subgift table

Stores information about gifted subs

```SQL
╔══════════════════════════╦═══════════╦═══════════════════════════╦═════════════════════════╗
║ Column                   ║ Type      ║ Constraints               ║ Description             ║
╠══════════════════════════╬═══════════╬═══════════════════════════╬═════════════════════════╣
║ `serial`                 ║ INTEGER   ║ PRIMARY KEY AUTOINCREMENT ║ Unique ID               ║
║ `user_id`                ║ TEXT      ║ FOREIGN KEY → user        ║ Gifter                  ║
║ `room_id`                ║ TEXT      ║ FOREIGN KEY → room        ║ Channel                 ║
║ `timestamp`              ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Gift time               ║
║ `tmi_sent_ts`            ║ TEXT      ║ NOT NULL                  ║ Twitch timestamp        ║
║ `msg_id`                 ║ TEXT      ║ NOT NULL                  ║ Message ID              ║
║ `source_msg_id`          ║ TEXT      ║                           ║ Source message ID       ║
║ `community_gift_id`      ║ TEXT      ║                           ║ Community gift batch ID ║
║ `fun_string`             ║ TEXT      ║                           ║ Fun string metadata     ║
║ `gift_months`            ║ INTEGER   ║ DEFAULT 0                 ║ Months gifted           ║
║ `months`                 ║ INTEGER   ║ DEFAULT 0                 ║ Recipient total months  ║
║ `origin_id`              ║ TEXT      ║                           ║ Origin ID               ║
║ `recipient_id`           ║ TEXT      ║                           ║ Recipient user ID       ║
║ `recipient_display_name` ║ TEXT      ║                           ║ Recipient display name  ║
║ `recipient_user_name`    ║ TEXT      ║                           ║ Recipient username      ║
║ `sender_count`           ║ INTEGER   ║ DEFAULT 0                 ║ Gifter s total gifts    ║
║ `sub_plan_name`          ║ TEXT      ║                           ║ Plan name               ║
║ `sub_plan`               ║ TEXT      ║                           ║ Plan tier               ║
║ `system_msg`             ║ TEXT      ║                           ║ System message          ║
╚══════════════════════════╩═══════════╩═══════════════════════════╩═════════════════════════╝
```

### submysterygift table

Stores information about mass subgift events

```SQL
╔═════════════════════════╦═══════════╦═══════════════════════════╦═════════════════════════╗
║ Column                  ║ Type      ║ Constraints               ║ Description             ║
╠═════════════════════════╬═══════════╬═══════════════════════════╬═════════════════════════╣
║ `serial`                ║ INTEGER   ║ PRIMARY KEY AUTOINCREMENT ║ Unique ID               ║
║ `user_id`               ║ TEXT      ║ FOREIGN KEY → user        ║ Gifter                  ║
║ `room_id`               ║ TEXT      ║ FOREIGN KEY → room        ║ Channel                 ║
║ `timestamp`             ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Gift time               ║
║ `tmi_sent_ts`           ║ TEXT      ║ NOT NULL                  ║ Twitch timestamp        ║
║ `msg_id`                ║ TEXT      ║ NOT NULL                  ║ Message ID              ║
║ `source_msg_id`         ║ TEXT      ║                           ║ Source message ID       ║
║ `community_gift_id`     ║ TEXT      ║ NOT NULL                  ║ Gift batch ID           ║
║ `contribution_type`     ║ TEXT      ║                           ║ Contribution type       ║
║ `current_contributions` ║ INTEGER   ║ DEFAULT 0                 ║ Current contributions   ║
║ `target_contributions`  ║ INTEGER   ║ DEFAULT 0                 ║ Target contributions    ║
║ `user_contributions`    ║ INTEGER   ║ DEFAULT 0                 ║ User s contributions    ║
║ `mass_gift_count`       ║ INTEGER   ║ DEFAULT 0                 ║ Number of subs gifted   ║
║ `origin_id`             ║ TEXT      ║                           ║ Origin ID               ║
║ `sub_plan`              ║ TEXT      ║                           ║ Plan tier               ║
║ `system_msg`            ║ TEXT      ║ NOT NULL                  ║ System message          ║
╚═════════════════════════╩═══════════╩═══════════════════════════╩═════════════════════════╝
```

### bits table

Stores information about bits and cheer events

```SQL
╔══════════════════╦═══════════╦═══════════════════════════╦════════════════════════════════╗
║ Column           ║ Type      ║ Constraints               ║ Description                    ║
╠══════════════════╬═══════════╬═══════════════════════════╬════════════════════════════════╣
║ `serial`         ║ INTEGER   ║ PRIMARY KEY AUTOINCREMENT ║ Unique ID                      ║
║ `user_id`        ║ TEXT      ║ FOREIGN KEY → user        ║ Cheerer                        ║
║ `room_id`        ║ TEXT      ║ FOREIGN KEY → room        ║ Channel                        ║
║ `source_room_id` ║ TEXT      ║                           ║ Source channel (shared chat)   ║
║ `timestamp`      ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Cheer time                     ║
║ `bits`           ║ INTEGER   ║                           ║ Number of bits                 ║
╚══════════════════╩═══════════╩═══════════════════════════╩════════════════════════════════╝
```

### bitsbadgetier table

Stores information about bits badge tier events

```SQL
╔═══════════════════════╦═══════════╦═══════════════════════════╦═══════════════════════════╗
║ Column                ║ Type      ║ Constraints               ║ Description               ║
╠═══════════════════════╬═══════════╬═══════════════════════════╬═══════════════════════════╣
║ `serial`              ║ INTEGER   ║ PRIMARY KEY AUTOINCREMENT ║ Unique ID                 ║
║ `room_id`             ║ TEXT      ║ FOREIGN KEY → room        ║ Channel                   ║
║ `user_id`             ║ TEXT      ║ FOREIGN KEY → user        ║ User                      ║
║ `timestamp`           ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Achievement time          ║
║ `msg_param_threshold` ║ INTEGER   ║ DEFAULT 0                 ║ Bits threshold reached    ║
║ `system_msg`          ║ TEXT      ║                           ║ System message            ║
╚═══════════════════════╩═══════════╩═══════════════════════════╩═══════════════════════════╝
```

### raid table

Stores information about channel raid events

```SQL
╔═════════════════════════════╦═══════════╦═══════════════════════════╦══════════════════════╗
║ Column                      ║ Type      ║ Constraints               ║ Description          ║
╠═════════════════════════════╬═══════════╬═══════════════════════════╬══════════════════════╣
║ `serial`                    ║ INTEGER   ║ PRIMARY KEY AUTOINCREMENT ║ Unique ID            ║
║ `user_id`                   ║ TEXT      ║ FOREIGN KEY → user        ║ Raider               ║
║ `room_id`                   ║ TEXT      ║ FOREIGN KEY → room        ║ Target channel       ║
║ `source_room_id`            ║ TEXT      ║                           ║ Source channel       ║
║ `timestamp`                 ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Raid time            ║
║ `tmi_sent_ts`               ║ TEXT      ║ NOT NULL                  ║ Twitch timestamp     ║
║ `msg_id`                    ║ TEXT      ║ NOT NULL                  ║ Message ID           ║
║ `source_msg_id`             ║ TEXT      ║                           ║ Source message ID    ║
║ `msg_param_displayName`     ║ TEXT      ║                           ║ Raider display name  ║
║ `msg_param_login`           ║ TEXT      ║                           ║ Raider login         ║
║ `msg_param_profileImageURL` ║ TEXT      ║                           ║ Profile image URL    ║
║ `msg_param_viewerCount`     ║ TEXT      ║                           ║ Number of raiders    ║
║ `system_msg`                ║ TEXT      ║ NOT NULL                  ║ System message       ║
╚═════════════════════════════╩═══════════╩═══════════════════════════╩══════════════════════╝
```

### viewermilestone table

Stores viewer milestone events, e.g. watch streaks

```SQL
╔════════════════╦═══════════╦═══════════════════════════╦══════════════════════╗
║ Column         ║ Type      ║ Constraints               ║ Description          ║
╠════════════════╬═══════════╬═══════════════════════════╬══════════════════════╣
║ `serial`       ║ INTEGER   ║ PRIMARY KEY AUTOINCREMENT ║ Unique ID            ║
║ `room_id`      ║ TEXT      ║ FOREIGN KEY → room        ║ Channel              ║
║ `user_id`      ║ TEXT      ║ FOREIGN KEY → user        ║ User                 ║
║ `display_name` ║ TEXT      ║                           ║ User display name    ║
║ `timestamp`    ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Milestone time       ║
║ `streak`       ║ INTEGER   ║ DEFAULT 0                 ║ Watch streak value   ║
║ `system_msg`   ║ TEXT      ║                           ║ System message       ║
╚════════════════╩═══════════╩═══════════════════════════╩══════════════════════╝
```

### payforward table

Stores information about payforward events, i.e. continuation of subgifts, 
e.g. communitypayforward and standardpayforward

```SQL
╔═════════════════════════════╦═══════════╦═══════════════════════════╦═════════════════════════════════╗
║ Column                      ║ Type      ║ Constraints               ║ Description                     ║
╠═════════════════════════════╬═══════════╬═══════════════════════════╬═════════════════════════════════╣
║ `serial`                    ║ INTEGER   ║ PRIMARY KEY AUTOINCREMENT ║ Unique ID                       ║
║ `user_id`                   ║ TEXT      ║ FOREIGN KEY → user        ║ New gifter                      ║
║ `room_id`                   ║ TEXT      ║ FOREIGN KEY → room        ║ Channel                         ║
║ `timestamp`                 ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Event time                      ║
║ `tmi_sent_ts`               ║ TEXT      ║ NOT NULL                  ║ Twitch timestamp                ║
║ `msg_id`                    ║ TEXT      ║ NOT NULL                  ║ Message ID                      ║
║ `source_msg_id`             ║ TEXT      ║                           ║ Source message ID               ║
║ `prior_gifter_anonymous`    ║ TEXT      ║                           ║ Prior gifter anonymous flag     ║
║ `prior_gifter_id`           ║ TEXT      ║ FOREIGN KEY → user        ║ Original gifter                 ║
║ `prior_gifter_display_name` ║ TEXT      ║                           ║ Original gifter display name    ║
║ `prior_gifter_user_name`    ║ TEXT      ║                           ║ Original gifter username        ║
║ `recipient_id`              ║ TEXT      ║                           ║ New recipient ID                ║
║ `recipient_display_name`    ║ TEXT      ║                           ║ New recipient display name      ║
║ `recipient_user_name`       ║ TEXT      ║                           ║ New recipient username          ║
║ `system_msg`                ║ TEXT      ║ NOT NULL                  ║ System message                  ║
╚═════════════════════════════╩═══════════╩═══════════════════════════╩═════════════════════════════════╝
```

### paidupgrade table

Stores information about paidupgrade events, e.g. upgrades of a Primesub to a regular sub

```SQL
╔═════════════════╦═══════════╦═══════════════════════════╦═════════════════════╗
║ Column          ║ Type      ║ Constraints               ║ Description         ║
╠═════════════════╬═══════════╬═══════════════════════════╬═════════════════════╣
║ `serial`        ║ INTEGER   ║ PRIMARY KEY AUTOINCREMENT ║ Unique ID           ║
║ `user_id`       ║ TEXT      ║ FOREIGN KEY → user        ║ User upgrading      ║
║ `room_id`       ║ TEXT      ║ FOREIGN KEY → room        ║ Channel             ║
║ `timestamp`     ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Upgrade time        ║
║ `tmi_sent_ts`   ║ TEXT      ║ NOT NULL                  ║ Twitch timestamp    ║
║ `msg_id`        ║ TEXT      ║ NOT NULL                  ║ Message ID          ║
║ `source_msg_id` ║ TEXT      ║                           ║ Source message ID   ║
║ `sender_login`  ║ TEXT      ║                           ║ User login          ║
║ `sender_name`   ║ TEXT      ║                           ║ User display name   ║
║ `sub_plan`      ║ TEXT      ║                           ║ New plan tier       ║
║ `system_msg`    ║ TEXT      ║ NOT NULL                  ║ System message      ║
╚═════════════════╩═══════════╩═══════════════════════════╩═════════════════════╝
```

### onetapgift table

Stores information about one-tap gift redemptions

```SQL
╔═════════════════════╦═══════════╦═══════════════════════════╦═════════════════════╗
║ Column              ║ Type      ║ Constraints               ║ Description         ║
╠═════════════════════╬═══════════╬═══════════════════════════╬═════════════════════╣
║ `serial`            ║ INTEGER   ║ PRIMARY KEY AUTOINCREMENT ║ Unique ID           ║
║ `user_id`           ║ TEXT      ║ FOREIGN KEY → user        ║ Redeemer            ║
║ `room_id`           ║ TEXT      ║ FOREIGN KEY → room        ║ Channel             ║
║ `timestamp`         ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Redemption time     ║
║ `tmi_sent_ts`       ║ TEXT      ║ NOT NULL                  ║ Twitch timestamp    ║
║ `msg_id`            ║ TEXT      ║ NOT NULL                  ║ Message ID          ║
║ `source_msg_id`     ║ TEXT      ║                           ║ Source message ID   ║
║ `bits_spent`        ║ INTEGER   ║ DEFAULT 0                 ║ Bits spent          ║
║ `gift_id`           ║ TEXT      ║ NOT NULL                  ║ Gift ID             ║
║ `user_display_name` ║ TEXT      ║                           ║ User display name   ║
║ `system_msg`        ║ TEXT      ║ NOT NULL                  ║ System message      ║
╚═════════════════════╩═══════════╩═══════════════════════════╩═════════════════════╝
```

### roomstate table

Stores information about channel mode settings

```SQL
╔═══════════════════╦═══════════╦═══════════════════════════╦═══════════════════════════════════════════╗
║ Column            ║ Type      ║ Constraints               ║ Description                               ║
╠═══════════════════╬═══════════╬═══════════════════════════╬═══════════════════════════════════════════╣
║ `timestamp`       ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ State change time                         ║
║ `room_id`         ║ TEXT      ║ PRIMARY KEY               ║ Channel                                   ║
║ `emote_only`      ║ INTEGER   ║ DEFAULT 0                 ║ Emote-only mode (0=off, 1=on)             ║
║ `followers_only`  ║ INTEGER   ║ DEFAULT 0                 ║ Followers-only duration (minutes, -1=off) ║
║ `r9k`             ║ INTEGER   ║ DEFAULT 0                 ║ R9K mode (0=off, 1=on)                    ║
║ `slow`            ║ INTEGER   ║ DEFAULT 0                 ║ Slow mode duration (seconds, 0=off)       ║
║ `subs_only`       ║ INTEGER   ║ DEFAULT 0                 ║ Subscribers-only mode (0=off, 1=on)       ║
╚═════════════════════╩═══════════╩═══════════════════════════╩═════════════════════════════════════════╝
```

### userlist table

Stores information about JOIN / PART events for a given channel

```SQL
╔═══════════════╦═══════════╦═══════════════════════════╦═══════════════════════════╗
║ Column        ║ Type      ║ Constraints               ║ Description               ║
╠═══════════════╬═══════════╬═══════════════════════════╬═══════════════════════════╣
║ `serial`      ║ INTEGER   ║ PRIMARY KEY AUTOINCREMENT ║ Unique ID                 ║
║ `timestamp`   ║ TIMESTAMP ║ DEFAULT CURRENT_TIMESTAMP ║ Event time                ║
║ `room_name`   ║ TEXT      ║ NOT NULL                  ║ Channel name              ║
║ `room_id`     ║ TEXT      ║                           ║ Channel ID (if known)     ║
║ `username`    ║ TEXT      ║ NOT NULL                  ║ Username                  ║
║ `join_part`   ║ TEXT      ║ NOT NULL                  ║ Event type (JOIN/PART)    ║
╚═══════════════╩═══════════╩═══════════════════════════╩═══════════════════════════╝
```

## Requirements
```
Python (3.14+)                   
Flask (3.0.0)            # for REST API
flask-cors (4.0.0)       # for REST API
python-dotenv (1.0.0)    # for environment variables
requests                 # for OAUTH
```

## License

MIT License - Feel free to use this project for learning purposes.

