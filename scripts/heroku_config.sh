heroku config:set FLASK_ENV=production
heroku config:set DATABASE_URL='postgres://ektuvpjbwccunx:c3fe1fb1c95d0c3759b5dad14b0b6aed666818051bae0d42ea5010026789bacf@ec2-107-22-163-220.compute-1.amazonaws.com:5432/d4blv1ufhm7ut9'
heroku config:set APP_SETTINGS='project.config.ProductionConfig'