import pygame.font


class PlayerButton:
    """
    Button used to choose which player plays the game.
    """

    def __init__(self, ai_game, player, neighbour):
        """Initialize player button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # Set the dimensions and properties of the button.
        self.width, self.height = 50, 50
        self.button_color = (0, 0, 0)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.rect.midbottom = neighbour.midtop

        if player == '1':
            self.rect.x = self.rect.x - 40
        elif player == '2':
            self.rect.x = self.rect.x + 40

        self.rect.y = self.rect.y - 10

        self._prep_img()

    def _prep_img(self):
        """Draw image inside button like rect."""
        self.img = pygame.image.load('assets/images/power_up.bmp')
        self.image_rect = self.img.get_rect()
        self.image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(0, self.rect)
        self.screen.blit(self.img, self.image_rect)
