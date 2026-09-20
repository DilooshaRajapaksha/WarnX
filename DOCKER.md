# Running WarnX with Docker

One command starts the whole backend. The frontend is optional and has two modes.
Every part runs in its own container, so if one part crashes the others keep working.

## What runs where

| Container | What it is | Port | How to start |
|---|---|---|---|
| gateway | the one door the app talks to | 8000 | always |
| weather-service | Weather Monitoring Agent | 8001 | always |
| action-service | Action Suggestion Agent | 8002 | always |
| coordination-service | Coordination Agent | 8003 | always |
| learning-service | Learning Agent | 8004 | always |
| postgres (PostGIS) | one database per service | 5433 | always |
| redis | fast shared cache | 6379 | always |
| frontend-web | the app as a website (for demos, opens in any browser) | 3000 | profile `web` |
| frontend-dev | Expo dev server, for testing on a real phone with Expo Go | 8081 | profile `mobile` |

## First-time setup

1. Install Docker Desktop and make sure it is running.
2. In the repo root, copy `.env.example` to `.env` (PowerShell: `copy .env.example .env`).
3. Add these lines to the repo's `.gitignore` if they are not there yet:

       .env
       node_modules/
       dist/
       .expo/
       __pycache__/

## Commands

| I want to... | Command |
|---|---|
| Start only the backend | `docker compose up --build` |
| Backend + website version of the app | `docker compose --profile web up --build` then open http://localhost:3000 |
| Backend + phone testing | `docker compose --profile mobile up --build` |
| Check which services are alive | open http://localhost:8000/api/status |
| See the backend API docs | open http://localhost:8000/docs |
| Watch one service's logs | `docker compose logs -f coordination-service` |
| Stop one service (to test failure) | `docker compose stop weather-service` |
| Start it again | `docker compose start weather-service` |
| Stop everything | `docker compose down` |
| Wipe the databases and start clean | `docker compose down -v` |

## The frontend project

The `app/` folder already holds the WarnX mobile app (Expo, Expo Router, NativeWind, TypeScript). Nothing to create.
Its Docker files (`Dockerfile`, `Dockerfile.dev`, `nginx.conf`, `.dockerignore`) live in the same folder.
See `app/README.md` for how the app is organised and how to run it without Docker.

## Talking to the backend from the app

Read the backend address from this variable, never hard-code it:

    process.env.EXPO_PUBLIC_API_URL

- In `frontend-web`, it is set from `PUBLIC_API_URL` in `.env` when the image is built. If you change it, rebuild.
- In `frontend-dev`, it becomes `http://<HOST_IP>:8000` automatically.

Every request goes through the gateway (port 8000). For example: `POST /api/coordination/reports/verify`.
If a service is down, the gateway answers with status 503 and a short message.
The app should catch that and show a friendly message for that feature only.

## Testing on a real phone (profile `mobile`)

1. Phone and PC must be on the same Wi-Fi.
2. Find your PC's IPv4 address with `ipconfig` and put it in `.env` as `HOST_IP=192.168.x.x`.
3. Allow ports 8000 and 8081 in Windows Firewall when Windows asks.
4. Run `docker compose --profile mobile up --build`, then look at the terminal for the QR code, and scan it with Expo Go.
5. After you change `package.json`, run `docker compose --profile mobile up --build -V frontend-dev` so the container gets the new packages.

Honest note: Windows does not always tell Docker when a file changed, so live reload can be slow in this mode.
For everyday screen design, running `npx expo start` directly on your PC is faster. Use the Docker mode when you want everyone to have an identical setup.

## Team rules

- One person, one folder. Backend friends stay in their own `backend/services/<name>` folder. Frontend friends stay in `app/`.
- Every backend service must keep its `GET /health` endpoint.
- Services never import each other's code. They only talk over HTTP.
- Add Python packages to your own service's `requirements.txt` and rebuild that service: `docker compose up --build <service-name>`.
- Never commit `.env`. Never put API keys in code.
- `backend/infra/postgres/init.sql` only runs the first time. To add a new database later, run `docker compose down -v` and start again.
- If the website version is opened from another device, add its address (for example `http://192.168.1.20:3000`) to `CORS_ORIGINS` in `.env`.
