SET PARAM = %~1
IF  "%1" == "" GOTO dump
GOTO load
:dump
python manage.py dumpdata --format=xml --indent 2 auth > data/initial_data/users.xml 
python manage.py dumpdata --format=xml --indent 2 admin > data/initial_data/admin.xml
python manage.py dumpdata --format=xml --indent 2 Forum > data/initial_data/forum.xml 
python manage.py dumpdata --format=xml --indent 2 Blog > data/initial_data/blog.xml 
python manage.py dumpdata --format=xml --indent 2 Biblio > data/initial_data/biblio.xml 
python manage.py dumpdata --format=xml --indent 2 Apuntes > data/initial_data/apuntes.xml 
python manage.py dumpdata --format=xml --indent 2 UserMechanics > data/initial_data/user_mechanics.xml 
GOTO end
:load
python manage.py loaddata --format=xml data/initial_data/user.xml
python manage.py loaddata --format=xml data/initial_data/admin.xml
python manage.py loaddata --format=xml --app Forum data/initial_data/forum.xml
python manage.py loaddata --format=xml --app Blog data/initial_data/blog.xml
python manage.py loaddata --format=xml --app Biblio data/initial_data/biblio.xml
python manage.py loaddata --format=xml --app Apuntes data/initial_data/apuntes.xml
python manage.py loaddata --format=xml --app UserMechanics data/initial_data/user_mechanics.xml
:end