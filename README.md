# Maika Alpha

Backend conversacional basado en Rasa para M.A.I.K.A. Este repositorio concentra el "cerebro" del bot: NLU, reglas, historias, acciones personalizadas, contenido biblico indexado y metricas locales.

## Objetivo

Este proyecto resuelve tres cosas:

- interpretar mensajes en lenguaje natural relacionados con Biblia, oracion, devocionales y dinamicas de jovenes
- responder con contenido estructurado usando `domain.yml`, `stories.yml`, `rules.yml` y acciones Python
- exponer un webhook REST que pueda ser consumido por la app Flutter principal

## Stack

- Python 3.8+
- Rasa 3.x
- rasa-sdk
- SQLite local para metricas y resultados

## Capacidades principales

- busqueda de versiculos por libro, capitulo y versiculo
- busqueda por tema usando indices en memoria
- historias y conceptos biblicos
- devocionales y oraciones guiadas
- informacion de iglesia y apoyo pastoral
- quiz biblico y estadisticas
- respuestas con metadatos emocionales para el avatar

## Arquitectura

```text
Usuario/App Flutter
    ->
REST webhook de Rasa
    ->
NLU + policies
    ->
domain.yml / stories.yml / rules.yml
    ->
actions.py y acciones auxiliares
    ->
respuesta JSON para cliente Flutter
```

### Flujo interno

1. El cliente envia un mensaje al endpoint `/webhooks/rest/webhook`.
2. Rasa clasifica intent, entidades y contexto.
3. Core decide entre respuesta estatica o accion personalizada.
4. Si aplica, `actions.py` consulta contenido local o metricas.
5. La respuesta vuelve como texto y, en varios casos, con `emotion` para el avatar.

## Archivos clave

### Configuracion de Rasa

- `config.yml`: pipeline NLU y policies
- `domain.yml`: intents, slots, respuestas, acciones declaradas
- `endpoints.yml`: endpoint del action server
- `credentials.yml`: canales soportados

### Datos conversacionales

- `data/stories.yml`: historias guiadas
- `data/rules.yml`: reglas directas
- `data/nlu.yml`: ejemplos NLU si existe en tu rama de trabajo

### Logica de negocio

- `actions/actions.py`: acciones principales
- `actions/action_trivia.py`: trivia
- `actions/action_srs.py`: repaso espaciado
- `actions/action_missions.py`: misiones
- `actions/action_bingo.py`: bingo de valores

### Persistencia y metricas

- `sqlite_metrics.py`: acceso a metricas locales
- `metrics.db`: base SQLite generada localmente

### Contenido y documentacion

- `data/`: contenido biblico y datasets
- `INDICE_DOCUMENTACION.md`: mapa del resto de documentos

## Estructura del proyecto

```text
Maika_beta_1/
  actions/
  data/
  models/
  results/
  tests/
  tools/
  config.yml
  domain.yml
  endpoints.yml
  credentials.yml
  sqlite_metrics.py
  evaluate_model.py
  README.md
```

## Arranque rapido

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Entrenar el modelo

```bash
rasa train
```

### 3. Levantar el action server

```bash
rasa run actions
```

### 4. Levantar el servidor del bot

```bash
rasa run --enable-api --cors "*"
```

### 5. Probar por consola

```bash
rasa shell
```

## Comandos utiles

```bash
rasa data validate
rasa train
rasa test
rasa shell
rasa run --enable-api --cors "*"
rasa run actions
```

## Integracion con Flutter

La app principal consume este bot via HTTP. Archivos de referencia del lado Flutter:

- `lib/core/constants/rasa_config.dart`
- `lib/data/datasources/rasa_api.dart`
- `lib/presentation/pages/chat/avatar_rasa_service.dart`

### Contrato esperado

Entrada:

```json
{
  "sender": "avatar_user",
  "message": "quiero un devocional"
}
```

Salida tipica:

```json
[
  {
    "text": "Aqui tienes tu devocional...",
    "custom": {
      "emotion": "inspirada"
    }
  }
]
```

En acciones personalizadas tambien puede devolverse:

```json
{
  "json_message": {
    "emotion": "feliz"
  }
}
```

## Respuestas emocionales

El bot puede adjuntar `emotion` para que el cliente Flutter cambie el avatar visual. Eso se hace desde:

- respuestas estaticas en `domain.yml`
- `send_emotional_message()` en `actions/actions.py`

Ejemplos de emociones usadas:

- `feliz`
- `triste`
- `inspirada`
- `orando`
- `dudando`
- `feliz_logro`
- `sonrojada`

## Contenido indexado y busqueda

Una parte importante del rendimiento viene del contenido cargado e indexado al inicio:

- `BIBLE_INDEX`: acceso rapido a versiculos puntuales
- `TOPIC_INDEX`: busqueda por palabras clave
- `QUIZ_DATA`: preguntas para quiz y trivia

Esto evita recorrer todo el contenido en cada consulta y permite respuestas mas rapidas.

## Quiz y metricas

El sistema de quiz guarda datos locales para medir uso y progreso:

- resultados por usuario
- historial de quizzes
- ranking basico
- consultas de uso

Archivos clave:

- `sqlite_metrics.py`
- `metrics.db`

## Evaluacion y pruebas

Archivos utiles:

- `evaluate_model.py`: evaluacion del modelo
- `tests/`: pruebas del proyecto
- `test_rng.py`: pruebas auxiliares

Comandos tipicos:

```bash
python evaluate_model.py
rasa test
pytest
```

## Personalizacion

Si quieres adaptar el bot a otra iglesia o ministerio, normalmente debes tocar:

- `domain.yml`: intents, respuestas y acciones
- `data/stories.yml`: flujos conversacionales
- `data/rules.yml`: reglas directas
- `actions/actions.py`: logica de negocio
- archivos de contenido dentro de `data/`

## Documentacion complementaria

Si necesitas mas detalle, empieza por:

- `INDICE_DOCUMENTACION.md`
- `LISTO_PARA_ENTRENAR.md`
- `INSTRUCCIONES_ENTRENAMIENTO.md`
- `GUIA_USO_QUIZ.md`
- `MEJORAS_REALIZADAS.md`

## Estado

Este repositorio esta orientado a:

- desarrollo iterativo del bot
- experimentacion con NLU y flujos conversacionales
- integracion con la app principal M.A.I.K.A

## Licencia

Proyecto de uso educativo y de investigacion.
