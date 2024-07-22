# Sumarizador de redes

Sumariza a partir de un un listado de redes indicado por el usuario.

## Script

Ejecutar el script:

```python
[user@fedora sumarize]$ python main.py -p 50
Ingresa las redes separadas por coma:
1.1.1.0/24, 3.3.3.0/24, 2.2.2.0/24, 3.3.2.0/24
['1.1.1.0/24', '2.2.2.0/24', '3.3.2.0/23']
Redes sumarizadas:
1.1.1.0/24
2.2.2.0/24
3.3.2.0/23
```

Las redes pueden ingresarse con o sin espacios, pero deben estar separadas por coma.

## Porcentaje de coincidencia

El porcentaje de coincidencia hace referencia al porcentaje que ocupan los hosts de una red con respecto a su superred. Por ejemplo, si tenemos las redes 10.10.0.0/24 y 10.10.2.0/24, estas no son contiguas pero se pueden sumarizar en la red 10.10.0.0/26 si el usuario así lo requiere, esta red contiene 1024 direcciones IP, la suma de las direcciones IP de las redes 10.10.0.0/24 y 10.10.2.0/24 es de 512, luego el porcentaje de coincidencia es 50%. Si el usuario ingresa un porcentaje mayor a 50%, las redes no se van a sumarizar.

## Github

- [DOPMA](https://github.com/Miguvasg/networksummarizer)

## Desarrollador

- [@Miguvasg](https://github.com/Miguvasg)
