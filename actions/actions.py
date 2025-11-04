# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
import random
from datetime import datetime
import re
from collections import defaultdict
import unicodedata

# Importar el sistema de métricas SQLite
from sqlite_metrics import (
    save_quiz_result, save_user_query, save_usage_stat,
    get_user_quiz_history, get_leaderboard, get_usage_stats
)

# Índice global en memoria para búsquedas rápidas
BIBLE_INDEX = {}
TOPIC_INDEX = defaultdict(list)
QUIZ_DATA = {}

def normalize(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text.lower())
        if unicodedata.category(c) != 'Mn'
    )

class BibleIndexer:
    """Clase para manejar la indexación bíblica en memoria"""
    
    @staticmethod
    def load_bible_data():
        """Carga y indexa el contenido bíblico al arrancar"""
        try:
            with open("data/bible_content.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Indexar versículos para búsqueda O(1)
            for verse in data["verses"]:
                key = (verse["book"].lower(), verse["chapter"], verse["verse"])
                BIBLE_INDEX[key] = verse["text"]
            
            # Crear índice de temas para búsqueda full-text
            for verse in data["verses"]:
                text = verse["text"].lower()
                words = re.findall(r'\b\w+\b', text)
                for word in words:
                    if len(word) > 2:  # Ignorar palabras muy cortas
                        TOPIC_INDEX[word].append({
                            "book": verse["book"],
                            "chapter": verse["chapter"],
                            "verse": verse["verse"],
                            "text": verse["text"]
                        })
            
            # Cargar preguntas del quiz
            if "quiz_questions" in data:
                QUIZ_DATA["questions"] = data["quiz_questions"]
            
            return data
        except Exception as e:
            print(f"Error cargando datos bíblicos: {e}")
            return {"verses": [], "stories": [], "concepts": []}

# Cargar datos al importar el módulo
BIBLE_DATA = BibleIndexer.load_bible_data()

class ActionBuscarVersiculo(Action):
    def name(self) -> Text:
        return "action_buscar_versiculo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extraer entidades
        entities = tracker.latest_message.get("entities", [])
        libro = None
        capitulo = None
        versiculo = None
        
        for entity in entities:
            if entity["entity"] == "libro_biblico":
                libro = entity["value"]
            elif entity["entity"] == "capitulo":
                capitulo = entity["value"]
            elif entity["entity"] == "versiculo":
                versiculo = entity["value"]
        
        # Si no se extrajeron entidades, intentar extraer del texto
        if not libro or not capitulo or not versiculo:
            text = tracker.latest_message.get("text", "").lower()
            # Buscar patrones como "Juan 3:16", "juan 3:16", etc.
            import re
            pattern = r'(\w+)\s+(\d+):(\d+)'
            match = re.search(pattern, text)
            if match:
                libro = match.group(1)
                capitulo = match.group(2)
                versiculo = match.group(3)
        
        # Guardar consulta del usuario
        user_id = tracker.sender_id
        intent = tracker.latest_message.get("intent", {}).get("name", "preguntar_versiculo")
        entities_str = str(tracker.latest_message.get("entities", []))
        save_user_query(user_id, intent, entities_str)
        save_usage_stat(user_id, "verse_search", True)
        
        # Búsqueda O(1) usando el índice
        if libro and capitulo and versiculo:
            # Normalizar el nombre del libro
            libro_normalizado = libro.lower()
            if libro_normalizado == "juan":
                libro_normalizado = "juan"
            elif libro_normalizado == "genesis":
                libro_normalizado = "génesis"
            elif libro_normalizado == "salmos":
                libro_normalizado = "salmos"
            elif libro_normalizado == "romanos":
                libro_normalizado = "romanos"
            elif libro_normalizado == "filipenses":
                libro_normalizado = "filipenses"
            
            key = (libro_normalizado, capitulo, versiculo)
            if key in BIBLE_INDEX:
                response = f"**{libro.title()} {capitulo}:{versiculo}**\n\n{BIBLE_INDEX[key]}"
                dispatcher.utter_message(text=response)
                
                # Preguntar si fue útil
                dispatcher.utter_message(text="¿Te fue útil esta respuesta?")
                return []
        
        # Si no encuentra el versículo específico
        dispatcher.utter_message(text="No encontré ese versículo específico, pero aquí tienes algunos versículos inspiradores:")
        
        # Mostrar algunos versículos de ejemplo
        sample_verses = list(BIBLE_INDEX.items())[:3]
        for (book, chapter, verse), text in sample_verses:
            response = f"**{book.title()} {chapter}:{verse}**\n{text}"
            dispatcher.utter_message(text=response)
        
        dispatcher.utter_message(text="¿Te fue útil esta respuesta?")
        return []

class ActionSearchTopic(Action):
    """Búsqueda por tema usando índice full-text"""
    
    def name(self) -> Text:
        return "action_buscar_por_tema"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extraer tema de búsqueda
        message = tracker.latest_message.get("text", "").lower()
        
        # Buscar palabras clave en el mensaje
        keywords = re.findall(r'\b\w+\b', message)
        relevant_verses = []
        
        for keyword in keywords:
            norm_keyword = normalize(keyword)
            for word, verses in TOPIC_INDEX.items():
                if norm_keyword in normalize(word):
                    relevant_verses.extend(verses)
        
        # Eliminar duplicados y limitar resultados
        unique_verses = []
        seen = set()
        for verse in relevant_verses:
            key = (verse["book"], verse["chapter"], verse["verse"])
            if key not in seen:
                unique_verses.append(verse)
                seen.add(key)
        
        # Mostrar los 3-5 versículos más relevantes
        if unique_verses:
            dispatcher.utter_message(text=f"Encontré {len(unique_verses[:5])} versículos relacionados con tu búsqueda:")
            
            for verse in unique_verses[:5]:
                response = f"**{verse['book']} {verse['chapter']}:{verse['verse']}**\n{verse['text']}"
                dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="No encontré versículos específicos sobre ese tema, pero aquí tienes algunos versículos inspiradores:")
            
            # Mostrar versículos aleatorios
            sample_verses = random.sample(list(BIBLE_INDEX.items()), 3)
            for (book, chapter, verse), text in sample_verses:
                response = f"**{book.title()} {chapter}:{verse}**\n{text}"
                dispatcher.utter_message(text=response)
        
        dispatcher.utter_message(text="¿Te fue útil esta respuesta?")
        return []

class ActionObtenerHistoriaBiblica(Action):
    def name(self) -> Text:
        return "action_obtener_historia_biblica"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extraer concepto de la historia
        concepto = next((entity["value"] for entity in tracker.latest_message["entities"] 
                        if entity["entity"] == "concepto"), None)
        
        # Buscar historia específica
        if concepto and "stories" in BIBLE_DATA:
            for story in BIBLE_DATA["stories"]:
                if concepto.lower() in story["topic"].lower():
                    response = f"**Historia de {story['topic']}**\n\n{story['summary']}"
                    dispatcher.utter_message(text=response)
                    dispatcher.utter_message(text="¿Te fue útil esta respuesta?")
                    return []
        
        # Si no encuentra la historia específica, mostrar una aleatoria
        if "stories" in BIBLE_DATA and BIBLE_DATA["stories"]:
            story = random.choice(BIBLE_DATA["stories"])
            response = f"**Historia de {story['topic']}**\n\n{story['summary']}"
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Te comparto la historia de Moisés, quien fue elegido por Dios para liberar a Israel de la esclavitud en Egipto. Esta historia nos enseña sobre la fe, la obediencia y cómo Dios usa a personas ordinarias para hacer cosas extraordinarias.")
        
        dispatcher.utter_message(text="¿Te fue útil esta respuesta?")
        return []

class ActionExplicarConcepto(Action):
    def name(self) -> Text:
        return "action_explicar_concepto"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extraer concepto
        concepto = next((entity["value"] for entity in tracker.latest_message["entities"] 
                        if entity["entity"] == "concepto"), None)
        
        # Buscar concepto específico
        if concepto and "concepts" in BIBLE_DATA:
            for concept in BIBLE_DATA["concepts"]:
                if concepto.lower() == concept["term"].lower():
                    response = f"**{concept['term'].title()}**: {concept['definition']}"
                    dispatcher.utter_message(text=response)
                    dispatcher.utter_message(text="¿Te fue útil esta respuesta?")
                    return []
        
        # Conceptos adicionales
        conceptos_adicionales = {
            "fe": "La fe es la certeza de lo que se espera, la convicción de lo que no se ve (Hebreos 11:1). Es confiar completamente en Dios y sus promesas.",
            "gracia": "La gracia es el favor inmerecido de Dios. Es su amor y misericordia hacia nosotros, a pesar de nuestros pecados.",
            "arrepentimiento": "El arrepentimiento es cambiar de dirección, alejarse del pecado y volverse hacia Dios con un corazón contrito.",
            "salvación": "La salvación es el regalo de Dios por medio de Jesucristo, que nos libera del pecado y nos da vida eterna.",
            "adoración": "La adoración es rendir honor, gloria y alabanza a Dios con todo nuestro ser."
        }
        
        if concepto and concepto.lower() in conceptos_adicionales:
            response = f"**{concepto.title()}**: {conceptos_adicionales[concepto.lower()]}"
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Los conceptos bíblicos fundamentales incluyen fe, gracia, arrepentimiento, salvación y adoración. ¿Te gustaría que te explique alguno en particular?")
        
        dispatcher.utter_message(text="¿Te fue útil esta respuesta?")
        return []

class ActionGenerarDevocional(Action):
    def name(self) -> Text:
        return "action_generar_devocional"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        devocionales = [
            {
                "titulo": "Confía en el Señor",
                "versiculo": "Proverbios 3:5-6",
                "texto": "Confía en el Señor con todo tu corazón, y no te apoyes en tu propia prudencia. Reconócelo en todos tus caminos, y él enderezará tus sendas.",
                "reflexion": "Hoy, toma un momento para confiar completamente en Dios. Él conoce el camino que tienes por delante y te guiará paso a paso."
            },
            {
                "titulo": "La Paz de Dios",
                "versiculo": "Filipenses 4:6-7",
                "texto": "Por nada estéis afanosos, sino sean conocidas vuestras peticiones delante de Dios en toda oración y ruego, con acción de gracias. Y la paz de Dios, que sobrepasa todo entendimiento, guardará vuestros corazones y vuestros pensamientos en Cristo Jesús.",
                "reflexion": "En lugar de preocuparte, ora. Dios quiere escuchar tus peticiones y te dará su paz que sobrepasa todo entendimiento."
            },
            {
                "titulo": "Nuevas Misericordias",
                "versiculo": "Lamentaciones 3:22-23",
                "texto": "Por la misericordia del Señor no hemos sido consumidos, porque nunca decayeron sus misericordias. Nuevas son cada mañana; grande es tu fidelidad.",
                "reflexion": "Cada mañana es una nueva oportunidad. Las misericordias de Dios son nuevas cada día. ¡Alaba a Dios por su fidelidad!"
            }
        ]
        
        devocional = random.choice(devocionales)
        
        response = f"**{devocional['titulo']}**\n\n**Versículo del día:** {devocional['versiculo']}\n\n{devocional['texto']}\n\n**Reflexión:** {devocional['reflexion']}"
        
        dispatcher.utter_message(text=response)
        dispatcher.utter_message(text="¿Te fue útil esta respuesta?")
        return []

class ActionObtenerEventos(Action):
    def name(self) -> Text:
        return "action_obtener_eventos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        eventos = [
            "**Domingo 10:00** - Servicio de Adoración",
            "**Domingo 11:30** - Escuela Dominical",
            "**Miércoles 19:00** - Estudio Bíblico",
            "**Jueves 19:30** - Reunión de Oración",
            "**Sábado 15:00** - Ministerio de Jóvenes",
            "**Sábado 16:30** - Ministerio de Niños"
        ]
        
        response = "**Próximos eventos en la iglesia:**\n\n" + "\n".join(eventos)
        response += "\n\nPara más información, contacta a la oficina de la iglesia."
        
        dispatcher.utter_message(text=response)
        dispatcher.utter_message(text="¿Te fue útil esta respuesta?")
        return []

class ActionObtenerHorarios(Action):
    def name(self) -> Text:
        return "action_obtener_horarios"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        church_info = BIBLE_DATA.get("church", {}) if isinstance(BIBLE_DATA, dict) else {}
        
        horarios = church_info.get("hours", ["Domingo 10:00", "Jueves 19:30"]) if isinstance(church_info, dict) else ["Domingo 10:00", "Jueves 19:30"]
        
        response = "**Horarios de servicios:**\n\n"
        for horario in horarios:
            response += f"• {horario}\n"
        
        address = church_info.get('address', 'Av. San Martín #1234, Barrio Equipetrol') if isinstance(church_info, dict) else 'Av. San Martín #1234, Barrio Equipetrol'
        pastor = church_info.get('pastor', 'Pr. Juan Pérez') if isinstance(church_info, dict) else 'Pr. Juan Pérez'
        
        response += f"\n**Dirección:** {address}\n"
        response += f"**Pastor:** {pastor}"
        
        dispatcher.utter_message(text=response)
        dispatcher.utter_message(text="¿Te fue útil esta respuesta?")
        return []

class ActionOracionGuiada(Action):
    def name(self) -> Text:
        return "action_oracion_guiada"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extraer tema de oración
        tema = next((entity["value"] for entity in tracker.latest_message["entities"] 
                    if entity["entity"] == "tema_oracion"), None)
        
        oraciones = {
            "familia": "Padre celestial, bendice a mi familia. Ayúdanos a crecer juntos en tu amor y sabiduría. Protege a cada miembro y guíanos en tu camino. En el nombre de Jesús, amén.",
            "momentos difíciles": "Señor, en estos momentos difíciles, ayúdame a confiar en ti. Dame la fuerza que necesito y recuérdame que tú estás conmigo. En tus manos pongo mi situación. Amén.",
            "sanidad": "Dios de misericordia, te pido por sanidad. Tú eres el médico de médicos. Restaura mi cuerpo, mente y espíritu según tu voluntad. En el nombre de Jesús, amén.",
            "agradecimiento": "Gracias, Padre, por todas tus bendiciones. Por la vida, la salud, la familia y tu amor incondicional. Te alabo por tu fidelidad. En el nombre de Jesús, amén."
        }
        
        if tema and tema.lower() in oraciones:
            oracion = oraciones[tema.lower()]
        else:
            oracion = "Padre celestial, gracias por este día. Ayúdame a caminar en tu voluntad y a ser una bendición para otros. En el nombre de Jesús, amén."
        
        response = f"**Oración guiada:**\n\n{oracion}\n\nTómate un momento para meditar en estas palabras y hacer tu propia oración."
        
        dispatcher.utter_message(text=response)
        dispatcher.utter_message(text="¿Te fue útil esta respuesta?")
        return []

class ActionAyudaEspiritual(Action):
    def name(self) -> Text:
        return "action_ayuda_espiritual"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        recursos = [
            "**Recuerda que Dios está contigo** - 'No te desampararé, ni te dejaré' (Hebreos 13:5)",
            "**Ora sin cesar** - Habla con Dios sobre tus preocupaciones",
            "**Lee la Biblia** - La palabra de Dios es luz para tu camino",
            "**Busca comunidad** - No estás solo, otros pueden apoyarte",
            "**Habla con un líder espiritual** - El pastor o líderes pueden aconsejarte"
        ]
        
        response = "Entiendo que estás pasando por un momento difícil. Aquí tienes algunos recursos para ayudarte:\n\n"
        response += "\n".join(recursos)
        response += "\n\n¿Te gustaría que oremos juntos o que te ayude a encontrar un versículo específico?"
        
        dispatcher.utter_message(text=response)
        dispatcher.utter_message(text="¿Te fue útil esta respuesta?")
        return []

class ActionEstudioBiblico(Action):
    def name(self) -> Text:
        return "action_estudio_biblico"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        estudios = [
            {
                "titulo": "Fundamentos de la Fe",
                "descripcion": "Estudio básico sobre los principios fundamentales del cristianismo",
                "duracion": "4 semanas",
                "temas": ["Salvación", "Fe", "Gracia", "Oración"]
            },
            {
                "titulo": "Vidas de Fe en la Biblia",
                "descripcion": "Estudio de personajes bíblicos y sus lecciones para nosotros",
                "duracion": "6 semanas",
                "temas": ["Abraham", "Moisés", "David", "Daniel", "Pedro", "Pablo"]
            },
            {
                "titulo": "Los Frutos del Espíritu",
                "descripcion": "Estudio profundo sobre Galatas 5:22-23",
                "duracion": "9 semanas",
                "temas": ["Amor", "Gozo", "Paz", "Paciencia", "Benignidad", "Bondad", "Fe", "Mansedumbre", "Templanza"]
            }
        ]
        
        estudio = random.choice(estudios)
        
        response = f"**{estudio['titulo']}**\n\n{estudio['descripcion']}\n\n**Duración:** {estudio['duracion']}\n**Temas:** {', '.join(estudio['temas'])}\n\n¿Te gustaría que profundicemos en algún tema específico?"
        
        dispatcher.utter_message(text=response)
        dispatcher.utter_message(text="¿Te fue útil esta respuesta?")
        return []

class ActionConsejoPastoral(Action):
    def name(self) -> Text:
        return "action_consejo_pastoral"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        church_info = BIBLE_DATA.get("church", {}) if isinstance(BIBLE_DATA, dict) else {}
        
        pastor = church_info.get("pastor", "Pr. Juan Pérez") if isinstance(church_info, dict) else "Pr. Juan Pérez"
        direccion = church_info.get("address", "Av. San Martín #1234, Barrio Equipetrol") if isinstance(church_info, dict) else "Av. San Martín #1234, Barrio Equipetrol"
        
        response = f"Para consejo pastoral específico, te recomiendo contactar directamente con nuestro pastor:\n\n"
        response += f"**{pastor}**\n"
        response += f"**Dirección:** {direccion}\n"
        response += f"**Horarios de atención:** Lunes a Viernes 9:00 - 17:00\n"
        response += f"**Teléfono:** (591) 3-123-4567\n"
        response += f"**Email:** pastor@iglesia.com\n\n"
        response += "El pastor estará encantado de ayudarte con cualquier consulta espiritual o pastoral."
        
        dispatcher.utter_message(text=response)
        dispatcher.utter_message(text="¿Te fue útil esta respuesta?")
        return []

# GAMIFICACIÓN - SISTEMA DE QUIZ
class ActionStartQuiz(Action):
    """Inicia un quiz bíblico de 3 preguntas"""
    
    def name(self) -> Text:
        return "action_start_quiz"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if "questions" not in QUIZ_DATA:
            dispatcher.utter_message(text="Lo siento, no hay preguntas disponibles en este momento.")
            return []
        
        # Guardar estadística de uso
        user_id = tracker.sender_id
        save_usage_stat(user_id, "quiz_start", True)
        
        # Seleccionar 3 preguntas aleatorias
        questions = random.sample(QUIZ_DATA["questions"], 3)
        
        # Guardar las preguntas en el slot para el quiz
        quiz_data = {
            "questions": questions,
            "current_question": 0,
            "score": 0,
            "start_time": datetime.now().isoformat()
        }
        
        # Mostrar primera pregunta
        question = questions[0]
        options_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(question["options"])])
        
        response = f"**Quiz Bíblico**\n\nPregunta 1 de 3:\n\n{question['question']}\n\n{options_text}\n\nResponde con el número de tu opción (1, 2, 3 o 4)."
        
        dispatcher.utter_message(text=response)
        
        # Guardar en slot para usar en el procesamiento
        return [SlotSet("quiz_data", quiz_data)]

class ActionProcessQuizAnswer(Action):
    """Procesa la respuesta del quiz y muestra la siguiente pregunta"""
    
    def name(self) -> Text:
        return "action_process_quiz_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Obtener la respuesta del usuario
        user_answer = tracker.latest_message.get("text", "").strip()
        
        try:
            answer_number = int(user_answer) - 1  # Convertir a índice 0-based
        except ValueError:
            dispatcher.utter_message(text="Por favor, responde con un número del 1 al 4.")
            return []
        
        # Obtener datos del quiz del slot
        quiz_data = tracker.get_slot("quiz_data")
        if not quiz_data:
            dispatcher.utter_message(text="No hay un quiz activo. Inicia uno nuevo con 'quiero hacer un quiz'.")
            return []
        
        # Detectar si es quiz (current_question) o trivia (current)
        current_question = quiz_data.get("current_question", quiz_data.get("current", 0))
        score = quiz_data.get("score", 0)
        questions = quiz_data.get("questions", [])
        
        if current_question >= len(questions):
            dispatcher.utter_message(text="El quiz ya terminó.")
            return []
        
        # Verificar respuesta
        question = questions[current_question]
        # Detectar si es quiz (correct_answer) o trivia (correct)
        correct_answer = question.get("correct_answer") or question.get("correct", 0)
        is_correct = (answer_number == correct_answer)
        
        if is_correct:
            score += 1
            dispatcher.utter_message(text=f"¡Correcto! 🎉\n\n{question.get('explanation', '')}")
        else:
            correct_option = question['options'][correct_answer] if correct_answer < len(question['options']) else ""
            dispatcher.utter_message(text=f"Incorrecto. La respuesta correcta era: {correct_option}\n\n{question.get('explanation', '')}")
        
        # Actualizar datos del quiz/trivia
        quiz_data["score"] = score
        # Actualizar el campo correcto según el tipo
        if "current_question" in quiz_data:
        quiz_data["current_question"] = current_question + 1
        else:
            quiz_data["current"] = current_question + 1
        
        # Verificar si es la última pregunta
        if current_question + 1 >= len(questions):
            # Detectar si es trivia o quiz para el mensaje final
            quiz_session_id = tracker.get_slot("quiz_session_id")
            is_trivia = "current" in quiz_data or quiz_session_id == "local"
            
            if is_trivia or quiz_session_id == "local":
                # Formato para trivia
                dispatcher.utter_message(text=f"¡Terminaste! Puntaje: {score}/{len(questions)}")
            else:
                # Formato para quiz
            percentage = (score / len(questions)) * 100
            
            # Guardar resultado en SQLite
            user_id = tracker.sender_id
            save_quiz_result(user_id, score, len(questions), quiz_data)
            save_usage_stat(user_id, "quiz_complete", True)
            
            response = f"**Quiz terminado!**\n\nPuntuación: {score}/{len(questions)} ({percentage:.1f}%)\n\n"
            
            if percentage >= 80:
                response += "¡Excelente! 🏆 Tienes un gran conocimiento bíblico."
            elif percentage >= 60:
                response += "¡Muy bien! 👍 Sigue estudiando la palabra de Dios."
            else:
                response += "¡Buen intento! 📚 Te recomiendo estudiar más la Biblia."
            
            dispatcher.utter_message(text=response)
            
            # Limpiar slot del quiz/trivia
            return [SlotSet("quiz_data", None)]
            
        else:
            # Detectar si es trivia o quiz para el formato del mensaje
            quiz_session_id = tracker.get_slot("quiz_session_id")
            is_trivia = "current" in quiz_data or quiz_session_id == "local"
            
            # Mostrar siguiente pregunta
            next_question = questions[current_question + 1]
            options_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(next_question["options"])])
            
            if is_trivia or quiz_session_id == "local":
                # Formato para trivia
                response = f"Trivia bíblica ({current_question + 2}/{len(questions)})\n\n{next_question['question']}\n\n{options_text}"
            else:
                # Formato para quiz
            response = f"Pregunta {current_question + 2} de {len(questions)}:\n\n{next_question['question']}\n\n{options_text}\n\nResponde con el número de tu opción (1, 2, 3 o 4)."
            
            dispatcher.utter_message(text=response)
            
            # Actualizar slot con los nuevos datos
            return [SlotSet("quiz_data", quiz_data)]

class ActionConfirmResponse(Action):
    """Maneja las confirmaciones de utilidad de las respuestas"""
    
    def name(self) -> Text:
        return "action_confirm_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Detectar si la respuesta fue útil o no
        message = tracker.latest_message.get("text", "").lower()
        
        # Guardar feedback del usuario
        user_id = tracker.sender_id
        is_helpful = any(word in message for word in ["sí", "si", "correcto", "útil", "util", "gracias"])
        
        # Obtener la última intención del usuario
        intent = tracker.get_intent_of_latest_message() or "confirmar_respuesta"
        entities = str(tracker.latest_message.get("entities", []))
        
        # Actualizar la última consulta con el feedback
        save_user_query(user_id, intent, entities, is_helpful)
        
        if is_helpful:
            dispatcher.utter_message(text="¡Me alegra haber podido ayudarte! ¿Hay algo más en lo que pueda asistirte?")
        else:
            dispatcher.utter_message(text="Entiendo. ¿En qué puedo ayudarte de manera diferente?")
        
        return []

class ActionFallback(Action):
    """Maneja casos donde no se entiende la intención del usuario"""
    
    def name(self) -> Text:
        return "action_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = "No estoy seguro de entenderte completamente. Puedo ayudarte con:\n\n"
        response += "• Buscar versículos bíblicos\n"
        response += "• Contar historias bíblicas\n"
        response += "• Explicar conceptos bíblicos\n"
        response += "• Dar devocionales\n"
        response += "• Información de la iglesia\n"
        response += "• Oraciones guiadas\n"
        response += "• Quiz bíblico\n\n"
        response += "¿Qué te gustaría hacer?"
        
        dispatcher.utter_message(text=response)
        return []

class ActionShowStats(Action):
    """Muestra estadísticas del usuario"""
    
    def name(self) -> Text:
        return "action_show_stats"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_id = tracker.sender_id
        
        # Obtener historial del usuario
        quiz_history = get_user_quiz_history(user_id, 5)
        leaderboard = get_leaderboard(5)
        
        response = "**Tus Estadísticas:**\n\n"
        
        if quiz_history:
            response += "**Últimos Quizzes:**\n"
            for quiz in quiz_history:
                response += f"• {quiz['score']}/{quiz['total_questions']} ({quiz['percentage']:.1f}%) - {quiz['timestamp']}\n"
        else:
            response += "Aún no has completado ningún quiz.\n"
        
        response += "\n**Top 5 del Ranking:**\n"
        for i, player in enumerate(leaderboard, 1):
            response += f"{i}. Usuario {player['user_id'][:8]}... - {player['best_percentage']:.1f}% ({player['best_score']}/{3})\n"
        
        dispatcher.utter_message(text=response)
        return []
