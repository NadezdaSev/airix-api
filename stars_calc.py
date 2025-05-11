def parse_stars(filename):
    activated_stars = []

    try:
        with open(filename, encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()

                # Пропуск пустых строк
                if not line:
                    continue

                print(f"Строка {i}: {repr(line)}")  # 🪵 Отладка

                if "|" not in line:
                    print(f"⚠️ Проблема на строке {i}: разделитель не найден")
                    continue

                try:
                    name, coord = [x.strip() for x in line.split("|")]
                    coord = float(coord)

                    # ВСТАВЬ ЛОГИКУ АКТИВАЦИИ ЗДЕСЬ (временная заглушка):
                    if name == "Spica":
                        activated_stars.append({"name": name, "linked_to": "MC", "orb": 0.42})

                except Exception as e:
                    print(f"❌ Ошибка при разборе строки {i}: {e}")

    except Exception as err:
        print(f"🧨 Не удалось открыть файл: {err}")

    return activated_stars
