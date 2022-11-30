# from testing import testing
import os
# from . import usercreate
import usercreate


if __name__ == "__main__":
    # определяем директорию программки


    # словарь конфига, который будет передаваться в обучение или  тестирование
    # config = {"user": "default"}
    # здесь должна начинаться работа за дефолтного юзера
    if input("1 - default, 2 - new user") == "1":
        usercreate.main(default=True)
    else:
        usercreate.main(default=False)

 #   testing.testing(config)




