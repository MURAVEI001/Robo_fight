import tkinter as tk
import math

class Robot:
    def __init__(self, x, y, color, width=60, height=40):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.angle = 0  # в градусах, 0 = смотрит вправо
        self.speed = 3
        self.rotation_step = 0.5
        
    def rotate(self, direction):
        """Поворот робота: direction = 1 (против часовой), -1 (по часовой)"""
        self.angle = (self.angle + direction * self.rotation_step) % 360
        
    def move_forward(self):
        """Движение вперед"""
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed  # ИЗМЕНИЛ ЗНАК: + вместо -
        
        self.x = max(self.width/2, min(800 - self.width/2, self.x))
        self.y = max(self.height/2, min(600 - self.height/2, self.y))
            
    def move_backward(self):
        """Движение назад"""
        rad = math.radians(self.angle)
        self.x -= math.cos(rad) * self.speed
        self.y -= math.sin(rad) * self.speed  # ИЗМЕНИЛ ЗНАК: - вместо +
        
        self.x = max(self.width/2, min(800 - self.width/2, self.x))
        self.y = max(self.height/2, min(600 - self.height/2, self.y))
            
    def get_corners(self):
        """Получение координат углов прямоугольника с учетом поворота"""
        half_w = self.width / 2
        half_h = self.height / 2
        rad = math.radians(self.angle)
        
        # Углы прямоугольника без поворота
        # При angle = 0, робот смотрит вправо, передняя часть - правая сторона
        corners = [
            (-half_w, -half_h),  # левый верхний
            (half_w, -half_h),   # правый верхний (передний)
            (half_w, half_h),    # правый нижний (передний)
            (-half_w, half_h)    # левый нижний
        ]
        
        # Поворачиваем и смещаем углы
        rotated_corners = []
        for dx, dy in corners:
            # Поворот
            rx = dx * math.cos(rad) - dy * math.sin(rad)
            ry = dx * math.sin(rad) + dy * math.cos(rad)
            # Смещение к позиции робота
            rotated_corners.append((self.x + rx, self.y + ry))
            
        return rotated_corners
    
    def get_front_square(self):
        """Получение координат красного квадрата на передней части робота"""
        rad = math.radians(self.angle)
        
        # Размер красного квадрата
        red_square_size = min(self.width * 0.7, self.height * 0.8)
        
        # Центр красного квадрата - на передней части робота
        # Смещаем от центра робота вперед на половину ширины
        center_x = self.x + math.cos(rad) * (self.width / 2 - red_square_size / 4)
        center_y = self.y + math.sin(rad) * (self.width / 2 - red_square_size / 4)
        
        half_red = red_square_size / 2
        
        # Углы квадрата без поворота
        corners = [
            (-half_red, -half_red),
            (half_red, -half_red),
            (half_red, half_red),
            (-half_red, half_red)
        ]
        
        # Поворачиваем и смещаем углы красного квадрата
        rotated_corners = []
        for dx, dy in corners:
            # Поворот (такой же, как у робота)
            rx = dx * math.cos(rad) - dy * math.sin(rad)
            ry = dx * math.sin(rad) + dy * math.cos(rad)
            # Смещение к позиции красного квадрата
            rotated_corners.append((center_x + rx, center_y + ry))
            
        return rotated_corners

class RobotGladiators:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Роботы-гладиаторы")
        
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='black')
        self.canvas.pack()
        
        # Создаем роботов с разными начальными направлениями для наглядности
        self.robot1 = Robot(100, 500, 'blue', width=60, height=40)
        self.robot1.angle = 315  # Начальный угол 45 градусов
        
        self.robot2 = Robot(700, 100, 'green', width=60, height=40)
        self.robot2.angle = 135  # Начальный угол 135 градусов
        
        self.keys_pressed = set()
        
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        
        self.canvas.focus_set()
        
        self.collision_count = 0
        self.debug_info = ""
        
        # Добавляем координатную сетку для отладки
        self.show_grid = False
        
        self.game_loop()
        
    def on_key_press(self, event):
        key = event.keysym
        self.keys_pressed.add(key)
        
    def on_key_release(self, event):
        key = event.keysym
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
            
    def update_robots(self):
        # Управление первым роботом
        if any(k in self.keys_pressed for k in ['w', 'W']):
            self.robot1.move_forward()
        if any(k in self.keys_pressed for k in ['s', 'S']):
            self.robot1.move_backward()
        if any(k in self.keys_pressed for k in ['a', 'A']):
            self.robot1.rotate(-1)  # Против часовой стрелки
        if any(k in self.keys_pressed for k in ['d', 'D']):
            self.robot1.rotate(1)  # По часовой стрелке
            
        # Управление вторым роботом
        if 'Up' in self.keys_pressed:
            self.robot2.move_forward()
        if 'Down' in self.keys_pressed:
            self.robot2.move_backward()
        if 'Left' in self.keys_pressed:
            self.robot2.rotate(-1)  # Против часовой стрелки
        if 'Right' in self.keys_pressed:
            self.robot2.rotate(1)  # По часовой стрелке
            
        # Проверка столкновений
        if self.check_collision(self.robot1, self.robot2):
            self.collision_count += 1
            
    def check_collision(self, robot1, robot2):
        """Упрощенная проверка столкновений"""
        distance = math.sqrt((robot1.x - robot2.x)**2 + (robot1.y - robot2.y)**2)
        return distance < 50  # Простая проверка расстояния
        
    def draw_grid(self):
        """Рисует координатную сетку для отладки"""
        # Вертикальные линии
        for x in range(0, 801, 50):
            self.canvas.create_line(x, 0, x, 600, fill='#222222', width=1)
            if x % 100 == 0:
                self.canvas.create_text(x, 10, text=str(x), fill='#666666', font=('Arial', 8))
        
        # Горизонтальные линии
        for y in range(0, 601, 50):
            self.canvas.create_line(0, y, 800, y, fill='#222222', width=1)
            if y % 100 == 0:
                self.canvas.create_text(10, y, text=str(y), fill='#666666', font=('Arial', 8))
                
        # Центр координат
        self.canvas.create_oval(395, 295, 405, 305, fill='red')
        self.canvas.create_text(420, 300, text='(400,300)', fill='red', font=('Arial', 10))
        
    def draw_robot(self, robot):
        """Отрисовка робота"""
        corners = robot.get_corners()
        
        # Рисуем основной прямоугольник
        self.canvas.create_polygon(corners, fill=robot.color, outline='white', width=2)
        
        # Рисуем красный квадрат на передней части
        red_square_corners = robot.get_front_square()
        self.canvas.create_polygon(red_square_corners, fill='red', outline='darkred', width=2)
        
    # def draw_ui(self):
    #     """Отрисовка интерфейса"""
    #     self.canvas.create_text(10, 10, anchor='nw', fill='white',
    #                            text=f'Столкновений: {self.collision_count}')
        
    #     self.canvas.create_text(10, 30, anchor='nw', fill='white',
    #                            text=f'Синий: {self.robot1.angle:.1f}° (x:{int(self.robot1.x)}, y:{int(self.robot1.y)})')
        
    #     self.canvas.create_text(10, 50, anchor='nw', fill='white',
    #                            text=f'Зеленый: {self.robot2.angle:.1f}° (x:{int(self.robot2.x)}, y:{int(self.robot2.y)})')
        
    #     # Отображаем направление роботов
    #     rad1 = math.radians(self.robot1.angle)
    #     rad2 = math.radians(self.robot2.angle)
        
    #     direction1 = ""
    #     if -22.5 <= self.robot1.angle <= 22.5:
    #         direction1 = "→ Вправо"
    #     elif 22.5 < self.robot1.angle <= 67.5:
    #         direction1 = "↗ Вверх-вправо"
    #     elif 67.5 < self.robot1.angle <= 112.5:
    #         direction1 = "↑ Вверх"
    #     elif 112.5 < self.robot1.angle <= 157.5:
    #         direction1 = "↖ Вверх-влево"
    #     elif 157.5 < self.robot1.angle <= 202.5:
    #         direction1 = "← Влево"
    #     elif 202.5 < self.robot1.angle <= 247.5:
    #         direction1 = "↙ Вниз-влево"
    #     elif 247.5 < self.robot1.angle <= 292.5:
    #         direction1 = "↓ Вниз"
    #     elif 292.5 < self.robot1.angle <= 337.5:
    #         direction1 = "↘ Вниз-вправо"
    #     else:
    #         direction1 = "→ Вправо"
            
    #     self.canvas.create_text(10, 70, anchor='nw', fill='lightblue',
    #                            text=f'Направление синего: {direction1}')
        
    def game_loop(self):
        self.canvas.delete('all')
        
        # Обработка специальных клавиш
        if 'g' in self.keys_pressed or 'G' in self.keys_pressed:
            self.show_grid = not self.show_grid
            self.keys_pressed.discard('g')
            self.keys_pressed.discard('G')
            
        if 'r' in self.keys_pressed or 'R' in self.keys_pressed:
            self.reset_positions()
            self.keys_pressed.discard('r')
            self.keys_pressed.discard('R')
        
        if self.show_grid:
            self.draw_grid()
            
        self.update_robots()
        self.draw_robot(self.robot1)
        self.draw_robot(self.robot2)
        # self.draw_ui()
        
        if 'Escape' in self.keys_pressed:
            self.root.quit()
        
        self.root.after(16, self.game_loop)
        
    def reset_positions(self):
        """Сброс позиций роботов к начальным"""
        self.robot1.x, self.robot1.y = 200, 300
        self.robot1.angle = 45
        
        self.robot2.x, self.robot2.y = 600, 300
        self.robot2.angle = 135
        
        self.collision_count = 0
        
    def run(self):
        self.canvas.focus_set()
        self.root.mainloop()

if __name__ == "__main__":
    print("Запуск игры 'Роботы-гладиаторы'...")
    print("ИСПРАВЛЕНА СИСТЕМА ПОВОРОТА!")
    print("Теперь стрелка направления и корпус робота двигаются синхронно")
    print("\nУправление:")
    print("  Синий робот: W - вперед, S - назад, A/D - поворот")
    print("  Зеленый робот: Стрелки - движение и поворот")
    print("  G - показать/скрыть координатную сетку")
    print("  R - сбросить позиции роботов")
    print("  ESC - выход")
    print("\nНаправления:")
    print("  0° = вправо, 90° = вниз, 180° = влево, 270° = вверх")
    print("\nПеред началом убедитесь, что окно игры активно!")
    
    game = RobotGladiators()
    game.run()