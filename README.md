# flask_app


flask db init
flask db migrate
flask db upgrade 
flask user create <mail> <password>

pybabel extract -F babel.cfg -k _l -o app/resources/translations/messages.pot app
pybabel init -i app/resources/translations/messages.pot -d app/resources/translations -l en
pybabel compile -d app/resources/translations
After update translation
pybabel extract -F babel.cfg -k _l -o app/resources/translations/messages.pot app
pybabel update -i app/resources/translations/messages.pot -d app/resources/translations
pybabel compile -d app/resources/translations
redis
/usr/local/opt/redis/bin/redis-server /usr/local/etc/redis.conf
brew services start redis
brew services stop redis
celery
celery -A entry.cel worker -l INFO
test locale mail server
python -m smtpd -c DebuggingServer -n localhost:1025