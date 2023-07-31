# U731 Server Requirements

## Hardware Requirements
- macOS 10.15.4 or later
- Windows 10 or later

## Software Requirements
- Python v3.8 or later ([Download here](https://python.org/downloads))
- Git v2.26.2 or later ([Download here](https://git-scm.com/downloads))

## Environment Variable Requirements

- `APIKey`: API Key to be used by JS files on the front-end to authorise requests to the API.
- `AccessPassword`: Password to be used to access the system's admin panel.
- `EmailingServicesEnabled`: Set to `True` to enable emailing services (aka email user when feedback received).
- `SystemEmail`: Email address to be used by the system to send emails (must be gmail email address that has 2FA on with an app password generated).
- `SystemEmailAppPassword`: App password generated for the system email address.
- `RuntimePort`: Port number that the server should be serving at.

© Copyright 2023 Prakhar Trivedi