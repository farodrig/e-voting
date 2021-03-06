# e-voting

Proyecto para el Curso de Seguridad de Software del Departamento de Ciencias de la Computación de la Universidad de Chile.

Este consta de una aplicación web para poder crear encuestas públicas y privadas, mandar invitaciones para responder encuestas y poder ver los resultados globales y parciales de estas.

## Inicialización de la App:

    La App funciona utilizando mysql como Sistema de Administración de Base de Datos. Esta debe esar instalada para poder utilizar la app.
    Tambien, se debe crear una Base de Datos llamada "evoting" para que los pasos siguientes funcionen.
    Esto puede ser modificado en evoting/settings.py donde se puede modificar:
        - El nombre de la base de datos.
        - El usuario de mysql.
        - La contraseña de dicho usuario.
        - El host del servidor de Mysql
        - El puerto donde corre Mysql en el anterior host.


	Para hacer funcionar la app tambien deben instalarse los siguientes paquetes:
		- Django 1.8
		- MySQL-python 1.2.5 *

	Esta instalación puede ser hecha a traves de pip o de forma manual.
	Para hacerlo con pip se puede llamar de la siguiente forma:
		$ pip install -r requirements.txt

	* En algunos casos lanza error por la falta del archivo mysql_config, se puede solucionar con el siguiente comando:
	    - sudo apt-get install libmysqlclient-dev


## Ejecución de la App:

	Para hacer correr la app, simplemente siga los siguientes pasos:
	    $ python manage.py migrate
	    $ python manage.py loaddata initData.json
		$ python manage.py runserver

	La aplicación quedará corriendo por defecto en: http://localhost:8000/

El repositorio de la aplicación se puede encontrar en: https://github.com/farodrig/e-voting