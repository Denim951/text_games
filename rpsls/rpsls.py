import random

# Game rules mapping: (winner, loser): reason
RULES = {
    ('scissors', 'lizard'): 'Scissors decapitate lizard',
    ('scissors', 'paper'): 'Scissors cuts paper',
    ('paper', 'rock'): 'Paper covers rock',
    ('rock', 'lizard'): 'Rock crushes lizard',
    ('lizard', 'spock'): 'Lizard poisons Spock',
    ('spock', 'scissors'): 'Spock smashes scissors',
    ('lizard', 'paper'): 'Lizard eats paper',
    ('paper', 'spock'): 'Paper disproves Spock',
    ('spock', 'rock'): 'Spock vaporizes rock',
    ('rock', 'scissors'): 'Rock crushes scissors',
}

CHOICES = ['rock', 'paper', 'scissors', 'lizard', 'spock']

def get_user_choice():
    print("Choose one:")
    for idx, choice in enumerate(CHOICES, 1):
        print(f"{idx}. {choice.capitalize()}")
    while True:
        try:
            selection = int(input("Enter number (1-5): "))
            if 1 <= selection <= 5:
                return CHOICES[selection - 1]
        except ValueError:
            pass
        print("Invalid input. Please try again.")

def get_computer_choice():
    return random.choice(CHOICES)

def determine_winner(user, computer):
    if user == computer:
        return 'tie', "It's a tie!"
    elif (user, computer) in RULES:
        return 'win', RULES[(user, computer)]
    elif (computer, user) in RULES:
        return 'lose', RULES[(computer, user)]
    else:
        return 'error', "Unexpected result."

def main():
    print("Welcome to Rock Paper Scissors Lizard Spock!")
    while True:
        user_choice = get_user_choice()
        computer_choice = get_computer_choice()
        print(f"\nYou chose: {user_choice.capitalize()}")
        print(f"Computer chose: {computer_choice.capitalize()}")
        result, reason = determine_winner(user_choice, computer_choice)
        print(reason)
        if result == 'win':
            print("You win!\n")
        elif result == 'lose':
            print("You lose!\n")
        else:
            print("It's a tie!\n")
        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()