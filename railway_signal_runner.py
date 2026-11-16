
import math
import random
import sys
import pygame

pygame.init()

# ------------------------------------------------------------
# TRAIN SIGNAL RUNNER
# Controls:
#   P       - Pause / resume
#   R       - Restart after game over
#   SPACE   - Sound the train horn
#   ESC     - Quit
#
# GREEN  = Proceed at normal speed
# YELLOW = Slow down
# RED    = Stop before the signal
# ------------------------------------------------------------

WIDTH, HEIGHT = 1000, 600
FPS = 60
GROUND_Y = 430

SKY = (130, 200, 238)
WHITE = (245, 248, 250)
DARK = (35, 48, 61)
GRASS = (79, 145, 75)
RAIL = (75, 78, 82)
SLEEPER = (105, 73, 48)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Railway Signal Runner")
clock = pygame.time.Clock()

font = pygame.font.SysFont("verdana", 19, bold=True)
small_font = pygame.font.SysFont("verdana", 14)
big_font = pygame.font.SysFont("verdana", 42, bold=True)


def draw_text(surface, text, x, y, colour=WHITE, use_font=font):
    surface.blit(use_font.render(text, True, colour), (x, y))


class Train:
    def __init__(self):
        self.x = 650
        self.y = GROUND_Y - 26
        self.speed = 4.0
        self.target_speed = 4.0
        self.max_speed = 6.0
        self.rect = pygame.Rect(self.x - 90, self.y - 42, 180, 76)
        self.wheel_phase = 0.0
        self.horn_timer = 0

    def update(self, signal):
        if signal == "RED":
            self.target_speed = 0.0
        elif signal == "YELLOW":
            self.target_speed = 1.7
        else:
            self.target_speed = self.max_speed

        if self.speed < self.target_speed:
            self.speed = min(self.target_speed, self.speed + 0.045)
        elif self.speed > self.target_speed:
            self.speed = max(self.target_speed, self.speed - 0.12)

        self.wheel_phase += self.speed * 0.13
        self.rect.center = (self.x, self.y)

        if self.horn_timer > 0:
            self.horn_timer -= 1

    def draw(self, surface):
        x, y = self.x, self.y

        # Three passenger coaches
        for coach_x in (x - 180, x - 360, x - 540):
            left = coach_x - 85

            pygame.draw.rect(
                surface, (190, 48, 48),
                (left, y - 43, 170, 57),
                border_radius=8
            )

            pygame.draw.rect(
                surface, (135, 34, 38),
                (left + 3, y + 2, 164, 10),
                border_radius=3
            )

            pygame.draw.rect(
                surface, (65, 72, 82),
                (left + 7, y - 51, 156, 10),
                border_radius=5
            )

            # Coach windows
            for window_index in range(4):
                wx = left + 13 + window_index * 39

                pygame.draw.rect(
                    surface, (105, 190, 220),
                    (wx, y - 31, 29, 22),
                    border_radius=4
                )

                pygame.draw.line(
                    surface, (230, 245, 250),
                    (wx + 14, y - 30),
                    (wx + 14, y - 10), 2
                )

            # Coach door
            pygame.draw.rect(
                surface, (145, 35, 39),
                (left + 151, y - 37, 13, 39),
                border_radius=2
            )

            # Coach wheels
            for wx in (coach_x - 52, coach_x + 52):
                pygame.draw.circle(
                    surface, (35, 39, 44),
                    (wx, y + 17), 14
                )

                pygame.draw.circle(
                    surface, (175, 180, 184),
                    (wx, y + 17), 7
                )

                spoke_y = int(math.sin(self.wheel_phase) * 5)

                pygame.draw.line(
                    surface, (70, 75, 80),
                    (wx - 5, y + 17 - spoke_y),
                    (wx + 5, y + 17 + spoke_y), 2
                )

        # Couplers between coaches and locomotive
        for coupler_x in (x - 275, x - 95):
            pygame.draw.rect(
                surface, (45, 48, 52),
                (coupler_x, y + 5, 20, 7)
            )

        # Locomotive body
        pygame.draw.rect(
            surface, (190, 48, 48),
            (x - 91, y - 43, 166, 57),
            border_radius=10
        )

        pygame.draw.rect(
            surface, (135, 34, 38),
            (x - 91, y + 2, 166, 12),
            border_radius=4
        )

        # Front engine nose
        pygame.draw.polygon(
            surface, (210, 58, 53),
            [
                (x + 65, y - 43),
                (x + 104, y - 20),
                (x + 104, y + 13),
                (x + 65, y + 13)
            ]
        )

        pygame.draw.rect(
            surface, (80, 92, 104),
            (x + 83, y - 24, 17, 23),
            border_radius=3
        )

        # Locomotive windows
        for wx in (x - 70, x - 35, x):
            pygame.draw.rect(
                surface, (105, 190, 220),
                (wx, y - 31, 25, 22),
                border_radius=4
            )

            pygame.draw.line(
                surface, (230, 245, 250),
                (wx + 12, y - 30),
                (wx + 12, y - 10), 2
            )

        # Roof and headlight
        pygame.draw.rect(
            surface, (65, 72, 82),
            (x - 82, y - 51, 148, 10),
            border_radius=5
        )

        pygame.draw.circle(
            surface, (255, 238, 150),
            (x + 98, y - 4), 7
        )

        pygame.draw.circle(
            surface, (255, 255, 220),
            (x + 98, y - 4), 3
        )

        # Locomotive wheels
        for wx in (x - 60, x - 5, x + 53):
            pygame.draw.circle(
                surface, (35, 39, 44),
                (wx, y + 17), 14
            )

            pygame.draw.circle(
                surface, (175, 180, 184),
                (wx, y + 17), 7
            )

            spoke_y = int(math.sin(self.wheel_phase) * 5)

            pygame.draw.line(
                surface, (70, 75, 80),
                (wx - 5, y + 17 - spoke_y),
                (wx + 5, y + 17 + spoke_y), 2
            )

        pygame.draw.rect(
            surface, (45, 48, 52),
            (x + 103, y + 7, 18, 7)
        )

        # Horn effect
        if self.horn_timer > 0:
            pygame.draw.arc(
                surface, (255, 255, 255),
                (x + 95, y - 60, 35, 35),
                -1.1, 1.1, 3
            )


class Signal:
    COLORS = {
        "RED": (225, 45, 45),
        "YELLOW": (255, 195, 35),
        "GREEN": (35, 190, 80),
    }

    def __init__(self, x, state):
        self.x = float(x)
        self.state = state
        self.passed = False
        self.timer = random.randint(150, 230)

        self.rect = pygame.Rect(
            int(x - 16), GROUND_Y - 180, 32, 150
        )

    def update(self, world_speed):
        self.x -= world_speed
        self.rect.x = int(self.x - 16)

        self.timer -= 1

        if self.timer <= 0:
            sequence = ["RED", "GREEN", "YELLOW"]

            self.state = sequence[
                (sequence.index(self.state) + 1) % len(sequence)
            ]

            self.timer = {
                "RED": 180,
                "GREEN": 240,
                "YELLOW": 90
            }[self.state]

    def draw(self, surface):
        x = int(self.x)
        pole_top = GROUND_Y - 175

        pygame.draw.rect(
            surface, (75, 79, 83),
            (x - 5, pole_top, 10, 178)
        )

        pygame.draw.rect(
            surface, (45, 49, 54),
            (x - 23, pole_top, 46, 105),
            border_radius=8
        )

        pygame.draw.rect(
            surface, (125, 130, 135),
            (x - 19, pole_top + 4, 38, 97),
            border_radius=6
        )

        # Signal lamps
        lamp_states = ["RED", "YELLOW", "GREEN"]

        for index, lamp in enumerate(lamp_states):
            cy = pole_top + 20 + index * 31

            if lamp == self.state:
                colour = self.COLORS[lamp]

                pygame.draw.circle(
                    surface, colour, (x, cy), 11
                )

                pygame.draw.circle(
                    surface, (255, 255, 255),
                    (x - 3, cy - 3), 3
                )
            else:
                pygame.draw.circle(
                    surface, (55, 58, 61),
                    (x, cy), 10
                )

        label = small_font.render(self.state, True, WHITE)

        label_bg = pygame.Rect(
            x - 35, pole_top - 25, 70, 20
        )

        pygame.draw.rect(
            surface, (35, 48, 61),
            label_bg, border_radius=4
        )

        surface.blit(
            label, label.get_rect(center=label_bg.center)
        )


def draw_background(surface, offset):
    surface.fill(SKY)

    # Clouds
    for i in range(5):
        cx = int(
            (i * 245 - offset * 0.18) % (WIDTH + 150)
        ) - 60

        cy = 75 + (i % 3) * 45

        pygame.draw.circle(
            surface, (245, 250, 252), (cx, cy), 18
        )

        pygame.draw.circle(
            surface, (245, 250, 252),
            (cx + 22, cy - 7), 23
        )

        pygame.draw.circle(
            surface, (245, 250, 252),
            (cx + 45, cy), 17
        )

    # Distant hills
    pygame.draw.rect(
        surface, (115, 169, 111),
        (0, 315, WIDTH, 115)
    )

    for i in range(7):
        hx = int(
            (i * 190 - offset * 0.35) % (WIDTH + 220)
        ) - 100

        pygame.draw.ellipse(
            surface, (91, 151, 96),
            (hx, 275, 230, 110)
        )

    # Grass
    pygame.draw.rect(
        surface, GRASS,
        (0, GROUND_Y - 10, WIDTH, HEIGHT - GROUND_Y + 10)
    )

    # Railway ballast
    pygame.draw.polygon(
        surface, (112, 108, 99),
        [
            (0, GROUND_Y - 15),
            (WIDTH, GROUND_Y - 15),
            (WIDTH, GROUND_Y + 75),
            (0, GROUND_Y + 75)
        ]
    )

    # Railway sleepers
    sleeper_offset = int(offset) % 54

    for sx in range(-54, WIDTH + 54, 54):
        x = sx - sleeper_offset

        pygame.draw.rect(
            surface, SLEEPER,
            (x, GROUND_Y + 13, 34, 13),
            border_radius=2
        )

    # Rails
    pygame.draw.rect(
        surface, RAIL,
        (0, GROUND_Y + 5, WIDTH, 7)
    )

    pygame.draw.rect(
        surface, RAIL,
        (0, GROUND_Y + 43, WIDTH, 7)
    )

    pygame.draw.line(
        surface, (190, 193, 195),
        (0, GROUND_Y + 5),
        (WIDTH, GROUND_Y + 5), 2
    )

    pygame.draw.line(
        surface, (190, 193, 195),
        (0, GROUND_Y + 43),
        (WIDTH, GROUND_Y + 43), 2
    )


def reset_game():
    return {
        "train": Train(),
        "signals": [],
        "score": 0,
        "lives": 3,
        "world_offset": 0.0,
        "spawn_timer": 0,
        "paused": False,
        "game_over": False,
        "message": "Watch the signal boards!",
        "message_timer": 180,
        "last_signal": "GREEN",
    }


game = reset_game()
running = True

while running:
    clock.tick(FPS)

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_p and not game["game_over"]:
                game["paused"] = not game["paused"]

            elif event.key == pygame.K_r and game["game_over"]:
                game = reset_game()

            elif event.key == pygame.K_SPACE and not game["game_over"]:
                game["train"].horn_timer = 25

    # --------------------------------------------------------
    # GAME UPDATE
    # --------------------------------------------------------
    if not game["paused"] and not game["game_over"]:

        train = game["train"]

        # Find the next upcoming signal
        upcoming = None

        for signal in game["signals"]:
            if signal.x > train.x + 95:
                upcoming = signal
                break

        active_state = upcoming.state if upcoming else "GREEN"

        train.update(active_state)

        world_speed = train.speed

        game["world_offset"] += world_speed
        game["spawn_timer"] += 1

        # Spawn signal boards with larger gaps
        if game["spawn_timer"] >= 300 and len(game["signals"]) < 3:

            game["spawn_timer"] = 0

            state = random.choices(
                ["GREEN", "YELLOW", "RED"],
                weights=[5, 3, 4],
                k=1
            )[0]

            last_x = max(
                [s.x for s in game["signals"]],
                default=WIDTH
            )

            signal_gap = 750

            game["signals"].append(
                Signal(
                    max(WIDTH + 250, last_x + signal_gap),
                    state
                )
            )

        # Update signals and check train safety
        for signal in game["signals"]:

            signal.update(world_speed)

            stop_line = signal.x - 120

            # Check red signal
            if signal.state == "RED" and not signal.passed:

                if train.x + 95 >= stop_line and train.speed > 0.35:

                    game["lives"] -= 1
                    signal.passed = True

                    game["message"] = "RED SIGNAL! Stop before the board!"
                    game["message_timer"] = 150

                    if game["lives"] <= 0:
                        game["game_over"] = True

            # Check when train passes a signal
            if signal.x < train.x - 130 and not signal.passed:

                signal.passed = True

                if signal.state == "RED" and train.speed <= 0.35:

                    game["score"] += 50
                    game["message"] = "Good stop! +50 points"

                elif signal.state == "YELLOW":

                    game["score"] += 20
                    game["message"] = "Caution followed! +20 points"

                else:

                    game["score"] += 10
                    game["message"] = "Green signal! Keep going"

                game["message_timer"] = 100

        # Remove old signals
        game["signals"] = [
            s for s in game["signals"] if s.x > -80
        ]

        # Reward safe progress
        game["score"] += max(
            0, int(train.speed * 0.08)
        )

        if game["message_timer"] > 0:
            game["message_timer"] -= 1

    # --------------------------------------------------------
    # DRAW BACKGROUND
    # --------------------------------------------------------
    draw_background(screen, game["world_offset"])

    # Trackside posts
    for i in range(8):

        px = int(
            (i * 170 - game["world_offset"] * 0.8)
            % (WIDTH + 170)
        ) - 30

        pygame.draw.rect(
            screen, (235, 235, 220),
            (px, GROUND_Y - 42, 8, 28)
        )

        pygame.draw.rect(
            screen, (190, 45, 45),
            (px, GROUND_Y - 42, 8, 8)
        )

    # Draw signals
    for signal in game["signals"]:
        signal.draw(screen)

    # Draw train
    game["train"].draw(screen)

    # Stop line before red signal
    for signal in game["signals"]:

        if signal.state == "RED" and signal.x > game["train"].x:

            line_x = int(signal.x - 120)

            pygame.draw.line(
                screen, (255, 255, 255),
                (line_x, GROUND_Y - 4),
                (line_x, GROUND_Y + 58), 3
            )

            break

    # --------------------------------------------------------
    # HUD
    # --------------------------------------------------------
    pygame.draw.rect(
        screen, (28, 45, 58),
        (0, 0, WIDTH, 48)
    )

    draw_text(
        screen, f"SCORE  {game['score']}", 18, 12
    )

    draw_text(
        screen, f"LIVES  {game['lives']}", 210, 12
    )

    draw_text(
        screen, f"SPEED  {game['train'].speed:.1f}", 355, 12
    )

    draw_text(
        screen, "P: pause   SPACE: horn   R: restart",
        570, 15, (222, 232, 238), small_font
    )

    # Signal guide
    guide_y = HEIGHT - 42

    pygame.draw.rect(
        screen, (28, 45, 58),
        (0, guide_y, WIDTH, 42)
    )

    draw_text(
        screen, "RED: STOP", 20, guide_y + 11,
        (255, 105, 105), small_font
    )

    draw_text(
        screen, "YELLOW: SLOW DOWN",
        175, guide_y + 11,
        (255, 210, 80), small_font
    )

    draw_text(
        screen, "GREEN: GO",
        405, guide_y + 11,
        (100, 235, 135), small_font
    )

    # Message panel
    if game["message_timer"] > 0 and not game["game_over"]:

        msg = small_font.render(
            game["message"], True, WHITE
        )

        panel = pygame.Rect(
            WIDTH // 2 - 190, 65, 380, 30
        )

        pygame.draw.rect(
            screen, (35, 48, 61),
            panel, border_radius=7
        )

        screen.blit(
            msg, msg.get_rect(center=panel.center)
        )

    # Pause screen
    if game["paused"]:

        shade = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )

        shade.fill((8, 18, 28, 150))
        screen.blit(shade, (0, 0))

        label = big_font.render(
            "PAUSED", True, WHITE
        )

        screen.blit(
            label,
            label.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )
        )

    # Game over screen
    if game["game_over"]:

        shade = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )

        shade.fill((8, 18, 28, 180))
        screen.blit(shade, (0, 0))

        title = big_font.render(
            "GAME OVER", True, WHITE
        )

        screen.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 45)
            )
        )

        draw_text(
            screen,
            f"Final score: {game['score']}",
            WIDTH // 2 - 100,
            HEIGHT // 2 + 5
        )

        draw_text(
            screen,
            "Press R to play again  |  ESC to quit",
            WIDTH // 2 - 190,
            HEIGHT // 2 + 48,
            WHITE,
            small_font
        )

    pygame.display.flip()

pygame.quit()
sys.exit()
