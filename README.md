# scraperSchools
Comando hecho en Python que extrae la información de una escuela mexicana a travez de su CCT. 

### Requisitos

1. Python 3.7
2. Tener instalado el modulo click
```bash
pip3 install click
```

### Ejecutar el script

* Ver todos los comandos
```bash
python3 scrap.py --help
```

* Obtener los datos de una escuela a partir de su CCT.
```bash
python3 scrap.py --cct 20PPR0001O
```

* Obtener los datos de una escuela a partir de su CCT y guardarlo en un archivo dataSchool.json
```bash
python3 scrap.py --cct 20PPR0001O --to-json > data.json
```
