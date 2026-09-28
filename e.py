"""Алло, это мемный отдел? — безопасная комедийная мини-игра на Pygame.

Весь игровой контент вымышленный: никаких настоящих схем, денег или личных данных.
Запуск: python main.py
Запуск: python outputs/main.py
"""

import math
import random
import sys
from typing import Dict, List, Tuple

import pygame


pygame.init()
pygame.display.set_caption("Алло, это мемный отдел?")
WIDTH, HEIGHT = 1120, 760
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Палитра
BG = (17, 19, 38)
PANEL = (29, 32, 59)
PANEL_LIGHT = (39, 43, 75)
WHITE = (244, 245, 255)
MUTED = (163, 169, 199)
PURPLE = (160, 113, 255)
CYAN = (83, 222, 222)
GREEN = (109, 224, 164)
PINK = (255, 123, 165)
YELLOW = (255, 206, 105)
RED = (255, 91, 112)

FONT = pygame.font.SysFont("segoeui", 20)
FONT_SMALL = pygame.font.SysFont("segoeui", 16)
FONT_MED = pygame.font.SysFont("segoeui", 25, bold=True)
FONT_BIG = pygame.font.SysFont("segoeui", 48, bold=True)
FONT_TITLE = pygame.font.SysFont("segoeui", 56, bold=True)

# Один раз рисуем мягкий градиентный фон, чтобы анимация оставалась лёгкой.
BACKGROUND = pygame.Surface((WIDTH, HEIGHT))
for _y in range(HEIGHT):
    _t = _y / HEIGHT
    _col = (int(13 + 13 * _t), int(17 + 10 * _t), int(38 + 17 * _t))
    pygame.draw.line(BACKGROUND, _col, (0, _y), (WIDTH, _y))
_glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.draw.circle(_glow, (93, 55, 181, 24), (110, 155), 245)
pygame.draw.circle(_glow, (30, 142, 159, 23), (1010, 625), 265)
pygame.draw.circle(_glow, (138, 81, 115, 12), (745, 230), 175)
BACKGROUND.blit(_glow, (0, 0))
_star_rng = random.Random(27)
STARS = [(_star_rng.randrange(WIDTH), _star_rng.randrange(HEIGHT), _star_rng.uniform(0.0, math.tau), _star_rng.choice((1, 1, 1, 2))) for _ in range(82)]


# У всех вариантов только абсурдные реплики. Риск — игровая шкала подозрительности,
# а не оценка какого-либо реального поведения.
CHARACTERS: List[Dict] = [
    {
        "name": "Бабушка-криптоэксперт", "role": "главный аналитик компота",
        "name": "Бабушка-криптоэксперт", "kind": "grandma", "role": "главный аналитик компота",
        "color": (247, 174, 113), "face": "Б", "hello": "Алло! Я как раз считаю курс варенья к гречке.",
        "yes": ["Записала на салфетку. Салфетка одобрила!", "О, звучит как прогноз погоды для пельменей.", "Принято. Мой кактус уже аплодирует."],
        "no": ["Хм. Даже мой чайник так не договаривался.", "Секундочку, позову рассудок. Он сегодня на даче.", "Мне кажется, тут звонит очень странная табуретка."],
        "options": [
            ("Сверим курс компота и гречки.", 3, 0),
            ("Предлагаю облаку выбрать любимый пирожок.", 3, 1),
            ("Я официальный представитель тайного комитета чайников.", 1, 7),
        ],
    },
    {
        "name": "Говорящий холодильник", "role": "хранитель ночных перекусов",
        "name": "Говорящий холодильник", "kind": "fridge", "role": "хранитель ночных перекусов",
        "color": (100, 198, 226), "face": "Х", "hello": "Кто там? Я занят: охлаждаю вчерашний анекдот.",
        "yes": ["Бззз! Полка для этой идеи уже освобождена.", "Звучит свежо. Положу это рядом с сыром.", "Мотор одобрительно загудел в тональности до."],
        "no": ["Не-а. Даже магнит с уткой нахмурился.", "Кажется, это сообщение испортилось при комнатной температуре.", "Я бы ответил, но у меня разморозка."],
        "options": [
            ("Обсудим температуру вареников.", 3, 0),
            ("Внутри не застряла маленькая опера?", 3, 1),
            ("Звоню от имени настольной лампы.", 1, 7),
        ],
    },
    {
        "name": "Кот-налоговый инспектор", "role": "проверяет коробки и декларации",
        "name": "Кот-налоговый инспектор", "kind": "cat", "role": "проверяет коробки и декларации",
        "color": (220, 151, 192), "face": "К", "hello": "Мяу. У вас есть декларация на эту коробку?",
        "yes": ["Мяу, принято! Лазерная указка проходит как космолёт.", "Ваша шутка освобождена от налога на скуку.", "Ставлю штамп лапой. Чернила — тунец."],
        "no": ["Подозрительно. Эта фраза пахнет пылесосом.", "Мур. В коробке с логикой пусто.", "Налоговый кодекс требует немедленно поспать."],
        "options": [
            ("Ваша декларация мяукает в ре мажоре.", 3, 0),
            ("Списать лазерную указку как космолёт.", 3, 1),
            ("Я инспектор облачных коробок.", 1, 7),
        ],
    },
    {
        "name": "Голубь-урбанист", "role": "эксперт по балконам и крошкам",
        "name": "Голубь-урбанист", "kind": "pigeon", "role": "эксперт по балконам и крошкам",
        "color": (151, 190, 234), "face": "Г", "hello": "Кар! То есть, кхм, добрый день. Где тут остановка?",
        "yes": ["Каррр! На карте появилась улица Крошечная.", "Согласовано. Скамейка будет круглой и очень важной.", "Отличный план! Я уже поставил на него крошечный штамп."],
        "no": ["Кар! Это нарушает правила голубиной парковки.", "Я не понял, зато красиво взлетел.", "Тут явно не хватает фонтана и одного батона."],
        "options": [
            ("Зарегистрируем пробку на вашем балконе.", 3, 0),
            ("Объявляю этот батон памятником архитектуры.", 3, 1),
            ("Я представляю министерство скамеек.", 1, 7),
        ],
    },
    {
        "name": "Принтер-прорицатель", "role": "предсказывает замятие бумаги",
        "name": "Принтер-прорицатель", "kind": "printer", "role": "предсказывает замятие бумаги",
        "color": (181, 164, 240), "face": "П", "hello": "Ваше будущее распечатано… но зажевано на третьей странице.",
        "yes": ["Бип! Предсказание сбылось: сейчас будет смешно.", "Печатаю ответ на воображаемой бумаге.", "На листе проявилась большая улыбающаяся скрепка."],
        "no": ["Ошибка 404: смысл не найден.", "Пожалуйста, подождите. Я думаю со скоростью одной страницы в минуту.", "Бип-бип. В этом разговоре закончился тонер логики."],
        "options": [
            ("Отправляю вам факс мысленно.", 3, 0),
            ("Пусть скрепка предскажет погоду на Марсе.", 3, 1),
            ("Я официальный голос бумаги формата А5.", 1, 7),
        ],
    },
    {
        "name": "Луна на автоответчике", "role": "ночной оператор кратеров",
        "name": "Луна на автоответчике", "kind": "moon", "role": "ночной оператор кратеров",
        "color": (245, 213, 133), "face": "Л", "hello": "Пи-и-ип. Луна слушает. Пожалуйста, не будите кратеры.",
        "yes": ["На обратной стороне Луны кто-то тихо хихикнул.", "Записано звёздной пылью. Доставка — во сне.", "Ваш ответ получил четыре маленькие кометы."],
        "no": ["Кратер связи временно занят сыром.", "Пи-и-ип. Даже звёзды не поняли, но им понравилось.", "Попробуйте после следующего затмения здравого смысла."],
        "options": [
            ("Кто украл у Луны вторник?", 3, 0),
            ("Обсудим договор с привидением-астронавтом.", 3, 1),
            ("Я ночной инспектор лунных тапочек.", 1, 7),
        ],
    },
]

RANDOM_EVENTS = [
    ("Соседский кактус поставил лайк вашему абсурду.", 2, 0),
    ("В трубке прозвучало соло на ложках. Подозрительность −3.", 0, -3),
    ("Полиция мемов прислала предупреждение в виде смешного носка.", 0, 5),
    ("Чайник объявил минуту молчания по скучным диалогам.", 3, -2),
]


def draw_text(surface, text: str, font, color, x: int, y: int, anchor="topleft") -> pygame.Rect:
    rendered = font.render(str(text), True, color)
    rect = rendered.get_rect(**{anchor: (x, y)})
    surface.blit(rendered, rect)
    return rect


def wrap_text(text: str, font, max_width: int) -> List[str]:
    words = str(text).split()
    lines: List[str] = []
    line = ""
    for word in words:
        candidate = word if not line else line + " " + word
        if font.size(candidate)[0] <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines or [""]


def draw_wrapped(surface, text: str, font, color, rect: pygame.Rect, line_gap=5, align="left") -> int:
    y = rect.y
    for line in wrap_text(text, font, rect.width):
        if align == "center":
            draw_text(surface, line, font, color, rect.centerx, y, "midtop")
        else:
            draw_text(surface, line, font, color, rect.x, y)
        y += font.get_linesize() + line_gap
    return y


def rounded(surface, rect: pygame.Rect, color, radius=18, border=None, border_width=1):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, rect, border_width, border_radius=radius)


def draw_card(surface, rect: pygame.Rect, color=PANEL, accent=None, border=(65, 70, 112)):
    """Слегка приподнятая карточка с цветным бликом по верхнему краю."""
    shadow = rect.move(0, 6)
    rounded(surface, shadow, (10, 12, 28), 22)
    rounded(surface, rect, color, 22, border, 1)
    pygame.draw.line(surface, (88, 94, 143), (rect.x + 22, rect.y + 1), (rect.right - 22, rect.y + 1), 1)
    if accent:
        pygame.draw.line(surface, accent, (rect.x + 23, rect.y + 2), (rect.x + 98, rect.y + 2), 3)


def button(surface, rect: pygame.Rect, label: str, color, hovered=False, small=False):
    fill = tuple(min(255, int(ch * (1.12 if hovered else 1))) for ch in color)
    pygame.draw.rect(surface, (9, 11, 26), rect.move(0, 4), border_radius=14)
    rounded(surface, rect, fill, 14, (94, 94, 135), 1)
    pygame.draw.line(surface, tuple(min(255, c + 35) for c in fill), (rect.x + 15, rect.y + 2), (rect.right - 15, rect.y + 2), 2)
    font = FONT_MED if not small else FONT_SMALL
    draw_text(surface, label, font, WHITE, rect.centerx, rect.centery, "center")


def draw_background(ticks: int):
    screen.fill(BG)
    # Мягкие цветные пятна и крошечные мерцающие точки.
    pygame.draw.circle(screen, (28, 27, 58), (90, 120), 180)
    pygame.draw.circle(screen, (24, 43, 63), (1040, 690), 230)
    for i in range(24):
        x = (i * 173 + 31) % WIDTH
        y = (i * 97 + 17) % HEIGHT
        twinkle = 1 + int((math.sin(ticks * 0.002 + i) + 1) * 1.5)
        pygame.draw.circle(screen, (76, 80, 122), (x, y), twinkle)
    screen.blit(BACKGROUND, (0, 0))
    # Мерцающие звёзды и плавно дрейфующие пылинки добавляют глубину сцене.
    for x, y, phase, radius in STARS:
        pulse = (math.sin(ticks * 0.0017 + phase) + 1) * 0.5
        shade = int(58 + pulse * 92)
        pygame.draw.circle(screen, (shade // 2, shade // 2, shade), (x, y), radius)
    drift_x = int((ticks * 0.012) % (WIDTH + 100)) - 50
    pygame.draw.circle(screen, (46, 51, 91), (drift_x, 640), 2)
    pygame.draw.circle(screen, (48, 77, 101), ((drift_x + 425) % WIDTH, 114), 2)


def draw_phone(surface, center: Tuple[int, int], scale=1.0, wobble=0.0):
    x, y = center
    x += int(math.sin(pygame.time.get_ticks() / 250) * wobble)
    w, h = int(94 * scale), int(154 * scale)
    rect = pygame.Rect(x - w // 2, y - h // 2, w, h)
    rounded(surface, rect, (78, 65, 133), int(20 * scale), (191, 175, 255), max(2, int(3 * scale)))
    screen_rect = pygame.Rect(rect.x + int(9 * scale), rect.y + int(18 * scale), w - int(18 * scale), h - int(39 * scale))
    rounded(surface, screen_rect, (31, 36, 64), int(10 * scale))
    pygame.draw.circle(surface, CYAN, (x, y + h // 2 - int(12 * scale)), max(2, int(4 * scale)))
    pygame.draw.arc(surface, CYAN, pygame.Rect(x - int(21 * scale), y - int(25 * scale), int(42 * scale), int(42 * scale)), math.pi, math.pi * 2, max(2, int(3 * scale)))
    pygame.draw.arc(surface, CYAN, pygame.Rect(x - int(14 * scale), y - int(18 * scale), int(28 * scale), int(28 * scale)), math.pi, math.pi * 2, max(2, int(3 * scale)))
    pygame.draw.circle(surface, CYAN, (x, y - int(4 * scale)), max(2, int(4 * scale)))


def draw_avatar(surface, rect: pygame.Rect, character: Dict, pulse=0.0):
    cx, cy = rect.center
    radius = min(rect.width, rect.height) // 2
    glow = int(5 + (math.sin(pulse) + 1) * 3)
    pygame.draw.circle(surface, (48, 49, 83), (cx, cy), radius + glow)
    pygame.draw.circle(surface, character["color"], (cx, cy), radius)
    # Простой мультяшный персонаж без внешних изображений.
    pygame.draw.circle(surface, (255, 255, 255), (cx - radius // 3, cy - radius // 7), max(4, radius // 9))
    pygame.draw.circle(surface, (255, 255, 255), (cx + radius // 3, cy - radius // 7), max(4, radius // 9))
    pygame.draw.circle(surface, (35, 35, 54), (cx - radius // 3, cy - radius // 7), max(2, radius // 18))
    pygame.draw.circle(surface, (35, 35, 54), (cx + radius // 3, cy - radius // 7), max(2, radius // 18))
    pygame.draw.arc(surface, (75, 45, 65), pygame.Rect(cx - radius // 3, cy + radius // 8, radius * 2 // 3, radius // 2), 0, math.pi, 3)
    draw_text(surface, character["face"], FONT_SMALL, (55, 49, 76), cx, cy + radius - 8, "midbottom")
    scale = radius / 72
    bob = int(math.sin(pulse * 1.3) * 2 * scale)
    cy += bob
    glow = int((math.sin(pulse) + 1) * 3 * scale)
    pygame.draw.circle(surface, (7, 10, 25), (cx, cy + int(5 * scale)), radius + int(7 * scale))
    pygame.draw.circle(surface, (60, 62, 103), (cx, cy), radius + int(5 * scale) + glow, max(1, int(2 * scale)))
    pygame.draw.circle(surface, (character["color"]), (cx, cy), radius + int(2 * scale))
    pygame.draw.circle(surface, (255, 255, 255), (cx - int(17 * scale), cy - int(42 * scale)), max(2, int(2 * scale)))
    pygame.draw.circle(surface, (255, 255, 255), (cx + int(42 * scale), cy - int(9 * scale)), max(1, int(1.5 * scale)))

    # Персонажи — самостоятельные мультяшные портреты, нарисованные примитивами.
    if character["kind"] == "grandma":
        skin, hair = (255, 220, 185), (119, 90, 126)
        pygame.draw.circle(surface, hair, (cx, cy - int(17 * scale)), int(46 * scale))
        for dx, dy, r in [(-36, -34, 19), (-19, -49, 18), (4, -51, 20), (27, -42, 17), (40, -22, 14)]:
            pygame.draw.circle(surface, hair, (cx + int(dx * scale), cy + int(dy * scale)), int(r * scale))
        pygame.draw.ellipse(surface, skin, pygame.Rect(cx - int(38 * scale), cy - int(38 * scale), int(76 * scale), int(87 * scale)))
        pygame.draw.circle(surface, (250, 136, 151), (cx - int(26 * scale), cy + int(13 * scale)), int(7 * scale))
        pygame.draw.circle(surface, (250, 136, 151), (cx + int(26 * scale), cy + int(13 * scale)), int(7 * scale))
        for dx in (-18, 18):
            pygame.draw.circle(surface, (255, 255, 255), (cx + int(dx * scale), cy - int(7 * scale)), int(10 * scale))
            pygame.draw.circle(surface, (46, 43, 67), (cx + int(dx * scale), cy - int(7 * scale)), int(4 * scale))
            pygame.draw.circle(surface, hair, (cx + int(dx * scale), cy - int(7 * scale)), int(13 * scale), max(1, int(2 * scale)))
        pygame.draw.circle(surface, (214, 139, 126), (cx, cy + int(7 * scale)), max(2, int(3 * scale)))
        pygame.draw.arc(surface, (132, 65, 89), pygame.Rect(cx - int(12 * scale), cy + int(10 * scale), int(24 * scale), int(15 * scale)), 0, math.pi, max(1, int(2 * scale)))
        pygame.draw.arc(surface, (244, 112, 154), pygame.Rect(cx - int(37 * scale), cy + int(36 * scale), int(74 * scale), int(37 * scale)), math.pi, math.tau, max(2, int(8 * scale)))

    elif character["kind"] == "fridge":
        body = pygame.Rect(cx - int(43 * scale), cy - int(58 * scale), int(86 * scale), int(116 * scale))
        rounded(surface, body, (218, 239, 246), int(15 * scale), (113, 163, 188), max(1, int(2 * scale)))
        pygame.draw.line(surface, (140, 182, 198), (body.x + 3, cy - int(12 * scale)), (body.right - 3, cy - int(12 * scale)), max(1, int(2 * scale)))
        pygame.draw.line(surface, (127, 165, 184), (cx + int(29 * scale), cy - int(1 * scale)), (cx + int(29 * scale), cy + int(26 * scale)), max(2, int(4 * scale)))
        for dx in (-15, 12):
            pygame.draw.ellipse(surface, WHITE, pygame.Rect(cx + int((dx - 6) * scale), cy - int(35 * scale), int(13 * scale), int(17 * scale)))
            pygame.draw.circle(surface, (39, 69, 94), (cx + int((dx + 1) * scale), cy - int(27 * scale)), max(2, int(3 * scale)))
        pygame.draw.arc(surface, (56, 110, 136), pygame.Rect(cx - int(13 * scale), cy - int(2 * scale), int(27 * scale), int(19 * scale)), 0, math.pi, max(1, int(2 * scale)))
        # Снежинка на дверце.
        sx, sy = cx - int(22 * scale), cy + int(31 * scale)
        pygame.draw.line(surface, CYAN, (sx - int(7 * scale), sy), (sx + int(7 * scale), sy), max(1, int(2 * scale)))
        pygame.draw.line(surface, CYAN, (sx, sy - int(7 * scale)), (sx, sy + int(7 * scale)), max(1, int(2 * scale)))
        pygame.draw.line(surface, CYAN, (sx - int(5 * scale), sy - int(5 * scale)), (sx + int(5 * scale), sy + int(5 * scale)), max(1, int(2 * scale)))

    elif character["kind"] == "cat":
        pygame.draw.polygon(surface, (160, 112, 160), [(cx - int(43 * scale), cy - int(22 * scale)), (cx - int(39 * scale), cy - int(61 * scale)), (cx - int(8 * scale), cy - int(39 * scale))])
        pygame.draw.polygon(surface, (160, 112, 160), [(cx + int(8 * scale), cy - int(39 * scale)), (cx + int(39 * scale), cy - int(61 * scale)), (cx + int(44 * scale), cy - int(19 * scale))])
        pygame.draw.polygon(surface, (247, 168, 197), [(cx - int(34 * scale), cy - int(30 * scale)), (cx - int(37 * scale), cy - int(51 * scale)), (cx - int(20 * scale), cy - int(37 * scale))])
        pygame.draw.polygon(surface, (247, 168, 197), [(cx + int(20 * scale), cy - int(37 * scale)), (cx + int(37 * scale), cy - int(51 * scale)), (cx + int(36 * scale), cy - int(29 * scale))])
        pygame.draw.circle(surface, (234, 177, 207), (cx, cy), int(43 * scale))
        for dx in (-17, 17):
            pygame.draw.ellipse(surface, (228, 247, 172), pygame.Rect(cx + int((dx - 7) * scale), cy - int(12 * scale), int(14 * scale), int(20 * scale)))
            pygame.draw.ellipse(surface, (44, 49, 66), pygame.Rect(cx + int((dx - 2) * scale), cy - int(10 * scale), int(4 * scale), int(15 * scale)))
        pygame.draw.polygon(surface, (128, 73, 103), [(cx, cy + int(6 * scale)), (cx - int(6 * scale), cy), (cx + int(6 * scale), cy)])
        pygame.draw.line(surface, (114, 74, 101), (cx, cy + int(6 * scale)), (cx, cy + int(12 * scale)), max(1, int(2 * scale)))
        for dy in (3, 10):
            pygame.draw.line(surface, (114, 74, 101), (cx - int(12 * scale), cy + int(dy * scale)), (cx - int(37 * scale), cy + int((dy - 4) * scale)), max(1, int(1.5 * scale)))
            pygame.draw.line(surface, (114, 74, 101), (cx + int(12 * scale), cy + int(dy * scale)), (cx + int(37 * scale), cy + int((dy - 4) * scale)), max(1, int(1.5 * scale)))
        pygame.draw.polygon(surface, YELLOW, [(cx, cy + int(45 * scale)), (cx - int(13 * scale), cy + int(25 * scale)), (cx + int(13 * scale), cy + int(25 * scale))])

    elif character["kind"] == "pigeon":
        pygame.draw.ellipse(surface, (112, 142, 174), pygame.Rect(cx - int(39 * scale), cy - int(14 * scale), int(67 * scale), int(56 * scale)))
        pygame.draw.ellipse(surface, (177, 193, 211), pygame.Rect(cx - int(28 * scale), cy - int(7 * scale), int(44 * scale), int(32 * scale)))
        pygame.draw.circle(surface, (132, 163, 190), (cx + int(18 * scale), cy - int(29 * scale)), int(25 * scale))
        pygame.draw.circle(surface, (220, 225, 232), (cx + int(25 * scale), cy - int(34 * scale)), int(8 * scale))
        pygame.draw.circle(surface, (39, 47, 61), (cx + int(28 * scale), cy - int(34 * scale)), max(2, int(4 * scale)))
        pygame.draw.polygon(surface, (245, 167, 97), [(cx + int(37 * scale), cy - int(26 * scale)), (cx + int(59 * scale), cy - int(19 * scale)), (cx + int(39 * scale), cy - int(13 * scale))])
        pygame.draw.line(surface, (214, 139, 97), (cx - int(10 * scale), cy + int(36 * scale)), (cx - int(13 * scale), cy + int(51 * scale)), max(1, int(2 * scale)))
        pygame.draw.line(surface, (214, 139, 97), (cx + int(10 * scale), cy + int(36 * scale)), (cx + int(13 * scale), cy + int(51 * scale)), max(1, int(2 * scale)))
        pygame.draw.arc(surface, (89, 125, 155), pygame.Rect(cx - int(16 * scale), cy - int(3 * scale), int(30 * scale), int(33 * scale)), 0, math.pi, max(1, int(2 * scale)))

    elif character["kind"] == "printer":
        paper = pygame.Rect(cx - int(25 * scale), cy - int(57 * scale), int(50 * scale), int(48 * scale))
        rounded(surface, paper, (249, 248, 239), int(3 * scale))
        for line in range(3):
            pygame.draw.line(surface, (178, 180, 196), (paper.x + int(8 * scale), paper.y + int((12 + line * 9) * scale)), (paper.right - int(7 * scale), paper.y + int((12 + line * 9) * scale)), max(1, int(1 * scale)))
        body = pygame.Rect(cx - int(49 * scale), cy - int(28 * scale), int(98 * scale), int(75 * scale))
        rounded(surface, body, (209, 208, 229), int(13 * scale), (127, 123, 168), max(1, int(2 * scale)))
        pygame.draw.rect(surface, (76, 82, 124), pygame.Rect(cx - int(37 * scale), cy - int(20 * scale), int(74 * scale), int(34 * scale)), border_radius=int(7 * scale))
        for dx in (-13, 13):
            pygame.draw.circle(surface, CYAN, (cx + int(dx * scale), cy - int(4 * scale)), max(2, int(5 * scale)))
        pygame.draw.arc(surface, WHITE, pygame.Rect(cx - int(13 * scale), cy + int(1 * scale), int(26 * scale), int(14 * scale)), 0, math.pi, max(1, int(2 * scale)))
        pygame.draw.rect(surface, (245, 245, 252), pygame.Rect(cx - int(30 * scale), cy + int(25 * scale), int(60 * scale), int(20 * scale)), border_radius=int(3 * scale))
        pygame.draw.circle(surface, GREEN, (cx + int(35 * scale), cy + int(20 * scale)), max(2, int(4 * scale)))

    else:  # Луна
        pygame.draw.circle(surface, (255, 239, 181), (cx, cy), int(48 * scale))
        pygame.draw.circle(surface, (238, 205, 143), (cx - int(17 * scale), cy - int(14 * scale)), int(9 * scale))
        pygame.draw.circle(surface, (238, 205, 143), (cx + int(24 * scale), cy + int(14 * scale)), int(13 * scale))
        pygame.draw.circle(surface, (238, 205, 143), (cx - int(23 * scale), cy + int(25 * scale)), int(5 * scale))
        for dx in (-16, 16):
            pygame.draw.arc(surface, (83, 72, 92), pygame.Rect(cx + int((dx - 7) * scale), cy - int(8 * scale), int(14 * scale), int(12 * scale)), math.pi, math.tau, max(1, int(2 * scale)))
        pygame.draw.arc(surface, (157, 99, 102), pygame.Rect(cx - int(12 * scale), cy + int(10 * scale), int(24 * scale), int(14 * scale)), 0, math.pi, max(1, int(2 * scale)))
        # Маленькие орбитальные звёздочки.
        for angle in (pulse * 0.35, pulse * 0.35 + math.pi):
            sx = cx + int(math.cos(angle) * radius * 0.8)
            sy = cy + int(math.sin(angle) * radius * 0.8)
            pygame.draw.circle(surface, WHITE, (sx, sy), max(1, int(2 * scale)))


def draw_meter(surface, rect: pygame.Rect, value: float, ticks: int):
    rounded(surface, rect, (14, 17, 35), 12, (68, 72, 108), 1)
    inner = rect.inflate(-8, -8)
    fill_w = int(inner.width * max(0, min(100, value)) / 100)
    if fill_w:
        color = GREEN if value < 55 else YELLOW if value < 80 else RED
        if value >= 80 and (ticks // 250) % 2:
            color = (255, 139, 129)
        fill_rect = pygame.Rect(inner.x, inner.y, max(0, fill_w), inner.height)
        rounded(surface, fill_rect, color, 8)


def new_game():
    return {
        "score": 0, "suspicion": 12.0, "time_left": 75.0,
        "state": "ready", "character": random.choice(CHARACTERS),
        "line": "", "reply": "", "last_event": "Первый звонок готов. Выбирай максимально нелепый ответ!",
        "event_color": CYAN, "call_count": 0, "streak": 0, "last_gain": 0,
        "particles": [], "call_started": False,
    }


def choose_character(game):
    choices = [item for item in CHARACTERS if item is not game["character"]]
    game["character"] = random.choice(choices)
    game["state"] = "ready"
    game["line"] = ""
    game["reply"] = ""
    game["call_started"] = False
    game["last_event"] = "Следующий персонаж уже снял трубку… почти."
    game["event_color"] = CYAN


def make_particles(game, x, y, color, count=12):
    for _ in range(count):
        game["particles"].append({
            "x": x + random.randint(-25, 25), "y": y + random.randint(-15, 15),
            "vx": random.uniform(-55, 55), "vy": random.uniform(-110, -35),
            "life": random.uniform(0.55, 1.05), "color": color,
        })


def start_call(game):
    game["state"] = "choosing"
    game["call_started"] = True
    game["last_event"] = "На линии: " + game["character"]["hello"]
    game["event_color"] = CYAN


def answer(game, choice_index):
    char = game["character"]
    option = char["options"][choice_index]
    phrase, absurdity, risk = option
    game["line"] = phrase
    chance = max(0.20, min(0.93, 0.48 + absurdity * 0.16 - risk * 0.035))
    success = random.random() < chance
    game["call_count"] += 1
    if success:
        game["streak"] += 1
        points = 10 + absurdity * 4 + min(game["streak"], 5) * 2
        game["score"] += points
        game["last_gain"] = points
        game["suspicion"] = max(0, game["suspicion"] + risk - 7 - absurdity * 0.7)
        game["reply"] = random.choice(char["yes"])
        game["last_event"] = f"МЕМ УДАЛСЯ! +{points} мем-баллов. " + game["reply"]
        game["event_color"] = GREEN
        make_particles(game, 470, 350, GREEN)
    else:
        game["streak"] = 0
        game["last_gain"] = 0
        game["suspicion"] = min(100, game["suspicion"] + 10 + risk * 0.7)
        game["reply"] = random.choice(char["no"])
        game["last_event"] = "Собеседник насторожился. " + game["reply"]
        game["event_color"] = YELLOW
        make_particles(game, 470, 350, YELLOW, 7)

    # Иногда в разговор вмешивается совершенно посторонний предмет.
    if random.random() < 0.26:
        event, score_delta, suspicion_delta = random.choice(RANDOM_EVENTS)
        game["score"] = max(0, game["score"] + score_delta)
        game["suspicion"] = max(0, min(100, game["suspicion"] + suspicion_delta))
        game["last_event"] += "  " + event
    game["suspicion"] = max(0, min(100, game["suspicion"]))
    game["state"] = "result"


def draw_start(ticks):
    draw_background(ticks)
    # Декоративные мультяшные орбиты вокруг телефона.
    # Декоративная орбита, абоненты и мягко пульсирующие кольца вызова.
    pulse = (math.sin(ticks * 0.004) + 1) * 0.5
    for ring in range(3):
        radius = int(88 + ring * 27 + pulse * 5)
        pygame.draw.circle(screen, (47 + ring * 7, 52 + ring * 6, 94 + ring * 7), (850, 290), radius, 1)
    pygame.draw.ellipse(screen, (70, 69, 116), pygame.Rect(720, 185, 265, 210), 2)
    pygame.draw.ellipse(screen, (70, 69, 116), pygame.Rect(750, 155, 210, 270), 2)
    draw_phone(screen, (850, 290), 1.35, 3)
    for index, (px, py) in enumerate(((724, 245), (979, 197), (986, 373))):
        badge = pygame.Rect(px - 31, py - 31, 62, 62)
        pygame.draw.circle(screen, (14, 17, 37), (px, py + 3), 36)
        draw_avatar(screen, badge, CHARACTERS[(index * 2 + 1) % len(CHARACTERS)], ticks * 0.003 + index)
    draw_text(screen, "КОМИЧЕСКАЯ ПАРОДИЯ", FONT_SMALL, CYAN, 72, 94)
    draw_text(screen, "Алло, это", FONT_TITLE, WHITE, 70, 145)
    draw_text(screen, "мемный отдел?", FONT_TITLE, PURPLE, 70, 204)
    draw_wrapped(screen, "Ты — вымышленный агент абсурда. Звони странным персонажам и отвечай так нелепо, чтобы даже холодильник рассмеялся.", FONT, MUTED, pygame.Rect(76, 304, 575, 94), 8)
    rounded(screen, pygame.Rect(72, 430, 556, 112), PANEL, 18, (66, 72, 114), 1)
    draw_card(screen, pygame.Rect(72, 430, 556, 112), PANEL, CYAN)
    draw_text(screen, "ЦЕЛЬ РАУНДА", FONT_SMALL, YELLOW, 94, 447)
    draw_wrapped(screen, "Набирай мем-баллы, следи за таймером и не заполняй шкалу подозрительности — иначе придёт вымышленная полиция мемов.", FONT_SMALL, WHITE, pygame.Rect(94, 474, 515, 58), 4)
    start_rect = pygame.Rect(74, 586, 305, 60)
    button(screen, start_rect, "НАЧАТЬ ИГРУ  [ENTER]", PURPLE, start_rect.collidepoint(pygame.mouse.get_pos()))
    # Три маленькие метки объясняют тон игры, не перегружая экран текстом.
    for i, (label, color) in enumerate((("6 АБОНЕНТОВ", CYAN), ("75 СЕКУНД", YELLOW), ("100% АБСУРДА", PINK))):
        x = 674 + i * 137
        chip = pygame.Rect(x, 566, 127, 32)
        rounded(screen, chip, (31, 34, 62), 12, (68, 72, 112), 1)
        pygame.draw.circle(screen, color, (chip.x + 13, chip.centery), 4)
        draw_text(screen, label, FONT_SMALL, WHITE, chip.x + 24, chip.centery, "midleft")
    draw_text(screen, "Выбор ответа: клавиши 1–3 или клик мышью", FONT_SMALL, MUTED, 75, 670)
    draw_text(screen, "Только вымышленные персонажи и абсурдные реплики", FONT_SMALL, MUTED, 75, 696)
    return start_rect


def draw_game(game, ticks):
    draw_background(ticks)
    # Верхняя панель
    pygame.draw.circle(screen, PURPLE, (49, 42), 17)
    draw_phone(screen, (49, 42), 0.19, 0)
    draw_text(screen, "АЛЛО, ЭТО МЕМНЫЙ ОТДЕЛ?", FONT_MED, WHITE, 38, 25)
    draw_text(screen, "КОМИЧЕСКАЯ ПАРОДИЯ", FONT_SMALL, CYAN, 40, 57)
    rounded(screen, pygame.Rect(630, 22, 212, 62), PANEL, 14)
    draw_text(screen, "АЛЛО, ЭТО МЕМНЫЙ ОТДЕЛ?", FONT_MED, WHITE, 72, 25)
    draw_text(screen, "КОМИЧЕСКАЯ ПАРОДИЯ", FONT_SMALL, CYAN, 74, 57)
    draw_card(screen, pygame.Rect(630, 22, 212, 62), PANEL, YELLOW)
    draw_text(screen, "МЕМ-БАЛЛЫ", FONT_SMALL, MUTED, 649, 30)
    draw_text(screen, f"{game['score']:04d}", FONT_MED, YELLOW, 649, 49)
    rounded(screen, pygame.Rect(859, 22, 220, 62), PANEL, 14)
    draw_card(screen, pygame.Rect(859, 22, 220, 62), PANEL, CYAN)
    draw_text(screen, "ВРЕМЯ", FONT_SMALL, MUTED, 879, 30)
    remain = max(0, int(game["time_left"]))
    draw_text(screen, f"{remain // 60:02d}:{remain % 60:02d}", FONT_MED, WHITE, 879, 49)
    draw_meter(screen, pygame.Rect(40, 94, 1040, 9), 100 * game["time_left"] / 75, ticks)
    pygame.draw.rect(screen, (38, 42, 77), pygame.Rect(40, 96, 1040, 7), border_radius=4)
    time_color = CYAN if game["time_left"] > 20 else YELLOW if game["time_left"] > 8 else RED
    time_width = int(1036 * game["time_left"] / 75)
    if time_width:
        pygame.draw.rect(screen, time_color, pygame.Rect(42, 97, time_width, 5), border_radius=3)

    # Левая карточка звонка
    card = pygame.Rect(40, 126, 700, 386)
    rounded(screen, card, PANEL, 22, (65, 70, 112), 1)
    draw_card(screen, card, PANEL, PURPLE)
    char = game["character"]
    avatar_rect = pygame.Rect(76, 164, 156, 156)
    draw_avatar(screen, avatar_rect, char, ticks * 0.004)
    draw_text(screen, char["name"], FONT_MED, WHITE, 264, 165)
    draw_text(screen, char["role"], FONT_SMALL, MUTED, 266, 202)
    status = "ГОТОВ К ЗВОНКУ" if game["state"] == "ready" else "НА ЛИНИИ" if game["state"] == "choosing" else "РАЗГОВОР ЗАВЕРШЁН"
    status = "НАБОР ГОТОВ" if game["state"] == "ready" else "НА ЛИНИИ" if game["state"] == "choosing" else "ГОТОВО"
    status_color = CYAN if game["state"] != "result" else GREEN
    rounded(screen, pygame.Rect(264, 235, 170, 29), (40, 56, 77), 12)
    pulse_r = 4 + int((math.sin(ticks * 0.008) + 1) * 1.5)
    pygame.draw.circle(screen, status_color, (279, 249), pulse_r)
    draw_text(screen, status, FONT_SMALL, status_color, 349, 249, "center")
    draw_text(screen, status, FONT_SMALL, status_color, 357, 249, "center")
    # Маленькая маркировка «эфира» и бегущий индикатор связи.
    draw_text(screen, f"ЗВОНОК № {game['call_count'] + 1:02d}", FONT_SMALL, (125, 130, 169), 680, 165, "topright")
    for bar in range(5):
        bar_h = 6 + int((math.sin(ticks * 0.009 + bar * 0.8) + 1) * 5) if game["state"] == "choosing" else 4
        pygame.draw.rect(screen, CYAN if game["state"] == "choosing" else (74, 81, 124), pygame.Rect(674 + bar * 6, 242 - bar_h // 2, 3, bar_h), border_radius=2)

    if game["state"] == "ready":
        bubble = pygame.Rect(76, 344, 628, 92)
        rounded(screen, bubble, PANEL_LIGHT, 16)
        draw_text(screen, "Новый абонент обнаружен!", FONT_MED, WHITE, bubble.x + 22, bubble.y + 16)
        draw_text(screen, "Нажми кнопку, чтобы начать безопасный мемный диалог.", FONT_SMALL, MUTED, bubble.x + 22, bubble.y + 54)
        call_rect = pygame.Rect(215, 453, 350, 43)
        button(screen, call_rect, "ПОЗВОНИТЬ  [E]", PURPLE, call_rect.collidepoint(pygame.mouse.get_pos()), True)
    elif game["state"] == "choosing":
        bubble = pygame.Rect(76, 342, 628, 148)
        rounded(screen, bubble, PANEL_LIGHT, 16)
        draw_text(screen, "АБОНЕНТ ГОВОРИТ:", FONT_SMALL, CYAN, bubble.x + 20, bubble.y + 14)
        draw_wrapped(screen, char["hello"], FONT, WHITE, pygame.Rect(bubble.x + 20, bubble.y + 43, bubble.width - 40, 80), 5)
        call_rect = None
    else:
        bubble = pygame.Rect(76, 342, 628, 148)
        rounded(screen, bubble, PANEL_LIGHT, 16)
        draw_text(screen, "ТВОЙ ОТВЕТ:", FONT_SMALL, CYAN, bubble.x + 20, bubble.y + 12)
        draw_wrapped(screen, game["line"], FONT_SMALL, WHITE, pygame.Rect(bubble.x + 20, bubble.y + 36, bubble.width - 40, 42), 2)
        draw_text(screen, "ПЕРСОНАЖ ОТВЕЧАЕТ:", FONT_SMALL, YELLOW, bubble.x + 20, bubble.y + 83)
        draw_wrapped(screen, game["reply"], FONT_SMALL, WHITE, pygame.Rect(bubble.x + 20, bubble.y + 106, bubble.width - 40, 39), 2)
        call_rect = pygame.Rect(215, 453, 350, 43)
        button(screen, call_rect, "СЛЕДУЮЩИЙ ЗВОНОК  [E]", CYAN, call_rect.collidepoint(pygame.mouse.get_pos()), True)

    # Шкала справа
    meter_card = pygame.Rect(760, 126, 320, 386)
    rounded(screen, meter_card, PANEL, 22, (65, 70, 112), 1)
    draw_card(screen, meter_card, PANEL, RED if game["suspicion"] >= 70 else CYAN)
    draw_text(screen, "ПОДОЗРИТЕЛЬНОСТЬ", FONT_SMALL, MUTED, 784, 153)
    draw_text(screen, f"{int(game['suspicion'])}%", FONT_BIG, RED if game["suspicion"] >= 70 else CYAN, 784, 181)
    draw_meter(screen, pygame.Rect(784, 251, 270, 22), game["suspicion"], ticks)
    # Тонкие деления помогают считывать приближение к критической отметке.
    for marker in (25, 50, 75):
        mx = 788 + int(262 * marker / 100)
        pygame.draw.line(screen, (25, 28, 51), (mx, 257), (mx, 267), 2)
    draw_text(screen, "МЕМ-ПОЛИЦИЯ", FONT_SMALL, MUTED, 784, 301)
    draw_wrapped(screen, "Если шкала заполнится — раунд закончится, а вам выпишут штраф в один смешной носок.", FONT_SMALL, WHITE, pygame.Rect(784, 328, 262, 70), 5)
    pygame.draw.circle(screen, (49, 47, 82), (918, 452), 38)
    draw_text(screen, "!", FONT_BIG, RED if game["suspicion"] >= 70 else YELLOW, 918, 452, "center")
    draw_text(screen, "СЕРИЯ МЕМОВ", FONT_SMALL, MUTED, 784, 403)
    draw_text(screen, f"×{game['streak']}", FONT_MED, YELLOW if game["streak"] else MUTED, 1048, 400, "topright")
    for dot in range(5):
        dot_color = (PURPLE if dot < game["streak"] else (54, 58, 92))
        pygame.draw.circle(screen, dot_color, (795 + dot * 24, 433), 7)
        if dot < game["streak"]:
            pygame.draw.circle(screen, (218, 205, 255), (795 + dot * 24, 433), 2)
    badge_y = 474 + int(math.sin(ticks * 0.003) * 2)
    shield = [(918, badge_y - 25), (943, badge_y - 15), (939, badge_y + 11), (918, badge_y + 27), (897, badge_y + 11), (893, badge_y - 15)]
    pygame.draw.polygon(screen, (52, 48, 84), shield)
    pygame.draw.polygon(screen, RED if game["suspicion"] >= 70 else YELLOW, shield, 2)
    pygame.draw.circle(screen, WHITE, (911, badge_y - 2), 3)
    pygame.draw.circle(screen, WHITE, (925, badge_y - 2), 3)
    pygame.draw.arc(screen, WHITE, pygame.Rect(908, badge_y + 1, 20, 12), math.pi, math.tau, 2)

    # Подсказки выбора
    draw_text(screen, "ВЫБЕРИ ОТВЕТ", FONT_SMALL, MUTED, 44, 529)
    draw_text(screen, "ВЫБЕРИ ОТВЕТ", FONT_SMALL, WHITE, 44, 529)
    draw_text(screen, "1–3 на клавиатуре или нажми карточку", FONT_SMALL, MUTED, 1076, 529, "topright")
    option_rects: List[pygame.Rect] = []
    option_colors = (PURPLE, CYAN, PINK)
    for i, option in enumerate(char["options"]):
        x = 40 + i * 355
        rect = pygame.Rect(x, 556, 340, 112)
        option_rects.append(rect)
        if game["state"] == "choosing":
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            rounded(screen, rect, PANEL_LIGHT if not hovered else (53, 55, 91), 16, PURPLE if hovered else (71, 75, 115), 2 if hovered else 1)
            key_box = pygame.Rect(x + 13, 569, 31, 31)
            rounded(screen, key_box, PURPLE, 9)
            accent = option_colors[i]
            if hovered:
                pygame.draw.rect(screen, (8, 10, 24), rect.move(0, 5), border_radius=18)
            rounded(screen, rect.move(0, 3), (10, 12, 28), 16)
            rounded(screen, rect, PANEL_LIGHT if not hovered else (53, 55, 91), 16, accent if hovered else (71, 75, 115), 2 if hovered else 1)
            pygame.draw.line(screen, accent, (rect.x + 18, rect.y + 2), (rect.x + 87, rect.y + 2), 3)
            key_box = pygame.Rect(x + 13, 571, 34, 34)
            rounded(screen, key_box, accent, 10)
            draw_text(screen, str(i + 1), FONT_SMALL, WHITE, key_box.centerx, key_box.centery, "center")
            draw_wrapped(screen, option[0], FONT_SMALL, WHITE, pygame.Rect(x + 54, 567, 271, 77), 4)
            draw_wrapped(screen, option[0], FONT_SMALL, WHITE, pygame.Rect(x + 58, 568, 267, 76), 4)
            draw_text(screen, "АБСУРДНЫЙ ОТВЕТ", FONT_SMALL, accent, x + 58, 637)
        else:
            rounded(screen, rect, (25, 28, 51), 16, (52, 57, 91), 1)
            rounded(screen, pygame.Rect(x + 13, 571, 34, 34), (41, 44, 72), 10)
            draw_text(screen, f"{i + 1}", FONT_SMALL, (103, 108, 142), x + 24, 570)
            draw_text(screen, "Ответ появится во время звонка", FONT_SMALL, (103, 108, 142), x + 54, 574)
            draw_text(screen, f"{i + 1}", FONT_SMALL, (103, 108, 142), x + 30, 588, "center")
            draw_text(screen, "Ответ появится во время звонка", FONT_SMALL, (103, 108, 142), x + 58, 579)

    # Событие разговора в нижней строке
    event_rect = pygame.Rect(40, 690, 1040, 42)
    rounded(screen, event_rect, (25, 28, 51), 12)
    draw_wrapped(screen, game["last_event"], FONT_SMALL, game["event_color"], pygame.Rect(56, 699, 1005, 32), 1)
    rounded(screen, event_rect, (25, 28, 51), 12, (52, 57, 91), 1)
    pygame.draw.circle(screen, game["event_color"], (58, 711), 5)
    draw_wrapped(screen, game["last_event"], FONT_SMALL, game["event_color"], pygame.Rect(72, 699, 985, 32), 1)

    # Мелкие анимированные мем-конфетти
    for particle in game["particles"]:
        pygame.draw.circle(screen, particle["color"], (int(particle["x"]), int(particle["y"])), max(1, int(4 * particle["life"])))
    return option_rects, call_rect


def draw_end(game, ticks, reason):
    draw_background(ticks)
    phone_center = (845, 315)
    draw_phone(screen, phone_center, 1.2, 1.5)
    phone_center = (838, 306)
    # Финальная сцена: телефон, победивший (или настороженный) абонент и конфетти.
    for ring in range(3):
        pygame.draw.circle(screen, (45 + ring * 7, 51 + ring * 6, 90 + ring * 8), (930, 315), 92 + ring * 25, 1)
    draw_phone(screen, phone_center, 1.15, 2)
    draw_avatar(screen, pygame.Rect(918, 245, 146, 146), game["character"], ticks * 0.004)
    for i in range(18):
        x = 760 + (i * 71 + ticks // 17) % 330
        y = 140 + (i * 47 + ticks // 23) % 340
        color = (PURPLE, CYAN, PINK, YELLOW)[i % 4]
        pygame.draw.circle(screen, color, (x, y), 2 + i % 2)
    draw_text(screen, "РАУНД ЗАВЕРШЁН", FONT_SMALL, CYAN, 78, 104)
    if reason == "suspicion":
        draw_text(screen, "Мем-полиция", FONT_TITLE, (32, 18, 39), 80, 162)
        draw_text(screen, "Мем-полиция", FONT_TITLE, RED, 76, 157)
        draw_text(screen, "вышла на связь!", FONT_TITLE, (32, 18, 39), 80, 223)
        draw_text(screen, "вышла на связь!", FONT_TITLE, WHITE, 76, 218)
        detail = "Они конфисковали скуку и выписали штраф в один смешной носок."
    else:
        draw_text(screen, "Время вышло!", FONT_TITLE, (32, 18, 39), 80, 162)
        draw_text(screen, "Время вышло!", FONT_TITLE, WHITE, 76, 157)
        draw_text(screen, "Но мемы остались.", FONT_TITLE, (32, 18, 39), 80, 223)
        draw_text(screen, "Но мемы остались.", FONT_TITLE, PURPLE, 76, 218)
        detail = "Последний абонент попросил перезвонить после следующего затмения."
    draw_wrapped(screen, detail, FONT, MUTED, pygame.Rect(82, 312, 560, 60), 6)
    rounded(screen, pygame.Rect(77, 408, 565, 105), PANEL, 18, (67, 72, 114), 1)
    draw_card(screen, pygame.Rect(77, 408, 565, 105), PANEL, YELLOW)
    draw_text(screen, "ИТОГОВЫЙ СЧЁТ", FONT_SMALL, MUTED, 101, 427)
    draw_text(screen, f"{game['score']}", FONT_BIG, YELLOW, 101, 452)
    draw_text(screen, f"звонков: {game['call_count']}     подозрительность: {int(game['suspicion'])}%", FONT_SMALL, WHITE, 286, 467)
    pygame.draw.line(screen, (74, 78, 117), (286, 488), (604, 488), 1)
    draw_text(screen, "ПОСЛЕДНИЙ АБОНЕНТ", FONT_SMALL, MUTED, 286, 427)
    draw_text(screen, game["character"]["name"], FONT_SMALL, CYAN, 286, 447)
    restart = pygame.Rect(80, 565, 280, 60)
    menu = pygame.Rect(378, 565, 245, 60)
    button(screen, restart, "ЕЩЁ РАУНД  [R]", PURPLE, restart.collidepoint(pygame.mouse.get_pos()))
    button(screen, menu, "В МЕНЮ  [ENTER]", PANEL_LIGHT, menu.collidepoint(pygame.mouse.get_pos()))
    draw_text(screen, "Вымышленная комедия. Никаких реальных схем или данных.", FONT_SMALL, MUTED, 82, 660)
    return restart, menu


def main():
    screen_name = "start"
    game = new_game()
    end_reason = "time"
    running = True

    while running:
        dt = min(clock.tick(60) / 1000.0, 0.05)
        ticks = pygame.time.get_ticks()
        mouse = pygame.mouse.get_pos()
        start_rect = restart_rect = menu_rect = None
        option_rects: List[pygame.Rect] = []
        call_rect = None

        if screen_name == "start":
            start_rect = draw_start(ticks)
        elif screen_name == "game":
            game["time_left"] -= dt
            if game["time_left"] <= 0:
                game["time_left"] = 0
                screen_name, end_reason = "end", "time"
            elif game["suspicion"] >= 100:
                screen_name, end_reason = "end", "suspicion"

            for particle in game["particles"]:
                particle["x"] += particle["vx"] * dt
                particle["y"] += particle["vy"] * dt
                particle["vy"] += 125 * dt
                particle["life"] -= dt
            game["particles"] = [p for p in game["particles"] if p["life"] > 0]
            option_rects, call_rect = draw_game(game, ticks)
        else:
            restart_rect, menu_rect = draw_end(game, ticks, end_reason)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if screen_name == "game":
                        screen_name = "start"
                    else:
                        running = False
                elif screen_name == "start" and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    game = new_game()
                    screen_name = "game"
                elif screen_name == "game":
                    if event.key == pygame.K_e:
                        if game["state"] == "ready":
                            start_call(game)
                        elif game["state"] == "result":
                            choose_character(game)
                    elif game["state"] == "choosing" and event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        answer(game, event.key - pygame.K_1)
                    elif event.key == pygame.K_RETURN and game["state"] == "ready":
                        start_call(game)
                elif screen_name == "end":
                    if event.key == pygame.K_r:
                        game = new_game()
                        screen_name = "game"
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        screen_name = "start"
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if screen_name == "start" and start_rect and start_rect.collidepoint(event.pos):
                    game = new_game()
                    screen_name = "game"
                elif screen_name == "game":
                    if game["state"] == "choosing":
                        for i, rect in enumerate(option_rects):
                            if rect.collidepoint(event.pos):
                                answer(game, i)
                                break
                    elif call_rect and call_rect.collidepoint(event.pos):
                        if game["state"] == "ready":
                            start_call(game)
                        elif game["state"] == "result":
                            choose_character(game)
                elif screen_name == "end":
                    if restart_rect and restart_rect.collidepoint(event.pos):
                        game = new_game()
                        screen_name = "game"
                    elif menu_rect and menu_rect.collidepoint(event.pos):
                        screen_name = "start"

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()