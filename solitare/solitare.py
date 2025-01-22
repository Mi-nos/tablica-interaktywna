from typing import Optional

import random
import arcade

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Pasjans"

#wielkosc kart
CARD_SCALE = 0.6
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

#rozmiar maty
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

#Dolne 2 pola
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

#góry rząd kart
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
#dolny rząd kart
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

#jeśli karty w stosie są rozłożone, jak daleko się rozchodzą
CARD_VERTICAL_OFFSET = CARD_HEIGHT * CARD_SCALE * 0.3
FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_red2.png"

#stałe opisujace stosy
PILE_COUNT = 13
BOTTOM_FACE_DOWN_PILE = 0
BOTTOM_FACE_UP_PILE = 1
PLAY_PILE_1 = 2
PLAY_PILE_2 = 3
PLAY_PILE_3 = 4
PLAY_PILE_4 = 5
PLAY_PILE_5 = 6
PLAY_PILE_6 = 7
PLAY_PILE_7 = 8
TOP_PILE_1 = 9
TOP_PILE_2 = 10
TOP_PILE_3 = 11
TOP_PILE_4 = 12

TOP_PILE_SUITS = {
    TOP_PILE_1: "Clubs",
    TOP_PILE_2: "Hearts",
    TOP_PILE_3: "Spades",
    TOP_PILE_4: "Diamonds",
}

class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self, suit, value, scale=1):
        """ Card constructor """
        self.suit = suit
        self.value = value
        #obrazki dla spritow
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"
        self.is_face_up = False
        super().__init__(FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")

    def face_down(self):
        """ Turn card face-down """
        self.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        self.is_face_up = False

    def face_up(self):
        """ Turn card face-up """
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    @property
    def is_face_down(self):
        """ Is this card face down? """
        return not self.is_face_up

class MyGame(arcade.Window):
    #główna klasa

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list: Optional[arcade.SpriteList] = None
        arcade.set_background_color(arcade.color.AMAZON)
        self.held_cards = None
        #Orginalna pozycja kart gdy przesuwamy tam gdzie nei mozna
        self.held_cards_original_position = None

        self.pile_mat_list = None
        self.piles = None

    def setup(self):

        #rozpoczyna gre
        self.held_cards = []
        self.held_cards_original_position = []
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X, BOTTOM_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X + X_SPACING, BOTTOM_Y
        self.pile_mat_list.append(pile)

        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)

        self.card_list = arcade.SpriteList()

        #tworzenie kart
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit, card_value, CARD_SCALE)
                card.position = START_X, BOTTOM_Y
                self.card_list.append(card)

        #mieszanie
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        self.piles = [[] for _ in range(PILE_COUNT)]
        for card in self.card_list:
            self.piles[BOTTOM_FACE_DOWN_PILE].append(card)
        for pile_no in range(PLAY_PILE_1, PLAY_PILE_7 + 1):
            for j in range(pile_no - PLAY_PILE_1 + 1):
                card = self.piles[BOTTOM_FACE_DOWN_PILE].pop()
                self.piles[pile_no].append(card)
                card.position = self.pile_mat_list[pile_no].position
                self.pull_to_top(card)

        for i in range(PLAY_PILE_1, PLAY_PILE_7 + 1):
            self.piles[i][-1].face_up()

    def on_draw(self):
        #ekran
        self.clear()

        self.pile_mat_list.draw()
        self.card_list.draw()

        # Sprawdzenie warunku zwycięstwa
        if self.check_victory():
            arcade.draw_text(
                "Wygrałeś! Naciśnij [R], aby rozpocząć nową grę.",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.WHITE,
                font_size=24,
                anchor_x="center",
            )

    def pull_to_top(self, card: arcade.Sprite):
        self.card_list.remove(card)
        self.card_list.append(card)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.R:
            #Restart
            self.setup()

    def on_mouse_press(self, x, y, button, key_modifiers):
        cards = arcade.get_sprites_at_point((x, y), self.card_list)
        if len(cards) > 0:
            primary_card = cards[-1]
            assert isinstance(primary_card, Card)

            pile_index = self.get_pile_for_card(primary_card)
            if pile_index == BOTTOM_FACE_DOWN_PILE:
                # Flip three cards
                for i in range(3):
                    if len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:
                        break
                    card = self.piles[BOTTOM_FACE_DOWN_PILE][-1]
                    card.face_up()
                    card.position = self.pile_mat_list[BOTTOM_FACE_UP_PILE].position
                    self.piles[BOTTOM_FACE_DOWN_PILE].remove(card)
                    self.piles[BOTTOM_FACE_UP_PILE].append(card)
                    self.pull_to_top(card)

            elif primary_card.is_face_down:
                primary_card.face_up()
            else:
                self.held_cards = [primary_card]
                self.held_cards_original_position = [self.held_cards[0].position]
                self.pull_to_top(self.held_cards[0])
                card_index = self.piles[pile_index].index(primary_card)
                for i in range(card_index + 1, len(self.piles[pile_index])):
                    card = self.piles[pile_index][i]
                    self.held_cards.append(card)
                    self.held_cards_original_position.append(card.position)
                    self.pull_to_top(card)
        else:
            mats = arcade.get_sprites_at_point((x, y), self.pile_mat_list)

            if len(mats) > 0:
                mat = mats[0]
                mat_index = self.pile_mat_list.index(mat)
                if mat_index == BOTTOM_FACE_DOWN_PILE and len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:
                    temp_list = self.piles[BOTTOM_FACE_UP_PILE].copy()
                    for card in reversed(temp_list):
                        card.face_down()
                        self.piles[BOTTOM_FACE_UP_PILE].remove(card)
                        self.piles[BOTTOM_FACE_DOWN_PILE].append(card)
                        card.position = self.pile_mat_list[BOTTOM_FACE_DOWN_PILE].position

    def remove_card_from_pile(self, card):
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break

    def get_pile_for_card(self, card):
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

    def move_card_to_new_pile(self, card, pile_index):
        self.remove_card_from_pile(card)
        self.piles[pile_index].append(card)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):

        if len(self.held_cards) == 0:
            return

        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True
        if arcade.check_for_collision(self.held_cards[0], pile):

            pile_index = self.pile_mat_list.index(pile)

            if pile_index == self.get_pile_for_card(self.held_cards[0]):
                pass

            elif PLAY_PILE_1 <= pile_index <= PLAY_PILE_7:
                if len(self.piles[pile_index]) > 0:
                    top_card = self.piles[pile_index][-1]
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = top_card.center_x, \
                                                top_card.center_y - CARD_VERTICAL_OFFSET * (i + 1)
                else:
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = pile.center_x, \
                                                pile.center_y - CARD_VERTICAL_OFFSET * i

                for card in self.held_cards:
                    self.move_card_to_new_pile(card, pile_index)
                reset_position = False

            elif TOP_PILE_1 <= pile_index <= TOP_PILE_4 and len(self.held_cards) == 1:
                held_card = self.held_cards[0]
                top_pile = self.piles[pile_index]

                if len(top_pile) == 0:
                    # Jeśli stos jest pusty, można położyć tylko Króla
                    if held_card.value == "K" and held_card.suit == TOP_PILE_SUITS[pile_index]:
                        held_card.position = pile.position
                        self.move_card_to_new_pile(held_card, pile_index)
                        reset_position = False
                else:
                    # Jeśli stos nie jest pusty, sprawdź kolor i wartość
                    top_card = top_pile[-1]
                    if (
                        held_card.suit == top_card.suit  # Ten sam kolor
                        and CARD_VALUES.index(held_card.value) == CARD_VALUES.index(top_card.value) - 1
                    ):
                        held_card.position = pile.position
                        self.move_card_to_new_pile(held_card, pile_index)
                        reset_position = False



        if reset_position:
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]
        self.held_cards = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

    def check_victory(self):
        for pile_index in range(TOP_PILE_1, TOP_PILE_4 + 1):
            if len(self.piles[pile_index]) != 13:
                return False
        return True



def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()