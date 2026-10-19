import os
from durus.file_storage import FileStorage
from durus.connection import Connection
from durus.persistent_dict import PersistentDict
from models import Alumno, Calificacion

class EscuelaRepository:
    def __init__(self, db_path="data/escuela.durus"):
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        self.storage = FileStorage(db_path)
        self.connection = Connection(self.storage)
        # Caracteristica 5: Persistencia por alcanzabilidad
        self.root = self.connection.get_root()

        # Usamos un PersistentDict para simular la colección principal de la escuela
        if "alumnos" not in self.root:
            self.root["alumnos"] = PersistentDict()
            self.connection.commit()

        self.alumnos = self.root["alumnos"]

    def close(self):
        self.storage.close()

    def commit(self):
        self.connection.commit()

    def abort(self):
        self.connection.abort()

    def registrar_alumno(self, nombre, apellido, email, matricula, grado):
        alumno = Alumno(nombre, apellido, email, matricula, grado)
        self.alumnos[matricula] = alumno
        self.commit()
        return alumno

    def obtener_alumno(self, matricula):
        return self.alumnos.get(matricula)

    def eliminar_alumno(self, matricula):
        if matricula in self.alumnos:
            del self.alumnos[matricula]
            self.commit()

    def obtener_todos_los_alumnos(self):
        return list(self.alumnos.values())

    def buscar_alumnos_destacados(self, promedio_minimo):
        destacados = []
        for alumno in self.alumnos.values():
            if alumno.calcular_promedio() > promedio_minimo:
                destacados.append(alumno)
        return destacados
    
    def buscar_alumnos_con_reprobadas(self):
        alumnos_reprobados = []
        for alumno in self.alumnos.values():
            for calificacion in alumno.get_calificaciones():
                if calificacion.get_valor() < 6.0:
                    alumnos_reprobados.append(alumno)
                    break 
        return alumnos_reprobados