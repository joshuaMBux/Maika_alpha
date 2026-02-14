# 🎯 Mejoras del Sistema de Quiz con Niveles de Dificultad

## 📊 Resumen de Cambios

Se ha implementado un sistema completo de niveles de dificultad para los quiz y trivias bíblicas, expandiendo significativamente el banco de preguntas.

---

## ✨ Nuevas Características

### 1. 🎚️ **Sistema de Niveles de Dificultad**

El bot ahora pregunta al usuario qué nivel de dificultad prefiere antes de iniciar el quiz:

- **⭐ Nivel Fácil**: Preguntas básicas para principiantes
- **⭐⭐ Nivel Medio**: Preguntas intermedias
- **⭐⭐⭐ Nivel Difícil**: Preguntas avanzadas para expertos

### 2. 📚 **Banco de Preguntas Expandido**

**Antes**: 5 preguntas básicas
**Ahora**: 30 preguntas clasificadas por dificultad

#### Distribución de Preguntas:
- **Nivel Fácil**: 10 preguntas
- **Nivel Medio**: 10 preguntas  
- **Nivel Difícil**: 10 preguntas

---

## 📖 Ejemplos de Preguntas por Nivel

### ⭐ Nivel Fácil
- ¿Quién construyó el arca?
- ¿En qué ciudad nació Jesús?
- ¿Cuántos días tardó Dios en crear el mundo?
- ¿Quién derrotó a Goliat?
- ¿Cuál es el primer libro de la Biblia?
- ¿Cuántos apóstoles tuvo Jesús?
- ¿Quién fue tragado por un gran pez?
- ¿Qué comieron los israelitas en el desierto?
- ¿Quién fue el primer hombre creado por Dios?
- ¿Cuántos mandamientos dio Dios a Moisés?

### ⭐⭐ Nivel Medio
- ¿Quién fue vendido por sus hermanos como esclavo?
- ¿Cuántos días ayunó Jesús en el desierto?
- ¿Quién negó a Jesús tres veces?
- ¿En qué río fue bautizado Jesús?
- ¿Cuántos libros tiene el Nuevo Testamento?
- ¿Quién interpretó el sueño del faraón?
- ¿Qué mujer fue jueza de Israel?
- ¿Cuántos años vagaron los israelitas por el desierto?
- ¿Quién escribió la mayoría de los Salmos?
- ¿Qué apóstol era recaudador de impuestos?

### ⭐⭐⭐ Nivel Difícil
- ¿Cuántos años tenía Abraham cuando nació Isaac?
- ¿Qué profeta fue llevado al cielo en un carro de fuego?
- ¿Cuántos hijos tuvo Jacob?
- ¿Qué rey de Israel construyó el primer templo?
- ¿Cuántos días estuvo Lázaro en la tumba antes de ser resucitado?
- ¿Qué profeta vio la visión del valle de los huesos secos?
- ¿Cuántos capítulos tiene el libro de Apocalipsis?
- ¿Quién fue el sucesor de Moisés?
- ¿Cuántos años reinó el rey David?
- ¿Qué apóstol fue llamado 'el discípulo amado'?

---

## 🎮 Flujo de Conversación Mejorado

### Ejemplo de Uso:

```
Usuario: "Quiero hacer un quiz"

Bot: "¡Excelente! 🎯 Antes de empezar, ¿qué nivel de dificultad prefieres?

1️⃣ Fácil - Preguntas básicas para principiantes
2️⃣ Medio - Preguntas intermedias
3️⃣ Difícil - Preguntas avanzadas para expertos

Responde con el número o el nombre del nivel. 😊"

Usuario: "Medio"

Bot: "Quiz Bíblico ⭐⭐ Nivel Medio

Pregunta 1 de 3:

¿Quién fue vendido por sus hermanos como esclavo?

1. Isaac
2. Jacob
3. José
4. Benjamín

Responde con el número de tu opción (1, 2, 3 o 4)."
```

---

## 🆕 Nuevos Intents

### **seleccionar_nivel_facil**
Ejemplos:
- "fácil"
- "nivel fácil"
- "1"
- "principiante"
- "básico"
- "soy principiante"

### **seleccionar_nivel_medio**
Ejemplos:
- "medio"
- "nivel medio"
- "2"
- "intermedio"
- "tengo algo de conocimiento"

### **seleccionar_nivel_dificil**
Ejemplos:
- "difícil"
- "nivel difícil"
- "3"
- "avanzado"
- "experto"
- "quiero un reto"

---

## 🔧 Cambios Técnicos

### 1. **Archivo trivia_bank.json**
- ✅ Expandido de 5 a 30 preguntas
- ✅ Cada pregunta tiene campo `"difficulty"`: "facil", "medio", o "dificil"
- ✅ Todas las preguntas tienen explicaciones bíblicas

### 2. **Engine de Trivia (actions/engine/trivia.py)**
- ✅ Función `start_trivia()` ahora acepta parámetro `difficulty`
- ✅ Filtra preguntas por nivel de dificultad
- ✅ Fallback a todas las preguntas si no hay suficientes del nivel

### 3. **Acciones Actualizadas**
- ✅ `ActionIniciarTrivia`: Detecta nivel del intent o slot
- ✅ `ActionStartQuiz`: Filtra preguntas por dificultad
- ✅ Muestra emoji de nivel en el mensaje

### 4. **Domain.yml**
- ✅ Nuevo slot: `nivel_dificultad`
- ✅ Nuevo slot: `esperando_nivel`
- ✅ Nueva respuesta: `utter_preguntar_nivel`
- ✅ 3 nuevos intents de selección de nivel

### 5. **Stories y Rules**
- ✅ 3 nuevas stories para cada nivel
- ✅ 4 nuevas rules para manejo de niveles
- ✅ Flujo completo de selección de nivel

---

## 📊 Estadísticas de Mejoras

| Categoría | Antes | Ahora | Incremento |
|-----------|-------|-------|------------|
| Preguntas totales | 5 | 30 | +500% |
| Niveles de dificultad | 0 | 3 | +3 |
| Intents nuevos | 0 | 3 | +3 |
| Stories nuevas | 1 | 4 | +3 |
| Rules nuevas | 1 | 5 | +4 |
| Slots nuevos | 0 | 2 | +2 |

---

## 🎯 Beneficios

### 1. **Experiencia Personalizada**
- Los usuarios pueden elegir el nivel que se ajuste a su conocimiento
- Evita frustración con preguntas muy difíciles o muy fáciles

### 2. **Mayor Engagement**
- Más preguntas = más variedad
- Los usuarios pueden progresar de fácil a difícil

### 3. **Educación Gradual**
- Principiantes pueden empezar con lo básico
- Expertos tienen un verdadero desafío

### 4. **Mejor Retención**
- Cada pregunta tiene explicación bíblica
- Los usuarios aprenden con cada respuesta

---

## 🚀 Cómo Usar

### Para Usuarios:

1. **Iniciar Quiz**:
   - "Quiero hacer un quiz"
   - "Hazme un test bíblico"

2. **Seleccionar Nivel**:
   - Responde con: "fácil", "medio", "difícil"
   - O con números: "1", "2", "3"

3. **Responder Preguntas**:
   - Responde con el número de la opción (1-4)

### Para Desarrolladores:

1. **Entrenar el modelo**:
```bash
rasa train
```

2. **Probar en shell**:
```bash
rasa shell
```

3. **Agregar más preguntas**:
   - Editar `data/content/trivia_bank.json`
   - Agregar campo `"difficulty"`: "facil", "medio", o "dificil"

---

## 📝 Formato de Pregunta

```json
{
  "question": "¿Pregunta aquí?",
  "options": ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],
  "correct": 0,
  "difficulty": "facil",
  "explanation": "Explicación bíblica con referencia."
}
```

---

## 🎨 Características Visuales

- **⭐** = Nivel Fácil
- **⭐⭐** = Nivel Medio
- **⭐⭐⭐** = Nivel Difícil
- **🎯** = Quiz/Trivia
- **✅** = Respuesta correcta
- **❌** = Respuesta incorrecta
- **🏆** = Puntuación alta

---

## 🔮 Futuras Mejoras Sugeridas

1. **Más Preguntas**: Expandir a 50+ preguntas por nivel
2. **Categorías**: Antiguo Testamento, Nuevo Testamento, Personajes, etc.
3. **Modo Cronometrado**: Agregar límite de tiempo
4. **Racha de Victorias**: Sistema de rachas consecutivas
5. **Logros**: Badges por completar niveles
6. **Modo Multijugador**: Competir con otros usuarios

---

## ✅ Validación

- ✅ Todas las preguntas tienen 4 opciones
- ✅ Todas las preguntas tienen explicación bíblica
- ✅ Todas las preguntas están clasificadas por dificultad
- ✅ El sistema filtra correctamente por nivel
- ✅ Fallback funciona si no hay suficientes preguntas
- ✅ Los intents detectan correctamente el nivel
- ✅ Las stories y rules cubren todos los flujos

---

**¡El sistema de quiz ahora es más robusto, educativo y personalizado! 🎯📖✨**
