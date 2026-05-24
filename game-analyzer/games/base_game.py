"""
Базовый класс для поддержки различных игр
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any


class BaseGame(ABC):
    """Базовый класс для реализации поддержки конкретных игр"""
    
    def __init__(self, game_name: str):
        self.game_name = game_name
    
    @abstractmethod
    def get_default_stats(self) -> Dict[str, Any]:
        """Возвращает стандартные метрики для этой игры"""
        pass
    
    @abstractmethod
    def analyze_specific_metrics(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Анализирует специфичные для игры метрики
        
        Returns:
            dict с ключами 'strengths', 'weaknesses', 'recommendations'
        """
        pass
    
    def validate_stats(self, stats: Dict[str, Any]) -> bool:
        """Проверяет корректность переданной статистики"""
        default_stats = self.get_default_stats()
        for key in default_stats:
            if key not in stats:
                return False
        return True


class FPSGame(BaseGame):
    """Реализация для FPS игр (CS:GO, Valorant, Apex и т.д.)"""
    
    def __init__(self):
        super().__init__("FPS")
    
    def get_default_stats(self) -> Dict[str, Any]:
        return {
            "kills": 0,
            "deaths": 0,
            "assists": 0,
            "score": 0,
            "accuracy": 0.0,
            "headshots": 0,
            "playtime_minutes": 0
        }
    
    def analyze_specific_metrics(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        strengths = []
        weaknesses = []
        recommendations = []
        
        # Анализ headshot percentage
        if "headshots" in stats and "kills" in stats and stats["kills"] > 0:
            hs_percentage = (stats["headshots"] / stats["kills"]) * 100
            if hs_percentage > 50:
                strengths.append(f"Отличный процент хедшотов: {hs_percentage:.1f}%")
            elif hs_percentage < 20:
                weaknesses.append(f"Низкий процент хедшотов: {hs_percentage:.1f}%")
                recommendations.append("Тренируйте прицеливание на уровне головы")
        
        # Анализ точности
        if "accuracy" in stats:
            if stats["accuracy"] > 60:
                strengths.append(f"Высокая точность: {stats['accuracy']}%")
            elif stats["accuracy"] < 30:
                weaknesses.append(f"Низкая точность: {stats['accuracy']}%")
                recommendations.append("Используйте тренировочные карты для улучшения аима")
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations
        }


class MOBAGame(BaseGame):
    """Реализация для MOBA игр (Dota 2, LoL)"""
    
    def __init__(self):
        super().__init__("MOBA")
    
    def get_default_stats(self) -> Dict[str, Any]:
        return {
            "kills": 0,
            "deaths": 0,
            "assists": 0,
            "last_hits": 0,
            "denies": 0,
            "gpm": 0,  # gold per minute
            "xpm": 0,  # experience per minute
            "playtime_minutes": 0
        }
    
    def analyze_specific_metrics(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        strengths = []
        weaknesses = []
        recommendations = []
        
        # Анализ KDA
        if all(k in stats for k in ["kills", "deaths", "assists"]):
            kda = (stats["kills"] + stats["assists"]) / max(stats["deaths"], 1)
            if kda > 3:
                strengths.append(f"Отличный KDA: {kda:.2f}")
            elif kda < 1.5:
                weaknesses.append(f"Низкий KDA: {kda:.2f}")
                recommendations.append("Избегайте необоснованных смертей")
        
        # Анализ фармa (last hits)
        if "last_hits" in stats:
            lh_per_min = stats["last_hits"] / max(stats["playtime_minutes"], 1)
            if lh_per_min > 8:
                strengths.append(f"Хороший фарм: {lh_per_min:.1f} LH/мин")
            elif lh_per_min < 4:
                weaknesses.append(f"Слабый фарм: {lh_per_min:.1f} LH/мин")
                recommendations.append("Улучшайте ластхитинг на крипах")
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations
        }


class BattleRoyaleGame(BaseGame):
    """Реализация для Battle Royale игр (PUBG, Fortnite, Apex Legends)"""
    
    def __init__(self):
        super().__init__("Battle Royale")
    
    def get_default_stats(self) -> Dict[str, Any]:
        return {
            "kills": 0,
            "deaths": 0,
            "damage_dealt": 0,
            "placement": 0,
            "team_placement": 0,
            "survival_time": 0,
            "playtime_minutes": 0
        }
    
    def analyze_specific_metrics(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        strengths = []
        weaknesses = []
        recommendations = []
        
        # Анализ placement
        if "team_placement" in stats:
            if stats["team_placement"] <= 3:
                strengths.append(f"Отличное место: #{stats['team_placement']}")
            elif stats["team_placement"] > 50:
                weaknesses.append(f"Низкое место: #{stats['team_placement']}")
                recommendations.append("Улучшайте позиционирование в зоне")
        
        # Анализ урона
        if "damage_dealt" in stats:
            if stats["damage_dealt"] > 1000:
                strengths.append(f"Высокий урон: {stats['damage_dealt']}")
            elif stats["damage_dealt"] < 200:
                weaknesses.append(f"Малый урон: {stats['damage_dealt']}")
                recommendations.append("Ищите больше конфликтов для практики боя")
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations
        }


def get_game_handler(game_type: str) -> BaseGame:
    """Фабричная функция для получения обработника игры"""
    # Импортируем внутри функции чтобы избежать циклического импорта
    from games.brawl_stars import BrawlStarsGame
    
    handlers = {
        "fps": FPSGame,
        "moba": MOBAGame,
        "battle_royale": BattleRoyaleGame,
        "brawl_stars": BrawlStarsGame
    }
    
    handler_class = handlers.get(game_type.lower(), BaseGame)
    return handler_class()
