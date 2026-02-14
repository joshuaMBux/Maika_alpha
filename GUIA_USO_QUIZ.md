# 🎯 Guía Rápida: Cómo Usar el Nuevo Sistema de Quiz

## 🚀 Inicio Rápido

### 1. Entrenar el Modelo
```bash
rasa train
```

### 2. Iniciar el Servidor de Acciones
```bash
rasa run actions
```

### 3. Probar en Shell
```bash
rasa shell
```

---

## 💬 Ejemplos de Conversación

### Ejemplo 1: Quiz Nivel Fácil

```
Tú: Hola
Bot: ¡Bendiciones! 🙏 Soy tu asistente espiritual...

Tú: Quiero hacer un quiz
Bot: ¡Excelente! 🎯 Antes de empezar, ¿qué nivel de dificultad prefieres?

     1️⃣ Fácil - Preguntas básicas para principiantes
     2️⃣ Medio - Preguntas intermedias
     3️⃣ Difícil - Preguntas avanzadas para expertos

Tú: Fácil
Bot: Quiz Bíblico ⭐ Nivel Fácil

     Pregunta 1 de 3:
     ¿Quién construyó el arca?
     
     1. Moisés
     2. Noé
     3. Abraham
     4. David

Tú: 2
Bot: ¡Correcto! 🎉
     Dios mandó a Noé a construir el arca para salvarse del diluvio (Génesis 6).
     
     Pregunta 2 de 3:
     ...
```

### Ejemplo 2: Quiz Nivel Difícil

```
Tú: Quiero un quiz difícil
Bot: ¡Excelente! 🎯 Antes de empezar, ¿qué nivel de dificultad prefieres?
     ...

Tú: 3
Bot: Quiz Bíblico ⭐⭐⭐ Nivel Difícil

     Pregunta 1 de 3:
     ¿Cuántos años tenía Abraham cuando nació Isaac?
     
     1. 75
     2. 90
     3. 100
     4. 120

Tú: 3
Bot: ¡Correcto! 🎉
     Abraham tenía 100 años cuando nació su hijo Isaac (Génesis 21:5).
     ...
```

### Ejemplo 3: Trivia Bíblica

```
Tú: Quiero jugar trivia
Bot: ¡Excelente! 🎯 Antes de empezar, ¿qué nivel de dificultad prefieres?
     ...

Tú: medio
Bot: Trivia bíblica (1/5) ⭐⭐ Nivel Medio

     ¿Quién fue vendido por sus hermanos como esclavo?
     
     1. Isaac
     2. Jacob
     3. José
     4. Benjamín

Tú: 3
Bot: ¡Correcto! Siguiente (2/5):
     ...
```

---

## 🎮 Comandos Disponibles

### Iniciar Quiz/Trivia
- "Quiero hacer un quiz"
- "Hazme un test bíblico"
- "Quiero jugar trivia"
- "Dame preguntas bíblicas"
- "Ponme un quiz"

### Seleccionar Nivel
**Fácil:**
- "fácil"
- "nivel fácil"
- "1"
- "principiante"
- "básico"

**Medio:**
- "medio"
- "nivel medio"
- "2"
- "intermedio"

**Difícil:**
- "difícil"
- "nivel difícil"
- "3"
- "avanzado"
- "experto"
- "quiero un reto"

### Responder Preguntas
- Responde con el número: "1", "2", "3", o "4"

---

## 📊 Niveles de Dificultad

### ⭐ Nivel Fácil
**Para:** Principiantes, nuevos creyentes, niños
**Preguntas:** 10 disponibles
**Ejemplos:**
- ¿Quién construyó el arca?
- ¿En qué ciudad nació Jesús?
- ¿Cuántos apóstoles tuvo Jesús?

### ⭐⭐ Nivel Medio
**Para:** Creyentes con conocimiento básico
**Preguntas:** 10 disponibles
**Ejemplos:**
- ¿Quién negó a Jesús tres veces?
- ¿Cuántos libros tiene el Nuevo Testamento?
- ¿Qué mujer fue jueza de Israel?

### ⭐⭐⭐ Nivel Difícil
**Para:** Estudiosos de la Biblia, expertos
**Preguntas:** 10 disponibles
**Ejemplos:**
- ¿Cuántos años tenía Abraham cuando nació Isaac?
- ¿Qué profeta vio la visión del valle de los huesos secos?
- ¿Cuántos capítulos tiene el libro de Apocalipsis?

---

## 🎯 Tips para Mejores Resultados

### 1. **Sé Específico**
✅ "Quiero un quiz difícil"
✅ "Dame un quiz nivel medio"
❌ "Quiz" (muy vago)

### 2. **Usa Números o Palabras**
✅ "1" o "fácil"
✅ "2" o "medio"
✅ "3" o "difícil"

### 3. **Responde con Números**
✅ "2"
❌ "La segunda opción" (puede no funcionar)

### 4. **Progresa Gradualmente**
- Empieza con nivel fácil
- Avanza a medio cuando te sientas cómodo
- Desafíate con nivel difícil

---

## 🔧 Solución de Problemas

### Problema: "No hay preguntas disponibles"
**Solución:** 
- Verifica que `data/content/trivia_bank.json` existe
- Ejecuta `python verificar_quiz.py` para validar

### Problema: El bot no entiende el nivel
**Solución:**
- Usa palabras simples: "fácil", "medio", "difícil"
- O usa números: "1", "2", "3"
- Entrena el modelo: `rasa train`

### Problema: Las preguntas no se filtran por nivel
**Solución:**
- Verifica que las acciones estén corriendo: `rasa run actions`
- Revisa que cada pregunta tenga el campo `"difficulty"`

---

## 📈 Estadísticas y Progreso

El sistema guarda automáticamente:
- ✅ Puntuación de cada quiz
- ✅ Nivel de dificultad usado
- ✅ Historial de respuestas
- ✅ Ranking de mejores puntuaciones

Para ver tus estadísticas:
```
Tú: Muéstrame mis estadísticas
Bot: [Muestra tu progreso y ranking]
```

---

## 🎨 Características Especiales

### Explicaciones Bíblicas
Cada respuesta incluye:
- ✅ Referencia bíblica
- ✅ Contexto de la respuesta
- ✅ Aprendizaje adicional

### Emojis Visuales
- 🎯 Quiz/Trivia
- ⭐ Nivel Fácil
- ⭐⭐ Nivel Medio
- ⭐⭐⭐ Nivel Difícil
- 🎉 Respuesta correcta
- 📖 Explicación bíblica

### Mensajes Motivacionales
- Puntuación ≥80%: "¡Excelente! 🏆"
- Puntuación ≥60%: "¡Muy bien! 👍"
- Puntuación <60%: "¡Buen intento! 📚"

---

## 🚀 Próximos Pasos

1. ✅ **Practica**: Haz varios quiz de diferentes niveles
2. ✅ **Progresa**: Avanza de fácil a difícil
3. ✅ **Aprende**: Lee las explicaciones bíblicas
4. ✅ **Compite**: Intenta mejorar tu puntuación
5. ✅ **Comparte**: Invita a otros a probar el quiz

---

## 📞 Soporte

Si encuentras problemas:
1. Verifica que el modelo esté entrenado
2. Asegúrate de que las acciones estén corriendo
3. Revisa los logs para errores
4. Consulta la documentación de Rasa

---

**¡Disfruta aprendiendo la Palabra de Dios de forma interactiva! 🎯📖✨**
