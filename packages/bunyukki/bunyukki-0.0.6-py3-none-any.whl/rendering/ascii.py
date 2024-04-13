def char_to_ascii(input_char):
    ascii_code = ord(input_char)
    return ascii_code

def string_to_ascii(input_string):
    ascii_list = [ord(char) for char in input_string]
    return ascii_list

# 메뉴 출력 함수
def print_menu():
    print("1. 문자의 ASCII 코드 확인")
    print("2. 문자열의 ASCII 코드 확인")
    print("3. 숫자의 ASCII 코드 확인")
    print("0. 프로그램 종료")

# 메인 함수
def main():
    while True:
        print_menu()
        choice = input("원하는 작업을 선택하세요 (0, 1, 2, 3 중 하나): ")

        if choice == '0':
            print("프로그램을 종료합니다.")
            break
        elif choice == '1':
            input_char = input("ASCII 코드를 확인할 문자를 입력하세요: ")
            ascii_result = char_to_ascii(input_char)
            print(f"입력한 문자 '{input_char}'의 ASCII 코드는: {ascii_result}")
        elif choice == '2':
            input_string = input("ASCII 코드를 확인할 문자열을 입력하세요: ")
            ascii_result = string_to_ascii(input_string)
            print(f"입력한 문자열 '{input_string}'의 ASCII 코드는: {ascii_result}")
        elif choice == '3':
            input_number = input("ASCII 코드를 확인할 숫자를 입력하세요: ")
            ascii_result = ord(input_number)
            print(f"입력한 숫자 '{input_number}'의 ASCII 코드는: {ascii_result}")
        else:
            print("잘못된 입력입니다. 다시 입력해주세요.")

if __name__ == "__main__":
    main()
