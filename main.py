from repository import EscuelaRepository
from models import Calificacion

"""
Demostración de BDOO para el proyecto COBACH
Aqui ejecutamos un flujo de limpieza, creación y consultas para demostrar el CRUD y 
las caracteristica de la rúbrica
"""

def main():
    repo = EscuelaRepository("data/escuela.durus")

    if repo.obtener_alumno("MAT-001"):
        repo.eliminar_alumno("MAT-001")
    if repo.obtener_alumno("MAT-002"):
        repo.eliminar_alumno("MAT-002")

    alumno1 = repo.registrar_alumno("Carlos", "Ramirez", "carlos@cobach.mx", "MAT-001", "4to Semestre")
    alumno2 = repo.registrar_alumno("Ana", "Torres", "ana@cobach.mx", "MAT-002", "4to Semestre")

    alumno1 = repo.obtener_alumno("MAT-001")
    alumno1.set_nombre("Carlos Alberto")
    repo.commit()

    alumno1.asignar_calificacion(Calificacion(101, 1, 9.0))
    alumno1.asignar_calificacion(Calificacion(102, 1, 8.5))
    repo.commit()

    alumno2.asignar_calificacion(Calificacion(101, 1, 7.0))
    alumno2.asignar_calificacion(Calificacion(102, 1, 5.5))
    repo.commit()

    print("--- PRUEBA DE ENCAPSULAMIENTO ---")
    try:
        cal_invalida = Calificacion(103, 1, 11.5)
        alumno1.asignar_calificacion(cal_invalida)
    except ValueError as e:
        print(e)

    print("\n--- PRUEBA DE TRANSACCIONES (ABORT) ---")
    total_previo = len(alumno1.get_calificaciones())
    alumno1.asignar_calificacion(Calificacion(104, 1, 8.0))
    repo.abort()
    
    alumno1 = repo.obtener_alumno("MAT-001")
    total_post_abort = len(alumno1.get_calificaciones())
    print(total_previo == total_post_abort)

    print("\n--- PRUEBA DE HERENCIA Y POLIMORFISMO ---")
    print(alumno1.consultar_informacion())

    print("\n--- PRUEBA DE NAVEGACION DEL GRAFO ---")
    # Consulta 1 
    # SELECT a.matricula, a.nombre, AVG(c.calificacion) as promedio 
    # FROM alumnos a JOIN calificaciones c ON a.id = c.alumno_id 
    # GROUP BY a.id HAVING promedio > 8.0;
    
    destacados = repo.buscar_alumnos_destacados(8.0)
    for destacado in destacados:
        print(f"Destacado: {destacado.consultar_informacion()}")

    # Consulta 2
    # SELECT DISTINCT a.matricula, a.nombre 
    # FROM alumnos a JOIN calificaciones c ON a.id = c.alumno_id 
    # WHERE c.calificacion < 6.0;
    
    con_reprobadas = repo.buscar_alumnos_con_reprobadas()
    for al in con_reprobadas:
        print(f"Alerta: {al.consultar_informacion()}")

    print("\n--- PRUEBA DE ELIMINACION EN CASCADA Y CRUD ---")
    repo.eliminar_alumno("MAT-001")
    eliminado = repo.obtener_alumno("MAT-001")
    print(eliminado is None)

    repo.close()

if __name__ == "__main__":
    main()