#!/usr/bin/env python3
"""
Script para evaluar el rendimiento del modelo de Rasa
Calcula F1 Score, Precision y Accuracy usando datos de prueba
"""

import asyncio
import json
from typing import Dict, List, Tuple
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support
import rasa
from rasa.core.agent import Agent
from rasa.model_training import train
from rasa.shared.nlu.training_data.loading import load_data
from rasa.shared.core.training_data.structures import StoryGraph
import os
import sys
from datetime import datetime

# Importar el sistema de métricas SQLite
from sqlite_metrics import save_model_evaluation

async def evaluate_model_performance(model_path: str, test_data_path: str) -> Dict:
    """
    Evalúa el rendimiento del modelo usando datos de prueba

    Args:
        model_path: Ruta al modelo entrenado
        test_data_path: Ruta a los datos de prueba

    Returns:
        Diccionario con métricas de evaluación
    """

    print("🔍 Iniciando evaluación del modelo...")

    try:
        # Cargar el agente con el modelo
        agent = Agent.load(model_path)

        # Cargar datos de prueba
        test_data = load_data(test_data_path)

        true_intents = []
        predicted_intents = []
        true_entities = []
        predicted_entities = []

        print(f"📊 Evaluando {len(test_data.training_examples)} ejemplos de prueba...")

        # Evaluar cada ejemplo
        for example in test_data.training_examples:
            if example.get("intent"):
                true_intent = example.get("intent")
                true_intents.append(true_intent)

                # Obtener predicción del modelo
                result = await agent.parse_message(example.get("text", ""))

                predicted_intent = result.get("intent", {}).get("name", "unknown")
                predicted_intents.append(predicted_intent)

                # Evaluar entidades si existen
                true_ents = example.get("entities", [])
                pred_ents = result.get("entities", [])

                true_entities.extend([ent.get("entity") for ent in true_ents])
                predicted_entities.extend([ent.get("entity") for ent in pred_ents])

        # Calcular métricas de intents
        if true_intents and predicted_intents:
            # Overall accuracy
            accuracy = accuracy_score(true_intents, predicted_intents)

            # Precision, Recall, F1-Score por clase y promedio
            precision, recall, f1, support = precision_recall_fscore_support(
                true_intents, predicted_intents, average='weighted', zero_division=0
            )

            # F1-Score macro (promedio simple)
            precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
                true_intents, predicted_intents, average='macro', zero_division=0
            )

            # Reporte detallado por clase
            report = classification_report(true_intents, predicted_intents, zero_division=0, output_dict=True)

            # Calcular métricas de entidades si existen
            entity_metrics = {}
            if true_entities and predicted_entities:
                try:
                    ent_accuracy = accuracy_score(true_entities, predicted_entities)
                    ent_precision, ent_recall, ent_f1, _ = precision_recall_fscore_support(
                        true_entities, predicted_entities, average='weighted', zero_division=0
                    )
                    entity_metrics = {
                        "entity_accuracy": ent_accuracy,
                        "entity_precision": ent_precision,
                        "entity_recall": ent_recall,
                        "entity_f1": ent_f1
                    }
                except:
                    entity_metrics = {"error": "No se pudieron calcular métricas de entidades"}

            # Resultados finales
            results = {
                "timestamp": datetime.now().isoformat(),
                "model_path": model_path,
                "test_examples": len(test_data.training_examples),
                "unique_intents": len(set(true_intents)),

                # Métricas principales
                "accuracy": accuracy,
                "precision_weighted": precision,
                "recall_weighted": recall,
                "f1_score_weighted": f1,

                "precision_macro": precision_macro,
                "recall_macro": recall_macro,
                "f1_score_macro": f1_macro,

                # Reporte detallado
                "classification_report": report,

                # Entidades
                "entity_metrics": entity_metrics,

                # Estadísticas adicionales
                "intent_distribution": pd.Series(true_intents).value_counts().to_dict(),
                "prediction_distribution": pd.Series(predicted_intents).value_counts().to_dict()
            }

            return results

        else:
            return {"error": "No se encontraron intents para evaluar"}

    except Exception as e:
        print(f"❌ Error durante la evaluación: {str(e)}")
        return {"error": str(e)}

def print_evaluation_report(results: Dict):
    """Imprime un reporte legible de la evaluación"""

    print("\n" + "="*60)
    print("📊 REPORTE DE EVALUACIÓN DEL MODELO")
    print("="*60)

    if "error" in results:
        print(f"❌ ERROR: {results['error']}")
        return

    print(f"📅 Fecha: {results['timestamp']}")
    print(f"📁 Modelo: {os.path.basename(results['model_path'])}")
    print(f"📝 Ejemplos evaluados: {results['test_examples']}")
    print(f"🎯 Intents únicos: {results['unique_intents']}")

    print("\n" + "-"*40)
    print("📈 MÉTRICAS PRINCIPALES")
    print("-"*40)

    print(f"🎯 Accuracy: {results['accuracy']:.4f}")
    print(f"🔍 Precision (weighted): {results['precision_weighted']:.4f}")
    print(f"📊 Recall (weighted): {results['recall_weighted']:.4f}")
    print(f"⭐ F1-Score (weighted): {results['f1_score_weighted']:.4f}")
    print(f"🔍 Precision (macro): {results['precision_macro']:.4f}")
    print(f"📊 Recall (macro): {results['recall_macro']:.4f}")
    print(f"⭐ F1-Score (macro): {results['f1_score_macro']:.4f}")
    # Top 5 intents mejor clasificados
    print("\n" + "-"*40)
    print("🏆 TOP 5 INTENTS MEJOR CLASIFICADOS")
    print("-"*40)

    intent_f1 = {intent: metrics['f1-score'] for intent, metrics in results['classification_report'].items()
                 if isinstance(metrics, dict) and intent != 'weighted avg' and intent != 'macro avg'}

    sorted_intents = sorted(intent_f1.items(), key=lambda x: x[1], reverse=True)
    for intent, f1 in sorted_intents[:5]:
        precision = results['classification_report'][intent]['precision']
        recall = results['classification_report'][intent]['recall']
        support = results['classification_report'][intent]['support']
        print(f"{intent:20} | F1: {f1:.3f} | Prec: {precision:.3f} | Rec: {recall:.3f} | Sup: {support}")

    # Intent distribution
    print("\n" + "-"*40)
    print("📊 DISTRIBUCIÓN DE INTENTS")
    print("-"*40)

    for intent, count in results['intent_distribution'].items():
        percentage = (count / sum(results['intent_distribution'].values())) * 100
        print(f"{intent:20} | {count:3d} ejemplos ({percentage:5.1f}%)")

    # Entity metrics
    if results.get('entity_metrics') and 'error' not in results['entity_metrics']:
        print("\n" + "-"*40)
        print("🏷️ MÉTRICAS DE ENTIDADES")
        print("-"*40)

        em = results['entity_metrics']
        print(f"🎯 Entity Accuracy: {em['entity_accuracy']:.4f}")
        print(f"🔍 Entity Precision: {em['entity_precision']:.4f}")
        print(f"📊 Entity Recall: {em['entity_recall']:.4f}")
        print(f"⭐ Entity F1: {em['entity_f1']:.4f}")
async def main():
    """Función principal para ejecutar la evaluación"""

    # Configurar rutas
    model_path = "models"
    test_data_path = "data/test_data.yml"

    # Verificar que existan los archivos
    if not os.path.exists(test_data_path):
        print(f"❌ Error: No se encuentra el archivo de datos de prueba: {test_data_path}")
        return

    # Buscar el modelo más reciente
    if os.path.exists(model_path):
        model_files = [f for f in os.listdir(model_path) if f.endswith('.tar.gz')]
        if model_files:
            latest_model = max(model_files, key=lambda x: os.path.getctime(os.path.join(model_path, x)))
            model_path = os.path.join(model_path, latest_model)
        else:
            print(f"❌ Error: No se encontraron modelos en {model_path}")
            return
    else:
        print(f"❌ Error: No se encuentra el directorio de modelos: {model_path}")
        return

    print(f"🤖 Modelo a evaluar: {model_path}")
    print(f"📋 Datos de prueba: {test_data_path}")

    # Ejecutar evaluación
    results = await evaluate_model_performance(model_path, test_data_path)

    # Imprimir reporte
    print_evaluation_report(results)

    # Guardar en base de datos si no hay error
    if "error" not in results:
        try:
            # Extraer métricas principales para guardar
            metrics_data = {
                "accuracy": results["accuracy"],
                "precision": results["precision_weighted"],
                "recall": results["recall_weighted"],
                "f1_score": results["f1_score_weighted"],
                "test_examples": results["test_examples"],
                "unique_intents": results["unique_intents"]
            }

            save_model_evaluation(metrics_data)
            print("\n✅ Métricas guardadas en la base de datos SQLite")

        except Exception as e:
            print(f"\n⚠️ No se pudieron guardar las métricas: {str(e)}")

    print("\n" + "="*60)
    print("🎯 EVALUACIÓN COMPLETADA")
    print("="*60)

if __name__ == "__main__":
    # Ejecutar evaluación
    asyncio.run(main())