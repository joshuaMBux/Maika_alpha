# 🚀 Instrucciones de Entrenamiento y Despliegue

## ✅ Verificación Previa

Antes de entrenar, verifica que tienes todos los archivos:

### Archivos Modificados ✅
- ✅ `data/nlu.yml` - NLU expandido con ejemplos cristianos
- ✅ `domain.yml` - Respuestas mejoradas y nuevos intents
- ✅ `data/stories.yml` - Nuevas historias de conversación
- ✅ `data/rules.yml` - Nuevas reglas de respuesta
- ✅ `data/synonyms.yml` - Sinónimos cristianos expandidos
- ✅ `data/content/trivia_bank.json` - 30 preguntas con niveles
- ✅ `actions/action_trivia.py` - Soporte de niveles
- ✅ `actions/engine/trivia.py` - Filtrado por dificultad
- ✅ `actions/actions.py` - Quiz con niveles

### Documentación Creada ✅
- ✅ `MEJORAS_REALIZADAS.md` - Detalles de mejoras NLU
- ✅ `GUIA_RAPIDA_MEJORAS.md` - Resumen visual
- ✅ `MEJORAS_QUIZ_NIVELES.md` - Sistema de quiz
- ✅ `GUIA_USO_QUIZ.md` - Guía práctica
- ✅ `RESUMEN_COMPLETO_MEJORAS.md` - Resumen total

---

## 📋 Pasos de Entrenamiento

### Paso 1: Validar Datos
```bash
rasa data validate
```

**Resultado esperado**: "Your Rasa NLU data is consistent!"

### Paso 2: Entrenar el Modelo
```bash
rasa train
```

**Tiempo estimado**: 2-5 minutos
**Resultado esperado**: Modelo guardado en `models/`

### Paso 3: Iniciar Servidor de Acciones
```bash
rasa run actions
```

**Puerto**: 5055
**Mantener corriendo**: Sí, en una terminal separada

### Paso 4: Probar en Shell
```bash
rasa shell
```

**Alternativa con debug**:
```bash
rasa shell --debug
```

---

## 🧪 Pruebas Recomendadas

### Test 1: Saludo Cristiano
```
Tú: Bendiciones hermano
Esperado: Respuesta con "Paz del Señor" o similar
```

### Test 2: Quiz con Nivel Fácil
```
Tú: Quiero hacer un quiz
Bot: [Pregunta nivel de dificultad]
Tú: Fácil
Esperado: Quiz con preguntas básicas y emoji ⭐
```

### Test 3: Quiz con Nivel Medio
```
Tú: Quiero un quiz medio
Bot: [Pregunta nivel]
Tú: 2
Esperado: Quiz con preguntas intermedias y emoji ⭐⭐
```

### Test 4: Quiz con Nivel Difícil
```
Tú: Dame un quiz difícil
Bot: [Pregunta nivel]
Tú: Difícil
Esperado: Quiz con preguntas avanzadas y emoji ⭐⭐⭐
```

### Test 5: Petición de Oración
```
Tú: Necesito oración por mi familia
Esperado: Oración guiada con versículo
```

### Test 6: Búsqueda de Versículo
```
Tú: Dame un versículo sobre amor
Esperado: Versículo con referencia bíblica
```

### Test 7: Agradecimiento
```
Tú: Gracias hermano, que Dios te bendiga
Esperado: Respuesta con "Amén" o "Gloria a Dios"
```

---

## 🔍 Verificación de Funcionalidad

### Checklist de Funciones

#### NLU Mejorado
- [ ] Reconoce saludos cristianos
- [ ] Reconoce despedidas bendecidas
- [ ] Detecta estados emocionales con contexto
- [ ] Entiende peticiones de oración variadas
- [ ] Reconoce sinónimos cristianos

#### Sistema de Quiz
- [ ] Pregunta nivel de dificultad
- [ ] Filtra preguntas por nivel
- [ ] Muestra emoji correcto (⭐/⭐⭐/⭐⭐⭐)
- [ ] Acepta respuestas numéricas (1-4)
- [ ] Muestra explicaciones bíblicas
- [ ] Calcula puntuación correctamente

#### Respuestas Cristianas
- [ ] Usa lenguaje fraternal
- [ ] Incluye versículos bíblicos
- [ ] Tiene múltiples variaciones
- [ ] Usa emojis apropiados
- [ ] Tono cálido y empático

---

## 🐛 Solución de Problemas

### Problema 1: Error al entrenar
**Síntoma**: `rasa train` falla
**Solución**:
```bash
# Validar datos primero
rasa data validate

# Ver errores específicos
rasa train --debug
```

### Problema 2: Acciones no funcionan
**Síntoma**: Quiz no inicia o no filtra por nivel
**Solución**:
```bash
# Verificar que el servidor de acciones esté corriendo
# Terminal 1:
rasa run actions

# Terminal 2:
rasa shell
```

### Problema 3: No reconoce intents
**Síntoma**: Bot no entiende comandos
**Solución**:
```bash
# Re-entrenar el modelo
rasa train --force

# Probar con debug
rasa shell --debug
```

### Problema 4: Preguntas no se filtran
**Síntoma**: Todas las preguntas son del mismo nivel
**Solución**:
1. Verificar `data/content/trivia_bank.json`
2. Cada pregunta debe tener `"difficulty": "facil/medio/dificil"`
3. Re-iniciar servidor de acciones

### Problema 5: Respuestas no son cristianas
**Síntoma**: Bot usa respuestas antiguas
**Solución**:
```bash
# Re-entrenar forzando actualización
rasa train --force

# Limpiar cache
rm -rf .rasa/cache
rasa train
```

---

## 📊 Métricas de Éxito

Después de entrenar, verifica:

### Métricas de Entrenamiento
- **Accuracy NLU**: Debe ser >85%
- **F1 Score**: Debe ser >0.80
- **Tiempo de entrenamiento**: 2-5 minutos

### Métricas de Uso
- **Intents reconocidos**: >90%
- **Respuestas útiles**: >80%
- **Quiz completados**: Tracking en SQLite

---

## 🔄 Actualización Continua

### Agregar Más Preguntas

1. Editar `data/content/trivia_bank.json`
2. Agregar pregunta con formato:
```json
{
  "question": "¿Tu pregunta?",
  "options": ["Op1", "Op2", "Op3", "Op4"],
  "correct": 0,
  "difficulty": "facil",
  "explanation": "Explicación con referencia bíblica."
}
```
3. Re-iniciar servidor de acciones

### Agregar Más Intents

1. Editar `data/nlu.yml`
2. Agregar intent con ejemplos
3. Editar `domain.yml` para incluir intent
4. Agregar respuesta o acción
5. Re-entrenar: `rasa train`

### Mejorar Respuestas

1. Editar `domain.yml`
2. Modificar `responses:`
3. Re-entrenar: `rasa train`

---

## 🚀 Despliegue en Producción

### Opción 1: Servidor Local
```bash
# Terminal 1: Acciones
rasa run actions

# Terminal 2: Rasa
rasa run --enable-api --cors "*"
```

### Opción 2: Docker
```bash
# Construir imagen
docker build -t chatbot-cristiano .

# Ejecutar
docker run -p 5005:5005 chatbot-cristiano
```

### Opción 3: Rasa X
```bash
# Instalar Rasa X
pip install rasa-x --extra-index-url https://pypi.rasa.com/simple

# Ejecutar
rasa x
```

---

## 📞 Comandos Útiles

### Desarrollo
```bash
# Entrenar
rasa train

# Probar
rasa shell

# Debug
rasa shell --debug

# Validar
rasa data validate

# Visualizar
rasa visualize
```

### Producción
```bash
# Servidor API
rasa run --enable-api

# Acciones
rasa run actions

# Con CORS
rasa run --enable-api --cors "*"
```

### Mantenimiento
```bash
# Limpiar cache
rm -rf .rasa/cache

# Ver logs
tail -f rasa.log

# Backup modelo
cp models/*.tar.gz backups/
```

---

## ✅ Checklist Final

Antes de considerar completo:

- [ ] Modelo entrenado sin errores
- [ ] Servidor de acciones corriendo
- [ ] Todos los tests pasados
- [ ] Documentación revisada
- [ ] Base de datos SQLite funcionando
- [ ] Preguntas clasificadas correctamente
- [ ] Respuestas cristianas activas
- [ ] Sinónimos funcionando
- [ ] Niveles de quiz operativos

---

## 🎉 ¡Listo para Usar!

Si todos los pasos anteriores están completos:

✅ El chatbot está entrenado
✅ Las mejoras están activas
✅ El sistema de quiz funciona
✅ Las respuestas son cristianas
✅ La documentación está disponible

**¡Que Dios bendiga este proyecto! 🙏✨**

---

## 📚 Recursos Adicionales

- [Documentación Rasa](https://rasa.com/docs/)
- [Rasa Community](https://forum.rasa.com/)
- [Rasa GitHub](https://github.com/RasaHQ/rasa)

---

**Versión**: 2.0
**Última actualización**: Noviembre 2024
**Estado**: ✅ Listo para Entrenamiento
