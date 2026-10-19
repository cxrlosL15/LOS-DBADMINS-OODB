from durus.persistent import Persistent
from durus.persistent_list import PersistentList

# Caracteristica 1 y 3: Las clases heredan de Persistent, Usuario es la superclase
class Usuario(Persistent):
    def __init__(self, nombre, apellido, email):
        # Caracteristica 2: Encapsulamiento, usamos el prefijo _ para proteger los atributos
        self._nombre = nombre
        self._apellido = apellido
        self._email = email

    def consultar_informacion(self):
        return f"{self._nombre} {self._apellido} - {self._email}"

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre):
        self._nombre = nombre

    def get_apellido(self):
        return self._apellido

    def set_apellido(self, apellido):
        self._apellido = apellido

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email

class Alumno(Usuario):
    def __init__(self, nombre, apellido, email, matricula, grado):
        super().__init__(nombre, apellido, email)
        self._matricula = matricula
        self._grado = grado
        # Caracteristica 4: Objeto complejo, en vez de llaves foráneas como en SQL, guardamos
        # las calificaciones directamente en una lista persistente nativa
        self._calificaciones = PersistentList()

    def calcular_promedio(self):
        if not self._calificaciones:
            return 0.0
        total = sum(c.get_valor() for c in self._calificaciones)
        return total / len(self._calificaciones)

    def asignar_calificacion(self, calificacion):
        self._calificaciones.append(calificacion)

    def consultar_informacion(self):
        info_base = super().consultar_informacion()
        promedio = self.calcular_promedio()
        return f"[{self._matricula}] {info_base} | Grado: {self._grado} | Promedio: {promedio:.2f}"

    def get_matricula(self):
        return self._matricula

    def get_grado(self):
        return self._grado

    def set_grado(self, grado):
        self._grado = grado

    def get_calificaciones(self):
        return self._calificaciones

class Calificacion(Persistent):
    def __init__(self, materia_id, unidad, valor):
        self._materia_id = materia_id
        self._unidad = unidad
        self.set_valor(valor)

    def get_valor(self):
        return self._valor

    def set_valor(self, valor):
        if not (0 <= valor <= 10):
            raise ValueError("La calificacion debe estar entre 0 y 10")
        self._valor = valor

    def get_materia_id(self):
        return self._materia_id

    def get_unidad(self):
        return self._unidad