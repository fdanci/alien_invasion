import pygame.font


class Button:
    """
    Default Button model. Used for all buttons inside this game.
    """

    def __init__(self, ai_game, msg, neighbour_rect_above=None, color=(0, 255, 0)):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # Center the button if it doesn't have neighbours.
        if not neighbour_rect_above:
            self.rect.center = self.screen_rect.center
        else:
            self.rect.midtop = neighbour_rect_above.midbottom
        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
