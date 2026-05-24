"""
Главный файл программы - Game Progress Analyzer
"""
import sys
from pathlib import Path

# Добавляем корневую директорию в path для импортов
sys.path.insert(0, str(Path(__file__).parent))

from core.analyzer import GameAnalyzer


def print_welcome():
    """Выводит приветственное сообщение"""
    print("\n" + "="*60)
    print("🎮 GAME PROGRESS ANALYZER 🎮")
    print("="*60)
    print("Программа для анализа вашего прогресса в играх")
    print("="*60 + "\n")


def print_menu():
    """Выводит меню программы"""
    print("\n📋 МЕНЮ:")
    print("1. Добавить игровую сессию")
    print("2. Проанализировать производительность")
    print("3. Показать все игры")
    print("4. Показать статистику по игре")
    print("5. Выход")
    print()


def add_session_menu(analyzer: GameAnalyzer):
    """Меню добавления сессии"""
    print("\n➕ ДОБАВЛЕНИЕ ИГРОВОЙ СЕССИИ")
    print("-" * 40)
    
    game_name = input("Название игры: ").strip()
    if not game_name:
        print("❌ Название игры не может быть пустым")
        return
    
    print("\nВведите статистику (оставьте пустым, если не применимо):")
    
    stats = {}
    
    # Универсальные поля для шутеров
    print("\n--- Основные метрики ---")
    kills = input("Kills (убийства): ").strip()
    if kills:
        stats["kills"] = int(kills)
    
    deaths = input("Deaths (смерти): ").strip()
    if deaths:
        stats["deaths"] = int(deaths)
    
    assists = input("Assists (помощь): ").strip()
    if assists:
        stats["assists"] = int(assists)
    
    score = input("Score (очки): ").strip()
    if score:
        stats["score"] = int(score)
    
    accuracy = input("Accuracy % (точность): ").strip()
    if accuracy:
        stats["accuracy"] = float(accuracy)
    
    headshots = input("Headshots (хедшоты): ").strip()
    if headshots:
        stats["headshots"] = int(headshots)
    
    playtime = input("Playtime (минуты): ").strip()
    if playtime:
        stats["playtime_minutes"] = int(playtime)
    
    # Для MOBA
    print("\n--- MOBA метрики (если применимо) ---")
    last_hits = input("Last Hits: ").strip()
    if last_hits:
        stats["last_hits"] = int(last_hits)
    
    gpm = input("GPM (gold per minute): ").strip()
    if gpm:
        stats["gpm"] = int(gpm)
    
    # Для Battle Royale
    print("\n--- Battle Royale метрики (если применимо) ---")
    placement = input("Team Placement (место команды): ").strip()
    if placement:
        stats["team_placement"] = int(placement)
    
    damage = input("Damage Dealt (нанесён урон): ").strip()
    if damage:
        stats["damage_dealt"] = int(damage)
    
    analyzer.add_game_session(game_name, **stats)


def analyze_menu(analyzer: GameAnalyzer):
    """Меню анализа"""
    print("\n📊 АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("-" * 40)
    
    game_name = input("Название игры для анализа: ").strip()
    if not game_name:
        print("❌ Название игры не может быть пустым")
        return
    
    analyzer.print_analysis(game_name)


def show_all_games(analyzer: GameAnalyzer):
    """Показывает все отслеживаемые игры"""
    print("\n🎮 ВСЕ ИГРЫ:")
    print("-" * 40)
    
    games = analyzer.get_all_games()
    
    if not games:
        print("Пока нет сохранённых игр")
        return
    
    for i, game in enumerate(games, 1):
        stats = analyzer.get_game_stats(game)
        print(f"{i}. {game}")
        print(f"   Сессий: {stats.total_sessions}")
        print(f"   Тренд: {stats.trend}")
        if stats.avg_stats:
            print(f"   Средний K/D: {stats.avg_stats.get('kills', 0) / max(stats.avg_stats.get('deaths', 1), 1):.2f}")
        print()


def show_game_stats(analyzer: GameAnalyzer):
    """Показывает детальную статистику по игре"""
    print("\n📈 СТАТИСТИКА ПО ИГРЕ")
    print("-" * 40)
    
    game_name = input("Название игры: ").strip()
    if not game_name:
        print("❌ Название игры не может быть пустым")
        return
    
    stats = analyzer.get_game_stats(game_name)
    
    if not stats:
        print(f"❌ Игра '{game_name}' не найдена")
        return
    
    print(f"\n🎮 {stats.game_name}")
    print(f"   Всего сессий: {stats.total_sessions}")
    print(f"   Общее время: {stats.total_playtime:.1f} ч.")
    print(f"   Тренд: {stats.trend}")
    
    if stats.avg_stats:
        print("\n   Средние значения:")
        for key, value in stats.avg_stats.items():
            print(f"   • {key}: {value:.2f}" if isinstance(value, float) else f"   • {key}: {value}")
    
    print(f"\n   Последние {min(5, len(stats.sessions))} сессий:")
    for i, session in enumerate(stats.sessions[-5:], 1):
        print(f"   {i}. {session.timestamp.strftime('%d.%m.%Y %H:%M')}")
        for k, v in session.stats.items():
            print(f"      {k}: {v}")


def main():
    """Основная функция"""
    print_welcome()
    
    analyzer = GameAnalyzer()
    
    while True:
        print_menu()
        choice = input("Выберите пункт меню (1-5): ").strip()
        
        if choice == "1":
            add_session_menu(analyzer)
        elif choice == "2":
            analyze_menu(analyzer)
        elif choice == "3":
            show_all_games(analyzer)
        elif choice == "4":
            show_game_stats(analyzer)
        elif choice == "5":
            print("\n👋 Спасибо за использование Game Progress Analyzer!")
            print("Удачи в играх! 🎮\n")
            break
        else:
            print("\n❌ Неверный выбор, попробуйте снова")


if __name__ == "__main__":
    main()
