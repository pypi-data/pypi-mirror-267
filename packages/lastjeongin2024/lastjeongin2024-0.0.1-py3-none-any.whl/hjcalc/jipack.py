from datetime import datetime
import matplotlib.pyplot as plt

def tengugu_dan(dan):
    print(f'============={dan}===========')
    for i in range(1, 20):
        print(f'{dan} * {i} = {dan*i}')

def generate_donut_chart():
     plt.rc('font', family='NanumBarunGothic')

    # 비율과 라벨을 담을 리스트 초기화
    ratio = []
    labels = []

    # 비율과 라벨을 사용자로부터 입력 받음
    num_slices = int(input("도넛 그래프의 개수를 입력하세요: "))
    for i in range(num_slices):
        label = input(f"도넛 그래프의 {i+1}번째 항목의 이름을 입력하세요: ")
        time_str = input(f"{label} 공부한 시간을 24시간 기준으로 입력하세요 (예: 2시간 30분인 경우 02:30): ")
        hours, minutes = map(int, time_str.split(':'))
        total_minutes = hours * 60 + minutes
        ratio.append(total_minutes)
        labels.append(label)

    # 원형 그래프 생성
    plt.pie(ratio, labels=labels, autopct='%.1f%%', startangle=90, counterclock=False, wedgeprops=dict(width=0.4))
    plt.axis('equal')  # 원형 그래프의 종횡비를 동일하게 설정하여 원형으로 출력
    plt.show()

def calculate_days_until_dday():
    """
    디데이까지의 남은 일 수를 계산하는 함수
    """
    # 사용자로부터 디데이 날짜 입력 받기
    dday_input = input("디데이 날짜를 입력하세요 (yyyy-mm-dd 형식): ")
    dday_date = datetime.strptime(dday_input, "%Y-%m-%d")

    # 현재 날짜 가져오기
    today_date = datetime.today()

    # 디데이까지의 남은 일 수 계산
    days_left = (dday_date - today_date).days
    print("디데이까지 남은 일수:", days_left)

if __name__ == "__main__":
    # 테스트용 코드
    print("1. 구구단 출력")
    gugu_dan(9)

    print("\n2. 도넛 그래프 생성")
    generate_donut_chart()

    print("\n3. 디데이 계산")
    calculate_days_until_dday()
