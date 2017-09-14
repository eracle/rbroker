echo "yes" | python manage.py flush
python manage.py loaddata fixtures/data.json
python manage.py runserver

