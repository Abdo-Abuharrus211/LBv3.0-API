# LBv3.0

LBv3.0 is a very special project that I built for a friend. Unfortunately, it's very personal and therefore private, 
but the concept is a personal space on the Web featuring a memories gallery and some fun minigames inlcuding a nostalgia quiz.

The client app is built using TypeScript, vanilla React, and Vite, and is pretty simple and lightweight.
This Flask server is the backend for the app.

# Details
The server handles the following:
- Managing the database connection and queries
- Handling HTTP(S) requests from the client
- Executing business logic to process the minigame
- Verifying permitted users upon sign up and login
- Handling authentication and user sessions
- Sending responses back to the client app

# Deployment
Flask is wrapped in Gunicorn WSGI server, and is containerized using Docker.
The image is then built and deployed from DockerHub on Render.




