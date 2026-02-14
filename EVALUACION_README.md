# 📊 Script de Evaluación del Modelo Maika

## 🎯 ¿Qué mide este script?

El script `evaluate_model.py` mide las **métricas de rendimiento** del modelo de Rasa usando datos de prueba:

- **F1 Score** (Precisión + Recall balanceado)
- **Precision** (Exactitud de las predicciones positivas)
- **Accuracy** (Porcentaje total de aciertos)
- **Recall** (Capacidad para encontrar todos los casos positivos)

## 🚀 Cómo usar el script

### 1. **Requisitos previos**
```bash
pip install scikit-learn pandas
```

### 2. **Ejecutar evaluación**
```bash
python evaluate_model.py
```

### 3. **Resultado esperado**
```
🔍 Iniciando evaluación del modelo...
📊 Evaluando 45 ejemplos de prueba...
🤖 Modelo a evaluar: models\20251113-142126-dark-pulse.tar.gz
📋 Datos de prueba: data/test_data.yml

============================================================
📊 REPORTE DE EVALUACIÓN DEL MODELO
============================================================
📅 Fecha: 2025-11-14T02:05:48
📁 Modelo: 20251113-142126-dark-pulse.tar.gz
📝 Ejemplos evaluados: 45
🎯 Intents únicos: 14

----------------------------------------
📈 MÉTRICAS PRINCIPALES
----------------------------------------
🎯 Accuracy: 0.9565
🔍 Precision (weighted): 0.9587
📊 Recall (weighted): 0.9565
⭐ F1-Score (weighted): 0.9568
🔍 Precision (macro): 0.9423
📊 Recall (macro): 0.9356
⭐ F1-Score (macro): 0.9378

----------------------------------------
🏆 TOP 5 INTENTS MEJOR CLASIFICADOS
----------------------------------------
preguntar_versiculo   | F1: 1.000 | Prec: 1.000 | Rec: 1.000 | Sup: 5
saludar              | F1: 1.000 | Prec: 1.000 | Rec: 1.000 | Sup: 4
pedir_curiosidad_biblica | F1: 1.000 | Prec: 1.000 | Rec: 1.000 | Sup: 3
afirmar               | F1: 0.989 | Prec: 1.000 | Rec: 0.978 | Sup: 4

----------------------------------------
📊 DISTRIBUCIÓN DE INTENTS
----------------------------------------
preguntar_versiculo   |   5 ejemplos (11.1%)
saludar              |   4 ejemplos (8.9%)
pedir_curiosidad_biblica |   3 ejemplos (6.7%)
afirmar               |   4 ejemplos (8.9%)

✅ Métricas guardadas en la base de datos SQLite

============================================================
🎯 EVALUACIÓN COMPLETADA
============================================================
```

## 📋 Archivos utilizados

### `evaluate_model.py`
- Script principal de evaluación
- Calcula métricas usando scikit-learn
- Genera reportes detallados
- Guarda resultados en SQLite

### `data/test_data.yml`
- Datos de prueba con 45 ejemplos
- Cubre todos los intents principales
- Incluye entidades de libros bíblicos

### `sqlite_metrics.py`
- Sistema de almacenamiento de métricas
- Guarda historial de evaluaciones
- Permite seguimiento del rendimiento

## 🎯 Interpretación de métricas

### **Accuracy (Precisión global)**
- Porcentaje total de predicciones correctas
- **> 0.95**: Excelente rendimiento
- **0.85-0.95**: Bueno
- **< 0.85**: Necesita mejora

### **F1 Score**
- Balance entre precision y recall
- **> 0.90**: Muy buen rendimiento
- **0.80-0.90**: Aceptable
- **< 0.80**: Requiere optimización

### **Precision vs Recall**
- **Precision alta**: Pocas predicciones incorrectas positivas
- **Recall alto**: Pocas predicciones incorrectas negativas

## 🔧 Personalización

### Agregar más datos de prueba
Edita `data/test_data.yml` para incluir más ejemplos:

```yaml
- intent: nuevo_intent
  examples: |
    - ejemplo 1
    - ejemplo 2
    - ejemplo 3
```

### Modificar métricas
En `evaluate_model.py`, puedes cambiar:
- `average='weighted'` → `average='macro'` (promedio simple)
- `zero_division=0` → `zero_division=1` (manejo de división por cero)

## 📊 Historial de evaluaciones

Las métricas se guardan automáticamente en `metrics.db`. Para ver el historial:

```python
from sqlite_metrics import get_evaluation_history
history = get_evaluation_history()
print(history)
```

## 🎯 Próximos pasos

1. **Ejecutar evaluación regularmente** después de entrenamientos
2. **Comparar métricas** entre versiones del modelo
3. **Identificar intents problemáticos** y agregar más ejemplos de entrenamiento
4. **Optimizar thresholds** basados en las métricas

## 📈 Mejores prácticas

- **Datos de prueba separados**: Nunca usar datos de entrenamiento para evaluación
- **Balance de clases**: Asegurar representación equitativa de todos los intents
- **Métricas múltiples**: No depender solo de accuracy
- **Evaluación continua**: Medir rendimiento regularmente

---

**¡Este script te permite medir objetivamente el rendimiento de Maika y mejorar continuamente su precisión!** 🤖📊