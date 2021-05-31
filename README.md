# Melodic

Melodic e уеб апликация, с която може да слушате музика, да качвате песни и подкасти и да създавате плейлисти. 

## Направени точки 
I Milestone

- [X] basic UI
- [X] Authentication
- [X] Upload songs
- [X] Search songs

II Milestone

- [X] fix bug with overwriting songs when the file name is the same
- [X] fuzzyseacrh (over all important fields - name, artists, etc)

- [X] Player with
  - [X] song
  - [X] control for repeat/shuffle

- [ ] playlist management
- [ ] extend player and search to use playlist
- [X] extract mp3 metadata and prepopulate upload form

III Milestone
- [ ] CRUD on songs
- [ ] similar songs
- [X] improve UI (should be very polished)
## Как да инсталираме проекта?

Ако нямате инсталиран virtual environment, може да го направите като инсталирате python3-venv pakackage-a:

```bash
sudo apt install python3-venv
```

Тогава, трябва да създадете своят virtual environment:

```bash
python3 -m venv venv
```

После трябва да го активирате по следния начин:

```bash
source venv/bin/activate
```

След което инсталирате dependency-тата:

```bash
pip install -r requirements.txt
```

И накрая пускате проекта:

```bash
python run.py
```

## Използвани технологии

[Python 3](https://www.python.org)

[Flask](https://flask.palletsprojects.com/en/1.1.x/)

[HTML](https://devdocs.io/html/)

[CSS](https://devdocs.io/css/)

[Bootstrap](https://getbootstrap.com)

[Java Script](https://devdocs.io/javascript/)

## Автори на прокета

Мартин Врачев - програмист, дизайнер
Александър Йорданов - програмист, дизайнер

