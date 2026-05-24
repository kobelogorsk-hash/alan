# Game Progress Analyzer

Программа для анализа прогресса в играх, выявления плюсов и минусов игровой производительности.

## Возможности

- 📊 Отслеживание статистики по разным играм
- 📈 Анализ прогресса во времени
- ✅ Выявление сильных сторон
- ❌ Определение слабых мест
- 🎯 Рекомендации по улучшению

## Структура проекта

```
game-analyzer/
├── main.py              # Точка входа
├── core/
│   ├── __init__.py
│   ├── analyzer.py      # Логика анализа
│   └── models.py        # Модели данных
├── games/
│   ├── __init__.py
│   └── base_game.py     # Базовый класс для игр
├── data/
│   └── stats.json       # Хранение статистики
└── requirements.txt
```

## Установка

```bash
pip install -r requirements.txt
python game-analyzer/main.py
```

## Пример использования

```python
from core.analyzer import GameAnalyzer

analyzer = GameAnalyzer()
analyzer.add_game_session("CS:GO", kills=15, deaths=10, assists=5)
analyzer.analyze_performance("CS:GO")
```
