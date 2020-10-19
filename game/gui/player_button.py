import pygame.font


class PlayerButton:
    """
    Button used to choose which player plays the game.
    """

    def __init__(self, ai_game, player, neighbour):
        """Initialize player button attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.player = player
        # Set the dimensions and properties of the button.
        self.width, self.height = 80, 80

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.rect.midbottom = neighbour.midtop

        if self.player == '1':
            self.rect.x = self.rect.x - 40
        elif self.player == '2':
            self.rect.x = self.rect.x + 40

        self.rect.y = self.rect.y - 20

        self._prep_img()

    def _prep_img(self):
        """Draw player image inside button."""
        if self.player == '1':
            self.img = pygame.image.load('assets/images/player1.png')
        else:
            self.img = pygame.image.load('assets/images/player2.png')

        self.image_rect = self.img.get_rect()
        self.image_rect.center = self.rect.center

    def draw_button(self):
        if self.ai_game.settings.current_player == self.player:
            self.screen.fill((123,123,123), self.rect)
        self.screen.blit(self.img, self.image_rect)
