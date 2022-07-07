# News Papers Scrape
Sistema de Crawling para extracción de noticias relacionadas con la Universidad de Granada.

## Comando docker
Para levantar todo (realizando la construcción de la imagen de 0) realizar:
```docker-compose up --build -d```

Si ya tenemos la imagen construida no hace falta hacer --build luego hacemos:
```docker-compose up -d```

Si queremos tirar todo tan solo hacemos:
```docker-compose down```

Y crearán dos directorios (en los que mapeamos mongo db), que pueden borrarse con sudo:
```sudo rm -rf dump datos_db```
