# 🤖 Bot de Educación Bíblica para Iglesia

Un asistente virtual inteligente diseñado para potenciar la educación espiritual en la iglesia, proporcionando recursos bíblicos, devocionales, información de eventos y apoyo pastoral.

## 🎯 Funcionalidades Principales

### 📖 **Estudios Bíblicos Interactivos**
- **Búsqueda de versículos**: Encuentra versículos específicos por libro, capítulo y versículo
- **Historias bíblicas**: Narra historias bíblicas con lecciones espirituales
- **Conceptos bíblicos**: Explica términos y conceptos fundamentales de la fe
- **Estudios temáticos**: Recomienda estudios bíblicos organizados por temas

### 🙏 **Recursos Espirituales**
- **Devocionales diarios**: Reflexiones bíblicas para el crecimiento espiritual
- **Oraciones guiadas**: Oraciones por temas específicos (familia, sanidad, agradecimiento, etc.)
- **Ayuda espiritual**: Recursos para momentos difíciles y crisis espirituales
- **Consejo pastoral**: Información de contacto con líderes espirituales

### 🏛️ **Información de la Iglesia**
- **Horarios de servicios**: Información actualizada de todos los servicios
- **Eventos próximos**: Calendario de actividades y eventos especiales
- **Ministerios**: Información sobre diferentes ministerios y grupos
- **Contacto**: Datos de contacto del pastor y líderes

## 🚀 Funcionalidades Avanzadas

### 📱 **Sistema de Interacción Inteligente**
- **Reconocimiento de intenciones**: Entiende preguntas en lenguaje natural
- **Extracción de entidades**: Identifica libros bíblicos, capítulos, versículos y conceptos
- **Conversaciones contextuales**: Mantiene el contexto de la conversación
- **Respuestas personalizadas**: Adapta las respuestas según el usuario

### 🎨 **Recursos Multimedia**
- **Imágenes inspiradoras**: Acompaña las respuestas con imágenes motivacionales
- **Formato enriquecido**: Usa formato markdown para mejor presentación
- **Contenido estructurado**: Organiza la información de manera clara y accesible

## 🔥 **Nuevas Funcionalidades Avanzadas**

### 📚 **Contenido Bíblico Indexado Localmente**
- **Base de datos completa**: 5-10 libros bíblicos completos (Génesis, Éxodo, Salmos, Proverbios, Mateo, Juan, etc.)
- **Índice en memoria**: Búsquedas O(1) para respuestas instantáneas
- **80+ versículos**: Cobertura completa de pasajes fundamentales
- **Indexación automática**: Al arrancar el servidor, todos los versículos se indexan para búsquedas rápidas

### 🔍 **Búsqueda por Tema (Full-Text)**
- **Búsqueda semántica**: Encuentra versículos por palabras clave
- **Índice de temas**: Mini-índice de palabras clave en Python
- **Resultados relevantes**: Devuelve los 3-5 versículos más relevantes
- **Búsqueda inteligente**: No recorre toda la Biblia, solo las referencias asociadas

### 💬 **Flujo Conversacional Robusto**
- **Confirmaciones automáticas**: Después de cada respuesta clave pregunta "¿Te fue útil esta respuesta?"
- **Manejo de feedback**: Procesa respuestas afirmativas/negativas
- **Fallback inteligente**: Cuando no entiende, ofrece opciones claras
- **Conversación natural**: Mantiene el contexto y mejora con el uso

### 🎮 **Gamificación Mínima**
- **Quiz bíblico**: 3 preguntas de opción múltiple
- **Preguntas variadas**: Diferentes temas y niveles de dificultad
- **Almacenamiento local SQLite**: Guarda resultados {usuario, aciertos, fecha}
- **Sistema de puntuación**: Seguimiento del progreso del usuario
- **Estadísticas del usuario**: Historial de quizzes y ranking

## 📋 Comandos Disponibles

### 🔍 **Búsqueda Bíblica**
- `¿puedes mostrarme el versículo Juan 3:16?`
- `busco Génesis 1:1`
- `¿qué dice Salmos 23?`
- `necesito un versículo sobre amor`

### 🔍 **Búsqueda por Tema**
- `busco versículos sobre amor`
- `¿qué dice la Biblia sobre fe?`
- `necesito versículos de esperanza`
- `¿tienes pasajes sobre paz?`

### 📚 **Historias y Conceptos**
- `cuéntame la historia de Moisés`
- `¿qué pasó con David y Goliat?`
- `¿qué es la fe?`
- `explícame qué es la gracia`

### 🙏 **Recursos Espirituales**
- `necesito un devocional`
- `¿puedes orar por mí?`
- `necesito ayuda espiritual`
- `quiero orar por mi familia`

### 🏛️ **Información de Iglesia**
- `¿qué eventos hay en la iglesia?`
- `¿cuáles son los horarios?`
- `¿cuándo es el estudio bíblico?`
- `necesito hablar con el pastor`

### 🎮 **Gamificación**
- `quiero hacer un quiz`
- `empieza el quiz bíblico`
- `quiero probar mis conocimientos`
- `muéstrame mis estadísticas`
- `quiero ver mi ranking`

## 🛠️ Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- Rasa 3.x
- pip

### Instalación
```bash
# Clonar el repositorio
git clone [url-del-repositorio]
cd my_bible_bot

# Instalar dependencias
pip install -r requirements.txt

# Entrenar el modelo
rasa train

# Ejecutar el servidor de acciones
rasa run actions

# En otra terminal, ejecutar el bot
rasa shell
```

### Configuración Avanzada
1. **SQLite (Incluido)**: Para gamificación y métricas
   ```bash
   # Se crea automáticamente metrics.db en la raíz del proyecto
   # No requiere configuración adicional
   ```

2. **Personalizar contenido**: Edita `data/bible_content.json` con información específica de tu iglesia
3. **Ajustar respuestas**: Modifica `domain.yml` para personalizar las respuestas
4. **Agregar intenciones**: Expande `data/nlu.yml` con nuevos ejemplos
5. **Crear historias**: Añade nuevas conversaciones en `data/stories.yml`

## 📁 Estructura del Proyecto

```
my_bible_bot/
├── actions/
│   └── actions.py          # Acciones personalizadas con indexación
├── data/
│   ├── bible_content.json  # Contenido bíblico completo indexado
│   ├── nlu.yml            # Ejemplos de entrenamiento
│   ├── stories.yml        # Historias de conversación
│   └── rules.yml          # Reglas de comportamiento
├── models/                 # Modelos entrenados
├── config.yml             # Configuración del bot
├── domain.yml             # Dominio del bot
├── endpoints.yml          # Configuración de endpoints
├── sqlite_metrics.py      # Sistema de métricas local
├── requirements.txt       # Dependencias del proyecto
└── README.md             # Documentación
```

## 🔧 **Características Técnicas Avanzadas**

### 📊 **Sistema de Indexación**
- **BIBLE_INDEX**: Diccionario para búsquedas O(1) de versículos
- **TOPIC_INDEX**: Índice full-text para búsqueda por temas
- **Carga automática**: Al importar el módulo se indexa todo el contenido

### 🎯 **Búsqueda Inteligente**
- **Extracción de entidades**: Identifica libros, capítulos, versículos automáticamente
- **Búsqueda por tema**: Usa expresiones regulares para encontrar palabras clave
- **Resultados relevantes**: Elimina duplicados y limita resultados

### 💬 **Flujo Conversacional**
- **Confirmaciones**: Pregunta automáticamente si la respuesta fue útil
- **Fallback**: Maneja casos donde no entiende la intención
- **Contexto**: Mantiene información del usuario durante la sesión

### 🎮 **Gamificación**
- **Quiz aleatorio**: Selecciona 3 preguntas de un banco de 5
- **Almacenamiento local**: Guarda resultados en SQLite automáticamente
- **Puntuación**: Calcula porcentaje de aciertos
- **Estadísticas**: Historial de quizzes y ranking de usuarios

## 🎯 Próximas Mejoras

### 🔮 **Funcionalidades Futuras**
- **Sistema de recordatorios**: Notificaciones de eventos y devocionales
- **Quiz avanzado**: Más preguntas y diferentes niveles de dificultad
- **Plan de lectura personalizado**: Sugerencias de lectura según el nivel
- **Integración con redes sociales**: Compartir contenido en plataformas sociales
- **Sistema de mentores**: Conexión con líderes espirituales
- **Recursos multimedia**: Videos, podcasts y música de adoración
- **Análisis de crecimiento**: Seguimiento del progreso espiritual
- **Comunidad virtual**: Grupos de estudio y oración online

### 🤖 **Mejoras Técnicas**
- **Integración con APIs bíblicas**: Acceso a más contenido bíblico
- **Sistema de recomendaciones**: IA para sugerir contenido personalizado
- **Análisis de sentimientos**: Detectar necesidades espirituales
- **Multiidioma**: Soporte para diferentes idiomas
- **Integración con WhatsApp/Telegram**: Llegar a más personas
- **Base de datos completa**: Más libros bíblicos y contenido

## 📞 Soporte

Para soporte técnico o preguntas sobre el bot:
- **Email**: soporte@iglesia.com
- **Teléfono**: (591) 3-123-4567
- **WhatsApp**: +591 700-123-456

## 🙏 Agradecimientos

Este bot fue desarrollado para potenciar la educación espiritual y el crecimiento de la comunidad cristiana. Que Dios bendiga este proyecto y lo use para su gloria.

---

*"Y todo lo que hagáis, hacedlo de corazón, como para el Señor y no para los hombres."* - Colosenses 3:23 