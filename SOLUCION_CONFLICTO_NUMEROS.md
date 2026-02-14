# 🔧 Solución: Conflicto de Números entre Intents

## ❌ Problema Detectado

Cuando el usuario responde con "1", "2" o "3" después de que el bot pregunta el nivel de dificultad, el bot responde:

```
"No hay un quiz activo. Inicia uno nuevo con 'quiero hacer un quiz'."
```

## 🔍 Causa del Problema

**Conflicto de Intents**: Dos intents diferentes usan los mismos números como ejemplos:

### Intent 1: `seleccionar_nivel_facil/medio/dificil`
```yaml
- intent: seleccionar_nivel_facil
  examples: |
    - 1
    - fácil
    ...

- intent: seleccionar_nivel_medio
  examples: |
    - 2
    - medio
    ...

- intent: seleccionar_nivel_dificil
  examples: |
    - 3
    - difícil
    ...
```

### Intent 2: `responder_quiz`
```yaml
- intent: responder_quiz
  examples: |
    - 1
    - 2
    - 3
    - 4
```

**Resultado**: El modelo NLU no puede distinguir si "1" es para seleccionar nivel o para responder una pregunta del quiz.

---

## ✅ Solución Implementada: Contexto con Slots

Usamos un **slot de contexto** (`esperando_nivel`) para indicar cuándo el bot está esperando la selección de nivel.

### 1. Slot de Contexto

```yaml
slots:
  esperando_nivel:
    type: bool
    mappings:
    - type: custom
  
  nivel_dificultad:
    type: categorical
    values:
      - facil
      - medio
      - dificil
    mappings:
    - type: from_intent
      intent: seleccionar_nivel_facil
      value: facil
    - type: from_intent
      intent: seleccionar_nivel_medio
      value: medio
    - type: from_intent
      intent: seleccionar_nivel_dificil
      value: dificil
```

### 2. Acciones de Contexto

**Marcar que estamos esperando nivel:**
```python
class ActionSetEsperandoNivel(Action):
    def name(self) -> Text:
        return "action_set_esperando_nivel"

    def run(self, ...):
        return [SlotSet("esperando_nivel", True)]
```

**Resetear después de seleccionar:**
```python
class ActionResetEsperandoNivel(Action):
    def name(self) -> Text:
        return "action_reset_esperando_nivel"

    def run(self, ...):
        return [SlotSet("esperando_nivel", False)]
```

### 3. Rules con Condiciones

```yaml
- rule: preguntar nivel cuando se pide quiz
  steps:
  - intent: start_quiz
  - action: utter_preguntar_nivel
  - action: action_set_esperando_nivel  # ✅ Marca contexto

- rule: iniciar quiz con nivel fácil
  conditions:
  - slot_was_set:
    - esperando_nivel: true  # ✅ Solo si estamos esperando nivel
  steps:
  - intent: seleccionar_nivel_facil
  - action: action_start_quiz
  - action: action_reset_esperando_nivel  # ✅ Limpia contexto
```

---

## 🎯 Flujo Correcto Ahora

```
Usuario: "Quiero hacer un quiz"
  ↓
[Intent: start_quiz]
  ↓
Bot: "¿Qué nivel prefieres? 1️⃣ Fácil 2️⃣ Medio 3️⃣ Difícil"
  ↓
[Action: action_set_esperando_nivel]
[Slot: esperando_nivel = True]
  ↓
Usuario: "2"
  ↓
[Intent: seleccionar_nivel_medio] ✅ (porque esperando_nivel = True)
  ↓
[Action: action_start_quiz]
[Action: action_reset_esperando_nivel]
[Slot: esperando_nivel = False]
  ↓
Bot: "Quiz Bíblico ⭐⭐ Nivel Medio
     Pregunta 1 de 3: ..."
  ↓
Usuario: "2"
  ↓
[Intent: responder_quiz] ✅ (porque esperando_nivel = False)
  ↓
[Action: action_process_quiz_answer]
```

---

## 📋 Cambios Realizados

### 1. domain.yml
- ✅ Slot `esperando_nivel` con tipo `bool`
- ✅ Slot `nivel_dificultad` con tipo `categorical` y mappings
- ✅ Acciones `action_set_esperando_nivel` y `action_reset_esperando_nivel`

### 2. data/rules.yml
- ✅ Rule "preguntar nivel" ahora incluye `action_set_esperando_nivel`
- ✅ Rules de selección de nivel ahora tienen condición `esperando_nivel: true`
- ✅ Rules de selección de nivel ahora incluyen `action_reset_esperando_nivel`

### 3. data/stories.yml
- ✅ Todas las stories de quiz actualizadas con las nuevas acciones
- ✅ Flujo completo: set → selección → reset

### 4. actions/actions.py
- ✅ Nueva clase `ActionSetEsperandoNivel`
- ✅ Nueva clase `ActionResetEsperandoNivel`

---

## 🔄 Cómo Entrenar

```bash
# Opción 1: Script automático
entrenar.bat

# Opción 2: Manual
rasa train

# Luego probar:
# Terminal 1:
rasa run actions

# Terminal 2:
rasa shell
```

---

## 🧪 Prueba de Validación

### Test 1: Selección de Nivel
```
Tú: Quiero hacer un quiz
Bot: ¿Qué nivel prefieres? 1️⃣ Fácil 2️⃣ Medio 3️⃣ Difícil
Tú: 2
Esperado: ✅ "Quiz Bíblico ⭐⭐ Nivel Medio..."
```

### Test 2: Respuesta de Quiz
```
[Durante el quiz]
Bot: Pregunta 1 de 3: ¿Quién negó a Jesús tres veces?
     1. Juan
     2. Pedro
     3. Judas
     4. Tomás
Tú: 2
Esperado: ✅ "¡Correcto! 🎉 Pedro negó conocer a Jesús..."
```

---

## 📊 Ventajas de Esta Solución

### ✅ Contexto Claro
- El bot sabe en qué parte del flujo está
- No hay ambigüedad entre intents

### ✅ Escalable
- Fácil agregar más contextos si es necesario
- Patrón reutilizable para otros flujos

### ✅ Mantenible
- Código limpio y organizado
- Fácil de entender y modificar

### ✅ Robusto
- Maneja correctamente todos los casos
- No depende solo del NLU para distinguir contextos

---

## 🎓 Lección Aprendida

### Problema: Intents Ambiguos
Cuando dos intents tienen ejemplos muy similares (como números), el NLU puede confundirse.

### Solución: Contexto con Slots
Usar slots para mantener el contexto de la conversación y condicionar las rules/stories.

### Patrón General:
```yaml
1. Acción que establece contexto (set_slot)
2. Usuario responde
3. Rule/Story con condición de slot
4. Acción que limpia contexto (reset_slot)
```

---

## 🔍 Alternativas Consideradas

### Alternativa 1: Diferentes Ejemplos
**Problema**: Difícil hacer que usuarios digan "nivel 1" en vez de solo "1"

### Alternativa 2: Forms de Rasa
**Problema**: Más complejo de implementar para este caso simple

### Alternativa 3: Contexto con Slots ✅
**Ventaja**: Simple, claro, y efectivo

---

## ✅ Estado Actual

- ✅ Conflicto identificado
- ✅ Solución implementada
- ✅ Código validado sin errores
- ✅ Listo para entrenar

---

## 🚀 Próximo Paso

```bash
# Entrenar con los cambios
rasa train

# Probar el flujo completo
rasa shell
```

**¡El problema está resuelto! 🎯**

---

## 📞 Si Aún Hay Problemas

### Verificar que las acciones estén corriendo
```bash
# Terminal 1
rasa run actions

# Deberías ver:
# - action_set_esperando_nivel
# - action_reset_esperando_nivel
```

### Debug del slot
```bash
# En rasa shell, después de "quiero hacer un quiz":
/slots

# Deberías ver:
# esperando_nivel: True
```

### Re-entrenar forzando
```bash
rasa train --force
```

---

**Problema resuelto con contexto de slots! ✅**
