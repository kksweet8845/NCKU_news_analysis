# NCKU_news_analysis


## Build up environment

- Install dependencies
```
$ npm install
$ pip install -r requirements.txt
```
- Set up configurations
```
$ npm run default-config # go to modify the config.ini file
```
You need to set up `engine`, `name`, `user`, `password`, `host`, `port`.

## Some simple django commands

run server(inside news_site folder)
```
$ python manage.py runserver
```

shell
```
$ python manage.py shell
```

makemigrations
```
$ python manage.py makemigrations
```

migrate
```
$ python manage.py migrate newsdb
```
