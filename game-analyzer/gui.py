"""
GUI интерфейс для Game Progress Analyzer с поддержкой Brawl Stars
Использует CustomTkinter для современного внешнего вида
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import json
import os
from typing import List, Dict, Any

# Импорт логики анализа
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.analyzer import GameAnalyzer
from core.models import GameSession
from games.brawl_stars import BrawlStarsGame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GameSessionFrame(ctk.CTkFrame):
    """Фрейм для добавления игровой сессии"""
    
    def __init__(self, parent, add_callback):
        super().__init__(parent)
        self.add_callback = add_callback
        
        # Заголовок
        title = ctk.CTkLabel(self, text="Добавить игровую сессию", 
                            font=ctk.CTkFont(size=20, weight="bold"))
        title.grid(row=0, column=0, columnspan=3, pady=20)
        
        # Выбор игры
        ctk.CTkLabel(self, text="Игра:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.game_var = ctk.StringVar(value="Brawl Stars")
        self.game_combo = ctk.CTkComboBox(self, values=["Brawl Stars", "CS:GO", "Dota 2", "PUBG"],
                                         variable=self.game_var, command=self.on_game_change)
        self.game_combo.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # Дата и время
        ctk.CTkLabel(self, text="Дата:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.date_entry = ctk.CTkEntry(self, placeholder_text="YYYY-MM-DD")
        self.date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Поля для Brawl Stars
        self.bs_fields = {}
        self.create_bs_fields()
        
        # Кнопка добавления
        add_btn = ctk.CTkButton(self, text="Добавить сессию", command=self.add_session,
                               fg_color="green", hover_color="darkgreen")
        add_btn.grid(row=15, column=0, columnspan=3, pady=20)
        
        self.columnconfigure(1, weight=1)
    
    def create_bs_fields(self):
        """Создание полей для Brawl Stars"""
        fields = [
            ("Боец:", "brawler"),
            ("Режим:", "mode"),
            ("Место:", "rank"),
            ("Трофеи+", "trophy_change"),
            ("Убийства:", "kills"),
            ("Смерти:", "deaths"),
            ("Урон:", "damage"),
            ("Лечение:", "healing"),
            ("Супер использован:", "super_used"),
        ]
        
        for i, (label, key) in enumerate(fields):
            row = i + 3
            ctk.CTkLabel(self, text=label).grid(row=row, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(self, placeholder_text="0")
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            self.bs_fields[key] = entry
    
    def on_game_change(self, game):
        """Обработка смены игры"""
        # В будущем можно добавлять поля для других игр
        pass
    
    def add_session(self):
        """Добавление сессии"""
        try:
            session_data = {
                "game": self.game_var.get(),
                "date": self.date_entry.get(),
                "brawler": self.bs_fields["brawler"].get(),
                "mode": self.bs_fields["mode"].get(),
                "rank": int(self.bs_fields["rank"].get() or 0),
                "trophy_change": int(self.bs_fields["trophy_change"].get() or 0),
                "kills": int(self.bs_fields["kills"].get() or 0),
                "deaths": int(self.bs_fields["deaths"].get() or 0),
                "damage": int(self.bs_fields["damage"].get() or 0),
                "healing": int(self.bs_fields["healing"].get() or 0),
                "super_used": self.bs_fields["super_used"].get().lower() in ["да", "yes", "1", "true"],
            }
            
            self.add_callback(session_data)
            messagebox.showinfo("Успех", "Сессия добавлена!")
            
            # Очистка полей
            for key, entry in self.bs_fields.items():
                if key != "brawler" and key != "mode":
                    entry.delete(0, 'end')
                    if key in ["kills", "deaths", "damage", "healing"]:
                        entry.insert(0, "0")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неверные данные: {str(e)}")


class StatsFrame(ctk.CTkFrame):
    """Фрейм для отображения статистики"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        title = ctk.CTkLabel(self, text="Статистика и Анализ", 
                            font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        # Контейнер для графиков
        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Текстовая статистика
        self.stats_text = ctk.CTkTextbox(self, height=150)
        self.stats_text.pack(fill="x", padx=20, pady=10)
        
        # Плюсы и минусы
        self.analysis_frame = ctk.CTkFrame(self)
        self.analysis_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(self.analysis_frame, text="Плюсы:", 
                    font=ctk.CTkFont(weight="bold"), 
                    text_color="green").pack(anchor="w", padx=10)
        self.pros_text = ctk.CTkTextbox(self.analysis_frame, height=80, fg_color="#004400")
        self.pros_text.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(self.analysis_frame, text="Минусы:", 
                    font=ctk.CTkFont(weight="bold"), 
                    text_color="red").pack(anchor="w", padx=10)
        self.cons_text = ctk.CTkTextbox(self.analysis_frame, height=80, fg_color="#440000")
        self.cons_text.pack(fill="x", padx=10, pady=5)
        
        self.current_fig = None
    
    def update_stats(self, sessions: List[Dict], analysis: Dict):
        """Обновление статистики"""
        # Очистка предыдущего графика
        if self.current_fig:
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
        
        if len(sessions) > 0:
            # Создание графика трофеев
            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor('#2b2b2b')
            ax.set_facecolor('#2b2b2b')
            
            trophy_changes = [s.get('trophy_change', 0) for s in sessions]
            cumulative = []
            total = 0
            for change in trophy_changes:
                total += change
                cumulative.append(total)
            
            ax.plot(range(len(cumulative)), cumulative, marker='o', color='#1E90FF', linewidth=2)
            ax.set_title('Прогресс трофеев', color='white', fontsize=14)
            ax.set_xlabel('Сессии', color='white')
            ax.set_ylabel('Трофеи', color='white')
            ax.tick_params(colors='white')
            ax.grid(True, alpha=0.3)
            
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            self.current_fig = fig
        
        # Обновление текстовой статистики
        total_games = len(sessions)
        avg_kills = sum(s.get('kills', 0) for s in sessions) / max(total_games, 1)
        avg_deaths = sum(s.get('deaths', 0) for s in sessions) / max(total_games, 1)
        kd_ratio = avg_kills / max(avg_deaths, 0.1)
        total_trophies = sum(s.get('trophy_change', 0) for s in sessions)
        
        stats = f"""
📊 Общая статистика:
• Игр сыграно: {total_games}
• Средние убийства: {avg_kills:.1f}
• Средние смерти: {avg_deaths:.1f}
• K/D Ratio: {kd_ratio:.2f}
• Всего трофеев: {'+' if total_trophies >= 0 else ''}{total_trophies}
• Общий рейтинг: {analysis.get('overall_score', 0)}/100
"""
        self.stats_text.delete("1.0", "end")
        self.stats_text.insert("1.0", stats)
        
        # Обновление плюсов и минусов
        pros = analysis.get('strengths', [])
        cons = analysis.get('weaknesses', [])
        
        self.pros_text.delete("1.0", "end")
        self.cons_text.delete("1.0", "end")
        
        if pros:
            self.pros_text.insert("1.0", "\n".join(f"✓ {p}" for p in pros))
        else:
            self.pros_text.insert("1.0", "Нет данных для анализа")
        
        if cons:
            self.cons_text.insert("1.0", "\n".join(f"✗ {c}" for c in cons))
        else:
            self.cons_text.insert("1.0", "Нет данных для анализа")


class HistoryFrame(ctk.CTkFrame):
    """Фрейм для истории игр"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        title = ctk.CTkLabel(self, text="История игр", 
                            font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        # Таблица
        columns = ("date", "brawler", "mode", "rank", "trophies", "k/d")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        
        for col in columns:
            headers = {"date": "Дата", "brawler": "Боец", "mode": "Режим", 
                      "rank": "Место", "trophies": "Трофеи", "k/d": "K/D"}
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Кнопка удаления
        del_btn = ctk.CTkButton(self, text="Удалить выбранное", command=self.delete_selected,
                               fg_color="red", hover_color="darkred")
        del_btn.pack(pady=10)
        
        self.sessions = []
    
    def update_history(self, sessions: List[Dict]):
        """Обновление истории"""
        # Очистка
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.sessions = sessions
        
        # Добавление записей
        for session in reversed(sessions[-20:]):  # Последние 20
            kd = session.get('kills', 0) / max(session.get('deaths', 1), 1)
            self.tree.insert("", "end", values=(
                session.get('date', 'N/A'),
                session.get('brawler', 'N/A'),
                session.get('mode', 'N/A'),
                session.get('rank', 0),
                f"{session.get('trophy_change', 0):+d}",
                f"{kd:.2f}"
            ))
    
    def delete_selected(self):
        """Удаление выбранной записи"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            date = item['values'][0]
            brawler = item['values'][1]
            
            self.sessions = [s for s in self.sessions 
                           if not (s.get('date') == date and s.get('brawler') == brawler)]
            
            self.update_history(self.sessions)
            return True
        return False
    
    def get_sessions(self):
        return self.sessions


class MainWindow(ctk.CTk):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Brawl Stars Progress Analyzer")
        self.geometry("1200x800")
        
        # Инициализация анализатора
        self.analyzer = GameAnalyzer()
        self.brawl_stars = BrawlStarsGame()
        self.data_file = "data/bs_stats.json"
        
        # Загрузка данных
        self.load_data()
        
        # Создание табов
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Табы
        self.add_tab = self.tab_view.add("Добавить игру")
        self.stats_tab = self.tab_view.add("Статистика")
        self.history_tab = self.tab_view.add("История")
        
        # Инициализация фреймов
        self.session_frame = GameSessionFrame(self.add_tab, self.on_session_added)
        self.session_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.stats_frame = StatsFrame(self.stats_tab)
        self.stats_frame.pack(fill="both", expand=True)
        
        self.history_frame = HistoryFrame(self.history_tab)
        self.history_frame.pack(fill="both", expand=True)
        
        # Обновление UI
        self.refresh_all()
        
        # Автосохранение при закрытии
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_session_added(self, session_data):
        """Обработка добавленной сессии"""
        # Преобразование в формат модели
        session = self.brawl_stars.create_session(session_data)
        self.analyzer.add_session(session)
        self.sessions.append(session_data)
        
        self.save_data()
        self.refresh_all()
    
    def refresh_all(self):
        """Обновление всех вкладок"""
        sessions = self.sessions
        
        # Анализ
        if sessions:
            # Конвертация в формат для анализа
            bs_sessions = []
            for s in sessions:
                bs_session = self.brawl_stars.create_session(s)
                bs_sessions.append(bs_session)
            
            analysis = self.brawl_stars.analyze_performance(bs_sessions)
        else:
            analysis = {"overall_score": 0, "strengths": [], "weaknesses": []}
        
        self.stats_frame.update_stats(sessions, analysis)
        self.history_frame.update_history(sessions)
    
    def save_data(self):
        """Сохранение данных"""
        os.makedirs("data", exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.sessions, f, ensure_ascii=False, indent=2)
    
    def load_data(self):
        """Загрузка данных"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.sessions = json.load(f)
            except:
                self.sessions = []
        else:
            self.sessions = []
    
    def on_closing(self):
        """Обработка закрытия окна"""
        self.save_data()
        self.destroy()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
