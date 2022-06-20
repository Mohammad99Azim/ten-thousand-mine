from ten_thousand.game_logic import GameLogic
from ten_thousand.banker import Banker


def rolling_the_dice(roller, dice_num):
    random_dices_list = roller(dice_num)
    return random_dices_list


def is_user_cheating(user_input_list):
    is_he = [False for ind in range(len(user_input_list)) if
             random_dices.count(user_input_list[ind]) < user_input_list.count(user_input_list[ind])]
    return is_he


class Game:

    def __init__(self):
        self.round_counter = 0
        self.player_bank = Banker()
        self.dice_number = 6

    def play(self, roller=GameLogic.roll_dice):

        print('''Welcome to Ten Thousand
(y)es to play or (n)o to decline''')
        start_play = input('> ')
        if start_play[0] == 'n':
            return print('OK. Maybe another time')

        self.rolling_dice_text(self.dice_number, roller)
        self.user_input_handler(roller)

    def rolling_dice_text(self, dice_num, roller, print_start_round=1):
        if print_start_round == 1:
            self.round_counter += 1
            print(f'Starting round {self.round_counter}')
        global random_dices
        random_dices = rolling_the_dice(roller, dice_num)
        text = "*** "
        for x in random_dices:
            text += str(x) + " "
        text += "***"

        print(f'''Rolling {dice_num} dice...
{text}''')
        if GameLogic.calculate_score(random_dices) == 0:
            self.zlicher(roller)
        else:
            print("Enter dice to keep, or (q)uit:")

    def user_input_handler(self, roller):
        user_input_var = input("> ")
        if user_input_var == 'q':
            return self.user_choose_quit()
        elif user_input_var == 'b':
            self.user_input_bank(roller)
            self.user_input_handler(roller)
        elif user_input_var == 'r':
            self.user_input_roll(roller)
            self.user_input_handler(roller)
        else:
            self.user_input_dice(user_input_var)
            self.user_input_handler(roller)

    def user_choose_quit(self):
        self.dice_number = 6
        return print(f"Thanks for playing. You earned {self.player_bank.balance} points")

    def user_cheater_text(self):
        print('Cheater!!! Or possibly made a typo...')
        text = "*** "
        for x in random_dices:
            text += str(x) + " "
        text += "***"
        print(text)
        print('Enter dice to keep, or (q)uit:')
        return

    def user_input_bank(self, roller):
        print(f'''You banked {self.player_bank.shelved} points in round {self.round_counter}
Total score is {self.player_bank.bank()} points''')
        self.dice_number = 6
        self.rolling_dice_text(self.dice_number, roller)

    def user_input_roll(self, roller):
        self.rolling_dice_text(self.dice_number, roller, 0)

    def user_input_dice(self, dice_picked):
        dice_picked = dice_picked.replace(" ", "")
        user_input_list = sorted([int(x) for x in dice_picked])

        if is_user_cheating(user_input_list):
            self.player_bank.clear_shelf()
            return self.user_cheater_text()

        score_now = GameLogic.calculate_score(user_input_list)
        self.player_bank.shelf(score_now)

        if len(user_input_list) == 6 and (
                GameLogic.is_three_pairs(user_input_list) or user_input_list[0] == user_input_list[
            5] or user_input_list == [1, 2, 3, 4, 5, 6]):
            self.dice_number = 6
        else:
            self.dice_number -= len(user_input_list)
        print(f'''You have {self.player_bank.shelved} unbanked points and {self.dice_number} dice remaining
(r)oll again, (b)ank your points or (q)uit:''')

    ## V3

    def zlicher(self, roller):
        print('''****************************************
**        Zilch!!! Round over         **
****************************************''')
        self.player_bank.clear_shelf()
        self.user_input_bank(roller)


if __name__ == '__main__':
    one = Game()
    one.play()
    # rolling_dice_text(5)
