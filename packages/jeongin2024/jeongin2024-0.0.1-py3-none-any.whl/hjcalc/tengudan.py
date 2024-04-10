def gugu_dan(dan):
    print(f'============={dan}===========')
    for i in range(1, 20):
        print(f'{dan} * {i} = {dan*i}')

# 사용자로부터 단을 입력받습니다.
input_dan = int(input("십구단을 출력할 단을 입력하세요: "))

# 입력받은 단의 십구단을 출력합니다.
gugu_dan(input_dan)
