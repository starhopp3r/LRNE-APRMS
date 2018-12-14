# 🧭 Compass Dashboard

The 🧭 Compass Dashboard is designed to be a simple, lean and mean piece of software that acts as a mission control for HADR teams to use.

When someone mentions mission control, massive projectors and data screens spring to mind. A mission control is a place where data needs to be localised and at the same time highly relevant and useful to the operator. This dashboard was made with this philosophy in mind.

## Caveats

Some browsers cache the dashboard's contents to minimize load time. This behavior affects the iframe refresh function that's fired every time the client side javascript receives an emit message from the web server. To mitigate the effects of caching; the server uses cache response directives. Users are requested to clear cache and session data using their browser's menu to solve this problem to good effect.

## Planned Features

Just a scratchpad here to help in guiding newborn features.

### Technical

1. A complete JavaScript-based implementation of the *Vitals* map.
2. Removal of iframes.

### Feature Set

1. Compute difference in before and after images using OpenCV.
2. Detecting flood areas on satellite images using OpenCV.

## Tested Environments

Tested locally on my development machine, MacBook Pro running macOS Mojave (v10.14.1) on the following browsers.

- Safari 12.0.1
- Google Chrome 71.0.3578.98
- Firefox Quantum 64.0

## Enpoints

POST endpoint: `http://0.0.0.0:5000/inlet`

Dashboard endpoint: `http://0.0.0.0:5000/`