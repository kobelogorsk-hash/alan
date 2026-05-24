"""
База данных бойцов Brawl Stars и рекомендации по режимам
"""
from typing import Dict, List, Any


class BrawlerRecommendations:
    """Система рекомендаций бойцов для разных режимов Brawl Stars"""
    
    # База данных бойцов с их характеристиками
    BRAWLERS = {
        # УБИЙЦЫ (ASSASSINS)
        "Crow": {
            "type": "assassin",
            "difficulty": "high",
            "modes": {
                "Gem Grab": 9,
                "Showdown": 10,
                "Bounty": 9,
                "Heist": 6,
                "Brawl Ball": 7,
                "Hot Zone": 8,
                "Knockout": 9
            },
            "strengths": ["Мобильность", "Контроль территории", "Добивание"],
            "weaknesses": ["Низкий ХП", "Сложность в использовании"]
        },
        "Leon": {
            "type": "assassin",
            "difficulty": "medium",
            "modes": {
                "Gem Grab": 8,
                "Showdown": 10,
                "Bounty": 9,
                "Heist": 7,
                "Brawl Ball": 8,
                "Hot Zone": 7,
                "Knockout": 9
            },
            "strengths": ["Невидимость", "Бurst урон", "Мобильность"],
            "weaknesses": ["Зависит от супер-атаки", "Низкий ХП"]
        },
        "Mortis": {
            "type": "assassin",
            "difficulty": "high",
            "modes": {
                "Gem Grab": 7,
                "Showdown": 8,
                "Bounty": 8,
                "Heist": 9,
                "Brawl Ball": 7,
                "Hot Zone": 6,
                "Knockout": 8
            },
            "strengths": ["Высокая мобильность", "Увороты", "Урон по сейфу"],
            "weaknesses": ["Близкий бой", "Требует навыка"]
        },
        
        # ТАНКИ (TANKS)
        "El Primo": {
            "type": "tank",
            "difficulty": "low",
            "modes": {
                "Gem Grab": 6,
                "Showdown": 7,
                "Bounty": 5,
                "Heist": 8,
                "Brawl Ball": 9,
                "Hot Zone": 8,
                "Knockout": 7
            },
            "strengths": ["Высокий ХП", "Ультимейт для командных боёв", "Хорош в Brawl Ball"],
            "weaknesses": ["Ближний бой", "Легко кайтить"]
        },
        "Frank": {
            "type": "tank",
            "difficulty": "medium",
            "modes": {
                "Gem Grab": 7,
                "Showdown": 6,
                "Bounty": 6,
                "Heist": 8,
                "Brawl Ball": 8,
                "Hot Zone": 9,
                "Knockout": 8
            },
            "strengths": ["Оглушение", "Высокий урон", "Танковость"],
            "weaknesses": ["Медленный", "Зависит от супер-атаки"]
        },
        "Rosa": {
            "type": "tank",
            "difficulty": "low",
            "modes": {
                "Gem Grab": 8,
                "Showdown": 7,
                "Bounty": 6,
                "Heist": 7,
                "Brawl Ball": 7,
                "Hot Zone": 9,
                "Knockout": 8
            },
            "strengths": ["Кусты", "Щит", "Хороша в закрытых картах"],
            "weaknesses": ["Нужны кусты", "Ближний бой"]
        },
        "Bull": {
            "type": "tank",
            "difficulty": "low",
            "modes": {
                "Gem Grab": 6,
                "Showdown": 7,
                "Bounty": 5,
                "Heist": 8,
                "Brawl Ball": 7,
                "Hot Zone": 7,
                "Knockout": 7
            },
            "strengths": ["Высокий ХП", "Близкий урон", "Прост в использовании"],
            "weaknesses": ["Только ближний бой", "Нет мобильности"]
        },
        
        # СТРЕЛКИ (SHARPSHOOTERS)
        "Piper": {
            "type": "sharpshooter",
            "difficulty": "medium",
            "modes": {
                "Gem Grab": 8,
                "Showdown": 8,
                "Bounty": 10,
                "Heist": 7,
                "Brawl Ball": 6,
                "Hot Zone": 7,
                "Knockout": 9
            },
            "strengths": ["Дальний урон", "Высокий burst", "Мобильность с супером"],
            "weaknesses": ["Слаба вблизи", "Требует позиционирования"]
        },
        "Belle": {
            "type": "sharpshooter",
            "difficulty": "medium",
            "modes": {
                "Gem Grab": 8,
                "Showdown": 8,
                "Bounty": 9,
                "Heist": 8,
                "Brawl Ball": 7,
                "Hot Zone": 8,
                "Knockout": 9
            },
            "strengths": ["Маркировка", "Дальний урон", "Контроль"],
            "weaknesses": ["Слаба вблизи", "Зависит от команды"]
        },
        "Nani": {
            "type": "sharpshooter",
            "difficulty": "high",
            "modes": {
                "Gem Grab": 7,
                "Showdown": 9,
                "Bounty": 9,
                "Heist": 8,
                "Brawl Ball": 6,
                "Hot Zone": 7,
                "Knockout": 8
            },
            "strengths": ["Глобальная атака", "Контроль карты", "Высокий урон"],
            "weaknesses": ["Очень низкий ХП", "Сложная в управлении"]
        },
        
        # БОЙЦЫ ПОДДЕРЖКИ (SUPPORT)
        "Poco": {
            "type": "support",
            "difficulty": "low",
            "modes": {
                "Gem Grab": 9,
                "Showdown": 7,
                "Bounty": 7,
                "Heist": 8,
                "Brawl Ball": 9,
                "Hot Zone": 8,
                "Knockout": 9
            },
            "strengths": ["Лечение", "Урон по области", "Прост в использовании"],
            "weaknesses": ["Средний урон", "Предсказуемый"]
        },
        "Byron": {
            "type": "support",
            "difficulty": "medium",
            "modes": {
                "Gem Grab": 9,
                "Showdown": 8,
                "Bounty": 8,
                "Heist": 7,
                "Brawl Ball": 8,
                "Hot Zone": 8,
                "Knockout": 9
            },
            "strengths": ["Лечение/урон", "Дальняя дистанция", "Ульта на всю команду"],
            "weaknesses": ["Низкий ХП", "Требует точности"]
        },
        "Gene": {
            "type": "support",
            "difficulty": "medium",
            "modes": {
                "Gem Grab": 9,
                "Showdown": 8,
                "Bounty": 7,
                "Heist": 7,
                "Brawl Ball": 9,
                "Hot Zone": 8,
                "Knockout": 8
            },
            "strengths": ["Захват врагов", "Лечение", "Универсальность"],
            "weaknesses": ["Средний урон", "Зависит от супер-атаки"]
        },
        
        # КОНТРОЛЁРЫ (CONTROLLERS)
        "Sprout": {
            "type": "controller",
            "difficulty": "medium",
            "modes": {
                "Gem Grab": 8,
                "Showdown": 7,
                "Bounty": 6,
                "Heist": 7,
                "Brawl Ball": 8,
                "Hot Zone": 9,
                "Knockout": 7
            },
            "strengths": ["Контроль территории", "Стены", "Урон по области"],
            "weaknesses": ["Медленный", "Предсказуемые атаки"]
        },
        "Amber": {
            "type": "controller",
            "difficulty": "medium",
            "modes": {
                "Gem Grab": 7,
                "Showdown": 8,
                "Bounty": 7,
                "Heist": 8,
                "Brawl Ball": 9,
                "Hot Zone": 9,
                "Knockout": 8
            },
            "strengths": ["Контроль зоны", "Высокий DPS", "Защита объектов"],
            "weaknesses": ["Близкая дистанция", "Нужно время для урона"]
        },
        
        # МЕТатели (THROWERS)
        "Barley": {
            "type": "thrower",
            "difficulty": "low",
            "modes": {
                "Gem Grab": 7,
                "Showdown": 6,
                "Bounty": 7,
                "Heist": 9,
                "Brawl Ball": 7,
                "Hot Zone": 8,
                "Knockout": 6
            },
            "strengths": ["Урон за укрытиями", "Контроль зоны", "Хорош в Heist"],
            "weaknesses": ["Низкий ХП", "Медленные снаряды"]
        },
        "Dynamike": {
            "type": "thrower",
            "difficulty": "medium",
            "modes": {
                "Gem Grab": 7,
                "Showdown": 7,
                "Bounty": 8,
                "Heist": 8,
                "Brawl Ball": 7,
                "Hot Zone": 8,
                "Knockout": 7
            },
            "strengths": ["Урон за укрытиями", "Две гранаты", "Высокий потенциал"],
            "weaknesses": ["Низкий ХП", "Требует точности"]
        },
        "Tick": {
            "type": "thrower",
            "difficulty": "low",
            "modes": {
                "Gem Grab": 8,
                "Showdown": 9,
                "Bounty": 8,
                "Heist": 9,
                "Brawl Ball": 6,
                "Hot Zone": 7,
                "Knockout": 7
            },
            "strengths": ["Авто-наведение", "Контроль карты", "Ульта для давления"],
            "weaknesses": ["Очень низкий ХП", "Медленный"]
        }
    }
    
    # Перевод режимов на русский
    MODE_TRANSLATIONS = {
        "gem grab": "Gem Grab",
        "showdown": "Showdown",
        "bounty": "Bounty",
        "heist": "Heist",
        "brawl ball": "Brawl Ball",
        "hot zone": "Hot Zone",
        "knockout": "Knockout",
        "duels": "Duel"
    }
    
    @classmethod
    def get_recommendations_for_mode(cls, mode: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Получить топ бойцов для конкретного режима
        
        Args:
            mode: Название режима игры
            top_n: Количество рекомендуемых бойцов
            
        Returns:
            Список словарей с информацией о бойцах
        """
        mode_lower = mode.lower()
        
        # Нормализация названия режима
        for key, value in cls.MODE_TRANSLATIONS.items():
            if key in mode_lower or value.lower() in mode_lower:
                normalized_mode = key
                break
        else:
            normalized_mode = mode_lower
        
        # Сортировка бойцов по рейтингу для данного режима
        rated_brawlers = []
        for brawler_name, brawler_data in cls.BRAWLERS.items():
            rating = brawler_data["modes"].get(normalized_mode, 5)
            rated_brawlers.append({
                "name": brawler_name,
                "rating": rating,
                "type": brawler_data["type"],
                "difficulty": brawler_data["difficulty"],
                "strengths": brawler_data["strengths"],
                "weaknesses": brawler_data["weaknesses"]
            })
        
        # Сортировка по рейтингу (убывание)
        rated_brawlers.sort(key=lambda x: x["rating"], reverse=True)
        
        return rated_brawlers[:top_n]
    
    @classmethod
    def get_brawler_info(cls, brawler_name: str) -> Dict[str, Any]:
        """Получить полную информацию о бойце"""
        brawler = cls.BRAWLERS.get(brawler_name)
        if not brawler:
            return {"error": f"Боец {brawler_name} не найден"}
        
        return {
            "name": brawler_name,
            "type": brawler["type"],
            "difficulty": brawler["difficulty"],
            "best_modes": sorted(
                [(mode, rating) for mode, rating in brawler["modes"].items()],
                key=lambda x: x[1],
                reverse=True
            )[:3],
            "strengths": brawler["strengths"],
            "weaknesses": brawler["weaknesses"]
        }
    
    @classmethod
    def get_all_modes(cls) -> List[str]:
        """Вернуть список всех поддерживаемых режимов"""
        return list(cls.MODE_TRANSLATIONS.values())
    
    @classmethod
    def get_brawlers_by_type(cls, brawler_type: str) -> List[str]:
        """Вернуть список бойцов определённого типа"""
        return [
            name for name, data in cls.BRAWLERS.items()
            if data["type"] == brawler_type.lower()
        ]


def get_mode_recommendation_text(mode: str) -> str:
    """
    Генерировать текстовые рекомендации для режима
    
    Returns:
        Форматированный текст с рекомендациями
    """
    recommendations = BrawlerRecommendations.get_recommendations_for_mode(mode, top_n=5)
    
    if not recommendations:
        return f"Нет данных для режима '{mode}'"
    
    text = f"\n🎮 РЕКОМЕНДАЦИИ ДЛЯ РЕЖИМА: {mode.upper()}\n"
    text += "=" * 50 + "\n\n"
    
    for i, brawler in enumerate(recommendations, 1):
        stars = "⭐" * brawler["rating"]
        text += f"{i}. {brawler['name']} ({brawler['type']})\n"
        text += f"   Рейтинг: {stars} ({brawler['rating']}/10)\n"
        text += f"   Сложность: {brawler['difficulty']}\n"
        text += f"   Плюсы: {', '.join(brawler['strengths'][:2])}\n"
        if brawler['weaknesses']:
            text += f"   Минусы: {brawler['weaknesses'][0]}\n"
        text += "\n"
    
    # Добавить общие советы для режима
    text += "\n💡 ОБЩИЕ СОВЕТЫ:\n"
    
    mode_lower = mode.lower()
    if "gem grab" in mode_lower:
        text += "- Выбирайте бойцов с контролем и уроном по области\n"
        text += "- Избегайте агрессивных ассасинов без поддержки\n"
        text += "- Приоритет: контроль кристаллов, а не убийства\n"
    elif "brawl ball" in mode_lower:
        text += "- Танки и контролёры очень эффективны\n"
        text += "- Избегайте метателей на открытых картах\n"
        text += "- Важнее забивать голы, чем получать убийства\n"
    elif "showdown" in mode_lower:
        text += "- Ассасины и метатели сильны в соло\n"
        text += "- Избегайте ранних боёв, собирайте кубики сил\n"
        text += "- Используйте укрытия и контролируйте центр\n"
    elif "heist" in mode_lower:
        text += "- Метатели и танки для атаки сейфа\n"
        text += "- Стрелки для защиты от вражеской атаки\n"
        text += "- Координируйте атаку с командой\n"
    elif "bounty" in mode_lower:
        text += "- Стрелки доминируют на открытых картах\n"
        text += "- Сохраняйте звёзды, играйте осторожно\n"
        text += "- Контролируйте центр карты\n"
    else:
        text += "- Адаптируйте выбор бойца под карту\n"
        text += "- Слушайте свою команду\n"
        text += "- Экспериментируйте с разными билдами\n"
    
    return text


# Пример использования
if __name__ == "__main__":
    print(get_mode_recommendation_text("Gem Grab"))
    print("\n" + "="*70 + "\n")
    print(get_mode_recommendation_text("Brawl Ball"))
