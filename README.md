# 5g-edge-network

## Acutalizar Repositorio
Antes de trabajar, estando dentro de la carpeta local del proyecto, ejecutar:

```git checkout main```

```git pull origin main```

## Trabajar con una tarea
Cuando se trabaje con una tarea, es importante crear una branch (rama) y programarlo ahí, cuando ya esté terminado se sube el branch.

- El nombre de la rama debe iniciar con un prefijo, a corde el tipo:

```feature/``` ( Actividad relacionada con la programación (backend) y Conexiones, modelos y scripts (database).

```net/``` (Comandos de kernel traffic control, latencias y configuración de bridges (network).

```docs/``` (Actualizaciones del archivo README.md, manuales o matrices de puertos (documentation)).

```bugfix/``` (Fallos encontrados dentro de una rama de desarrollo, atención de menor prioridad).

```hotfix/``` (Errores críticos detectados en producción, requieren atención inmediata).

```infra/``` (Configuraciones de Docker, contenedores y entornos base (Infraestructura).

- Ejemplo de la creación de una rama para crear una base de datos

```git checkout -b feature/nombre-de-la-tarea```

## Subir los cambios
Dentro de la carpeta del proyecto en terminal, usar los siguientes comandos para subir cambios:

```git add .```  (añade los cambios realizados)

```git commit -m "Mensaje intuitivo de lo que contiene el cambio```

```git push origin feature/nombre-de-la-tarea```

# Creación de tareas del Sprint
1. **Descripción de la tarea**
  (Descripción clara y concisa de lo que se va a implementar

2. **Componentes afectados**
- Contenedor PostgresSQL
- Scipts de red ('tc')

3. **Criterios de Aceptación**
- [ ] El código pasa las pruebas sugeridas
- [ ] Compila correctamente
- [ ] Existe comunicación
