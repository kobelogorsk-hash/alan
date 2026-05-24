"""
Анализатор игровой производительности
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from .models import GameSession, GameStats, PerformanceAnalysis


class GameAnalyzer:
    """Основной класс для анализа игрового прогресса"""
    
    def __init__(self, data_file: str = "data/stats.json"):
        self.data_file = Path(data_file)
        self.games: Dict[str, GameStats] = {}
        self._load_data()
    
    def _load_data(self):
        """Загружает данные из файла"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for game_name, game_data in data.get("games", {}).items():
                    stats = GameStats(
                        game_name=game_name,
                        total_sessions=game_data.get("total_sessions", 0),
                        total_playtime=game_data.get("total_playtime", 0.0),
                        avg_stats=game_data.get("avg_stats", {}),
                        trend=game_data.get("trend", "stable")
                    )
                    for session_data in game_data.get("sessions", []):
                        session = GameSession.from_dict(session_data)
                        stats.sessions.append(session)
                    self.games[game_name] = stats
    
    def _save_data(self):
        """Сохраняет данные в файл"""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "games": {name: stats.to_dict() for name, stats in self.games.items()}
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_game_session(self, game_name: str, **stats):
        """
        Добавляет новую игровую сессию
        
        Args:
            game_name: Название игры
            **stats: Статистика сессии (kills, deaths, assists, score и т.д.)
        """
        session = GameSession(
            game_name=game_name,
            timestamp=datetime.now(),
            stats=stats
        )
        
        if game_name not in self.games:
            self.games[game_name] = GameStats(game_name=game_name)
        
        self.games[game_name].add_session(session)
        self._save_data()
        print(f"✅ Сессия для '{game_name}' добавлена!")
    
    def analyze_performance(self, game_name: str) -> Optional[PerformanceAnalysis]:
        """
        Анализирует производительность в игре
        
        Args:
            game_name: Название игры
            
        Returns:
            PerformanceAnalysis или None если игра не найдена
        """
        if game_name not in self.games:
            print(f"❌ Игра '{game_name}' не найдена")
            return None
        
        game_stats = self.games[game_name]
        analysis = PerformanceAnalysis(game_name=game_name)
        
        # Анализ сильных и слабых сторон
        strengths, weaknesses = self._analyze_strengths_weaknesses(game_stats)
        analysis.strengths = strengths
        analysis.weaknesses = weaknesses
        
        # Генерация рекомендаций
        analysis.recommendations = self._generate_recommendations(game_stats, weaknesses)
        
        # Расчёт общего scores
        analysis.overall_score = self._calculate_overall_score(game_stats)
        
        return analysis
    
    def _analyze_strengths_weaknesses(self, game_stats: GameStats) -> tuple:
        """Анализирует сильные и слабые стороны"""
        strengths = []
        weaknesses = []
        
        if not game_stats.avg_stats:
            return strengths, weaknesses
        
        # Пример анализа для шутеров (K/D ratio)
        if "kills" in game_stats.avg_stats and "deaths" in game_stats.avg_stats:
            kd_ratio = game_stats.avg_stats["kills"] / max(game_stats.avg_stats["deaths"], 1)
            
            if kd_ratio > 1.5:
                strengths.append(f"Отличный K/D рейтинг: {kd_ratio:.2f}")
            elif kd_ratio > 1.0:
                strengths.append(f"Хороший K/D рейтинг: {kd_ratio:.2f}")
            elif kd_ratio > 0.7:
                weaknesses.append(f"Средний K/D рейтинг: {kd_ratio:.2f}, можно улучшить")
            else:
                weaknesses.append(f"Низкий K/D рейтинг: {kd_ratio:.2f}, нужно работать над выживаемостью")
        
        # Анализ助攻 (assists)
        if "assists" in game_stats.avg_stats:
            avg_assists = game_stats.avg_stats["assists"]
            if avg_assists > 5:
                strengths.append(f"Хорошая командная игра (среднее количество ассистов: {avg_assists:.1f})")
            elif avg_assists < 2:
                weaknesses.append("Мало ассистов, попробуйте больше помогать команде")
        
        # Анализ точности (accuracy)
        if "accuracy" in game_stats.avg_stats:
            accuracy = game_stats.avg_stats["accuracy"]
            if accuracy > 60:
                strengths.append(f"Высокая точность стрельбы: {accuracy}%")
            elif accuracy < 30:
                weaknesses.append(f"Низкая точность стрельбы: {accuracy}%, тренируйте аим")
        
        # Тренд прогресса
        if game_stats.trend == "improving":
            strengths.append("Наблюдается положительная динамика прогресса 📈")
        elif game_stats.trend == "declining":
            weaknesses.append("Прогресс снижается, стоит пересмотреть подход к игре 📉")
        else:
            strengths.append("Стабильные результаты")
        
        # Количество сессий
        if game_stats.total_sessions >= 10:
            strengths.append(f"Опытный игрок ({game_stats.total_sessions} сессий)")
        elif game_stats.total_sessions < 3:
            weaknesses.append("Мало статистики для полноценного анализа")
        
        return strengths, weaknesses
    
    def _generate_recommendations(self, game_stats: GameStats, weaknesses: List[str]) -> List[str]:
        """Генерирует рекомендации на основе слабых сторон"""
        recommendations = []
        
        weakness_text = " ".join(weaknesses).lower()
        
        if "k/d" in weakness_text or "выживаемость" in weakness_text:
            recommendations.append("💡 Совет: Изучите карты, чтобы лучше понимать позиции для укрытий")
            recommendations.append("💡 Совет: Тренируйте позиционирование и не лезьте вперёд без поддержки")
        
        if "ассистов" in weakness_text or "командная" in weakness_text:
            recommendations.append("💡 Совет: Больше взаимодействуйте с командой, используйте голосовой чат")
        
        if "точность" in weakness_text or "аим" in weakness_text:
            recommendations.append("💡 Совет: Используйте тренировочные режимы для улучшения аима")
            recommendations.append("💡 Совет: Попробуйте уменьшить чувствительность мыши для лучшей точности")
        
        if "динамика" in weakness_text or "снижается" in weakness_text:
            recommendations.append("💡 Совет: Сделайте перерыв, избегайте тильта")
            recommendations.append("💡 Совет: Проанализируйте записи своих игр (реплеи)")
        
        if not recommendations:
            recommendations.append("🎯 Продолжайте в том же духе!")
            recommendations.append("🎯 Попробуйте новые тактики для разнообразия")
        
        return recommendations
    
    def _calculate_overall_score(self, game_stats: GameStats) -> float:
        """Рассчитывает общий score производительности (0-100)"""
        if not game_stats.avg_stats:
            return 0.0
        
        score = 50.0  # Базовый score
        
        # Бонус за K/D ratio
        if "kills" in game_stats.avg_stats and "deaths" in game_stats.avg_stats:
            kd_ratio = game_stats.avg_stats["kills"] / max(game_stats.avg_stats["deaths"], 1)
            if kd_ratio > 2.0:
                score += 20
            elif kd_ratio > 1.5:
                score += 15
            elif kd_ratio > 1.0:
                score += 10
            elif kd_ratio > 0.7:
                score += 5
            else:
                score -= 10
        
        # Бонус за тренд
        if game_stats.trend == "improving":
            score += 15
        elif game_stats.trend == "declining":
            score -= 10
        
        # Бонус за опыт
        if game_stats.total_sessions >= 20:
            score += 10
        elif game_stats.total_sessions >= 10:
            score += 5
        
        # Ограничиваем range 0-100
        return max(0.0, min(100.0, score))
    
    def get_all_games(self) -> List[str]:
        """Возвращает список всех отслеживаемых игр"""
        return list(self.games.keys())
    
    def get_game_stats(self, game_name: str) -> Optional[GameStats]:
        """Возвращает статистику по конкретной игре"""
        return self.games.get(game_name)
    
    def print_analysis(self, game_name: str):
        """Выводит красивый анализ в консоль"""
        analysis = self.analyze_performance(game_name)
        if not analysis:
            return
        
        print("\n" + "="*60)
        print(f"🎮 АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ: {analysis.game_name}")
        print("="*60)
        
        print(f"\n📊 Общий score: {analysis.overall_score:.1f}/100")
        
        if analysis.strengths:
            print("\n✅ СИЛЬНЫЕ СТОРОНЫ:")
            for strength in analysis.strengths:
                print(f"   • {strength}")
        
        if analysis.weaknesses:
            print("\n❌ СЛАБЫЕ СТОРОНЫ:")
            for weakness in analysis.weaknesses:
                print(f"   • {weakness}")
        
        if analysis.recommendations:
            print("\n💡 РЕКОМЕНДАЦИИ:")
            for rec in analysis.recommendations:
                print(f"   {rec}")
        
        print("\n" + "="*60)
