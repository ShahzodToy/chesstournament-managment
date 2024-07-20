# Django Project Setup

This is a sample Django project that demonstrates setting up a Django application with API documentation using `drf-yasg`.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Server](#running-the-server)
- [API Documentation](#api-documentation)
- [Creating Superuser](#creating-superuser)
- [Usage](#usage)


## Requirements

## API
-http://localhost:8000/swagger/

- Python 3.x
- pip (Python package installer)
- virtualenv (recommended)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ShahzodToy/chesstournament-managment.git
   cd yourproject

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

pip install -r requirements.txt

For API documentation 
pip install drf-yasg

python manage.py migrate

python manage.py runserver

Create Super to see what is happing in background

python manage.py createsuperuser


```About project Chess Tournamnet:

- **User Authentication and Authorization:**
    - Implement user registration and login functionality.
    - Use JWT for authentication.
    - Differentiate between regular users and admin users.
- **Player Management:**
    - Allow admins to add, update, delete, and view player information.
    - Player information should include name, age, rating, and country.
- **Tournament Management:**
    - Allow admins to create tournaments with specific start and end dates.
    - Each tournament should have a unique name and a list of participants.
    - Allow admins to assign players to tournaments.
- **Match Management:**
    - Automatically generate pairings for each round based on the Swiss-system tournament rules.
    - Allow admins to update the match results.
- **Leaderboard:**
    - Generate and display a leaderboard for each tournament showing the players' ranks, points, and other relevant statistics.


And also comperhensive api documentation for each endpoints with swagger and redoc tools:


**Project Endpoints Description**
User Management
User Registration:

Endpoint: POST /registration
View: SignUpView
Description: Allows new users to register by providing necessary information such as username, email, and password.
Email Verification:

Endpoint: POST /verify
View: VerifyAPIView
Description: Verifies a user's email address using a verification token sent to their email.
Resend Verification Email:

Endpoint: POST /re-send
View: GetNewVerification
Description: Resends the verification email to the user if they haven't received or lost the initial one.
Change User Information:

Endpoint: PUT /change-info
View: ChangeUserInformation
Description: Allows authenticated users to update their personal information such as name, email, or password.
Authentication
User Login:
Endpoint: POST /login

View: LoginViewApi
Description: Authenticates a user and returns a token for subsequent authenticated requests.
Admin User Management
View All Users:

Endpoint: GET /all-players
View: ViewUserInformation
Description: Allows admin users to view information about all registered users.
Delete User:

Endpoint: DELETE /delete-user/<str:username>
View: DeletePlayersView
Description: Allows admin users to delete a user account by specifying the username.
Update User Information (Admin):

Endpoint: PUT /update-playersinfo/<str:username>
View: ChangeUserInformationAdminView
Description: Allows admin users to update information for a specific user by username.
Tournament Management
Create Tournament:

Endpoint: POST /create-tournament
View: CreateTournamentView
Description: Allows users to create a new tournament by providing details such as name, date, and participants.
Generate Pairings:

Endpoint: POST /generate-pairings
View: GeneratePairingsView
Description: Generates match pairings for the tournament participants.
Update Match Result:

Endpoint: PUT /result-update/<int:match_id>
View: UpdateMatchResultView
Description: Allows users to update the result of a specific match by providing the match ID and result details.
Generate Leaderboard:

Endpoint: GET /leadbord/<int:tour_id>
View: GenerateLeaderBoardView
Description: Generates the leaderboard for a specific tournament by providing the tournament ID



## Thank you for you reading all the way down 😊😊😊😊