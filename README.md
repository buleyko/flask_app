# flask_app


flask db init
flask db migrate
lask db upgrade 
flask user create <mail> <password>

pybabel extract -F babel.cfg -k _l -o app/resources/translations/messages.pot app
pybabel init -i app/resources/translations/messages.pot -d app/resources/translations -l en
pybabel compile -d app/resources/translations
After update translation
pybabel extract -F babel.cfg -k _l -o app/resources/translations/messages.pot app
pybabel update -i app/resources/translations/messages.pot -d app/resources/translations
pybabel compile -d app/resources/translations