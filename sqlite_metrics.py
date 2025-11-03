"""
Sistema de métricas local usando SQLite
Almacena resultados del quiz, consultas y otras interacciones del usuario
"""

import sqlite3
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from contextlib import contextmanager

class MetricsManager:
    """Maneja el almacenamiento de métricas en SQLite"""
    
    def __init__(self, db_path: str = "metrics.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla para resultados del quiz
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quiz_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    percentage REAL NOT NULL,
                    quiz_data TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla para consultas del usuario
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    intent TEXT NOT NULL,
                    entities TEXT,
                    response_helpful BOOLEAN,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla para estadísticas de uso
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usage_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    success BOOLEAN,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla para leaderboard
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    best_score INTEGER NOT NULL,
                    best_percentage REAL NOT NULL,
                    total_quizzes INTEGER DEFAULT 1,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexiones a SQLite"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def save_quiz_result(self, user_id: str, score: int, total_questions: int, 
                        quiz_data: Dict[str, Any]) -> bool:
        """
        Guarda el resultado del quiz
        
        Args:
            user_id: ID del usuario
            score: Puntuación obtenida
            total_questions: Total de preguntas
            quiz_data: Datos del quiz (preguntas, respuestas, etc.)
        
        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            percentage = (score / total_questions) * 100
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Insertar resultado del quiz
                cursor.execute("""
                    INSERT INTO quiz_results (user_id, score, total_questions, percentage, quiz_data)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, score, total_questions, percentage, str(quiz_data)))
                
                # Actualizar leaderboard
                self._update_leaderboard(cursor, user_id, score, percentage)
                
                conn.commit()
                
                print(f"Resultado del quiz guardado: {score}/{total_questions} ({percentage:.1f}%)")
                return True
                
        except Exception as e:
            print(f"Error guardando resultado del quiz: {e}")
            return False
    
    def _update_leaderboard(self, cursor, user_id: str, score: int, percentage: float):
        """Actualiza el leaderboard del usuario"""
        # Verificar si el usuario ya existe en el leaderboard
        cursor.execute("""
            SELECT best_score, best_percentage, total_quizzes 
            FROM leaderboard WHERE user_id = ?
        """, (user_id,))
        
        result = cursor.fetchone()
        
        if result:
            best_score, best_percentage, total_quizzes = result
            
            # Actualizar si es mejor puntuación
            if score > best_score or percentage > best_percentage:
                cursor.execute("""
                    UPDATE leaderboard 
                    SET best_score = ?, best_percentage = ?, total_quizzes = ?, last_updated = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (max(score, best_score), max(percentage, best_percentage), total_quizzes + 1, user_id))
            else:
                cursor.execute("""
                    UPDATE leaderboard 
                    SET total_quizzes = ?, last_updated = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (total_quizzes + 1, user_id))
        else:
            # Insertar nuevo usuario
            cursor.execute("""
                INSERT INTO leaderboard (user_id, best_score, best_percentage, total_quizzes)
                VALUES (?, ?, ?, 1)
            """, (user_id, score, percentage))
    
    def save_user_query(self, user_id: str, intent: str, entities: Optional[str] = None, 
                       response_helpful: Optional[bool] = None) -> bool:
        """
        Guarda una consulta del usuario
        
        Args:
            user_id: ID del usuario
            intent: Intención detectada
            entities: Entidades extraídas (opcional)
            response_helpful: Si la respuesta fue útil (opcional)
        
        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO user_queries (user_id, intent, entities, response_helpful)
                    VALUES (?, ?, ?, ?)
                """, (user_id, intent, entities, response_helpful))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error guardando consulta del usuario: {e}")
            return False
    
    def save_usage_stat(self, user_id: str, action_type: str, success: bool = True) -> bool:
        """
        Guarda estadística de uso
        
        Args:
            user_id: ID del usuario
            action_type: Tipo de acción (quiz, search, story, etc.)
            success: Si la acción fue exitosa
        
        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO usage_stats (user_id, action_type, success)
                    VALUES (?, ?, ?)
                """, (user_id, action_type, success))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error guardando estadística de uso: {e}")
            return False
    
    def get_user_quiz_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Obtiene el historial de quizzes de un usuario
        
        Args:
            user_id: ID del usuario
            limit: Número máximo de resultados
        
        Returns:
            List[Dict]: Lista de resultados del usuario
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT score, total_questions, percentage, timestamp
                    FROM quiz_results 
                    WHERE user_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (user_id, limit))
                
                results = []
                for row in cursor.fetchall():
                    results.append({
                        "score": row[0],
                        "total_questions": row[1],
                        "percentage": row[2],
                        "timestamp": row[3]
                    })
                
                return results
                
        except Exception as e:
            print(f"Error obteniendo historial del usuario: {e}")
            return []
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """
        Obtiene el ranking de mejores puntuaciones
        
        Args:
            limit: Número máximo de resultados
        
        Returns:
            List[Dict]: Lista de mejores puntuaciones
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT user_id, best_score, best_percentage, total_quizzes
                    FROM leaderboard 
                    ORDER BY best_percentage DESC, best_score DESC
                    LIMIT ?
                """, (limit,))
                
                results = []
                for row in cursor.fetchall():
                    results.append({
                        "user_id": row[0],
                        "best_score": row[1],
                        "best_percentage": row[2],
                        "total_quizzes": row[3]
                    })
                
                return results
                
        except Exception as e:
            print(f"Error obteniendo leaderboard: {e}")
            return []
    
    def get_usage_stats(self, days: int = 30) -> Dict[str, Any]:
        """
        Obtiene estadísticas de uso
        
        Args:
            days: Número de días para analizar
        
        Returns:
            Dict[str, Any]: Estadísticas de uso
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Total de consultas
                cursor.execute("""
                    SELECT COUNT(*) FROM user_queries 
                    WHERE timestamp >= datetime('now', '-{} days')
                """.format(days))
                total_queries = cursor.fetchone()[0]
                
                # Consultas por intención
                cursor.execute("""
                    SELECT intent, COUNT(*) 
                    FROM user_queries 
                    WHERE timestamp >= datetime('now', '-{} days')
                    GROUP BY intent
                    ORDER BY COUNT(*) DESC
                """.format(days))
                queries_by_intent = dict(cursor.fetchall())
                
                # Total de quizzes
                cursor.execute("""
                    SELECT COUNT(*) FROM quiz_results 
                    WHERE timestamp >= datetime('now', '-{} days')
                """.format(days))
                total_quizzes = cursor.fetchone()[0]
                
                # Promedio de puntuación
                cursor.execute("""
                    SELECT AVG(percentage) FROM quiz_results 
                    WHERE timestamp >= datetime('now', '-{} days')
                """.format(days))
                avg_score = cursor.fetchone()[0] or 0
                
                return {
                    "total_queries": total_queries,
                    "queries_by_intent": queries_by_intent,
                    "total_quizzes": total_quizzes,
                    "average_quiz_score": round(avg_score, 1),
                    "period_days": days
                }
                
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {}

# Instancia global del manager
metrics_manager = MetricsManager()

# Funciones helper para uso en actions.py
def save_quiz_result(user_id: str, score: int, total_questions: int, 
                    quiz_data: Dict[str, Any]) -> bool:
    """Función helper para guardar resultados del quiz"""
    return metrics_manager.save_quiz_result(user_id, score, total_questions, quiz_data)

def save_user_query(user_id: str, intent: str, entities: Optional[str] = None, 
                   response_helpful: Optional[bool] = None) -> bool:
    """Función helper para guardar consultas del usuario"""
    return metrics_manager.save_user_query(user_id, intent, entities, response_helpful)

def save_usage_stat(user_id: str, action_type: str, success: bool = True) -> bool:
    """Función helper para guardar estadísticas de uso"""
    return metrics_manager.save_usage_stat(user_id, action_type, success)

def get_user_quiz_history(user_id: str, limit: int = 10) -> List[Dict]:
    """Función helper para obtener historial del usuario"""
    return metrics_manager.get_user_quiz_history(user_id, limit)

def get_leaderboard(limit: int = 10) -> List[Dict]:
    """Función helper para obtener el ranking"""
    return metrics_manager.get_leaderboard(limit)

def get_usage_stats(days: int = 30) -> Dict[str, Any]:
    """Función helper para obtener estadísticas de uso"""
    return metrics_manager.get_usage_stats(days) 