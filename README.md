# 5g-edge-network

## Acutalizar Repositorio
Antes de trabajar, estando dentro de la carpeta local del proyecto, ejecutar:
git checkout main
git pull origin main

## Trabajar con una tarea
Cuando se trabaje con una tarea, es importante crear una branch (rama) y programarlo ahí, cuando ya esté terminado se sube el branch.

El nombre de la rama debe iniciar con un prefijo, a corde el tipo:
feature/ (Desarrollo de nuevas funciones)
net/ (Infraestructura de red)
doc/ (Creación o edición de documentación)
bugfix/ (errores menores en branch)
hotfix/ (errores criticos en producción)

Ejemplo de la creación de una rama para crear una base de datos
**git checkout -b feature/nombre-de-la-tarea**

## Subir los cambios
Dentro de la carpeta del proyecto en terminal, usar los siguientes comandos para subir cambios:

**git add .**  (añade los cambios realizados)
**git commit -m "Mensaje intuitivo de lo que contiene el cambio"**
**git push origin feature/nombre-de-la-tarea**

# Creación de tareas del Sprint
1. **Descripción de la tarea**
  (Descripción clara y concisa de lo que se va a implementar

2. **Componentes afectados**
- [] Contenedor PostgresSQL
- [] Scipts de red ('tc')

3. **Criterios de Aceptación**
   1. El código pasa las pruebas sugeridas
   2. Compila correctamente
   3. Existe comunicación
