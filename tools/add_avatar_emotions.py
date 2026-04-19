import pathlib


TARGET_EMOTIONS = {
    "utter_saludar": "feliz",
    "utter_animar": "triste",
    "utter_feliz": "feliz",
    "utter_despedida": "feliz",
    "utter_cariño_maika": "sonrojada",
    "utter_curiosidad_biblica": "sorprendida",
    "utter_fallback": "dudando",
    # Nuevas emociones más específicas
    "utter_oracion_guiada": "orando",
    "utter_agradecer": "aliviada",
    "utter_testimonio": "inspirada",
    "utter_alabanza": "feliz",
    "utter_salvacion": "inspirada",
    "utter_promesa_biblica": "inspirada",
    "utter_fortaleza": "cansada",
    "utter_charlar_informal": "picara",
    "utter_mostrar_estadisticas": "feliz_logro",
}


def main() -> None:
    domain_path = pathlib.Path(__file__).resolve().parent.parent / "domain.yml"
    text = domain_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    out_lines: list[str] = []
    current_key: str | None = None

    for i, line in enumerate(lines):
        stripped = line.lstrip()

        # Detect inicio de bloque de respuesta
        if line.startswith("  utter_") and stripped.endswith(":"):
            key = stripped[:-1]  # quitar ':'
            current_key = key
            out_lines.append(line)
            continue

        # Si estamos dentro de un bloque de interés
        if current_key in TARGET_EMOTIONS:
            # Fin del bloque de respuestas (línea en blanco o nuevo intent/response)
            if (
                line.strip() == ""
                or (not line.startswith("    ") and not line.startswith("  - "))
            ):
                current_key = None
                out_lines.append(line)
                continue

            # Detectar líneas de texto de respuesta
            if line.startswith("    - text:"):
                out_lines.append(line)

                # Si ya hay un bloque custom inmediatamente debajo, no duplicar
                emotion = TARGET_EMOTIONS[current_key]
                next_line = lines[i + 1] if i + 1 < len(lines) else ""
                if next_line.strip().startswith("custom:"):
                    continue

                out_lines.append("      custom:")
                out_lines.append(f"        emotion: {emotion}")
                continue

        out_lines.append(line)

    domain_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
