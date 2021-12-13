import numpy  # 매우 유명한 행렬 계산 패키지
import pandas  # 매우 유명한 데이터프레임 라이브러리. 여기에서는 단지 좌석 표시를 이쁘게 하기 위해서만 사용함. (...)
import questionary  # CLI 에플리케이션 제작을 쉽게 해주는 패키지.
import re  # 정규 표현식 검사를 위한 모듈
from utils import ascii_icons  # 메인 화면 꾸미기를 위해 아스키 아트를 저장해둔 코드
from pyfiglet import Figlet  # 입력한 글자를 이쁜 아스키 아트로 바꿔주는 패키지.

# 고객이 선택한 내용을 저장하기 위한 dict 변수
customer_data = {"title": "",  # 영화 제목
                 "adult": 0,  # 어른 수
                 "child": 0,  # 아이 수
                 "hall_name": "",  # 상영관 이름
                 "time": "",  # 시간대
                 "seat": '',  # 좌석 위치
                 "price": 0,  # 최종 가격
                 'payment': ''}  # 결제 수단

seat_list = numpy.random.choice(2, size=(7, 10), p=[0.85, 0.15])
# 좌석 배치를 넘파이 어레이로 랜덤 생성. 2 미만의 수(0과 1)을 7x10 사이즈로 생성하는데, 0은 85%의 확률로, 1은 15%의 확률로 나타나게 생성함.
# 여기서 숫자는 인원 수를 이야기 하는데, 0은 해당 좌석이 예약되지 않은 상태를, 1은 해당 좌석이 예약된 상태를 의미함.
# 시간만 많다면 SQLite로 좌석 위치를 저장하고 싶지만 지금은 그렇게까지 할 시간이 없기에 더미 데이터를 넘파이 어레이로 생성.

column_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # 열 번호 라벨들. 열 번호는 숫자로 0~9까지 표시.
row_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']  # 행 번호 라벨들. 행 번호는 영대문자로 A-G까지 표시.
seat_list = pandas.DataFrame(seat_list, index=row_labels, columns=column_labels)


# 넘파이 행렬로 무작위 생성한 좌석 데이터를 판다스로 옮겨옴.
# 판다스는 데이터프레임을 프린트 할 때 행열 라벨을 붙여줄 수 있고 알아서 좌우 간격 맞춰서 예쁘게 잘 나오기 때문에 판다스를 사용함.

def validator_seat_name(text: str) -> bool or str:
    '''

    고객이 입력한 좌석 위치 텍스트가 올바른 형식인지 체크하는 메소드입니다.
    이 프로그램은 고객이 직접 좌석 위치를 키보드로 입력하기 떄문에 좌석을 올바르게 입력하였는지 확인이 필요합니다.

    :param text: 고객이 직접 입력한 텍스트
    :return: 파라메터로 넘어온 text 가 올바른 형식이 아닐 경우에는 str 타입의 경고 문구를, 올바른 형식일때는 True를 반환합니다.
    '''

    if len(text) != 2:  # 입력한 좌석 글자 수가 두 글자가 맞는지 확인. 만약 아니라면
        return "대소문자를 구별하여 다시 한 번 정확히 입력해주세요."  # 다음과 같은 경고 문구를 반환

    # 입력한 좌석 글자가 B3 과 같이 영대문자 + 숫자의 조합인지 확인하기 위해 내장 정규표현식 모듈인 regex를 사용함.
    # 영대문자 + 숫자 조합을 검출해내는 패턴을 compile해서 메소드의 파라메터로 입력 받은 text와 매칭되는지 확인함.
    # None일 경우 매칭되지 않는 경우를 말함. 즉 형식이 영대문자 + 숫자 조합이 아닐 경우
    if re.compile('[A-G][0-9]').match(text) is None:
        return "대소문자를 구별하여 다시 한 번 정확히 입력해주세요."  # 다음과 같은 경고 문구를 반환

    row = text[0]  # 좌석의 행 번호. 입력받는 텍스트는 B3 과 같은 형식이므로 파라메터의 첫 번째 글자가 행 번호가 됨.
    column = text[1]  # 좌석의 열 번호. 입력받는 텍스트는 B3 과 같은 형식이므로 파라메터의 두 번째 글자가 열 번호가 됨.
    if seat_list[f'{column}'][f'{row}'] == 1:  # 고객이 입력한 좌석 위치가 이미 예약되어있다면
        return "해당 좌석은 이미 매진되었습니다. 다른 좌석을 선택해주세요."  # 다음과 같은 경고 문구를 반환

    else:  # 위의 조건을 모두 통과하면, (즉 다시 말해 형식에 문제가 없으면)
        return True  # True를 반환함.


def cost_calculator(customer_data: dict):
    '''

    고객이 선택한 내용을 담는 user_data라는 변수에서 상영관 이름과 성인 티켓 수, 청소년 티켓 수를 뽑아 가격을 계산합니다.
    :param customer_data: 고객이 선택한 내용을 담기 위한 dict 변수. key로 'hall_name'과 'adult', 'child'를 반드시 가지고 있어야합니다.
    :return: 영화표 예매 가격을 int 타입으로 리턴합니다.
    '''

    hall_cost: int;  # 상영관의 가격을 저장하는 변수.

    if customer_data['hall_name'] == '일반':  # 고객이 일반관을 선택했다면
        hall_cost = 13000  # 상영관의 가격은 13,000원
    elif customer_data['hall_name'] == '4DX':  # 고객이 4DX관을 선택했다면
        hall_cost = 16000  # 상영관의 가격은 16,000원
    elif customer_data['hall_name'] == 'IMAX':  # 고객이 IMAX관을 선택했다면
        hall_cost = 17000  # 상영관의 가격은 17,000원
    elif customer_data['hall_name'] == 'SCREEN X':  # 고객이 SCREEN X 관을 선택했다면
        hall_cost = 16000  # 상영관의 가격은 16,000원
    elif customer_data['hall_name'] == 'GOLD CLASS':  # 고객이 GOLD CLASS 관을 선택했다면
        hall_cost = 23000  # 가격은 23,000원
    elif customer_data['hall_name'] == 'SWEET BOX':  # 고객이 SWEET BOX 관을 선택했다면
        hall_cost = 21000  # 가격은 21,000원

    return int(hall_cost * customer_data['adult']) + (hall_cost * 0.8 * customer_data['child'])
    # 성인 예매 수와 청소년 예매 수를 이용해 상영관 가격과 곱하여 최종 가격 결정.
    # 이 때 청소년은 성인 가격의 20%을 할인함.


print(ascii_icons.slate)  # ascii_icons.py 에 저장되어있는 아스키 아트를 프린트 함. 슬레이트 아이콘이 프린트 됨.
print(Figlet(font='slant').renderText('Ajou Box'))  # Figlet 모듈을 이용해 Ajou Box라는 글자를 아스키 아트로 이쁘게 만들어 프린트 함.

# 질문지를 만들기 위해 questionary 라는 모듈을 이용함. form 메소드를 이용해 질문지 내용을 채움.
answers2 = questionary.form(
    welcome_message=questionary.confirm("환영합니다 Ajou Box입니다!! 🍿 시작해볼까요?", default=True, qmark='[INFO]'),
    # YES인지 NO인지 confirm을 하는 종류의 질문 생성.
    # default= 파라메터를 이용해 유저가 엔터를 누르면 자동으로 Yes를 선택하게 함. (기본 값)
    # qmark= 파라메터를 이용해 안내 텍스트 앞에는 [INFO]라는 접두어 붙임.

    title=questionary.select("보고 싶은 영화를 선택해주세요 🎞",  # 여러개의 리스트 중에 하나를 선택하는 종류(select)의 질문을 생성. 질문 메시지는 왼쪽과 같음. 아래는 여러 선택지.
                             choices=["엔칸토: 마법의 세계 (평점 8.6)",
                                      "듄 (평점 7.1)",
                                      "연애 빠진 로맨스 (평점 7.9)",
                                      "돈 룩 업 (평점 8.6)",
                                      "유체이탈자 (평점 8.1)",
                                      "스파이더맨: 노 웨이 홈 (평점 9.4)",
                                      "이터널스: (평점 4.4)",
                                      "태일이: (평점 9.5)"],
                             instruction="(화살표 키로 커서를 이동한 뒤 엔터를 누르세요)", qmark='[INFO]', use_shortcuts=True),
                                # instruction= 파라메터를 이용해 질문 메시지 옆에 안내 메시지를 띄움.
                                # qmark= 파라메터를 이용해 질문 메시지 앞에 [INFO]라는 접두어를 붙임.
                                # use_shortcuts= 파라메터를 이용해 숫자키로도 매뉴를 선택할 수 있게 함.

    number_adult=questionary.select("영화는 몇 명이 보나요? 구매하고자 하는 성인 티켓 수를 선택하세요 🎫", # 여러개의 리스트 중에 하나를 선택하는 종류(select)의 질문을 생성. 질문 메시지는 왼쪽과 같음. 아래는 여러 선택지.
                                    choices=["0명",
                                             "1명",
                                             "2명",
                                             "3명",
                                             "4명"],
                                    instruction="(화살표 키로 커서를 이동한 뒤 엔터를 누르세요)", qmark='[INFO]', use_indicator=True),
                                    # instruction= 파라메터를 이용해 질문 메시지 옆에 안내 메시지를 띄움.
                                    # qmark= 파라메터를 이용해 질문 메시지 앞에 [INFO]라는 접두어를 붙임.
                                    # use_indicator= 파라메터를 이용해 유저가 선택하고 있는 메뉴가 무엇인지 앞에 작게 보여줌.

    number_child=questionary.select("구매하고자 하는 청소년 티켓 수를 선택하세요 🎟", # 여러개의 리스트 중에 하나를 선택하는 종류(select)의 질문을 생성. 질문 메시지는 왼쪽과 같음. 아래는 여러 선택지.
                                    choices=["0명",
                                             "1명",
                                             "2명",
                                             "3명",
                                             "4명"],
                                    instruction="(화살표 키로 커서를 이동한 뒤 엔터를 누르세요)", qmark='[INFO]', use_indicator=True),
                                    # instruction= 파라메터를 이용해 질문 메시지 옆에 안내 메시지를 띄움.
                                    # qmark= 파라메터를 이용해 질문 메시지 앞에 [INFO]라는 접두어를 붙임.
                                    # use_indicator= 파라메터를 이용해 유저가 선택하고 있는 메뉴가 무엇인지 앞에 작게 보여줌.

    hall_name=questionary.select("어디서 보시겠어요? 상영관을 선택하세요 📽", # 여러개의 리스트 중에 하나를 선택하는 종류(select)의 질문을 생성. 질문 메시지는 왼쪽과 같음. 아래는 여러 선택지.
                                 choices=["일반",
                                          "4DX",
                                          "IMAX",
                                          "SCREEN X",
                                          "GOLD CLASS",
                                          "SWEET BOX"],
                                 instruction="(화살표 키로 커서를 이동한 뒤 엔터를 누르세요)", qmark='[INFO]', use_indicator=True),
                                    # instruction= 파라메터를 이용해 질문 메시지 옆에 안내 메시지를 띄움.
                                    # qmark= 파라메터를 이용해 질문 메시지 앞에 [INFO]라는 접두어를 붙임.
                                    # use_indicator= 파라메터를 이용해 유저가 선택하고 있는 메뉴가 무엇인지 앞에 작게 보여줌.

    time=questionary.select("언제 보시겠어요? 상영 시간을 선택하세요 ⏰", # 여러개의 리스트 중에 하나를 선택하는 종류(select)의 질문을 생성. 질문 메시지는 왼쪽과 같음. 아래는 여러 선택지.
                            choices=["18:00",
                                     "20:30",
                                     "23:00"],
                            instruction="(화살표 키로 커서를 이동한 뒤 엔터를 누르세요)", qmark='[INFO]', use_shortcuts=True)
                            # instruction= 파라메터를 이용해 질문 메시지 옆에 안내 메시지를 띄움.
                            # qmark= 파라메터를 이용해 질문 메시지 앞에 [INFO]라는 접두어를 붙임.
                            # use_indicator= 파라메터를 이용해 유저가 선택하고 있는 메뉴가 무엇인지 앞에 작게 보여줌.
).ask() # 위에서 채운 질문지 내용을 바로 콘솔에서 띄울 수 있도록 ask 메소드를 붙임.

# 고객 데이터 중간 저장
customer_data['title'] = answers2['title'] # 위의 질문지에서 받은 답변 중 title 파라메터에 담겼던 값을 dict 타입의 custom_data 변수에 'title'에 담음. 영화 제목 저장.
customer_data['adult'] = int(answers2['number_adult'][0]) # 위의 질문지에서 받은 답변 중 number_adult 파라메터에 담겼던 값을 dict 타입의 custom_data 변수에 'adult'에 담음. 성인 티켓 수 저장.
customer_data['child'] = int(answers2['number_child'][0]) # 위의 질문지에서 받은 답변 중 'number_child' 파라메터에 담겼던 값을 dict 타입의 custom_data 변수에 'child'에 담음. 청소년 티켓 수 저장.
customer_data['hall_name'] = answers2['hall_name'] # 위의 질문지에서 받은 답변 중 'hall_name' 파라메터에 담겼던 값을 dict 타입의 custom_data 변수에 'hall_name'에 담음. 상영관 이름 저장.
customer_data['time'] = answers2['time'] # 위의 질문지에서 받은 답변 중 'time' 파라메터에 담겼던 값을 dict 타입의 custom_data 변수에 'time'에 담음. 상영 시간 저장.

questionary.print("[INFO] 다음은 좌석 현황입니다. (0: 예약 가능, 1: 매진)", style='fg:#673ab7 bold') # questionary.print 를 이용해 formatted text 프린트. 스타일은 보라색에 볼드체.
print('           [스크린]         ') # 스크린 텍스트 프린트
print(seat_list) # 위에서 만든 좌석 정보 데이터프레임을 프린트.
print('')  # 줄바꿈

answers2 = questionary.form( # 질문지를 만들기 위해 questionary 라는 모듈을 이용함. form 메소드를 이용해 질문지 내용을 채움.
    seat=questionary.autocomplete("앉으실 좌석의 열과 행을 다음과 같이 입력해주세요. 💺 (예시: B3): ",  # autocomplete 타입의 질문 생성. 메시지는 왼쪽과 같음. 고객이 문자를 입력하면 아래 선택지를 자동완성 제안 해줌.
                                  choices=[
                                          "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9",
                                          "B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9",
                                          "C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9",
                                          "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9",
                                          "E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9",
                                          "F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9",
                                          "G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"],
                                  qmark='[INFO]', validate=validator_seat_name),
                                        # qmark= 파라메터를 이용해 질문 메시지 앞에 [INFO]라는 접두어를 붙임.
                                        # validator_seat_name 메소드를 validate 메소드로 사용. 해당 메소드에서 True가 반환되기 전 까지 다음으로 넘어갈 수 없음. 즉 다시말해 형식이 올바른지 검사.

    payment=questionary.select(f"금액은 {cost_calculator(customer_data)}원 입니다. 어떻게 결제하시겠어요? 💵", # 여러개의 리스트 중에 하나를 선택하는 종류(select)의 질문을 생성. 질문 메시지는 왼쪽과 같음. 아래는 여러 선택지.
                               choices=["신용카드",
                                        "현금",
                                        "카카오페이"],
                               instruction="(화살표 키로 커서를 이동한 뒤 엔터를 누르세요)", qmark='[INFO]', use_indicator=True),
                                    # instruction= 파라메터를 이용해 질문 메시지 옆에 안내 메시지를 띄움.
                                    # qmark= 파라메터를 이용해 질문 메시지 앞에 [INFO]라는 접두어를 붙임.
                                    # use_indicator= 파라메터를 이용해 유저가 선택하고 있는 메뉴가 무엇인지 앞에 작게 보여줌.

    success_message=questionary.confirm("결제가 완료되었습니다! 고맙습니다! 다음은 고객님의 예매 정보입니다. 🍿", default=True, qmark='[INFO]') # YES인지 NO인지 confirm을 하는 종류의 질문 생성.
    # default= 파라메터를 이용해 유저가 엔터를 누르면 자동으로 Yes를 선택하게 함. (기본 값)
    # qmark= 파라메터를 이용해 안내 텍스트 앞에는 [INFO]라는 접두어 붙임.
).ask() # 위에서 채운 질문지 내용을 바로 콘솔에서 띄울 수 있도록 ask 메소드를 붙임.

# 고객 데이터 중간 저장
customer_data['seat'] = answers2['seat'] # 위의 질문지에서 받은 답변 중 seat 파라메터에 담겼던 값을 dict 타입의 custom_data 변수에 'seat'에 담음. 영화 제목 저장.
customer_data['payment'] = answers2['payment'] # 위의 질문지에서 받은 답변 중 payment 파라메터에 담겼던 값을 dict 타입의 custom_data 변수에 'payment'에 담음. 결제 방법 저장.
customer_data['price'] = cost_calculator(customer_data) # 가격을 계산해 dict 타입의 custom_data 변수에 'price'에 담음. 결게 가격 저장.

# 최종 정보 프린트
print("====================================================")
print(Figlet(font='slant').renderText('Ajou Box')) # Figlet 모듈 이용해서 Ajou Box을 아스키아트로 표현.
print(f'영화명: {customer_data["title"]}\n'
      f'성인 티켓 수: {customer_data["adult"]}\n'
      f'청소년 티켓 수: {customer_data["child"]}\n'
      f'상영관: {customer_data["hall_name"]}\n'
      f'상영 시간: {customer_data["time"]}\n'
      f'좌석 위치: {customer_data["seat"]}\n'
      f'가격: {customer_data["price"]}\n'
      f'결제 수단: {customer_data["payment"]}')
print("====================================================")