"""
Модели данных для анализатора игрового прогресса
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any


@dataclass
class GameSession:
    """Представляет одну игровую сессию"""
    game_name: str
    timestamp: datetime
    stats: Dict[str, Any]
    
    def to_dict(self) -> dict:
        return {
            "game_name": self.game_name,
            "timestamp": self.timestamp.isoformat(),
            "stats": self.stats
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "GameSession":
        return cls(
            game_name=data["game_name"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            stats=data["stats"]
        )


@dataclass
class GameStats:
    """Агрегированная статистика по игре"""
    game_name: str
    total_sessions: int = 0
    total_playtime: float = 0.0  # в часах
    sessions: List[GameSession] = field(default_factory=list)
    
    # Динамические метрики
    avg_stats: Dict[str, float] = field(default_factory=dict)
    trend: str = "stable"  # improving, declining, stable
    
    def add_session(self, session: GameSession):
        self.sessions.append(session)
        self.total_sessions += 1
        self._recalculate_metrics()
    
    def _recalculate_metrics(self):
        """Пересчитывает средние значения и тренды"""
        if not self.sessions:
            return
        
        # Собираем все ключи статистики
        all_keys = set()
        for session in self.sessions:
            all_keys.update(session.stats.keys())
        
        # Вычисляем средние значения
        for key in all_keys:
            values = [s.stats.get(key, 0) for s in self.sessions if key in s.stats and isinstance(s.stats.get(key), (int, float))]
            if values:
                self.avg_stats[key] = sum(values) / len(values)
        
        # Определяем тренд (упрощённо)
        if len(self.sessions) >= 2:
            recent_avg = sum(self.sessions[-1].stats.values()) / max(len(self.sessions[-1].stats), 1)
            older_avg = sum(self.sessions[0].stats.values()) / max(len(self.sessions[0].stats), 1)
            
            if recent_avg > older_avg * 1.1:
                self.trend = "improving"
            elif recent_avg < older_avg * 0.9:
                self.trend = "declining"
            else:
                self.trend = "stable"
    
    def to_dict(self) -> dict:
        return {
            "game_name": self.game_name,
            "total_sessions": self.total_sessions,
            "total_playtime": self.total_playtime,
            "avg_stats": self.avg_stats,
            "trend": self.trend,
            "sessions": [s.to_dict() for s in self.sessions]
        }


@dataclass
class PerformanceAnalysis:
    """Результат анализа производительности"""
    game_name: str
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    overall_score: float = 0.0  # 0-100
    
    def to_dict(self) -> dict:
        return {
            "game_name": self.game_name,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "recommendations": self.recommendations,
            "overall_score": self.overall_score
        }
