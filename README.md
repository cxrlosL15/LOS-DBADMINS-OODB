# Implementación BDOO con Durus

Demostración de una Base de Datos Orientada a Objetos adaptada a partir del sistema escolar para COBACH, utilizando Python y Durus.

## Estructura del proyecto
* `models.py`: Clases persistentes (`Usuario`, `Alumno`, `Calificacion`). Demuestra encapsulamiento, herencia y relaciones complejas (`PersistentList`).
* `repository.py`: Clase `EscuelaRepository` encargada de la persistencia por alcanzabilidad desde el root (`PersistentDict`), transacciones (`commit`/`abort`) y consultas.
* `main.py`: Pruebas realizadas para validar el funcionamiento.

## Instalación y Ejecución

Instalar dependencias:
```bash
pip install -r requirements.txt
python main.py
```
