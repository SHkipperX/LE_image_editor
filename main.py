import os
from PIL import Image, ImageEnhance, ImageFilter
import sys
import requests
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sqlite3


class QhelperWindow(QWidget):
    def __init__(self):
        super(QhelperWindow, self).__init__()
        self.helptextUI()

    def helptextUI(self):
        try:
            self.setGeometry(600, 300, 350, 300)
            self.setFixedSize(350, 300)
            self.setWindowTitle('Помощь')
            self.text = QPlainTextEdit(self)
            self.text.setReadOnly(True)
            self.text.setGeometry(0, 0, 350, 300)
            with open('text', mode='r', encoding='utf8') as x:
                i = x.read()
                self.text.setPlainText(i)
        except:
            pass


class SignUp(QWidget):

    def __init__(self):
        super().__init__()

        if not os.path.isfile('BASE.db'):
            open('BASE.db', mode='w')
            con = sqlite3.connect('BASE.db')
            with con:
                con.execute(
                    """CREATE TABLE login 
                    (email    TEXT (10, 32) NOT NULL,
                    password TEXT (8, 16)  NOT NULL,
                    imagen   TEXT);""")
        self.logUI()

    def logUI(self):
        self.setGeometry(700, 400, 250, 150)
        self.setWindowTitle('Авторизация')
        self.setFixedSize(250, 150)

        self.bt_reset = QPushButton(self)
        self.bt_reset.setText('reset')
        self.bt_reset.setGeometry(200, 13, 50, 20)
        self.bt_reset.resize(50, 20)
        self.bt_reset.clicked.connect(self.reset_password)

        self.bt_Enter = QPushButton(self)
        self.bt_Enter.setText('Вход')
        self.bt_Enter.setGeometry(50, 100, 81, 35)
        self.bt_Enter.clicked.connect(self.log_in)

        self.bt_Reg = QPushButton(self)
        self.bt_Reg.setText('Регистрация')
        self.bt_Reg.setGeometry(150, 100, 81, 35)
        self.bt_Reg.clicked.connect(self.register)

        self.lb_eml = QLabel(self)
        self.lb_eml.setText('E-mail: ')
        self.lb_eml.move(37, 17)
        self.lb_psw = QLabel(self)
        self.lb_psw.setText('Пароль: ')
        self.lb_psw.move(30, 57)
        self.E_maill = QLineEdit(self)
        self.E_maill.setGeometry(80, 10, 120, 35)
        self.Passwordl = QLineEdit(self)
        self.Passwordl.setGeometry(80, 50, 120, 35)
        self.Passwordl.setEchoMode(QLineEdit.Password)
        self.flag = True
        self.shpsw = QRadioButton(self)
        self.shpsw.move(210, 60)
        self.shpsw.clicked.connect(self.hide_or_show)

        self.sp = ['mail.ru', 'gmail.com', 'e-mail.com', 'yandex.ru', 'rambler.com', 'yahoo.com']

    def hide_or_show(self):

        if self.flag:
            self.Passwordl.setEchoMode(QLineEdit.Normal)
            self.flag = False
        else:
            self.Passwordl.setEchoMode(QLineEdit.Password)
            self.flag = True

    def log_in(self):

        self.con = sqlite3.connect('BASE.db')
        self.cur = self.con.cursor()
        try:
            mail = self.E_maill.text().lower()
            passwordw = self.Passwordl.text()
            self.E_maill.setText('')
            self.Passwordl.setText('')
            if (mail.split('@')[1] in self.sp and
                    (len(passwordw) >= 8) and len(passwordw) <= 16):

                res = self.cur.execute(f"SELECT * FROM login WHERE email='{mail}'").fetchall()
                c = True
                for i in res:
                    if mail in i[0]:
                        if mail in i[0] and passwordw in i[1]:
                            c = False
                            msg = QMessageBox()
                            msg.setIcon(QMessageBox.Information)
                            msg.setText(
                                "Вы вошли!")
                            msg.setWindowTitle("Успех")
                            msg.exec_()
                            self.window = Example()
                            self.window.show()

                            break
                        else:
                            msg = QMessageBox()
                            msg.setIcon(QMessageBox.Critical)
                            msg.setText('Неверный пароль.')
                            msg.setWindowTitle("Ошибка")
                            msg.exec_()
                            c = False
                            break
                if c:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText('Такого пользователя не существует.')
                    msg.setWindowTitle("Ошибка")
                    msg.exec_()

            if (len(passwordw) < 8 or len(passwordw) > 16) or (mail.split('@')[1] not in self.sp):
                self.error_lenpassword_or_email()


        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Возможно одно из полей ввода осталось пустым или некоректно заполненым, заполните его.")
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def reset_password(self):
        self.con = sqlite3.connect('BASE.db')
        self.cur = self.con.cursor()
        try:
            mail = self.E_maill.text().lower()
            try:
                update_password, _ = QInputDialog.getText(self, 'Сброс пароля',
                                                          'Введите новый пароль: ')
                if update_password != '' and len(update_password) >= 8 and len(update_password) <= 16 and \
                        mail.split('@')[1] in self.sp:
                    res = self.cur.execute(f"SELECT * FROM login WHERE email='{mail}'").fetchall()
                    for i in res:
                        if i == res[0]:
                            set = self.cur.execute(
                                f'UPDATE login SET password="{update_password}" WHERE email="{mail}"')
                            self.con.commit()
                        else:
                            msg = QMessageBox()
                            msg.setIcon(QMessageBox.Critical)
                            msg.setText(f'Пользователя с почтовым ящиком <{mail}> не обнаружено...')
                            msg.setWindowTitle("Ошибка")
                            msg.exec_()
                else:
                    self.error_lenpassword_or_email()
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText('Проверьте заплнено ли поле Сброс пароля...\n'
                            'Длина должна быть не меннее 8 и не более 16 символов')
                msg.setWindowTitle("Ошибка")
                msg.exec_()


        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Проверьте заплнено ли поле с E-mail...')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def register(self):
        self.con = sqlite3.connect('BASE.db')
        self.cur = self.con.cursor()
        try:
            cc = True
            mail = self.E_maill.text().lower()
            passwordw = self.Passwordl.text()
            self.E_maill.setText('')
            self.Passwordl.setText('')

            if (len(passwordw) >= 8 or len(passwordw) <= 16) and (mail.split('@')[1] in self.sp):

                reg = self.cur.execute(f"SELECT * FROM login WHERE email='{mail}'").fetchall()
                for i in reg:
                    if mail in i[0]:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText('Пользователь с такой почтой уже существует.')
                        msg.setWindowTitle("Ошибка")
                        msg.exec_()
                        cc = False
                        break
                if cc:
                    reg = self.cur.execute(f"INSERT INTO login VALUES('{mail}', '{passwordw}', NULL)")
                    self.con.commit()
                    reg.close()

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText('Вы зарегистрированы!')
                    msg.setWindowTitle("Успех")
                    msg.exec_()


            else:
                self.error_lenpassword_or_email()


        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Возможно одно из полей ввода осталось пустым или некорректно заполненым, заполните его.")
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def error_lenpassword_or_email(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Пароль должен быть не менее 4 и не более 16 символов.\n'
                    'Поддерживаемые почтовые ящики: \n'
                    "['mail.ru', 'gmail.com', 'e-mail.com', 'yandex.ru', 'rambler.com', 'yahoo.com']")
        msg.setWindowTitle("Ошибка")
        msg.exec_()


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.image = QLabel(self)
        self.image.move(300, 20)
        self.image.resize(1600, 900)
        self.setGeometry(700, 400, 300, 180)
        self.setWindowTitle('PyQt+PIL')

        self.help = QPushButton(self)
        self.help.setText('Помощь')
        self.help.move(5, 890)
        self.help.clicked.connect(self.helper)

        self.bt_NewImg = QPushButton(self)
        self.bt_NewImg.setGeometry(10, 600, 140, 30)
        self.bt_NewImg.setText('Новое изображение')
        self.bt_NewImg.clicked.connect(self.new_Imagen)
        self.reset = QPushButton(self)
        self.reset.setGeometry(10, 560, 70, 40)
        self.reset.setText('Назад')
        self.reset.clicked.connect(self.Back)
        self.save_Img = QPushButton(self)
        self.save_Img.setGeometry(80, 560, 70, 40)
        self.save_Img.setText('Сохранить')
        self.save_Img.clicked.connect(self.save_Imagen)
        self.lbl_Url = QLabel(self)
        self.lbl_Url.setText('Поиск по Url')
        self.lbl_Url.move(10, 30)
        self.Urledit = QLineEdit(self)
        self.Urledit.setGeometry(0, 50, 100, 30)
        self.Url_btn = QPushButton(self)
        self.Url_btn.setGeometry(100, 50, 70, 30)
        self.Url_btn.setText('Найти')
        self.Url_btn.clicked.connect(self.Url_new_Imagen)
        self.cropp = QPushButton(self)
        self.cropp.setGeometry(10, 300, 70, 40)
        self.cropp.setText('Обрезка')
        self.cropp.clicked.connect(self.Crop)

        self.lbl_Rezk = QLabel(self)
        self.lbl_Rezk.setText('Резкость')
        self.lbl_Rezk.setGeometry(28, 177, 100, 30)
        self.sld_Rezk = QSlider(Qt.Horizontal, self)
        self.sld_Rezk.setRange(0, 30000)
        self.sld_Rezk.move(28, 200)
        self.sld_Rezk.valueChanged[int].connect(self.Rezkost)
        self.lbl_Bright = QLabel(self)
        self.lbl_Bright.setText('Яркость')
        self.lbl_Bright.setGeometry(28, 77, 100, 30)
        self.sld_Bright = QSlider(Qt.Horizontal, self)
        self.sld_Bright.setRange(10000, 110000)
        self.sld_Bright.move(28, 100)
        self.sld_Bright.valueChanged[int].connect(self.Brights)
        self.lbl_Contr = QLabel(self)
        self.lbl_Contr.setText('Контрасность')
        self.lbl_Contr.setGeometry(28, 127, 100, 30)
        self.sld_Contr = QSlider(Qt.Horizontal, self)
        self.sld_Contr.setRange(10000, 70000)
        self.sld_Contr.move(28, 150)
        self.sld_Contr.valueChanged[int].connect(self.Contrast)
        self.lbl_visibility = QLabel(self)
        self.lbl_visibility.setText('Прозрачность')
        self.lbl_visibility.setGeometry(28, 227, 100, 30)
        self.sld_visibility = QSlider(Qt.Horizontal, self)
        self.sld_visibility.setRange(0, 255)
        self.sld_visibility.move(28, 250)
        self.sld_visibility.valueChanged[int].connect(self.Visible)
        self.sld_rotate = QSlider(Qt.Horizontal, self)
        self.sld_rotate.setGeometry(500, 950, 1000, 40)
        self.sld_rotate.setRange(-360, 360)
        self.sld_rotate.valueChanged[int].connect(self.Rotate)
        self.filterbox = QComboBox(self)
        self.filterbox.addItems(['Cтандартное', 'Негатив', 'Cепия', 'ЧБ', 'Блюр', 'Контур', 'Маска', 'EDGE_ENHANCE',
                                 'ED_EN_MORE', 'FIND_EDGES'])
        self.filterbox.activated[str].connect(self.filters)
        self.sb_depth = QSpinBox(self)
        self.sb_depth.setMinimum(0)
        self.sb_depth.setMaximum(100)
        self.sb_depth.setGeometry(110, 0, 50, 30)

        self.spsp = []
        self.a = 0

    def Url_new_Imagen(self):
        c = False
        url = self.Urledit.text()
        self.Urledit.setText('')
        try:
            self.img = requests.get(url, stream=True).raw
            c = True
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Не возможно выполнить данное действие.\n "
                        "Возможно ссылка недействительна. Попробуйте другую ссылку...")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        if c:
            try:
                im = Image.open(self.img)
                im.save('Save-Imagen.png', 'png')
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Не забудте открыть сохраненое изображение...")
                msg.setWindowTitle("Успешно")
                msg.exec_()
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Не удалось сохранить изображение. \n"
                            "Попробуйте ещё раз...")
                msg.setWindowTitle("Ошибка")
                msg.exec_()

    def new_Imagen(self):
        try:
            self.new_img = QFileDialog.getOpenFileName(
                self, 'Выбрать картинку', '',
                'Картинка (*.png)'
            )[0]
            self.hesh = 'res.png'
            self.back = 'back.png'
            self.x = 'rezerv.png'
            im = QtGui.QImage()
            im.load(self.new_img)
            im.save(self.x)
            if self.new_img:
                self.pixmap = QPixmap(self.new_img)
                self.image.setPixmap(self.pixmap)
                self.image.setScaledContents(True)
        except:
            pass

    def Brights(self, value):
        try:
            im = Image.open(self.new_img)
            bright = ImageEnhance.Brightness(im)
            im = bright.enhance(value / 10000)
            im.save(self.hesh)
            self.pixmap = QPixmap(self.hesh)
            self.image.setPixmap(self.pixmap)
        except:
            self.error_im()

    def Contrast(self, value):
        try:
            im = Image.open(self.new_img)
            contraster = ImageEnhance.Contrast(im)
            im = contraster.enhance(value / 10000)
            im.save(self.hesh)
            self.pixmap = QPixmap(self.hesh)
            self.image.setPixmap(self.pixmap)
        except:
            self.error_im()

    def Rezkost(self, value):
        try:
            im = Image.open(self.new_img)
            rezkoster = ImageEnhance.Sharpness(im)
            im = rezkoster.enhance(value / 10000)
            im.save(self.hesh)
            self.pixmap = QPixmap(self.hesh)
            self.image.setPixmap(self.pixmap)
        except:
            self.error_im()

    def Visible(self, value):
        try:
            im_rgb = Image.open(self.new_img).convert('RGB')
            im_rgb.putalpha(int(value))
            im_rgb.save(self.hesh)
            self.pixmap = QPixmap(self.hesh)
            self.image.setPixmap(self.pixmap)
        except:
            self.error_im()

    def filters(self, filter):
        try:
            im = Image.open(self.new_img)
            im = im.convert("RGB")
            pix = im.load()
            x, y = im.size

            if filter == 'Cтандартное':
                im = QtGui.QImage()
                im.load(self.x)
                im.save(self.new_img)
                im.load(self.new_img)
                im.save(self.hesh)
                self.pixmap = QPixmap(self.hesh)
                self.image.setPixmap(self.pixmap)
                self.save_Imagen()

            if filter == 'Негатив':
                for i in range(x):
                    for j in range(y):
                        r, g, b = pix[i, j]
                        pix[i, j] = 255 - r, 255 - g, 255 - b
            if filter == 'Cепия':
                for i in range(x):
                    for j in range(y):
                        r, g, b = pix[i, j]
                        aver = (r + g + b) // 3
                        r = aver + int(self.sb_depth.text()) * 2
                        g = aver + int(self.sb_depth.text())
                        b = aver
                        if (r > 255):
                            r = 255
                        if (g > 255):
                            g = 255
                        if (b > 255):
                            b = 255
                        pix[i, j] = r, g, b
            if filter == 'ЧБ':
                for i in range(x):
                    for j in range(y):
                        r, g, b = pix[i, j]
                        Sum = (r + g + b)
                        if (Sum > (((255 + int(self.sb_depth.text())) // 2) * 3)):
                            r, g, b = 255, 255, 255
                        else:
                            r, g, b = 0, 0, 0
                        pix[i, j] = r, g, b
            if filter == 'Блюр':
                im = im.filter(ImageFilter.BLUR)
            if filter == 'Контур':
                im = im.filter(ImageFilter.CONTOUR)
            if filter == 'Маска':
                im = im.filter(ImageFilter.EMBOSS)
            if filter == 'EDGE_ENHANCE':
                im = im.filter(ImageFilter.EDGE_ENHANCE)
            if filter == 'ED_EN_MORE':
                im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
            if filter == 'FIND_EDGES':
                im = im.filter(ImageFilter.FIND_EDGES)
            im.save(self.hesh)
            self.pixmap = QPixmap(self.hesh)
            self.image.setPixmap(self.pixmap)
        except:
            self.error_im()

    def Back(self):
        try:
            im = QtGui.QImage()
            im.load(self.back)
            im.save(self.new_img)
            im.save(self.hesh)
            self.pixmap = QPixmap(self.hesh)
            self.image.setPixmap(self.pixmap)
            self.save_Imagen()


        except:
            self.error_im()

    def save_Imagen(self):
        try:
            im = QtGui.QImage()
            im.load(self.new_img)
            im.save(self.back)

            im = QtGui.QImage()
            im.load(self.hesh)
            im.save(self.new_img)


        except:
            self.error_im()

    def Rotate(self, value):
        try:
            im = Image.open(self.new_img)
            im = im.rotate(value)
            im.save(self.hesh)
            self.pixmap = QPixmap(self.hesh)
            self.image.setPixmap(self.pixmap)
        except:
            self.error_im()

    def Crop(self):
        try:
            im = Image.open(self.new_img)
            w, h = im.size
            otnhw = w / 1600
            otnhh = h / 900
            print(self.spsp)
            x, y, x1, y1 = self.spsp
            im = im.crop((int(x) * otnhw, int(y) * otnhh, int(x1) * otnhw, int(y1) * otnhh))
            im.save(self.hesh)
            self.pixmap = QPixmap(self.hesh)
            self.image.setPixmap(self.pixmap)
        except:
            self.error_im()

    def helper(self):
        self.txtHelp = QhelperWindow()
        self.txtHelp.show()

    def error_im(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Не возможно выполнить данное действие. \n"
                    "Попробуйте выбрать изображение...")
        msg.setWindowTitle("Ошибка")
        msg.exec_()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        self.spsp.append(x - 300)
        self.spsp.append(y - 20)
        if len(self.spsp) > 4:
            del self.spsp[0:2]
            del self.spsp[4:]
            print(self.spsp, 'EVENT')

    def keyPressEvent(self, event):
        if int(event.modifiers()) == (Qt.ShiftModifier):
            if event.key() == Qt.Key_Z:
                self.Back()
            if event.key() == Qt.Key_F5:
                self.save_Imagen()

    def closeEvent(self, event):
        notification = QtWidgets.QMessageBox.question \
            (self, 'Напоминание',
             "Вы не забыли сохранить изображение?",
             QtWidgets.QMessageBox.Yes,
             QtWidgets.QMessageBox.No)
        if notification == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SignUp()
    ex.show()
    app.exec()
    try:
        os.remove('rezerv.png')
        os.remove('res.png')
        os.remove('back.png')
    except:
        pass
    sys.exit()
