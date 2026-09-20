# WarnX mobile app

React Native (Expo) + Expo Router + NativeWind (Tailwind) + TypeScript.

## Folders

    app/                    screens (each file is a route)
      _layout.tsx           root layout, loads global.css
      (tabs)/               bottom tabs: Home, Alerts, Community, Recover
    src/
      api/                  talks to the backend gateway (client.ts, status.ts)
      components/           reusable pieces (ScreenContainer, ServiceStatusCard)
      hooks/                data hooks (useServiceStatus)
      i18n/                 Sinhala / Tamil / English text (empty for now)
    assets/                 icons and images
    tailwind.config.js      colors (brand + alert levels) live here

The folder named `app` inside `app` is normal for Expo Router. It is where the screens live.

## Run it on your PC without Docker

    npm install
    npx expo start

Press `w` for the browser, or scan the QR code with Expo Go on your phone.
The backend address comes from `EXPO_PUBLIC_API_URL`. Create a file named `.env` in this folder:

    EXPO_PUBLIC_API_URL=http://192.168.x.x:8000

Use your PC's Wi-Fi IP address (from `ipconfig`) when testing on a phone. Do not commit `.env`.

## Run it with Docker

See `DOCKER.md` in the repo root.

## Rules

- Every call to the backend goes through `src/api/client.ts`. Never write the server address inside a screen.
- If the backend is down, show a friendly message for that feature only. The rest of the app must keep working.
- After adding a package, use `npx expo install <package>` so the version matches Expo.
- Run `npm run typecheck` before you push.
