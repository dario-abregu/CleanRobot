# Agente Limpiador en Python

## Descripción

Este proyecto es una simulación de un agente limpiador utilizando Python y la biblioteca Tkinter para crear una interfaz gráfica. El agente puede limpiar un área definida por el usuario, representada como una matriz de celdas que pueden estar "sucias" o "limpias".

## Características

- **Interfaz Gráfica**: Desarrollada con Tkinter, permite a los usuarios ingresar el tamaño del suelo.
- **Validaciones**: Asegura que el número de filas y columnas no supere las 12 y que sean enteros positivos.
- **Proceso de Limpieza Visual**: El agente limpia celdas una por una, mostrando el proceso en tiempo real.
- **Mensajes Informativos**: Notifica al usuario cuando la limpieza ha terminado o si el área ya estaba limpia.
- **Reinicio de la Aplicación**: Permite reiniciar el proceso desde el principio sin cerrar la aplicación.

## Instrucciones de Uso

1. Ejecuta el script en un entorno que soporte Python 3.
2. Ingresa la cantidad de filas y columnas (máximo 12).
3. Presiona el botón "Iniciar" para comenzar la simulación.
4. Observa cómo el agente limpia el área, celda por celda.
5. Una vez finalizada la limpieza, puedes reiniciar el proceso.

## Código Explicado

El código se estructura de la siguiente manera:

- **Clase `AgenteLimpiador`**: 
  - Inicializa una matriz que representa el suelo, donde cada celda puede estar "sucia" o "limpia".
  - Contiene el método `limpiar` que cambia el estado de una celda a "limpia".

- **Clase `Aplicacion`**:
  - Hereda de `tk.Tk` y se encarga de crear la ventana principal.
  - Contiene métodos para crear la ventana de entrada, validar los datos ingresados, y gestionar la interfaz de limpieza.
  
- **Método `iniciar`**:
  - Valida la entrada del usuario y ajusta el tamaño de la ventana según el tamaño del suelo.
  - Llama a `crear_interfaz` para mostrar la matriz.

- **Método `crear_interfaz`**:
  - Crea botones para cada celda del suelo, y muestra los botones para limpiar todo y reiniciar.

- **Método `limpiar_todo`**:
  - Inicia el proceso de limpieza llamando a `proceso_limpiar`, que recorre cada celda, limpiando una por una con un retraso entre ellas para mostrar el progreso.

- **Método `mostrar_mensaje`**:
  - Muestra mensajes informativos al usuario sobre el estado de la limpieza.

## Requisitos

- Python 3.x
- Tkinter (incluido en la mayoría de las instalaciones de Python)

## Ejecución

Para ejecutar la aplicación, utiliza el siguiente comando en la terminal:

```bash
python nombre_del_script.py
