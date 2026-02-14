# ✅ Implementación: Sistema de Contexto para Juegos

## 🎯 Objetivo

Evitar conflictos entre diferentes juegos (quiz, trivia, SRS, misiones, bingo) usando un sistema de contexto global.

---

## ✅ Implementado

### 1. Slot de Contexto Global

```yaml
slots:
  juego_activo:
    type: categorical
    values:
      - quiz
      - trivia
      - srs
      - mision
      - bingo
      - ninguno
    mappings:
    - type: custom
```

**Propósito**: Mantener registro de qué juego está activo en cada momento.

### 2. Acciones de Contexto

#### ActionSetJuegoActivo
```python
class ActionSetJuegoActivo(Action):
    """Marca qué juego está activo actualmente"""
    
    def run(self, ...):
        intent = tracker.get_intent_of_latest_message()
        
        juego_map = {
            "start_quiz": "quiz",
            "jugar_trivia": "trivia",
            "aprender_verso": "srs",
            "repasar_verso": "srs",
            "empezar_mision": "mision",
            "bingo_valores": "bingo"
        }
        
        juego = juego_map.get(intent, "ninguno")
        return [SlotSet("juego_activo", juego)]
```

#### ActionResetJuegoActivo
```python
class ActionResetJuegoActivo(Action):
    """Resetea el juego activo a ninguno"""
    
    def run(self, ...):
        return [SlotSet("juego_activo", "ninguno")]
```

### 3. Rules Actualizadas con Contexto

#### Quiz
```yaml
- rule: preguntar nivel cuando se pide quiz
  steps:
  - intent: start_quiz
  - action: action_set_juego_activo  # ✅ Marca juego = quiz
  - action: utter_preguntar_nivel
  - action: action_set_esperando_nivel

- rule: iniciar quiz con nivel medio
  conditions:
  - slot_was_set:
    - esperando_nivel: true
    - juego_activo: quiz  # ✅ Solo si juego = quiz
  steps:
  - intent: seleccionar_nivel_medio
  - action: action_start_quiz
  - action: action_reset_esperando_nivel
```

#### Trivia
```yaml
- rule: preguntar nivel cuando se pide trivia
  steps:
  - intent: jugar_trivia
  - action: action_set_juego_activo  # ✅ Marca juego = trivia
  - action: utter_preguntar_nivel
  - action: action_set_esperando_nivel

- rule: iniciar trivia con nivel medio
  conditions:
  - slot_was_set:
    - esperando_nivel: true
    - juego_activo: trivia  # ✅ Solo si juego = trivia
  steps:
  - intent: seleccionar_nivel_medio
  - action: action_iniciar_trivia
  - action: action_reset_esperando_nivel

- rule: responder trivia
  conditions:
  - slot_was_set:
    - juego_activo: trivia  # ✅ Solo responde si trivia activa
  steps:
  - intent: responder_trivia
  - action: action_responder_trivia
```

#### SRS (Versículos)
```yaml
- rule: mostrar verso del día
  steps:
  - intent: aprender_verso
  - action: action_set_juego_activo  # ✅ Marca juego = srs
  - action: action_mostrar_verso

- rule: repasar verso (SRS)
  conditions:
  - slot_was_set:
    - juego_activo: srs  # ✅ Solo si SRS activo
  steps:
  - intent: repasar_verso
  - action: action_repaso_verso
```

#### Misiones
```yaml
- rule: mision del dia
  steps:
  - intent: empezar_mision
  - action: action_set_juego_activo  # ✅ Marca juego = mision
  - action: action_mision_hoy
```

#### Bingo
```yaml
- rule: bingo de valores
  steps:
  - intent: bingo_valores
  - action: action_set_juego_activo  # ✅ Marca juego = bingo
  - action: action_bingo
```

#### Finalizar Juego
```yaml
- rule: finalizar juego al despedirse
  steps:
  - intent: despedida
  - action: action_reset_juego_activo  # ✅ Limpia contexto
  - action: utter_despedida
```

---

## 🎮 Flujos de Ejemplo

### Flujo 1: Quiz Completo
```
Usuario: "Quiero hacer un quiz"
  ↓
[Intent: start_quiz]
  ↓
[Action: action_set_juego_activo]
[Slot: juego_activo = "quiz"]
  ↓
Bot: "¿Qué nivel prefieres? 1️⃣ Fácil 2️⃣ Medio 3️⃣ Difícil"
  ↓
[Action: action_set_esperando_nivel]
[Slot: esperando_nivel = True]
  ↓
Usuario: "2"
  ↓
[Intent: seleccionar_nivel_medio]
[Condición: esperando_nivel = True AND juego_activo = "quiz"] ✅
  ↓
[Action: action_start_quiz]
[Action: action_reset_esperando_nivel]
[Slot: esperando_nivel = False]
  ↓
Bot: "Quiz Bíblico ⭐⭐ Nivel Medio..."
  ↓
Usuario: "2"
  ↓
[Intent: responder_quiz]
[Condición: juego_activo = "quiz"] ✅
  ↓
[Action: action_process_quiz_answer]
```

### Flujo 2: Trivia Completo
```
Usuario: "Quiero jugar trivia"
  ↓
[Intent: jugar_trivia]
  ↓
[Action: action_set_juego_activo]
[Slot: juego_activo = "trivia"]
  ↓
Bot: "¿Qué nivel prefieres? 1️⃣ Fácil 2️⃣ Medio 3️⃣ Difícil"
  ↓
[Action: action_set_esperando_nivel]
[Slot: esperando_nivel = True]
  ↓
Usuario: "3"
  ↓
[Intent: seleccionar_nivel_dificil]
[Condición: esperando_nivel = True AND juego_activo = "trivia"] ✅
  ↓
[Action: action_iniciar_trivia]
[Action: action_reset_esperando_nivel]
[Slot: esperando_nivel = False]
  ↓
Bot: "Trivia bíblica ⭐⭐⭐ Nivel Difícil (1/5)..."
  ↓
Usuario: "1"
  ↓
[Intent: responder_trivia]
[Condición: juego_activo = "trivia"] ✅
  ↓
[Action: action_responder_trivia]
```

### Flujo 3: SRS (Versículos)
```
Usuario: "Quiero aprender un versículo"
  ↓
[Intent: aprender_verso]
  ↓
[Action: action_set_juego_activo]
[Slot: juego_activo = "srs"]
  ↓
[Action: action_mostrar_verso]
  ↓
Bot: "Verso del día: Juan 3:16..."
  ↓
Usuario: "Quiero repasar el versículo"
  ↓
[Intent: repasar_verso]
[Condición: juego_activo = "srs"] ✅
  ↓
[Action: action_repaso_verso]
```

---

## 📊 Beneficios

### ✅ Sin Conflictos
- Cada juego tiene su propio contexto
- No hay ambigüedad en las respuestas
- El bot siempre sabe qué esperar

### ✅ Escalable
- Fácil agregar nuevos juegos
- Solo agregar al `juego_map`
- Crear rules con condiciones

### ✅ Mantenible
- Código limpio y organizado
- Fácil de debuggear
- Logs claros de contexto

### ✅ Robusto
- Maneja múltiples juegos simultáneos (en diferentes sesiones)
- Limpia contexto al despedirse
- Previene estados inconsistentes

---

## 🔍 Debugging

### Ver Slot Actual
```bash
# En rasa shell:
/slots

# Deberías ver:
# juego_activo: quiz (o trivia, srs, etc.)
# esperando_nivel: True/False
```

### Logs de Debug
Las acciones imprimen logs:
```
[DEBUG] Juego activo establecido: quiz (intent: start_quiz)
[DEBUG] Juego activo reseteado a ninguno
```

---

## 🧪 Pruebas Recomendadas

### Test 1: Quiz → Trivia (Cambio de Juego)
```
Tú: Quiero hacer un quiz
Bot: ¿Qué nivel prefieres?
Tú: Adiós
Bot: ¡Que Dios te bendiga!
[juego_activo reseteado]

Tú: Hola
Bot: ¡Bendiciones!
Tú: Quiero jugar trivia
Bot: ¿Qué nivel prefieres?
[juego_activo = trivia]
```

### Test 2: Respuestas en Contexto Correcto
```
[Durante quiz]
Tú: 2
→ ✅ Detecta como respuesta de quiz

[Durante trivia]
Tú: 2
→ ✅ Detecta como respuesta de trivia
```

### Test 3: Selección de Nivel por Juego
```
[Quiz]
Tú: Quiero hacer un quiz
Bot: ¿Qué nivel prefieres?
Tú: 2
→ ✅ Inicia quiz nivel medio

[Trivia]
Tú: Quiero jugar trivia
Bot: ¿Qué nivel prefieres?
Tú: 3
→ ✅ Inicia trivia nivel difícil
```

---

## 📋 Archivos Modificados

### domain.yml
- ✅ Slot `juego_activo` agregado
- ✅ Acciones `action_set_juego_activo` y `action_reset_juego_activo`

### data/rules.yml
- ✅ Rules de quiz con condición `juego_activo: quiz`
- ✅ Rules de trivia con condición `juego_activo: trivia`
- ✅ Rules de SRS con condición `juego_activo: srs`
- ✅ Rules de misiones y bingo con `action_set_juego_activo`
- ✅ Rule de despedida con `action_reset_juego_activo`

### actions/actions.py
- ✅ Clase `ActionSetJuegoActivo`
- ✅ Clase `ActionResetJuegoActivo`

---

## 🚀 Próximos Pasos

### Implementado ✅
1. ✅ Sistema de contexto global
2. ✅ Niveles para quiz
3. ✅ Niveles para trivia
4. ✅ Contexto para todos los juegos

### Pendiente ⏳
1. ⏳ Niveles para SRS (versículos por dificultad)
2. ⏳ Niveles para Misiones
3. ⏳ Bingo interactivo completo
4. ⏳ Sistema de badges y logros

---

## ✅ Estado

**Implementación**: ✅ Completada
**Validación**: ✅ Sin errores
**Listo para**: Entrenar y probar

---

## 🎯 Entrenar y Probar

```bash
# Entrenar
rasa train

# Terminal 1: Acciones
rasa run actions

# Terminal 2: Probar
rasa shell
```

---

**¡Sistema de contexto global implementado exitosamente! 🎮✅**
