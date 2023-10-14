
# BackEndBase
Sistema base para el desarrollo de Back-End's usando Python (codename: **Lilith**)


# Descripción
Este sistema, describe el uso y puesta a punto de una **Api rest** usando [**Python**](https://www.python.org/downloads/) y [**Flask**](http://flask.pocoo.org/)

![flask](http://flask.pocoo.org/static/badges/powered-by-flask-s.png)


## Documentación
Puedes encontrar la documentación completa en el [sitio web del proyecto.](http://docs.awesome-backend.appspot.com/)


## Listado de Cambios

El listado completo de cambios (changelog), [por aquí.](CHANGELOG.md)


# Requisitos
- [**Python**](https://www.python.org/downloads/) 3.7.x
- [**virtualenv**](https://virtualenv.pypa.io/en/stable/) (Recomendado)

## Activar virtualenv en entornos Gnu/Linux, Mac OS

```sh
$ virtualenv --python python3 env
$ source env/bin/activate
```


## Instalar las dependencias
Una vez dentro del entorno, instalar las dependencias:

```sh
(env) $ pip install -r requirements.txt
```

# Uso de Firestore en modo local (opcional)
Si se esta usando [**FireStore**](https://firebase.google.com/docs/) como base de datos, se puede usar en modo local, definiendo una variable de entorno en el S.O., que tenga la ruta de una [cuenta de servicio](https://cloud.google.com/docs/authentication/getting-started).

```
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```


tambien es posible hacer uso del archivo **.flaskenv**, ubicado en la raiz del proyecto y fijar la variable de entorno, mencionada arriba:

```.flaskenv
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```


# Iniciando el servidor web
A continuación se describen algunas configuraciones para iniciar el servidor web.


## Usando python

```sh
(env) $ python main.py
```


## Usando gunicorn

```sh
(env) $ gunicorn --bind 0.0.0.0:6969 --reload --log-level debug main:app
```

## Desplegar en Google App Engine

```sh
(env) $ gcloud app deploy --project PROJECT_ID --version VERSION_ID --no-promote
```


>La direccion y el puerto por defecto es: [**http://localhost:6969**](http://localhost:6969)


# Recomendaciones
Editor recomendado [SublimeText 3](http://www.sublimetext.com/3)

Si se está susando  [SublimeText](http://www.sublimetext.com) como editor, puede agregar esta configuracion al archivo **.sublime-project** para mejorar la experiencia de uso del editor.

```json
{
    "build_systems":
    [
        {
            "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
            "name": "Anaconda Python Builder",
            "selector": "source.python",
            "shell_cmd": "\"python\" -u \"$file\""
        }
    ],
    "folders":
    [
        {
            "folder_exclude_patterns":
            [
                ".gcloud",
                "env",
                "test",
                "dist",
                "lib"
            ]
        },
        {
            "path": "."
        }
    ]
}

```

>La configuracion anterior exluye de busquedas e indexación, las carpetas descritas.


# Estructura del Proyecto (Propuesta)
```text
/
├── app
│   ├── config
│   └── __init__.py
│   │   ├── databases
│   │   ├── google
│   │   └── local_settings.py
│   │   └── settings.py
│   ├── ext
│   ├── home
│   ├── uploads
│   └── test
│   └── __init__.py
├── .editorconfig
├── .flaskenv
├── .gitignore
├── CHANGELOG.md
├── app.yaml
├── main.py
├── README.md
├── requirements.txt
├── wsgi.py
```


> El folder **Test** se utiliza para archivos de pruebas y adicionalmente el folder **.gcloud** si se usa [Google Cloud Platform.](https://cloud.google.com/)
