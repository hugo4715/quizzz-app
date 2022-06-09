#!/bin/sh

# Pass environment variables to VueJS
echo "VUE_APP_QUIZ_API_URL=\"$QUIZ_API_URL\"" > .env
echo "VUE_APP_QUIZ_UI_URL=\"$QUIZ_UI_URL\"" >> .env
cat .env

# Run application
npm run serve