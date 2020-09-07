#!/bin/bash
#
# Script zum Fixen der Django Migrations
#

app="videosite"

echo "Bitte erst Migrations in der Datenbank löschen:"
echo "SQL: delete from django_migrations;"
echo

read -e -p "Datenbank bereinigt ? (J|N)" auswahl

if [ $auswahl == "J" ]; then

    rm  -rf $app/migrations/~
    python manage.py migrate --fake
    python manage.py makemigrations $app
    python manage.py migrate --fake-initial

    echo -e "\nNun kann das Migrationssystem wieder normal genutzt werden."

else
    echo "Ohne saubere Datenbank bringt das nix!"
    exit
fi
