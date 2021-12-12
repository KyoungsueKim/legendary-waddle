import numpy
import questionary
import re
from utils import ascii_icons
from pyfiglet import Figlet

user_data = {"title": "",
             "adult": 0,
             "child": 0,
             "hall_name": "",
             "time": "",
             "position": '',
             "price": 0,
             'payment': ''}


def seat_validator(text: str):
    if len(text) != 2:
        return "대소문자를 구별하여 다시 한 번 정확히 입력해주세요."

    row = text[0]
    column = text[1]

    if re.compile('[A-G][0-9]').match(text) is None:
        return "대소문자를 구별하여 다시 한 번 정확히 입력해주세요."

    elif seat_list[f'{column}'][f'{row}'] == 1:
        return "해당 좌석은 이미 매진되었습니다. 다른 좌석을 선택해주세요."

    else:
        return True


def cost_calculator(user_data: dict):
    total_cost: int;
    hall_cost: int;

    if user_data['hall_name'] == '일반':
        hall_cost = 13000
    elif user_data['hall_name'] == '4DX':
        hall_cost = 16000
    elif user_data['hall_name'] == 'IMAX':
        hall_cost = 17000
    elif user_data['hall_name'] == 'SCREEN X':
        hall_cost = 16000
    elif user_data['hall_name'] == 'GOLD CLASS':
        hall_cost = 23000
    elif user_data['hall_name'] == 'SWEET BOX':
        hall_cost = 21000

    return int(hall_cost * user_data['adult']) + (hall_cost * 0.8 * user_data['child'])


print(ascii_icons.slate)
print(Figlet(font='slant').renderText('Ajou Box'))

answers1 = questionary.form(
    welcome_message=questionary.confirm("환영합니다 Ajou Box입니다!! 🍿 시작해볼까요?", default=True, qmark='[INFO]'),

    title=questionary.select("보고 싶은 영화를 선택해주세요 🎞",
                             choices=["엔칸토: 마법의 세계 (평점 8.6)",
                                      "듄 (평점 7.1)",
                                      "연애 빠진 로맨스 (평점 7.9)",
                                      "돈 룩 업 (평점 8.6)",
                                      "유체이탈자 (평점 8.1)",
                                      "스파이더맨: 노 웨이 홈 (평점 9.4)",
                                      "이터널스: (평점 4.4)",
                                      "태일이: (평점 9.5)"],
                             instruction="(화살표 키로 커서를 이동한 뒤 엔터를 누르세요)", qmark='[INFO]', use_shortcuts=True),

    number_adult=questionary.select("영화는 몇 명이 보나요? 구매하고자 하는 성인 티켓 수를 선택하세요 🎫",
                                    choices=["0명",
                                             "1명",
                                             "2명",
                                             "3명",
                                             "4명"],
                                    instruction="(화살표 키로 커서를 이동한 뒤 엔터를 누르세요)", qmark='[INFO]', use_indicator=True),

    number_child=questionary.select("구매하고자 하는 청소년 티켓 수를 선택하세요 🎟",
                                    choices=["0명",
                                             "1명",
                                             "2명",
                                             "3명",
                                             "4명"],
                                    instruction="(화살표 키로 커서를 이동한 뒤 엔터를 누르세요)", qmark='[INFO]', use_indicator=True),

    hall_name=questionary.select("어디서 보시겠어요? 상영관을 선택하세요 📽",
                                 choices=["일반",
                                          "4DX",
                                          "IMAX",
                                          "SCREEN X",
                                          "GOLD CLASS",
                                          "SWEET BOX"],
                                 instruction="(화살표 키로 커서를 이동한 뒤 엔터를 누르세요)", qmark='[INFO]', use_indicator=True),

    time=questionary.select("언제 보시겠어요? 상영 시간을 선택하세요 ⏰",
                            choices=["18:00",
                                     "20:30",
                                     "23:00"],
                            instruction="(화살표 키로 커서를 이동한 뒤 엔터를 누르세요)", qmark='[INFO]', use_shortcuts=True)
).ask()

# 유저 데이터 중간 저장
user_data['title'] = answers1['title']
user_data['adult'] = int(answers1['number_adult'][0])
user_data['child'] = int(answers1['number_child'][0])
user_data['hall_name'] = answers1['hall_name']
user_data['time'] = answers1['time']

questionary.print("[INFO] 다음은 좌석 현황입니다. (0: 예약 가능, 1: 매진)", style='fg:#673ab7 bold')

seat_list = numpy.random.choice(2, size=(7, 10), p=[0.85, 0.15])
column_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
row_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

import pandas

seat_list = pandas.DataFrame(seat_list, index=row_labels, columns=column_labels)
print('           [스크린]         ')
print(seat_list)
print('')  # 줄바꿈

answers2 = questionary.form(
    seat_row=questionary.autocomplete("앉으실 좌석의 열과 행을 다음과 같이 입력해주세요. 💺 (예시: B3): ",
                                      choices=[
                                          "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9",
                                          "B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9",
                                          "C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9",
                                          "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9",
                                          "E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9",
                                          "F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9",
                                          "G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"],
                                      qmark='[INFO]', validate=seat_validator),

    payment=questionary.select(f"금액은 {cost_calculator(user_data)}원 입니다. 어떻게 결제하시겠어요? 💵",
                               choices=["신용카드",
                                        "현금",
                                        "카카오페이"],
                               instruction="(화살표 키로 커서를 이동한 뒤 엔터를 누르세요)", qmark='[INFO]', use_indicator=True),

    success_message=questionary.confirm("결제가 완료되었습니다! 고맙습니다! 다음은 고객님의 예매 정보입니다. 🍿", default=True, qmark='[INFO]')
).ask()
