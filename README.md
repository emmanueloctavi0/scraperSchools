# scraperSchools
Comando hecho en Python que extrae la información de una escuela mexicana a travez de su CCT. 

### Requisitos

1. Python 3.7
```bash
python -m venv .env
```

Activar env en Linux
```bash
source .env/bin/activate
```

Activar env en Windows
```bash
.env\Scripts\activate.bat
```

Instalar requerimientos
```bash
python -m pip install --upgrade pip
pip install -r requirement.txt
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
