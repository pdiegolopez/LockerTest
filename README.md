# Prueba Pedro Diego López Maroto

### FastAPI
Se ha realizado la prueba con Fast API ya que tiene una sintaxis similar a
Flask pero incluye una buena cantidad de mejoras como:
 + Soporte Async
 + Validación automática mediante modelos pydantic
 + Generación automática de Swagger


### Próximos pasos
Para esta prueba no se han implementado:
+ Llamadas a base de datos Async
+ No se ha realizado un CRUD dedicado haciendo llamadas a SQLite directamente en los endpoints
+ Despliege productivo junto a Nginx con docker-compose y replicas
+ Base de datos postgres
+ En los scripts implementar argumentos de entrada introducibles por el usuario

### Levantar el servicio Rest API

Para levantar el servicio hay que generar la imagen docker y después
ejecutarla. Se puede hacer mediante estos comandos.

```commandline
docker build -t app .
docker run -it --rm -p 8000:8000 app
```

Una vez levantado se dispondrá de un swagger en http://127.0.0.1:8000/docs

### Realizar carga de datos

Para realizar la carga de datos podemos reaprovechar la imagen docker
que ya tiene las librerías necesarias instaladas. En otra terminal y
con el servicio Rest API levantado ejecutar lo siguiente.

```commandline
docker run -it --rm app python3 /code/app/src/load_data.py
```

### Generar datos en csv
Para ejecutar este programa y obtener los datos es recomendable ejecutar
la imagen docker con un nombre de contenedor para poder obtener los ficheros

```commandline
docker run -it --name data app python3 /code/app/src/generate_data.py
docker cp data:/code/app/data .
docker container rm data
```
Con esto tendremos la carpeta data en el directorio actual con los ficheros
csv dentro.