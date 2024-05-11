
from algorithm import file_extarcotr


if __name__ == '__main__':

    test_file_info = "assets/邮件截图/邮件截图1.png"

    response = file_extarcotr.extract(test_file_info, 'rb')
    print(response)
