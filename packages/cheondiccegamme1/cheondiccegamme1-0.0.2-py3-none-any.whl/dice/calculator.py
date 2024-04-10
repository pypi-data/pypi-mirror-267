import random

def random_number():
    return random.randint(1,6)

def game():
    while True:
        user_input = int(input("1입력하면 랜덤 0입력하면 종료"))
        if user_input == 0:
            print("게임을 종료합니다.")
            break
        elif user_input == 1:
            print(random_number())
        else:
            print("잘못된값")