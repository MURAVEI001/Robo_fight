import tkinter as tk
import math
import random

class Robot:
    def __init__(self, x, y, color, width=60, height=40, max_speed=8):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.angle = 0
        self.speed = 0
        self.max_speed = max_speed
        self.acceleration = 0.15
        self.deceleration = 0.1
        self.rotation_step = 8
        self.velocity_x = 0
        self.velocity_y = 0
        self.angular_velocity = 0
        self.angular_deceleration = 0.95
        self.mass = 1.0
        self.score = 0
        self.collision_timer = 0
        self.health = 100
        self.active = True  # Активен ли робот в тренировочном режиме
        
    def apply_acceleration(self, forward, backward):
        if forward:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif backward:
            self.speed = max(self.speed - self.acceleration, -self.max_speed/2)
        else:
            if abs(self.speed) < self.deceleration:
                self.speed = 0
            elif self.speed > 0:
                self.speed -= self.deceleration
            else:
                self.speed += self.deceleration
        
        rad = math.radians(self.angle)
        self.velocity_x = math.cos(rad) * self.speed
        self.velocity_y = math.sin(rad) * self.speed
        
    def apply_rotation(self, direction):
        if direction != 0:
            self.angular_velocity += direction * self.rotation_step * 0.1
            self.angular_velocity = max(-2, min(2, self.angular_velocity))
        
        self.angle = (self.angle + self.angular_velocity) % 360
        self.angular_velocity *= self.angular_deceleration
        
    def update_position(self, field_width, field_height):
        old_x, old_y = self.x, self.y
        
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        collision_with_wall = False
        bounce_factor = 0.7
        
        if self.x - self.width/2 < 0:
            self.x = self.width/2
            self.velocity_x = -self.velocity_x * bounce_factor
            self.speed *= 0.8
            collision_with_wall = True
            
        if self.x + self.width/2 > field_width:
            self.x = field_width - self.width/2
            self.velocity_x = -self.velocity_x * bounce_factor
            self.speed *= 0.8
            collision_with_wall = True
            
        if self.y - self.height/2 < 0:
            self.y = self.height/2
            self.velocity_y = -self.velocity_y * bounce_factor
            self.speed *= 0.8
            collision_with_wall = True
            
        if self.y + self.height/2 > field_height:
            self.y = field_height - self.height/2
            self.velocity_y = -self.velocity_y * bounce_factor
            self.speed *= 0.8
            collision_with_wall = True
        
        if collision_with_wall:
            self.speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            
    def get_corners(self):
        half_w = self.width / 2
        half_h = self.height / 2
        rad = math.radians(self.angle)
        
        corners = [
            (-half_w, -half_h),
            (half_w, -half_h),
            (half_w, half_h),
            (-half_w, half_h)
        ]
        
        rotated_corners = []
        for dx, dy in corners:
            rx = dx * math.cos(rad) - dy * math.sin(rad)
            ry = dx * math.sin(rad) + dy * math.cos(rad)
            rotated_corners.append((self.x + rx, self.y + ry))
            
        return rotated_corners
    
    def get_front_square(self):
        rad = math.radians(self.angle)
        red_square_size = min(self.width * 0.7, self.height * 0.8)
        
        center_x = self.x + math.cos(rad) * (self.width / 2 - red_square_size / 4)
        center_y = self.y + math.sin(rad) * (self.width / 2 - red_square_size / 4)
        
        half_red = red_square_size / 2
        
        corners = [
            (-half_red, -half_red),
            (half_red, -half_red),
            (half_red, half_red),
            (-half_red, half_red)
        ]
        
        rotated_corners = []
        for dx, dy in corners:
            rx = dx * math.cos(rad) - dy * math.sin(rad)
            ry = dx * math.sin(rad) + dy * math.cos(rad)
            rotated_corners.append((center_x + rx, center_y + ry))
            
        return rotated_corners
    
    def get_bounding_circle(self):
        return math.sqrt((self.width/2)**2 + (self.height/2)**2)
    
    def get_momentum(self):
        return self.mass * self.speed
    
    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        
    def heal(self, amount):
        self.health = min(100, self.health + amount)
        
    def reset_stats(self):
        """Сброс статистики робота"""
        self.score = 0
        self.health = 100
        self.speed = 0
        self.velocity_x = 0
        self.velocity_y = 0

class RobotGladiators:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Роботы-гладиаторы")
        
        # Получаем размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Устанавливаем окно на весь экран
        self.root.attributes('-fullscreen', True)
        
        # Создаем холст на весь экран с черным фоном
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height, 
                               bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Сохраняем размеры поля
        self.field_width = screen_width
        self.field_height = screen_height
        
        # Создаем роботов
        self.robot1 = Robot(screen_width * 0.25, screen_height * 0.75, 'blue', 
                           width=45, height=70, max_speed=10)
        self.robot1.angle = 315
        
        self.robot2 = Robot(screen_width * 0.75, screen_height * 0.25, 'green', 
                           width=45, height=70, max_speed=10)
        self.robot2.angle = 135
        
        # Устанавливаем разные массы
        self.robot1.mass = 1.2
        self.robot2.mass = 0.9
        
        # Режимы игры
        self.game_mode = "competition"  # "competition" или "training"
        self.show_ui = True  # Показывать ли интерфейс
        self.training_opponent_active = True  # Активен ли соперник в тренировочном режиме
        
        # Состояние управления
        self.keys_pressed = set()
        
        # Привязка клавиш
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        
        self.canvas.focus_set()
        
        # Таймер и состояние игры
        self.game_time = 0
        self.game_over = False
        self.winner = None
        
        # Эффекты
        self.collision_effects = []
        self.spark_particles = []
        
        # Статистика
        self.total_collisions = 0
        
        # Меню выбора режима
        self.show_mode_selection = True
        
        self.game_loop()
        
    def on_key_press(self, event):
        key = event.keysym
        self.keys_pressed.add(key)
        
    def on_key_release(self, event):
        key = event.keysym
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
            
    def switch_game_mode(self, mode):
        """Переключение режима игры"""
        self.game_mode = mode
        self.show_mode_selection = False
        self.game_over = False
        self.game_time = 0
        
        # Сбрасываем позиции роботов
        self.reset_positions()
        
        # Сбрасываем статистику
        self.robot1.reset_stats()
        self.robot2.reset_stats()
        
        # В тренировочном режиме зеленый робот может быть неактивным
        if mode == "training" and not self.training_opponent_active:
            self.robot2.active = False
        else:
            self.robot2.active = True
            
    def toggle_ui(self):
        """Переключение видимости интерфейса"""
        self.show_ui = not self.show_ui
        
    def toggle_training_opponent(self):
        """Переключение активности соперника в тренировочном режиме"""
        if self.game_mode == "training":
            self.training_opponent_active = not self.training_opponent_active
            self.robot2.active = self.training_opponent_active
            
    def handle_collision(self, robot1, robot2):
        """Обрабатывает столкновение двух роботов с физикой"""
        dx = robot2.x - robot1.x
        dy = robot2.y - robot1.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance == 0:
            distance = 0.001
            
        nx = dx / distance
        ny = dy / distance
        
        rvx = robot2.velocity_x - robot1.velocity_x
        rvy = robot2.velocity_y - robot1.velocity_y
        
        vel_along_normal = rvx * nx + rvy * ny
        
        if vel_along_normal > 0:
            return
            
        restitution = 0.8
        
        impulse_scalar = -(1 + restitution) * vel_along_normal
        impulse_scalar /= (1/robot1.mass + 1/robot2.mass)
        
        impulse_x = impulse_scalar * nx
        impulse_y = impulse_scalar * ny
        
        robot1.velocity_x -= impulse_x / robot1.mass
        robot1.velocity_y -= impulse_y / robot1.mass
        robot2.velocity_x += impulse_x / robot2.mass
        robot2.velocity_y += impulse_y / robot2.mass
        
        robot1.speed = math.sqrt(robot1.velocity_x**2 + robot1.velocity_y**2)
        robot2.speed = math.sqrt(robot2.velocity_x**2 + robot2.velocity_y**2)
        
        self.create_collision_effect(robot1.x, robot1.y)
        
        # В режиме соревнования начисляем очки
        if self.game_mode == "competition":
            momentum1 = robot1.get_momentum()
            momentum2 = robot2.get_momentum()
            
            damage = int(abs(vel_along_normal) * 10)
            
            if momentum1 > momentum2:
                robot1.score += damage
                robot2.take_damage(damage)
                self.create_score_effect(robot1.x, robot1.y, f"+{damage}", robot1.color)
            elif momentum2 > momentum1:
                robot2.score += damage
                robot1.take_damage(damage)
                self.create_score_effect(robot2.x, robot2.y, f"+{damage}", robot2.color)
            else:
                robot1.take_damage(damage // 2)
                robot2.take_damage(damage // 2)
            
            self.check_game_over()
        
        self.total_collisions += 1
        
    def create_collision_effect(self, x, y):
        self.collision_effects.append({
            'x': x, 'y': y, 'radius': 30, 'alpha': 1.0, 'life': 20
        })
        
        for _ in range(15):
            angle = math.radians(random.randint(0, 360))
            speed = random.uniform(2, 8)
            self.spark_particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.randint(10, 30),
                'color': random.choice(['yellow', 'orange', 'red'])
            })
            
    def create_score_effect(self, x, y, text, color):
        self.spark_particles.append({
            'x': x, 'y': y,
            'vx': 0, 'vy': -2,
            'life': 40,
            'text': text,
            'color': color,
            'font_size': 18
        })
        
    def update_effects(self):
        for effect in self.collision_effects[:]:
            effect['life'] -= 1
            effect['alpha'] = effect['life'] / 20.0
            effect['radius'] += 1
            if effect['life'] <= 0:
                self.collision_effects.remove(effect)
                
        for particle in self.spark_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            if 'vy' in particle:
                particle['vy'] += 0.1
                
            if particle['life'] <= 0:
                self.spark_particles.remove(particle)
                
    def update_robots(self):
        """Обновляет состояние роботов"""
        if self.game_over or self.show_mode_selection:
            return
            
        self.game_time += 1
        
        # Управление первым роботом
        forward1 = any(k in self.keys_pressed for k in ['w', 'W'])
        backward1 = any(k in self.keys_pressed for k in ['s', 'S'])
        rotate_left1 = any(k in self.keys_pressed for k in ['a', 'A'])
        rotate_right1 = any(k in self.keys_pressed for k in ['d', 'D'])
        
        # Управление вторым роботом (только если он активен)
        forward2 = 'Up' in self.keys_pressed and self.robot2.active
        backward2 = 'Down' in self.keys_pressed and self.robot2.active
        rotate_left2 = 'Left' in self.keys_pressed and self.robot2.active
        rotate_right2 = 'Right' in self.keys_pressed and self.robot2.active
        
        self.robot1.apply_acceleration(forward1, backward1)
        
        if self.robot2.active:
            self.robot2.apply_acceleration(forward2, backward2)
        
        rotate_dir1 = (1 if rotate_left1 else 0) + (-1 if rotate_right1 else 0)
        rotate_dir2 = (1 if rotate_left2 else 0) + (-1 if rotate_right2 else 0)
        
        self.robot1.apply_rotation(rotate_dir1)
        
        if self.robot2.active:
            self.robot2.apply_rotation(rotate_dir2)
        
        self.robot1.update_position(self.field_width, self.field_height)
        
        if self.robot2.active:
            self.robot2.update_position(self.field_width, self.field_height)
        
        if self.check_collision(self.robot1, self.robot2):
            self.handle_collision(self.robot1, self.robot2)
            
        if self.game_mode == "competition" and self.game_time % 60 == 0:
            self.robot1.heal(0.5)
            self.robot2.heal(0.5)
            
    def check_collision(self, robot1, robot2):
        distance = math.sqrt((robot1.x - robot2.x)**2 + (robot1.y - robot2.y)**2)
        min_distance = robot1.get_bounding_circle() + robot2.get_bounding_circle()
        return distance < min_distance * 0.9
        
    def check_game_over(self):
        if self.game_mode == "competition":
            if self.robot1.health <= 0:
                self.game_over = True
                self.winner = "ЗЕЛЕНЫЙ РОБОТ"
            elif self.robot2.health <= 0:
                self.game_over = True
                self.winner = "СИНИЙ РОБОТ"
            elif self.game_time >= 60 * 60 * 3:
                self.game_over = True
                if self.robot1.score > self.robot2.score:
                    self.winner = "СИНИЙ РОБОТ"
                elif self.robot2.score > self.robot1.score:
                    self.winner = "ЗЕЛЕНЫЙ РОБОТ"
                else:
                    self.winner = "НИЧЬЯ"
    
    def reset_positions(self):
        """Сброс позиций роботов"""
        self.robot1.x, self.robot1.y = self.field_width * 0.25, self.field_height * 0.75
        self.robot1.angle = 315
        
        self.robot2.x, self.robot2.y = self.field_width * 0.75, self.field_height * 0.25
        self.robot2.angle = 135
        
        self.robot1.speed = 0
        self.robot2.speed = 0
        self.robot1.velocity_x = 0
        self.robot1.velocity_y = 0
        self.robot2.velocity_x = 0
        self.robot2.velocity_y = 0
        
    def draw_mode_selection(self):
        """Рисует меню выбора режима"""
        # Полупрозрачный фон
        self.canvas.create_rectangle(0, 0, self.field_width, self.field_height, 
                                     fill='black', stipple='gray50', width=0)
        
        # Заголовок
        self.canvas.create_text(self.field_width // 2, self.field_height // 4, 
                               text="ВЫБЕРИТЕ РЕЖИМ ИГРЫ", 
                               fill='yellow', font=('Arial', 48, 'bold'))
        
        # Кнопка режима соревнования
        comp_color = 'lightgreen' if self.game_mode == "competition" else 'gray'
        comp_y = self.field_height // 2 - 60
        self.canvas.create_rectangle(self.field_width//2 - 200, comp_y - 40,
                                    self.field_width//2 + 200, comp_y + 40,
                                    fill=comp_color, outline='white', width=3)
        self.canvas.create_text(self.field_width // 2, comp_y, 
                               text="СОРЕВНОВАНИЕ", 
                               fill='black', font=('Arial', 32, 'bold'))
        
        # Описание режима соревнования
        self.canvas.create_text(self.field_width // 2, comp_y + 70, 
                               text="• Очки за удары • Здоровье • Таймер • Финал по победе", 
                               fill='lightgray', font=('Arial', 16))
        
        # Кнопка тренировочного режима
        train_color = 'lightblue' if self.game_mode == "training" else 'gray'
        train_y = self.field_height // 2 + 100
        self.canvas.create_rectangle(self.field_width//2 - 200, train_y - 40,
                                    self.field_width//2 + 200, train_y + 40,
                                    fill=train_color, outline='white', width=3)
        self.canvas.create_text(self.field_width // 2, train_y, 
                               text="ТРЕНИРОВКА", 
                               fill='black', font=('Arial', 32, 'bold'))
        
        # Описание тренировочного режима
        self.canvas.create_text(self.field_width // 2, train_y + 70, 
                               text="• Нет очков • Нет здоровья • Выбор соперника • Бесконечная игра", 
                               fill='lightgray', font=('Arial', 16))
        
        # Подсказки
        hints = [
            "Нажмите 1 для выбора СОРЕВНОВАНИЯ",
            "Нажмите 2 для выбора ТРЕНИРОВКИ",
            "Нажмите ПРОБЕЛ для начала игры",
            "Нажмите ESC для выхода"
        ]
        
        for i, hint in enumerate(hints):
            self.canvas.create_text(self.field_width // 2, self.field_height - 150 + i*30,
                                   text=hint, fill='white', font=('Arial', 18))
    
    def draw_full_ui(self):
        """Рисует полный интерфейс"""
        if self.game_mode == "competition":
            minutes = self.game_time // 60 // 60
            seconds = (self.game_time // 60) % 60
            
            self.canvas.create_text(self.field_width // 2, 30, 
                                   text=f"{minutes:02d}:{seconds:02d}", 
                                   fill='white', font=('Arial', 24))
            
            # Панель синего робота
            self.canvas.create_text(150, 80, anchor='center', fill='lightblue',
                                   text=f"СИНИЙ РОБОТ", font=('Arial', 16, 'bold'))
            self.canvas.create_text(150, 110, anchor='center', fill='white',
                                   text=f"Очки: {self.robot1.score}", font=('Arial', 14))
            self.canvas.create_text(150, 130, anchor='center', fill='white',
                                   text=f"Скорость: {abs(self.robot1.speed):.1f}", font=('Arial', 12))
            
            # Панель зеленого робота
            self.canvas.create_text(self.field_width - 150, 80, anchor='center', fill='lightgreen',
                                   text=f"ЗЕЛЕНЫЙ РОБОТ", font=('Arial', 16, 'bold'))
            self.canvas.create_text(self.field_width - 150, 110, anchor='center', fill='white',
                                   text=f"Очки: {self.robot2.score}", font=('Arial', 14))
            self.canvas.create_text(self.field_width - 150, 130, anchor='center', fill='white',
                                   text=f"Скорость: {abs(self.robot2.speed):.1f}", font=('Arial', 12))
            
            # Полоски здоровья
            self.draw_health_bar(self.robot1, 50, 170)
            self.draw_health_bar(self.robot2, self.field_width - 150, 170)
            
            self.canvas.create_text(self.field_width // 2, 200, anchor='center', fill='white',
                                   text=f"Всего столкновений: {self.total_collisions}", 
                                   font=('Arial', 12))
        
        else:  # training mode
            minutes = self.game_time // 60 // 60
            seconds = (self.game_time // 60) % 60
            
            self.canvas.create_text(self.field_width // 2, 30, 
                                   text=f"ТРЕНИРОВКА: {minutes:02d}:{seconds:02d}", 
                                   fill='lightblue', font=('Arial', 24))
            
            # Информация о скорости
            self.canvas.create_text(150, 80, anchor='center', fill='lightblue',
                                   text=f"СИНИЙ", font=('Arial', 16, 'bold'))
            self.canvas.create_text(150, 110, anchor='center', fill='white',
                                   text=f"Скорость: {abs(self.robot1.speed):.1f}", font=('Arial', 14))
            
            if self.robot2.active:
                self.canvas.create_text(self.field_width - 150, 80, anchor='center', fill='lightgreen',
                                       text=f"ЗЕЛЕНЫЙ", font=('Arial', 16, 'bold'))
                self.canvas.create_text(self.field_width - 150, 110, anchor='center', fill='white',
                                       text=f"Скорость: {abs(self.robot2.speed):.1f}", font=('Arial', 14))
            else:
                self.canvas.create_text(self.field_width - 150, 80, anchor='center', fill='gray',
                                       text=f"НЕПОДВИЖЕН", font=('Arial', 16, 'bold'))
            
            self.canvas.create_text(self.field_width // 2, 150, anchor='center', fill='white',
                                   text=f"Всего столкновений: {self.total_collisions}", 
                                   font=('Arial', 14))
        
        # Управление
        controls = [
            "УПРАВЛЕНИЕ:",
            "Синий робот: W/S - вперед/назад, A/D - поворот",
            "Зеленый робот: Стрелки - движение и поворот",
            "H - скрыть/показать интерфейс",
            "R - сбросить позиции",
            "ESC - выход из игры",
            "",
            "СПЕЦИАЛЬНЫЕ КЛАВИШИ:",
            "M - меню выбора режима",
        ]
        
        if self.game_mode == "training":
            controls.append("T - переключить активность соперника")
        
        y_pos = self.field_height - len(controls) * 22
        for i, text in enumerate(controls):
            color = 'white'
            if i == 0: color = 'lightblue'
            elif i == 7: color = 'lightgreen'
            elif i > 7: color = 'lightyellow'
            
            self.canvas.create_text(20, y_pos + i*22, anchor='sw', 
                                   fill=color, text=text, font=('Arial', 11))
        
        # Если игра окончена, показываем результат
        if self.game_over and self.game_mode == "competition":
            self.draw_game_over_screen()
    
    def draw_health_bar(self, robot, x, y, width=100, height=10):
        self.canvas.create_rectangle(x, y, x + width, y + height, 
                                     fill='#333333', outline='#555555')
        
        health_width = max(0, width * robot.health / 100)
        health_color = '#00ff00' if robot.health > 50 else \
                      '#ffff00' if robot.health > 25 else '#ff0000'
        
        self.canvas.create_rectangle(x, y, x + health_width, y + height, 
                                     fill=health_color, outline='')
        
        self.canvas.create_text(x + width//2, y + height//2, 
                               text=f"{int(robot.health)}%", 
                               fill='white', font=('Arial', 8))
        
    def draw_robot(self, robot):
        corners = robot.get_corners()
        
        glow_width = int(min(4, abs(robot.speed) / 2))
        if glow_width > 0:
            self.canvas.create_polygon(corners, fill=robot.color, 
                                       outline='white', width=glow_width+1)
            
        self.canvas.create_polygon(corners, fill=robot.color, outline='white', width=1)
        
        red_square_corners = robot.get_front_square()
        self.canvas.create_polygon(red_square_corners, fill='red', outline='darkred', width=1)

    def draw_effects(self):
        for effect in self.collision_effects:
            alpha = int(effect['alpha'] * 255)
            color = f'#{alpha:02x}{alpha:02x}ff'
            self.canvas.create_oval(
                effect['x'] - effect['radius'], effect['y'] - effect['radius'],
                effect['x'] + effect['radius'], effect['y'] + effect['radius'],
                outline=color, width=2
            )
            
        for particle in self.spark_particles:
            if 'text' in particle:
                alpha = int(particle['life'] * 6.375)
                color = particle['color']
                self.canvas.create_text(
                    particle['x'], particle['y'],
                    text=particle['text'],
                    fill=color, font=('Arial', particle['font_size'])
                )
            else:
                size = max(1, particle['life'] // 5)
                self.canvas.create_oval(
                    particle['x'] - size, particle['y'] - size,
                    particle['x'] + size, particle['y'] + size,
                    fill=particle['color'], outline=''
                )
                
    def draw_game_over_screen(self):
        self.canvas.create_rectangle(0, 0, self.field_width, self.field_height, 
                                     fill='black', stipple='gray50', width=0)
        
        self.canvas.create_text(self.field_width // 2, self.field_height // 3, 
                               text="ИГРА ОКОНЧЕНА!", 
                               fill='yellow', font=('Arial', 48, 'bold'))
        
        self.canvas.create_text(self.field_width // 2, self.field_height // 2, 
                               text=f"ПОБЕДИТЕЛЬ: {self.winner}", 
                               fill='cyan', font=('Arial', 36))
        
        self.canvas.create_text(self.field_width // 2, self.field_height // 2 + 60, 
                               text=f"Синий: {self.robot1.score} очков | Зеленый: {self.robot2.score} очков", 
                               fill='white', font=('Arial', 24))
        
        self.canvas.create_text(self.field_width // 2, self.field_height - 100, 
                               text="Нажмите M для возврата в меню или ESC для выхода", 
                               fill='lightgray', font=('Arial', 20))
    
    def game_loop(self):
        self.canvas.delete('all')
        
        # Обработка клавиш управления
        if 'h' in self.keys_pressed or 'H' in self.keys_pressed:
            self.toggle_ui()
            self.keys_pressed.discard('h')
            self.keys_pressed.discard('H')
            
        if 'm' in self.keys_pressed or 'M' in self.keys_pressed:
            self.show_mode_selection = True
            self.game_over = False
            self.keys_pressed.discard('m')
            self.keys_pressed.discard('M')
            
        if 't' in self.keys_pressed or 'T' in self.keys_pressed:
            self.toggle_training_opponent()
            self.keys_pressed.discard('t')
            self.keys_pressed.discard('T')
            
        if 'r' in self.keys_pressed or 'R' in self.keys_pressed:
            self.reset_positions()
            self.keys_pressed.discard('r')
            self.keys_pressed.discard('R')
            
        if '1' in self.keys_pressed:
            self.switch_game_mode("competition")
            self.keys_pressed.discard('1')
            
        if '2' in self.keys_pressed:
            self.switch_game_mode("training")
            self.keys_pressed.discard('2')
            
        if 'space' in self.keys_pressed and self.show_mode_selection:
            self.show_mode_selection = False
            self.keys_pressed.discard('space')
        
        if self.show_mode_selection:
            self.draw_mode_selection()
        else:
            self.update_robots()
            self.update_effects()
            
            self.draw_effects()
            self.draw_robot(self.robot1)
            self.draw_robot(self.robot2)
            self.draw_effects()
            
            if self.show_ui:
                self.draw_full_ui()
            else:
                self.draw_minimal_ui()
        
        if 'Escape' in self.keys_pressed:
            self.root.quit()
        
        self.root.after(16, self.game_loop)
        
    def run(self):
        self.canvas.focus_set()
        self.root.mainloop()

if __name__ == "__main__":
    print("Запуск игры 'Роботы-гладиаторы'...")
    print("Игра запущена в полноэкранном режиме.")
    print("\nДОСТУПНЫЕ РЕЖИМЫ:")
    print("  1. СОРЕВНОВАНИЕ - полная версия с очками, здоровьем и таймером")
    print("  2. ТРЕНИРОВКА - упрощенная версия для практики")
    print("\nУПРАВЛЕНИЕ:")
    print("  В меню: 1/2 - выбор режима, ПРОБЕЛ - начать")
    print("  В игре: M - меню, H - скрыть интерфейс, R - сбросить позиции")
    print("  В тренировке: T - переключить активность соперника")
    print("  ESC - выход из игры")
    print("\nПеред началом убедитесь, что окно игры активно!")
    
    game = RobotGladiators()
    game.run()