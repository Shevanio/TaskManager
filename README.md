# 📋 TaskManager

Un gestor de tareas moderno con integración de IA para desglozar automáticamente tareas complejas en subtareas simples y accionables.

## ✨ Características

- **Gestión de tareas completa**: Agregar, listar, completar y eliminar tareas
- **Descomposición inteligente con IA**: Usa OpenAI para desglozar tareas complejas en subtareas
- **Persistencia de datos**: Almacenamiento automático en JSON
- **Interfaz interactiva**: Menú CLI intuitivo para operaciones
- **Estado de tareas**: Marca tareas como completadas con indicador visual (✅)

## 🚀 Inicio Rápido

### Requisitos previos

- Python 3.9+
- pip (gestor de paquetes de Python)
- Clave de API de OpenAI (para funcionalidades de IA)

### Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd TaskManager
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Edita .env y agrega tu OPENAI_API_KEY
```

### Uso

```bash
python main.py
```

Se abrirá un menú interactivo con las siguientes opciones:

```
 --- Task Manager --- 

1. Add Task                    # Agregar una tarea simple
2. Add complex Task (using AI) # Desglozar tarea con IA
3. Complete Task              # Marcar tarea como completada
4. List Tasks                 # Ver todas las tareas
5. Delete Task                # Eliminar una tarea
6. Update Tasks               # Recargar tareas desde archivo
7. Exit                       # Salir
```

## 📖 Ejemplos de uso

### Agregar una tarea simple
```
Enter your choice: 1
Enter task description: Comprar leche
Added task: [] #1 Comprar leche
```

### Desglozar una tarea compleja con IA
```
Enter your choice: 2
Enter complex task description: Organizar una conferencia tecnológica
```

La IA desglozará esto en subtareas como:
- Seleccionar ubicación y fecha
- Confirmar speakers y agenda
- Organizar logística y catering
- Promoción y registro de asistentes

Estas se agregarán automáticamente como tareas.

### Listar tareas
```
Enter your choice: 4
[] #1 Comprar leche
[✅] #2 Seleccionar ubicación y fecha
[] #3 Confirmar speakers y agenda
```

### Completar una tarea
```
Enter your choice: 3
Enter task id to complete: 1
Completed task: [✅] #1 Comprar leche
```

## 🏗️ Estructura del Proyecto

```
TaskManager/
├── main.py                    # Punto de entrada e interfaz CLI
├── task_manager.py            # Clase TaskManager y Task
├── ai_service.py              # Integración con OpenAI
├── tasks.json                 # Almacenamiento de tareas (generado)
├── requirements.txt           # Dependencias del proyecto
├── test_comprehensive.py      # Suite de tests completa
├── test.py                    # Tests básicos
└── README.md                  # Este archivo
```

## 🔌 API

### Clase Task

```python
task = Task(id, description, completed=False)

# Atributos
task.id           # int: ID único de la tarea
task.description  # str: Descripción de la tarea
task.completed    # bool: Estado de completación

# Métodos
str(task)         # str: Representación con emoji de estado
```

### Clase TaskManager

```python
manager = TaskManager()

# Métodos
manager.add_task(description)          # Task: Agrega una nueva tarea
manager.complete_task(id)              # Task|None: Marca como completada
manager.list_tasks()                   # List[Task]: Lista todas las tareas
manager.delete_task(id)                # Task|None: Elimina una tarea
manager.save_tasks()                   # None: Guarda en JSON
manager.load_tasks()                   # None: Carga desde JSON
manager.update_tasks()                 # None: Recarga desde archivo
```

### AI Service

```python
from ai_service import create_simple_tasks

# Desgloza una tarea en subtareas
subtasks = create_simple_tasks("Tarea compleja aquí")
# Retorna: List[str] de subtareas o error

# Ejemplo
subtasks = create_simple_tasks("Planificar un viaje a Europa")
for subtask in subtasks:
    print(subtask)
```

**Parámetros de la API OpenAI usados:**
- Modelo: `gpt-3.5-turbo`
- Temperatura: `0.7` (creatividad moderada)
- Max tokens: `300` (subtareas concisas)

## 🧪 Testing

El proyecto incluye una suite completa de tests con **30 casos de prueba** que cubren:

### Ejecutar todos los tests
```bash
python -m unittest test_comprehensive -v
```

### Tipos de tests incluidos

**Pruebas unitarias:**
- Creación y representación de tareas
- Operaciones CRUD de TaskManager
- Persistencia en JSON
- Manejo de errores
- Integración con OpenAI

**Pruebas de integración:**
- Workflow completo con IA
- Ciclo de vida de tareas

## ⚙️ Configuración

### Variables de entorno (.env)

```env
OPENAI_API_KEY=tu_clave_api_aqui
```

**Nota:** Nunca comitas el archivo `.env` con tu clave real.

### Archivo de almacenamiento (tasks.json)

Formato de almacenamiento:
```json
[
    {
        "id": 1,
        "description": "Comprar leche",
        "completed": false
    },
    {
        "id": 2,
        "description": "Estudiar Python",
        "completed": true
    }
]
```

## 🐛 Manejo de Errores

- **Clave API no configurada**: Se lanza `ValueError` si `OPENAI_API_KEY` no existe
- **API no disponible**: Se retorna un mensaje de error en lugar de fallar
- **ID de tarea no encontrado**: Operaciones retornan `None` silenciosamente
- **Archivo corrompido**: Se inicia con lista vacía

## 📋 Requisitos del Proyecto

```
openai>=1.0.0
python-dotenv>=0.19.0
```

Instala con:
```bash
pip install -r requirements.txt
```

## 🔐 Seguridad

- ⚠️ Nunca hardcodees tu API key
- ⚠️ Usa `.env` y nunca lo comitas
- ⚠️ Limita permisos de `tasks.json` si contiene datos sensibles

## 🤝 Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Notas de Desarrollo

### Estructura interna de TaskManager

- Las tareas se cargan en memoria al iniciar
- Se persisten en `tasks.json` después de cada operación
- IDs se auto-incrementan automáticamente
- El estado se mantiene entre sesiones

### Mejoras futuras

- [ ] Categorías y tags para tareas
- [ ] Fechas de vencimiento
- [ ] Prioridades
- [ ] Subtareas anidadas
- [ ] Base de datos (SQLite/PostgreSQL)
- [ ] API REST
- [ ] Interfaz web
- [ ] Soporte para múltiples usuarios

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado como herramienta de demostración de gestión de tareas con IA.

---

**¿Preguntas?** Revisa los tests en `test_comprehensive.py` para ver más ejemplos de uso.
