@echo off
echo ===== Starting Heroku Deployment Process =====
echo.

echo Step 1: Installing required packages...
pip install gunicorn
pip install -r "Flask Deployed App\requirements.txt"
echo.

echo Step 2: Navigating to project directory...
cd "Flask Deployed App"
echo.

echo Step 3: Initializing Git repository...
git init
echo.

echo Step 4: Adding all files to Git...
git add .
echo.

echo Step 5: Committing changes...
git commit -m "Initial commit for Heroku deployment"
echo.

echo Step 6: Login to Heroku (browser will open)...
heroku login
echo.

echo Step 7: Creating Heroku application...
heroku create plant-disease-detector
echo.

echo Step 8: Setting environment variables...
heroku config:set GROQ_API_KEY=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
echo.

echo Step 9: Deploying to Heroku...
git push heroku master
echo.

echo Step 10: Starting Heroku dyno...
heroku ps:scale web=1
echo.

echo Step 11: Opening application in browser...
heroku open
echo.

echo ===== Deployment Complete! =====
echo Your application is now live at https://plant-disease-detector.herokuapp.com/
echo.

pause 