# 🧭 Compass Dashboard

The 🧭 Compass Dashboard is designed to be a simple, lean and mean piece of software that acts as a mission control for HADR teams to use.

When someone mentions mission control, massive projectors and data screens spring to mind. A mission control is a place where data needs to be localised and at the same time highly relevant and useful to the operator. This dashboard was made with this philosophy in mind.

## Caveats

Not known.

## Tested Environments

Tested locally on my development machine, MacBook Pro running macOS Mojave (v10.14.1) on the following browsers.

- Safari 12.0.1
- Google Chrome 71.0.3578.98
- Firefox Quantum 64.0

## Enpoints

POST endpoint: `http://0.0.0.0:5000/inlet`

Dashboard endpoint: `http://0.0.0.0:5000/`

To launch server: `FLASK_ENV=development FLASK_APP=server.py DEBUG=True flask run --host=0.0.0.0`