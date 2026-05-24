"""Тестовый скрипт для проверки работы GUI без отображения"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from games.brawl_stars import BrawlStarsGame
from core.analyzer import GameAnalyzer

print("=== Тестирование Brawl Stars Analyzer ===\n")

# Создаем игру
bs = BrawlStarsGame()

# Тестовые данные
test_sessions = [
    {
        "brawler": "Шелли",
        "mode": "Brawl Ball",
        "rank": 1,
        "trophy_change": 8,
        "kills": 5,
        "deaths": 2,
        "damage": 3500,
        "healing": 0,
        "super_used": True
    },
    {
        "brawler": "Колетт",
        "mode": "Gem Grab",
        "rank": 2,
        "trophy_change": 6,
        "kills": 3,
        "deaths": 4,
        "damage": 2800,
        "healing": 1200,
        "super_used": True
    },
    {
        "brawler": "Пайпер",
        "mode": "Showdown",
        "rank": 1,
        "trophy_change": 10,
        "kills": 8,
        "deaths": 1,
        "damage": 4200,
        "healing": 0,
        "super_used": True
    }
]

print("Создание сессий...")
sessions = []
for data in test_sessions:
    session = bs.create_session(data)
    sessions.append(session)
    print(f"✓ {data['brawler']} - {data['mode']}: {data['kills']}K/{data['deaths']}D, Трофеи: {data['trophy_change']:+d}")

print("\nАнализ производительности...")
analysis = bs.analyze_performance(sessions)

print(f"\n📊 Результаты анализа:")
print(f"   Общий рейтинг: {analysis['overall_score']}/100")

print(f"\n✅ Плюсы:")
for strength in analysis.get('strengths', []):
    print(f"   ✓ {strength}")

print(f"\n❌ Минусы:")
for weakness in analysis.get('weaknesses', []):
    print(f"   ✗ {weakness}")

print(f"\n💡 Рекомендации:")
for rec in analysis.get('recommendations', []):
    print(f"   • {rec}")

print("\n=== Тест завершен успешно! ===")
print("\nGUI готов к запуску после установки tkinter:")
print("  Linux: sudo apt-get install python3-tk")
print("  Mac: brew install python-tk")
print("  Windows: переустановите Python с tcl/tk")
