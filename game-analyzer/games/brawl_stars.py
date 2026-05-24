"""
Модуль для поддержки игры Brawl Stars
"""
from typing import Dict, List, Any
from games.base_game import BaseGame


class BrawlStarsGame(BaseGame):
    """Реализация для мобильной игры Brawl Stars"""
    
    def __init__(self):
        super().__init__("Brawl Stars")
    
    def get_default_stats(self) -> Dict[str, Any]:
        """Возвращает стандартные метрики для Brawl Stars"""
        return {
            "trophies_earned": 0,  # Получено трофеев за матч
            "brawler_name": "",  # Имя бойца
            "game_mode": "",  # Режим игры (Gem Grab, Showdown, Brawl Ball и т.д.)
            "kills": 0,  # Убийства/нокауты
            "deaths": 0,  # Поражения/смерти
            "damage_dealt": 0,  # Нанесённый урон
            "damage_received": 0,  # Полученный урон
            "healing_done": 0,  # Лечение (для支援ных бойцов)
            "goals_scored": 0,  # Забитые голы (для Brawl Ball)
            "gems_collected": 0,  # Собранные кристаллы (для Gem Grab)
            "placement": 0,  # Место в Showdown
            "is_victory": False,  # Победа или поражение
            "playtime_minutes": 0,  # Длительность матча
            "super_used": 0,  # Использований супер-атаки
            "accuracy": 0.0,  # Точность атак (%)
        }
    
    def create_session(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Создаёт сессию из данных пользователя"""
        session = self.get_default_stats()
        session.update({
            "trophies_earned": data.get("trophy_change", 0),
            "brawler_name": data.get("brawler", ""),
            "game_mode": data.get("mode", ""),
            "kills": data.get("kills", 0),
            "deaths": data.get("deaths", 0),
            "damage_dealt": data.get("damage", 0),
            "healing_done": data.get("healing", 0),
            "super_used": 1 if data.get("super_used", False) else 0,
            "is_victory": data.get("rank", 0) <= 2,
            "placement": data.get("rank", 0),
        })
        return session
    
    def analyze_performance(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Анализирует несколько сессий и возвращает общую статистику"""
        if not sessions:
            return {
                "overall_score": 0,
                "strengths": [],
                "weaknesses": [],
                "recommendations": []
            }
        
        all_strengths = []
        all_weaknesses = []
        all_recommendations = []
        
        total_kills = 0
        total_deaths = 0
        total_trophies = 0
        total_damage = 0
        
        for session in sessions:
            analysis = self.analyze_specific_metrics(session)
            all_strengths.extend(analysis["strengths"])
            all_weaknesses.extend(analysis["weaknesses"])
            all_recommendations.extend(analysis["recommendations"])
            
            total_kills += session.get("kills", 0)
            total_deaths += session.get("deaths", 0)
            total_trophies += session.get("trophies_earned", 0)
            total_damage += session.get("damage_dealt", 0)
        
        # Общая статистика
        avg_kd = total_kills / max(total_deaths, 1)
        avg_trophies = total_trophies / len(sessions)
        
        # Расчет общего рейтинга
        score = 50
        if avg_kd > 2:
            score += 20
        elif avg_kd > 1:
            score += 10
        elif avg_kd < 0.5:
            score -= 15
        
        if avg_trophies > 5:
            score += 15
        elif avg_trophies > 0:
            score += 5
        elif avg_trophies < -5:
            score -= 15
        
        if total_damage / len(sessions) > 3000:
            score += 15
        elif total_damage / len(sessions) > 1500:
            score += 5
        
        score = max(0, min(100, score))
        
        return {
            "overall_score": score,
            "strengths": list(set(all_strengths))[:5],
            "weaknesses": list(set(all_weaknesses))[:5],
            "recommendations": list(set(all_recommendations))[:5]
        }
    
    def analyze_specific_metrics(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Анализирует специфичные метрики Brawl Stars
        
        Returns:
            dict с ключами 'strengths', 'weaknesses', 'recommendations'
        """
        strengths = []
        weaknesses = []
        recommendations = []
        
        # Анализ трофеев
        if "trophies_earned" in stats:
            trophies = stats["trophies_earned"]
            if trophies > 10:
                strengths.append(f"Отличный прирост трофеев: +{trophies}")
            elif trophies < -5:
                weaknesses.append(f"Потеря трофеев: {trophies}")
                recommendations.append("Играйте более осторожно и выбирайте подходящих бойцов")
        
        # Анализ K/D (нокауты/смерти)
        if "kills" in stats and "deaths" in stats:
            kd_ratio = stats["kills"] / max(stats["deaths"], 1)
            if kd_ratio > 2.0:
                strengths.append(f"Превосходный K/D: {kd_ratio:.2f}")
            elif kd_ratio > 1.0:
                strengths.append(f"Хороший K/D: {kd_ratio:.2f}")
            elif kd_ratio < 0.5:
                weaknesses.append(f"Низкий K/D: {kd_ratio:.2f}")
                recommendations.append("Избегайте необоснованных столкновений, играйте от команды")
        
        # Анализ урона
        if "damage_dealt" in stats:
            damage = stats["damage_dealt"]
            if damage > 5000:
                strengths.append(f"Высокий урон: {damage}")
            elif damage < 1000 and stats.get("deaths", 0) > 0:
                weaknesses.append(f"Малый урон: {damage}")
                recommendations.append("Стремитесь наносить больше урона перед смертью")
        
        # Анализ выживаемости
        if "damage_received" in stats and "deaths" in stats:
            if stats["deaths"] == 0 and stats["damage_received"] > 2000:
                strengths.append("Отличная выживаемость без смертей")
            elif stats["deaths"] > 2:
                weaknesses.append("Частые смерти, улучшите позиционирование")
                recommendations.append("Используйте укрытия и не выходите на открытую местность")
        
        # Специфичный анализ для режимов
        game_mode = stats.get("game_mode", "").lower()
        
        if "brawl ball" in game_mode:
            if stats.get("goals_scored", 0) > 2:
                strengths.append(f"Хорошая игра в нападении: {stats['goals_scored']} голов")
            elif stats.get("goals_scored", 0) == 0 and stats.get("kills", 0) > 3:
                recommendations.append("Чаще забивайте голы вместо погони за убийствами")
        
        if "gem grab" in game_mode:
            gems = stats.get("gems_collected", 0)
            if gems > 10:
                strengths.append(f"Активный сбор кристаллов: {gems}")
            elif gems == 0 and stats.get("is_victory", False):
                recommendations.append("Помогайте носителю кристаллов или станьте носителем")
        
        if "showdown" in game_mode:
            placement = stats.get("placement", 0)
            if placement <= 3:
                strengths.append(f"Отличное место в шоу-дауне: #{placement}")
            elif placement > 5:
                weaknesses.append(f"Низкое место в шоу-дауне: #{placement}")
                recommendations.append("В шоу-дауне избегайте ранних боёв, собирайте кубики сил")
        
        # Анализ лечения (для支援ных бойцов)
        if stats.get("healing_done", 0) > 3000:
            strengths.append(f"Отличная поддержка команды: {stats['healing_done']} лечения")
        
        # Анализ использования супер-атаки
        if stats.get("super_used", 0) > 3:
            strengths.append("Эффективное использование супер-атаки")
        elif stats.get("super_used", 0) == 0 and stats.get("playtime_minutes", 0) > 2:
            weaknesses.append("Супер-атака не использовалась")
            recommendations.append("Копите супер для важных моментов: командных боёв или захвата объектов")
        
        # Анализ точности
        if "accuracy" in stats:
            accuracy = stats["accuracy"]
            if accuracy > 70:
                strengths.append(f"Высокая точность атак: {accuracy}%")
            elif accuracy < 40:
                weaknesses.append(f"Низкая точность: {accuracy}%")
                recommendations.append("Тренируйтесь в режиме тренировки, изучите траекторию атак вашего бойца")
        
        # Общий результат матча
        if stats.get("is_victory", False):
            strengths.append("Победа в матче! 🏆")
        else:
            if stats.get("trophies_earned", 0) >= 0:
                strengths.append("Трофеи сохранены несмотря на поражение")
            else:
                recommendations.append("Проанализируйте ошибку и попробуйте другого бойца")
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations
        }


def get_brawl_stars_handler() -> BrawlStarsGame:
    """Фабричная функция для получения обработника Brawl Stars"""
    return BrawlStarsGame()
