def AbdulaBD():
    code = """
    # Пример кода для подключения к БД
import pymysql

class Database:
    try:
        def __init__(self, host, user, password, database):
            self.connection = pymysql.connect(host=host, user=user, password=password, database=database)
            self.cursor = self.connection.cursor()
            print(":)")
    except:
        print(":(")

    # Пример запроса в БД
    def get_categ(self):
        query = 'SELECT names FROM types'
        self.cursor.execute(query)
        names = self.cursor.fetchall()
        return [name[0] for name in names]

db = Database(host='localhost', user='root', password='root', database='apteka')

    """
    return code

def AbdulaMain():
    code = """ 
    # Пример кода для main
import sys
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow,QLabel,QRadioButton,QCheckBox,QMessageBox,QSpinBox
from PyQt5.uic import loadUi
from database import Database

class Itog(QMainWindow):
    def __init__(self,user_id):
        super(Itog,self).__init__()
        loadUi("itog.ui",self)
        self.user_id = user_id
        self.db = Database(host='localhost', user='root', password='root', database='apteka')
        self.showBasket()
        self.pushButton_3.clicked.connect(self.clear_basket)

    def clear_basket(self):
        for i in reversed(range(self.formLayout.count())):
            self.formLayout.itemAt(i).widget().setParent(None)

    def showBasket(self):
        query = f"SELECT nut_id, date, quatity FROM rubbin WHERE user_id = {self.user_id}"
        self.db.cursor.execute(query)
        orders = self.db.cursor.fetchall()

        if orders:
            total_price = 0
            total_items = 0
            order_text = ""
            for order in orders:
                nut_id = order[0]
                query = f"SELECT name, price FROM nutrition WHERE id = {nut_id}"
                self.db.cursor.execute(query)
                result = self.db.cursor.fetchone()
                if result:
                    name, price = result[0], result[1]
                    total_price += price * order[2]
                    total_items += order[2]
                    lb_text = f"РўРѕРІР°СЂ: {name}, Р”Р°С‚Р° Р·Р°РєР°Р·Р°: {order[1]}\n"
                    lb = QLabel(lb_text)
                    order_text = f"РћР±С‰РµРµ РєРѕР»РёС‡РµСЃС‚РІРѕ С‚РѕРІР°СЂРѕРІ: {total_items}\nРћР±С‰Р°СЏ СЃСѓРјРјР°: {total_price}СЂ\n"

                    quatity = int(order[2])
                    spinBox = QSpinBox()
                    spinBox.setValue(quatity)
                    self.formLayout.addWidget(lb)
                    self.formLayout.addWidget(spinBox)

            count_price_text = QLabel(order_text)
            self.verticalLayout.addWidget(count_price_text)

class MainWindow(QMainWindow):
    def __init__(self, user_id):
        super(MainWindow, self).__init__()
        self.user_id = user_id
        loadUi("window.ui", self)
        self.db = Database(host='localhost', user='root', password='root', database='apteka')
        self.comboBox.currentIndexChanged.connect(self.show_tovar)
        self.pushButton.clicked.connect(self.order)
        self.pushButton_2.clicked.connect(self.show_order)
        # self.pushButton_3.clicked.connect(self.back)


        #Combobox
        names = self.db.get_categ()
        self.comboBox.addItems(names)

        #CheckBox
    def show_tovar(self):
        comboindex = self.comboBox.currentIndex() + 1
        query = f"SELECT id,name,price FROM nutrition WHERE type_id = {comboindex}"
        self.db.cursor.execute(query)
        names = self.db.cursor.fetchall()
        self.db.connection.commit()

        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().setParent(None)

        for name in names:
            self.box = QCheckBox("{}.{}-{}СЂ".format(name[0],name[1],name[2]))
            self.verticalLayout.addWidget(self.box)

    def order(self):
        if not self.user_id:
            print("РћС€РёР±РєР°: РџРѕР»СЊР·РѕРІР°С‚РµР»СЊ РЅРµ Р°РІС‚РѕСЂРёР·РѕРІР°РЅ.")
            return

        checked_ids = []

        for i in range(self.verticalLayout.count()):
            widget = self.verticalLayout.itemAt(i).widget()
            if isinstance(widget, QCheckBox) and widget.isChecked():
                item_text = widget.text()
                item_id = item_text.split(".")[0]
                checked_ids.append(item_id)

        if checked_ids:
            for item_id in checked_ids:

                query = f"SELECT id FROM rubbin WHERE nut_id = {item_id} AND user_id = {self.user_id}"
                self.db.cursor.execute(query)
                existing_order = self.db.cursor.fetchone()
                if existing_order:

                    update_query = f"UPDATE rubbin SET quatity = quatity + 1 WHERE id = {existing_order[0]}"
                    self.db.cursor.execute(update_query)
                    self.db.connection.commit()
                else:

                    insert_query = f"INSERT INTO rubbin (nut_id, date, quatity, user_id) VALUES ({item_id}, NOW(), 1, {self.user_id})"
                    self.db.cursor.execute(insert_query)
                    self.db.connection.commit()


                    update_query = f"UPDATE nutrition SET quatity = quatity - 1, reserv = reserv + 1 WHERE id = {item_id}"
                    self.db.cursor.execute(update_query)
                    self.db.connection.commit()

            print("Р—Р°РєР°Р· СѓСЃРїРµС€РЅРѕ РґРѕР±Р°РІР»РµРЅ РІ Р±Р°Р·Сѓ РґР°РЅРЅС‹С….")
        else:
            print("РќРµС‚ РѕС‚РјРµС‡РµРЅРЅС‹С… С‚РѕРІР°СЂРѕРІ")

    def show_order(self):
        self.window = Itog(self.user_id)
        self.window.show()

class Aut(QMainWindow):
    def __init__(self):
        super(Aut,self).__init__()
        loadUi("aut.ui",self)
        self.db = Database(host='localhost', user='root', password='root', database='apteka')
        self.pushButton.clicked.connect(self.aut)

    #РђРІС‚РѕСЂРёР·Р°С†РёСЏ
    def aut(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()

        try:
            query = "SELECT id ,username, password FROM user WHERE username = %s AND password = %s"
            self.db.cursor.execute(query, (login, password))
            result = self.db.cursor.fetchone()

            if result:
                self.user_id = result[0]
                window.hide()
                self.window = MainWindow(self.user_id)
                self.window.show()
            else:
                QMessageBox.critical(self, "РћС€РёР±РєР° РІ Р°РІС‚РѕСЂРёР·Р°С†РёРё",
                                     "РћС€РёР±РєР° РІ Р°РІС‚РѕСЂРёР·Р°С†РёРё\nРќРµРІРµСЂРЅРѕ РЅР°Р±СЂР°РЅ Р»РѕРіРёРЅ РёР»Рё РїР°СЂРѕР»СЊ")
        except Exception as e:
            print("",e)
            QMessageBox.critical(self, "РћС€РёР±РєР°", "РџРѕР»Рµ Р»РѕРіРёРЅ РёР»Рё РїР°СЂРѕР»СЊ РїСѓСЃС‚С‹Рµ")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Aut()
    window.show()
    app.exit(app.exec_())
    """
    return code

def AbdulaUI():
    code = """ 
    #Аунтификация
    <?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>450</width>
    <height>500</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>450</width>
    <height>500</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>450</width>
    <height>500</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>Авторизация</string>
  </property>
  <property name="styleSheet">
   <string notr="true">background-color: rgb(255, 255, 255);</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>80</x>
      <y>380</y>
      <width>301</width>
      <height>51</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">font: 75 10pt &quot;Microsoft YaHei UI&quot;;
font-weight: bold;
color: rgb(255, 255, 255);
background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(61, 217, 245), stop:1 rgb(240, 53, 218));
border-style: solid;
border-radius:21px;</string>
    </property>
    <property name="text">
     <string>ВОЙТИ</string>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>10</y>
      <width>401</width>
      <height>91</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>26</pointsize>
      <weight>75</weight>
      <bold>true</bold>
     </font>
    </property>
    <property name="text">
     <string>Авторизация</string>
    </property>
    <property name="alignment">
     <set>Qt::AlignCenter</set>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>140</y>
      <width>141</width>
      <height>16</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>9</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">color: rgb(141, 141, 141);</string>
    </property>
    <property name="text">
     <string>Имя пользователя</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="lineEdit">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>170</y>
      <width>391</width>
      <height>31</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">color: rgb(107, 107, 107);</string>
    </property>
    <property name="inputMask">
     <string/>
    </property>
    <property name="text">
     <string/>
    </property>
    <property name="placeholderText">
     <string>Введите своё имя пользователя</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="lineEdit_2">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>270</y>
      <width>391</width>
      <height>31</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">color: rgb(107, 107, 107);</string>
    </property>
    <property name="inputMask">
     <string/>
    </property>
    <property name="text">
     <string/>
    </property>
    <property name="maxLength">
     <number>32767</number>
    </property>
    <property name="echoMode">
     <enum>QLineEdit::Password</enum>
    </property>
    <property name="dragEnabled">
     <bool>false</bool>
    </property>
    <property name="placeholderText">
     <string>Введите свой пароль</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_3">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>240</y>
      <width>141</width>
      <height>16</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>9</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">color: rgb(141, 141, 141);</string>
    </property>
    <property name="text">
     <string>Пароль</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>450</width>
     <height>26</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>



    #Main
    <?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>800</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>800</width>
    <height>800</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>800</width>
    <height>800</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>Магазин Детского питания</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>200</x>
      <y>10</y>
      <width>401</width>
      <height>91</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>26</pointsize>
      <weight>75</weight>
      <bold>true</bold>
     </font>
    </property>
    <property name="text">
     <string>АПТЕКА ДАРБ</string>
    </property>
    <property name="alignment">
     <set>Qt::AlignCenter</set>
    </property>
   </widget>
   <widget class="QComboBox" name="comboBox">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>180</y>
      <width>701</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>10</pointsize>
      <weight>75</weight>
      <bold>true</bold>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">color: rgb(255, 255, 255);
background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(61, 217, 245), stop:1 rgb(240, 53, 218));
border-style: solid;
border-radius:15px;</string>
    </property>
   </widget>
   <widget class="QWidget" name="verticalLayoutWidget">
    <property name="geometry">
     <rect>
      <x>70</x>
      <y>300</y>
      <width>661</width>
      <height>311</height>
     </rect>
    </property>
    <layout class="QVBoxLayout" name="verticalLayout"/>
   </widget>
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>60</x>
      <y>670</y>
      <width>301</width>
      <height>51</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">font: 75 10pt &quot;Microsoft YaHei UI&quot;;
font-weight: bold;
color: rgb(255, 255, 255);
background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(61, 217, 245), stop:1 rgb(240, 53, 218));
border-style: solid;
border-radius:21px;</string>
    </property>
    <property name="text">
     <string>ДОБАВИТЬ В КОРЗИНУ</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_2">
    <property name="geometry">
     <rect>
      <x>440</x>
      <y>670</y>
      <width>301</width>
      <height>51</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">font: 75 10pt &quot;Microsoft YaHei UI&quot;;
font-weight: bold;
color: rgb(255, 255, 255);
background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(61, 217, 245), stop:1 rgb(240, 53, 218));
border-style: solid;
border-radius:21px;</string>
    </property>
    <property name="text">
     <string>КОРЗИНА</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>150</y>
      <width>151</width>
      <height>21</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>9</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">color: rgb(141, 141, 141);</string>
    </property>
    <property name="text">
     <string>Выберите категорию</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_3">
    <property name="geometry">
     <rect>
      <x>70</x>
      <y>270</y>
      <width>151</width>
      <height>16</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>9</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">color: rgb(141, 141, 141);</string>
    </property>
    <property name="text">
     <string>Товары</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_3">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>10</y>
      <width>101</width>
      <height>21</height>
     </rect>
    </property>
    <property name="layoutDirection">
     <enum>Qt::LeftToRight</enum>
    </property>
    <property name="styleSheet">
     <string notr="true">font: 75 10pt &quot;Microsoft YaHei UI&quot;;
font-weight: bold;
color: rgb(255, 255, 255);
background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(61, 217, 245), stop:1 rgb(240, 53, 218));
border-style: solid;
border-radius:8px;</string>
    </property>
    <property name="text">
     <string> &lt; НАЗАД</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>



    """
    return code

def var5BD():
    code = """
   --
-- База данных: `warehouse2`
--

-- --------------------------------------------------------

--
-- Структура таблицы `categories`
--

CREATE TABLE `categories` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `categories`
--

INSERT INTO `categories` (`id`, `name`) VALUES
(1, 'Категория 1'),
(2, 'Категория 2'),
(3, '2'),
(4, '1'),
(5, 'Насыпной'),
(6, 'Опасный'),
(7, 'Наливной');

-- --------------------------------------------------------

--
-- Структура таблицы `shipments`
--

CREATE TABLE `shipments` (
  `id` int NOT NULL,
  `number` varchar(255) NOT NULL,
  `delivery_date` date NOT NULL,
  `weight` decimal(10,2) NOT NULL,
  `pallets` int NOT NULL,
  `category_id` int NOT NULL,
  `supplier_id` int NOT NULL,
  `location` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `shipments`
--

INSERT INTO `shipments` (`id`, `number`, `delivery_date`, `weight`, `pallets`, `category_id`, `supplier_id`, `location`) VALUES
(1, '01', '2011-11-20', '100.00', 7, 1, 2, '10'),
(2, '02', '2004-03-20', '200.00', 5, 3, 4, '6'),
(3, '03', '2023-05-12', '300.00', 7, 4, 6, '7'),
(4, '04', '2023-05-10', '500.00', 10, 4, 7, '3');

-- --------------------------------------------------------

--
-- Структура таблицы `suppliers`
--

CREATE TABLE `suppliers` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone_number` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `fax_number` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `suppliers`
--

INSERT INTO `suppliers` (`id`, `name`, `phone_number`, `fax_number`) VALUES
(1, 'Поставщик 1', '', ''),
(2, 'Поставщик 2', '', ''),
(3, 'Грузик', '', ''),
(4, '1', '', ''),
(5, 'ГРузило', '', ''),
(6, '4', '', ''),
(7, '3', '', ''),
(11, 'ИП Грузик', '8(915)222-33-44', '04455555545301'),
(80, 'ООО «ХимКо»', '8(996)782-33-44', '04452277745202'),
(143, 'ОАО «Буратино»', '8(915)222-65-64', '04452288845378');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('manager','clerk') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
(1, '1', '1', 'manager'),
(2, '2', '2', 'clerk');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `shipments`
--
ALTER TABLE `shipments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `supplier_id` (`supplier_id`);

--
-- Индексы таблицы `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `shipments`
--
ALTER TABLE `shipments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT для таблицы `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=144;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `shipments`
--
ALTER TABLE `shipments`
  ADD CONSTRAINT `shipments_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  ADD CONSTRAINT `shipments_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`);
COMMIT;

    """
    return code

def var5code():
    code = """
    import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QTextEdit, QMessageBox, QInputDialog


class WarehouseApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Система склада "Кладовая № 1"')
        self.resize(500, 300)

        self.login_label = QLabel('Логин')
        self.password_label = QLabel('Пароль')
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Войти')

        self.login_button.clicked.connect(self.login)

        login_layout = QHBoxLayout()
        login_layout.addWidget(self.login_label)
        login_layout.addWidget(self.login_input)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_input)

        form_layout = QVBoxLayout()
        form_layout.addLayout(login_layout)
        form_layout.addLayout(password_layout)
        form_layout.addWidget(self.login_button)

        self.setLayout(form_layout)

        # Подключение к базе данных
        try:
            self.db_connection = mysql.connector.connect(
                host='localhost',
                user='root',  # Имя пользователя для доступа к MySQL
                password='',  # Пароль для доступа к MySQL
                database='warehouse2'  # Название базы данных, которую мы создали
            )
        except mysql.connector.Error as e:
            QMessageBox.critical(self, 'Ошибка подключения к базе данных', str(e))
            sys.exit(1)

    def login(self):
        username = self.login_input.text()
        password = self.password_input.text()

        cursor = self.db_connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            role = user[3]
            if role == 'manager':
                self.manager_window = WarehouseManagerWindow(self.db_connection)
                self.manager_window.show()
            elif role == 'clerk':
                self.clerk_window = WarehouseClerkWindow(self.db_connection)
                self.clerk_window.show()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неизвестная роль пользователя')
        else:
            QMessageBox.warning(self, 'Ошибка авторизации', 'Неверный логин или пароль')


class WarehouseManagerWindow(QWidget):
    def __init__(self, db_connection):
        super().__init__()

        self.setWindowTitle('Интерфейс менеджера')
        self.resize(600, 400)
        self.db_connection = db_connection

        self.shipments_label = QLabel('Сводная информация о поставках')
        self.shipments_text = QTextEdit()
        self.shipments_text.setReadOnly(True)

        self.update_shipments_button = QPushButton('Обновить информацию о поставках')
        self.update_shipments_button.clicked.connect(self.update_shipments_info)

        self.shipment_location_button = QPushButton('Просмотреть информацию о местонахождении груза')
        self.shipment_location_button.clicked.connect(self.get_shipment_location)

        self.add_supplier_button = QPushButton('Добавить поставщика')
        self.add_supplier_button.clicked.connect(self.add_supplier)

        self.delete_supplier_button = QPushButton('Удалить поставщика')
        self.delete_supplier_button.clicked.connect(self.delete_supplier)

        self.edit_supplier_button = QPushButton('Редактировать поставщика')
        self.edit_supplier_button.clicked.connect(self.edit_supplier)

        self.generate_report_button = QPushButton('Сформировать отчет')
        self.generate_report_button.clicked.connect(self.generate_report)

        layout = QVBoxLayout()
        layout.addWidget(self.shipments_label)
        layout.addWidget(self.shipments_text)
        layout.addWidget(self.update_shipments_button)
        layout.addWidget(self.shipment_location_button)
        layout.addWidget(self.add_supplier_button)
        layout.addWidget(self.delete_supplier_button)
        layout.addWidget(self.edit_supplier_button)
        layout.addWidget(self.generate_report_button)

        self.setLayout(layout)

        self.update_shipments_info()

    def update_shipments_info(self):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM shipments"
        cursor.execute(query)
        shipments = cursor.fetchall()
        cursor.close()

        info = ""
        for shipment in shipments:
            info += f"Номер груза: {shipment[1]}\n"
            info += f"Дата поставки: {shipment[2]}\n"
            info += f"Вес в кг: {shipment[3]}\n"
            info += f"Количество палет: {shipment[4]}\n"
            info += "------------------------\n"

        self.shipments_text.setText(info)

    def get_shipment_location(self):
        shipment_number, ok_pressed = QInputDialog.getText(self, 'Просмотр информации о местонахождении груза',
                                                           'Введите номер груза')
        if ok_pressed and shipment_number.strip():
            cursor = self.db_connection.cursor()
            query = "SELECT location FROM shipments WHERE number = %s"
            cursor.execute(query, (shipment_number,))
            location = cursor.fetchone()
            cursor.close()
            if location:
                QMessageBox.information(self, 'Местонахождение груза',
                                        f"Груз с номером {shipment_number} находится в {location[0]}.")
            else:
                QMessageBox.warning(self, 'Ошибка', f"Груз с номером {shipment_number} не найден.")

    def add_supplier(self):
        supplier_name, ok_pressed = QInputDialog.getText(self, 'Добавление поставщика', 'Введите имя поставщика')
        if ok_pressed and supplier_name.strip():
            cursor = self.db_connection.cursor()
            query = "INSERT INTO suppliers (name) VALUES (%s)"
            cursor.execute(query, (supplier_name,))
            self.db_connection.commit()
            cursor.close()
            QMessageBox.information(self, 'Успех', 'Поставщик успешно добавлен.')
            self.update_shipments_info()

    def delete_supplier(self):
        supplier_id, ok_pressed = QInputDialog.getInt(self, 'Удаление поставщика', 'Введите ID поставщика')
        if ok_pressed:
            cursor = self.db_connection.cursor()
            query = "DELETE FROM suppliers WHERE id = %s"
            cursor.execute(query, (supplier_id,))
            self.db_connection.commit()
            cursor.close()
            QMessageBox.information(self, 'Успех', 'Поставщик успешно удален.')
            self.update_shipments_info()

    def edit_supplier(self):
        supplier_id, ok_pressed = QInputDialog.getInt(self, 'Редактирование поставщика', 'Введите ID поставщика')
        if ok_pressed:
            new_supplier_name, ok_pressed = QInputDialog.getText(self, 'Редактирование поставщика',
                                                                 'Введите новое имя поставщика')
            if ok_pressed and new_supplier_name.strip():
                cursor = self.db_connection.cursor()
                query = "UPDATE suppliers SET name = %s WHERE id = %s"
                cursor.execute(query, (new_supplier_name, supplier_id))
                self.db_connection.commit()
                cursor.close()
                QMessageBox.information(self, 'Успех', 'Имя поставщика успешно изменено.')
                self.update_shipments_info()

    def generate_report(self):
        # Получаем начальную и конечную даты отчета
        start_date, ok_pressed = QInputDialog.getText(self, 'Выбор даты', 'Введите начальную дату отчета (гггг-мм-дд)')
        if not ok_pressed or not start_date.strip():
            return
        end_date, ok_pressed = QInputDialog.getText(self, 'Выбор даты', 'Введите конечную дату отчета (гггг-мм-дд)')
        if not ok_pressed or not end_date.strip():
            return

        # Получаем информацию о поставках за выбранный период
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM shipments WHERE delivery_date BETWEEN %s AND %s"
        cursor.execute(query, (start_date, end_date))
        shipments = cursor.fetchall()

        # Получаем информацию об оплатах за выбранный период
        query = "SELECT * FROM payments WHERE payment_date BETWEEN %s AND %s"
        cursor.execute(query, (start_date, end_date))
        payments = cursor.fetchall()

        cursor.close()

        # Словарь для хранения информации о суммах оплаты поставщикам
        supplier_payments = {}

        # Вычисляем сумму надлежащей оплаты за все поставки и сумму фактически оплаченных сумм
        total_due_amount = 0
        total_paid_amount = 0
        for shipment in shipments:
            total_due_amount += shipment[6]  # Предполагаемая сумма оплаты поставщику
        for payment in payments:
            total_paid_amount += payment[2]  # Фактически оплаченная сумма

        # Собираем информацию о суммах оплаты поставщикам
        for shipment in shipments:
            supplier_id = shipment[7]
            if supplier_id not in supplier_payments:
                supplier_payments[supplier_id] = {'total_due': 0, 'total_paid': 0}
            supplier_payments[supplier_id]['total_due'] += shipment[6]
        for payment in payments:
            supplier_id = payment[3]
            supplier_payments[supplier_id]['total_paid'] += payment[2]

        # Формируем текст отчета
        report_text = f"Отчет о поставках за период с {start_date} по {end_date}:\n"
        report_text += f"Всего надлежащая сумма к оплате: {total_due_amount}\n"
        report_text += f"Фактически оплачено: {total_paid_amount}\n\n"
        report_text += "Суммы оплаты поставщикам:\n"
        for supplier_id, payment_info in supplier_payments.items():
            report_text += f"Поставщик ID {supplier_id}:\n"
            report_text += f"Надлежащая сумма к оплате: {payment_info['total_due']}\n"
            report_text += f"Фактически оплачено: {payment_info['total_paid']}\n"
            report_text += f"Остаток к оплате: {payment_info['total_due'] - payment_info['total_paid']}\n\n"

        # Отображаем отчет в диалоговом окне
        report_dialog = QMessageBox()
        report_dialog.setWindowTitle("Отчет о поставках")
        report_dialog.setText(report_text)
        report_dialog.exec_()


class WarehouseClerkWindow(QWidget):
    def __init__(self, db_connection):
        super().__init__()

        self.setWindowTitle('Интерфейс кладовщика')
        self.resize(600, 400)
        self.db_connection = db_connection

        self.inventory_label = QLabel('Список грузов на складе')
        self.inventory_text = QTextEdit()
        self.inventory_text.setReadOnly(True)

        self.update_inventory_button = QPushButton('Обновить информацию о грузах')
        self.update_inventory_button.clicked.connect(self.update_inventory_info)

        self.register_shipment_button = QPushButton('Зарегистрировать новый груз')
        self.register_shipment_button.clicked.connect(self.register_shipment)
        self.change_location_button = QPushButton('Изменить расположение груза')
        self.change_location_button.clicked.connect(self.change_location)

        layout = QVBoxLayout()
        layout.addWidget(self.inventory_label)
        layout.addWidget(self.inventory_text)
        layout.addWidget(self.update_inventory_button)
        layout.addWidget(self.register_shipment_button)
        layout.addWidget(self.change_location_button)

        self.setLayout(layout)

        self.update_inventory_info()

    def update_inventory_info(self):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM shipments"
        cursor.execute(query)
        shipments = cursor.fetchall()
        cursor.close()

        info = ""
        for shipment in shipments:
            info += f"Номер груза: {shipment[1]}\n"
            info += f"Дата поставки: {shipment[2]}\n"
            info += f"Вес в кг: {shipment[3]}\n"
            info += f"Количество палет: {shipment[4]}\n"
            info += f"Расположение: {shipment[5]}\n"
            info += "------------------------\n"

        self.inventory_text.setText(info)

    def register_shipment(self):
        shipment_number, ok_pressed = QInputDialog.getText(self, 'Регистрация нового груза', 'Введите номер груза')
        if ok_pressed and shipment_number.strip():
            delivery_date, ok_pressed = QInputDialog.getText(self, 'Регистрация нового груза',
                                                             'Введите дату поставки (гггг-мм-дд)')
            if ok_pressed and delivery_date.strip():
                weight, ok_pressed = QInputDialog.getDouble(self, 'Регистрация нового груза', 'Введите вес груза в кг')
                if ok_pressed:
                    pallets, ok_pressed = QInputDialog.getInt(self, 'Регистрация нового груза',
                                                              'Введите количество палет')
                    if ok_pressed:
                        location, ok_pressed = QInputDialog.getText(self, 'Регистрация нового груза',
                                                                    'Введите место расположения груза')
                        if ok_pressed and location.strip():
                            category_id = self.get_category_id()
                            supplier_id = self.get_supplier_id()
                            if shipment_number and delivery_date and weight and pallets and location and category_id and supplier_id:
                                cursor = self.db_connection.cursor()
                                query = "INSERT INTO shipments (number, delivery_date, weight, pallets, location, category_id, supplier_id) " \
                                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                                cursor.execute(query, (
                                    shipment_number, delivery_date, weight, pallets, location, category_id,
                                    supplier_id))
                                self.db_connection.commit()
                                cursor.close()
                                QMessageBox.information(self, 'Успех', 'Новый груз успешно зарегистрирован.')
                                self.update_inventory_info()
                            else:
                                QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, заполните все поля.')

    def get_category_id(self):
        category_name, ok_pressed = QInputDialog.getText(self, 'Регистрация нового груза', 'Введите категорию груза')
        if ok_pressed and category_name.strip():
            cursor = self.db_connection.cursor()
            query = "SELECT id FROM categories WHERE name = %s"
            cursor.execute(query, (category_name,))
            category = cursor.fetchone()
            cursor.close()
            if category:
                return category[0]
            else:
                cursor = self.db_connection.cursor()
                query = "INSERT INTO categories (name) VALUES (%s)"
                cursor.execute(query, (category_name,))
                self.db_connection.commit()
                cursor.close()
                return self.get_category_id()

    def get_supplier_id(self):
        supplier_name, ok_pressed = QInputDialog.getText(self, 'Регистрация нового груза', 'Введите поставщика груза')
        if ok_pressed and supplier_name.strip():
            cursor = self.db_connection.cursor()
            query = "SELECT id FROM suppliers WHERE name = %s"
            cursor.execute(query, (supplier_name,))
            supplier = cursor.fetchone()
            cursor.close()
            if supplier:
                return supplier[0]
            else:
                cursor = self.db_connection.cursor()
                query = "INSERT INTO suppliers (name) VALUES (%s)"
                cursor.execute(query, (supplier_name,))
                self.db_connection.commit()
                cursor.close()
                return self.get_supplier_id()

    def change_location(self):
        shipment_number, ok_pressed = QInputDialog.getText(self, 'Изменение расположения груза', 'Введите номер груза')
        if ok_pressed and shipment_number.strip():
            new_location, ok_pressed = QInputDialog.getText(self, 'Изменение расположения груза',
                                                            'Введите новое расположение груза')
            if ok_pressed and new_location.strip():
                cursor = self.db_connection.cursor()
                query = "UPDATE shipments SET location = %s WHERE number = %s"
                cursor.execute(query, (new_location, shipment_number))
                self.db_connection.commit()
                cursor.close()
                QMessageBox.information(self, 'Успех', 'Расположение груза успешно изменено.')
                self.update_inventory_info()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WarehouseApp()
    window.show()
    sys.exit(app.exec_())

    """
    return code

def var8BD():
    code = """ 
    CREATE TABLE `deti` (
  `id` int NOT NULL,
  `name` varchar(30) NOT NULL,
  `pri4ina` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `deti`
--

INSERT INTO `deti` (`id`, `name`, `pri4ina`) VALUES
(1, 'Игорь', 'Другое ');

-- --------------------------------------------------------

--
-- Структура таблицы `grupp_pedagog`
--

CREATE TABLE `grupp_pedagog` (
  `id` int NOT NULL,
  `id_pedagog_1` int NOT NULL,
  `id_pedagog_2` int NOT NULL,
  `id_gryppa` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `grupp_pedagog`
--

INSERT INTO `grupp_pedagog` (`id`, `id_pedagog_1`, `id_pedagog_2`, `id_gryppa`) VALUES
(1, 1, 2, 1),
(2, 2, 1, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `gryppa`
--

CREATE TABLE `gryppa` (
  `id` int NOT NULL,
  `nomer_grypp` int NOT NULL,
  `na4alo_raboti` date NOT NULL,
  `name_grypp` varchar(50) NOT NULL,
  `kol_dite` int NOT NULL,
  `kategori_grypp` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `gryppa`
--

INSERT INTO `gryppa` (`id`, `nomer_grypp`, `na4alo_raboti`, `name_grypp`, `kol_dite`, `kategori_grypp`) VALUES
(1, 221, '2009-08-20', 'Бельчата', 30, 'Общая'),
(2, 224, '2010-08-20', 'Зайчата', 28, 'Спортивная');

-- --------------------------------------------------------

--
-- Структура таблицы `pedagog`
--

CREATE TABLE `pedagog` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `id_nomer_grypp` int NOT NULL,
  `telefon` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `pedagog`
--

INSERT INTO `pedagog` (`id`, `name`, `id_nomer_grypp`, `telefon`) VALUES
(1, 'Иванов Иван Иванович', 1, '8(915)222-33-44'),
(2, 'Дбар Марина Валентиновна', 2, '8(915)222-65-64');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `roli` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `user_name`, `password`, `roli`) VALUES
(1, 'user1', 'password1', 'Admin');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `deti`
--
ALTER TABLE `deti`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `grupp_pedagog`
--
ALTER TABLE `grupp_pedagog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_gryppa` (`id_gryppa`),
  ADD KEY `id_pedagog_1` (`id_pedagog_1`),
  ADD KEY `id_pedagog_2` (`id_pedagog_2`);

--
-- Индексы таблицы `gryppa`
--
ALTER TABLE `gryppa`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `pedagog`
--
ALTER TABLE `pedagog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_nomer_grypp` (`id_nomer_grypp`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `deti`
--
ALTER TABLE `deti`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `grupp_pedagog`
--
ALTER TABLE `grupp_pedagog`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `gryppa`
--
ALTER TABLE `gryppa`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `pedagog`
--
ALTER TABLE `pedagog`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `grupp_pedagog`
--
ALTER TABLE `grupp_pedagog`
  ADD CONSTRAINT `grupp_pedagog_ibfk_2` FOREIGN KEY (`id_gryppa`) REFERENCES `gryppa` (`id`),
  ADD CONSTRAINT `grupp_pedagog_ibfk_3` FOREIGN KEY (`id_pedagog_1`) REFERENCES `pedagog` (`id_nomer_grypp`),
  ADD CONSTRAINT `grupp_pedagog_ibfk_4` FOREIGN KEY (`id_pedagog_2`) REFERENCES `pedagog` (`id_nomer_grypp`);
COMMIT;
    """
    return code

def var8code():
    code = """ 
    Библиотека pip install mysql-connector-python

import mysql.connector
from tkinter import *

# Подключение к базе данных
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='nepoceda'
)

# Создаем объект курсора для выполнения SQL-запросов
cursor = db_connection.cursor()

# Функция для отображения списка воспитателей
def show_pedagog_data():
    # Закрываем текущее окно
    root.destroy()

    # Отображаем информацию о воспитателях из таблицы pedagog
    pedagog_window = Tk()
    pedagog_window.title("Данные воспитателей")

    # Функция для просмотра журнала групп
    def show_group_journal():
        # Запрос к базе данных для получения информации о группах из таблицы gryppa
        select_query = "SELECT nomer_grypp, na4alo_raboti, name_grypp, kol_dite, kategori_grypp FROM gryppa"
        cursor.execute(select_query)
        gryppa_data = cursor.fetchall()

        # Отображаем информацию о журнале групп
        journal_window = Toplevel()
        journal_window.title("Журнал групп")

        for nomer_grypp, na4alo_raboti, name_grypp, kol_dite, kategori_grypp in gryppa_data:
            Label(journal_window, text=f"Группа: {name_grypp}").pack()
            Label(journal_window, text=f"Номер группы: {nomer_grypp}").pack()
            Label(journal_window, text=f"Начало занятий: {na4alo_raboti}").pack()
            Label(journal_window, text=f"Количество детей: {kol_dite}").pack()
            Label(journal_window, text=f"Категория группы: {kategori_grypp}").pack()
            Label(journal_window, text="").pack()

        # Функция для просмотра пропусков детей и изменения данных
        def view_absences():
            absences_window = Toplevel()
            absences_window.title("Пропуски детей")

            # Запрос к базе данных для получения информации о детях из таблицы deti
            select_absences_query = "SELECT name, pri4ina FROM deti"
            cursor.execute(select_absences_query)
            absences_data = cursor.fetchall()

            for name, pri4ina in absences_data:
                Label(absences_window, text=f"Имя: {name}").pack()
                Label(absences_window, text=f"Причина: {pri4ina}").pack()
                Label(absences_window, text="").pack()

            # Функция для изменения данных о ребенке
            def edit_child_data():
                edit_window = Toplevel()
                edit_window.title("Изменить данные ребенка")

                def save_changes():
                    new_name = new_name_entry.get()
                    new_reason = new_reason_entry.get()

                    # Обновляем информацию в таблице deti для данного ребенка
                    update_query = "UPDATE deti SET name = %s, pri4ina = %s WHERE name = %s"
                    cursor.execute(update_query, (new_name, new_reason, name))
                    db_connection.commit()
                    print(f"Данные ребенка {name} успешно изменены.")
                    edit_window.destroy()

                Label(edit_window, text="Имя:").pack()
                new_name_entry = Entry(edit_window)
                new_name_entry.pack()

                Label(edit_window, text="Причина:").pack()
                new_reason_entry = Entry(edit_window)
                new_reason_entry.pack()

                Button(edit_window, text="Сохранить", command=save_changes).pack()

            Button(absences_window, text="Изменить данные", command=edit_child_data).pack()

        Button(journal_window, text="Просмотр пропусков", command=view_absences).pack()

        journal_window.mainloop()

    # Функция для изменения данных воспитателя
    def edit_pedagog_info(pedagog_id):
        # Отображаем окно для изменения данных
        edit_window = Toplevel()
        edit_window.title(f"Изменить данные воспитателя {pedagog_id}")

        # Функция для сохранения измененных данных
        def save_changes():
            new_name = new_name_entry.get()
            new_telefon = new_telefon_entry.get()

            # Обновляем информацию в таблице pedagog для данного воспитателя
            update_query = "UPDATE pedagog SET name = %s, telefon = %s WHERE id = %s"
            cursor.execute(update_query, (new_name, new_telefon, pedagog_id))
            db_connection.commit()
            print(f"Информация для воспитателя {pedagog_id} успешно обновлена.")
            edit_window.destroy()
            show_pedagog_data()

        # Отображаем форму для изменения данных
        Label(edit_window, text="Имя:").pack()
        new_name_entry = Entry(edit_window)
        new_name_entry.pack()

        Label(edit_window, text="Телефон:").pack()
        new_telefon_entry = Entry(edit_window)
        new_telefon_entry.pack()

        Button(edit_window, text="Сохранить", command=save_changes).pack()

    # Запрос к базе данных для получения данных воспитателей
    select_query = "SELECT id, name, telefon FROM pedagog"
    cursor.execute(select_query)
    pedagog_data = cursor.fetchall()

    # Отображаем данные воспитателей
    for pedagog_id, name, telefon in pedagog_data:
        Label(pedagog_window, text=f"Воспитатель {pedagog_id}:").pack()
        Label(pedagog_window, text=f"Имя: {name}").pack()
        Label(pedagog_window, text=f"Телефон: {telefon}").pack()

        Button(pedagog_window, text="Изменить данные", command=lambda id=pedagog_id: edit_pedagog_info(id)).pack()
        Label(pedagog_window, text="").pack()  # Добавляем пустую строку для разделения данных

    # Кнопка для просмотра журнала групп
    Button(pedagog_window, text="Просмотр журнала групп", command=show_group_journal).pack()

    pedagog_window.mainloop()

# Функция для проверки аутентификации
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Запрос к базе данных для проверки аутентификации
    query = "SELECT user_name, password FROM users WHERE user_name = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        print("Аутентификация успешна. Доступ разрешен.")
        show_pedagog_data()
    else:
        print("Ошибка аутентификации. Неверное имя пользователя или пароль.")

# Функция для регистрации нового пользователя
def register_user():
    register_window = Tk()
    register_window.title("Регистрация")

    Label(register_window, text="Логин:").pack()
    new_username_entry = Entry(register_window)
    new_username_entry.pack()

    Label(register_window, text="Пароль:").pack()
    new_password_entry = Entry(register_window, show="*")
    new_password_entry.pack()

    def save_registration_details():
        new_username = new_username_entry.get()
        new_password = new_password_entry.get()

        # Вставляем нового пользователя в таблицу users
        insert_query = "INSERT INTO users (user_name, password) VALUES (%s, %s)"
        cursor.execute(insert_query, (new_username, new_password))
        db_connection.commit()
        print("Регистрация успешна. Данные пользователя сохранены в базе данных.")
        register_window.destroy()

    Button(register_window, text="Зарегистрироваться", command=save_registration_details).pack()

# Создаем графический интерфейс
root = Tk()
root.title("Авторизация")

Label(root, text="Логин:").pack()
username_entry = Entry(root)
username_entry.pack()

Label(root, text="Пароль:").pack()
password_entry = Entry(root, show="*")
password_entry.pack()

Button(root, text="Войти", command=login).pack()
Button(root, text="Зарегистрироваться", command=register_user).pack()

root.mainloop()

# Закрываем соединение с базой данных
cursor.close()
db_connection.close()
    """
    return code

def var11BD():
    code = """
    -- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 13 2024 г., 03:05
-- Версия сервера: 10.1.48-MariaDB
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `school_interface`
--

-- --------------------------------------------------------

--
-- Структура таблицы `accounts`
--

CREATE TABLE `accounts` (
  `id` int(50) NOT NULL,
  `surename` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `firstname` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fathername` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `login` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `accounts`
--

INSERT INTO `accounts` (`id`, `surename`, `firstname`, `fathername`, `status`, `phone`, `email`, `login`, `password`) VALUES
(1, 'Ким', 'Анна', 'Валерьевна', 'active', '8(915)222-33-44', 'User1@mail.ru', 'Teach1', '11Teach'),
(2, 'Иванов', 'Сергей', 'Петрович', 'active', '8(917)998-33-23', 'User2@yandex.ru', 'Teach2', '22Teach'),
(3, 'Борисов', 'Борис', 'Борисович', 'active', '8(917)998-27-28', 'User4@yandex.ru', 'Teach4', '44Teach'),
(4, 'Соколова', 'Нина', 'Олеговна', 'active', '8(925)755-33-55', 'User5@mail.ru', 'Teach5', '55Teach'),
(5, 'Власюк', 'Мария', 'Викторовна', 'active', '8(999)022-77-02', 'User7@mail.ru', 'Teach7', '77Teach'),
(6, 'Цой', 'Алиса', 'Семеновна', 'active', '8(915)001-01-44', 'User8@mail.ru', 'Teach8', '88Teach'),
(7, 'Шмель', 'Фаина', 'Федоровна', 'active', '8(917)998-55-60', 'User9@mail.ru', 'Teach9', '9Teach'),
(8, 'Дартаньян', 'Артак', 'Самвелович', 'active', '89148310428', 'umo228@gmail.com', 'root', 'root'),
(9, 'Собчак', 'Ксения', 'Михайловна', 'banned', '88005553535', 'symbol@inbox.ru', 'teamspirit', 'monkey'),
(10, 'Трафальгар', 'Ди', 'Вотерло', 'active', '89259625033', 'funpay@joykorzina.ru', 'vsemaiki', 'mortira');

-- --------------------------------------------------------

--
-- Структура таблицы `classes`
--

CREATE TABLE `classes` (
  `id` int(50) NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `classes`
--

INSERT INTO `classes` (`id`, `name`) VALUES
(1, '5'),
(2, '6'),
(3, '7'),
(4, '8');

-- --------------------------------------------------------

--
-- Структура таблицы `lessons`
--

CREATE TABLE `lessons` (
  `id` int(50) NOT NULL,
  `class_id` int(50) NOT NULL,
  `teacher_id` int(50) NOT NULL,
  `hours` int(50) NOT NULL,
  `discip` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `lessons`
--

INSERT INTO `lessons` (`id`, `class_id`, `teacher_id`, `hours`, `discip`) VALUES
(1, 1, 3, 50, 'Биология'),
(2, 1, 7, 75, 'Обществознание'),
(3, 1, 6, 85, 'Математика'),
(4, 1, 2, 45, 'Информатика');

-- --------------------------------------------------------

--
-- Структура таблицы `students`
--

CREATE TABLE `students` (
  `id` int(50) NOT NULL,
  `class_id` int(50) NOT NULL,
  `surename` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `firstname` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fathername` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `birthday_doc` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `students`
--

INSERT INTO `students` (`id`, `class_id`, `surename`, `firstname`, `fathername`, `birthday_doc`) VALUES
(1, 1, 'Барышев', 'Владимир', 'Магомедович', '85*6255'),
(2, 1, 'Бацаев', 'Абдула', 'Магомет-Баширович', '42354123'),
(3, 1, 'Еганов', 'Вячеслав', 'Борисович', '85192'),
(4, 1, 'Шишкин', 'Ильяс', 'Олеговна', '52525252'),
(5, 1, 'Карпова', 'Стефания', 'Викторовна', '65226225');

-- --------------------------------------------------------

--
-- Структура таблицы `teach_data`
--

CREATE TABLE `teach_data` (
  `id` int(50) NOT NULL,
  `acc_id` int(50) NOT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `education` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `teach_data`
--

INSERT INTO `teach_data` (`id`, `acc_id`, `category`, `education`) VALUES
(1, 1, 'Первая', 'высшее'),
(2, 2, 'вторая', 'высшее'),
(3, 3, '', 'высшее'),
(4, 4, 'Первая', 'магистратура'),
(5, 5, 'Высшая', 'высшее'),
(6, 7, 'Первая', 'высшее'),
(7, 9, 'Наивысшее', 'ученая степень');

-- --------------------------------------------------------

--
-- Структура таблицы `umo_data`
--

CREATE TABLE `umo_data` (
  `id` int(50) NOT NULL,
  `acc_id` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `umo_data`
--

INSERT INTO `umo_data` (`id`, `acc_id`) VALUES
(1, 8),
(2, 10);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `classes`
--
ALTER TABLE `classes`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `lessons`
--
ALTER TABLE `lessons`
  ADD PRIMARY KEY (`id`),
  ADD KEY `class_id` (`class_id`),
  ADD KEY `teacher_id` (`teacher_id`);

--
-- Индексы таблицы `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD KEY `class_id` (`class_id`);

--
-- Индексы таблицы `teach_data`
--
ALTER TABLE `teach_data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `acc_id` (`acc_id`);

--
-- Индексы таблицы `umo_data`
--
ALTER TABLE `umo_data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `acc_id` (`acc_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT для таблицы `classes`
--
ALTER TABLE `classes`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `lessons`
--
ALTER TABLE `lessons`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `students`
--
ALTER TABLE `students`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `teach_data`
--
ALTER TABLE `teach_data`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `umo_data`
--
ALTER TABLE `umo_data`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `lessons`
--
ALTER TABLE `lessons`
  ADD CONSTRAINT `lessons_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teach_data` (`id`),
  ADD CONSTRAINT `lessons_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`);

--
-- Ограничения внешнего ключа таблицы `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `students_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`);

--
-- Ограничения внешнего ключа таблицы `teach_data`
--
ALTER TABLE `teach_data`
  ADD CONSTRAINT `teach_data_ibfk_1` FOREIGN KEY (`acc_id`) REFERENCES `accounts` (`id`);

--
-- Ограничения внешнего ключа таблицы `umo_data`
--
ALTER TABLE `umo_data`
  ADD CONSTRAINT `umo_data_ibfk_1` FOREIGN KEY (`acc_id`) REFERENCES `accounts` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

    """
    return code

def var2BD():
    code = """--
-- База данных: `555`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Bookings`
--

CREATE TABLE `Bookings` (
  `BookingID` int NOT NULL,
  `MovieID` int NOT NULL,
  `SessionTime` time NOT NULL,
  `HallNumber` int NOT NULL,
  `TicketType` enum('Эконом','Комфорт','Детский') NOT NULL,
  `TicketID` int DEFAULT NULL,
  `ClientID` int NOT NULL,
  `TicketPrice` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Bookings`
--

INSERT INTO `Bookings` (`BookingID`, `MovieID`, `SessionTime`, `HallNumber`, `TicketType`, `TicketID`, `ClientID`, `TicketPrice`) VALUES
(1, 1, '10:00:00', 1, 'Комфорт', NULL, 1, '0.00');

-- --------------------------------------------------------

--
-- Структура таблицы `ClientMovies`
--

CREATE TABLE `ClientMovies` (
  `ClientID` int NOT NULL,
  `ClientName` varchar(255) NOT NULL,
  `Phone` varchar(15) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `MovieID` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `ClientMovies`
--

INSERT INTO `ClientMovies` (`ClientID`, `ClientName`, `Phone`, `Email`, `MovieID`) VALUES
(1, 'Иванов Иван', '1234567890', 'ivanov@example.com', 1),
(2, 'Петров Петр', '9876543210', 'petrov@example.com', 2),
(3, 'Сидоров Сидор', '5555555555', 'sidorov@example.com', 3);

-- --------------------------------------------------------

--
-- Структура таблицы `Managers`
--

CREATE TABLE `Managers` (
  `ManagerID` int NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Managers`
--

INSERT INTO `Managers` (`ManagerID`, `Username`, `Password`) VALUES
(1, 'manager', 'manager');

-- --------------------------------------------------------

--
-- Структура таблицы `Movies`
--

CREATE TABLE `Movies` (
  `MovieID` int NOT NULL,
  `Title` varchar(255) NOT NULL,
  `Genre` varchar(255) DEFAULT NULL,
  `Director` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Movies`
--

INSERT INTO `Movies` (`MovieID`, `Title`, `Genre`, `Director`) VALUES
(1, 'Фильм 1', 'Жанр 1', 'Режиссер 1'),
(2, 'Фильм 2', 'Жанр 2', 'Режиссер 2'),
(3, 'Фильм 3', 'Жанр 3', 'Режиссер 3');

-- --------------------------------------------------------

--
-- Структура таблицы `Tickets`
--

CREATE TABLE `Tickets` (
  `TicketID` int NOT NULL,
  `TicketType` enum('Эконом','Комфорт','Детский') NOT NULL,
  `TicketPrice` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Tickets`
--

INSERT INTO `Tickets` (`TicketID`, `TicketType`, `TicketPrice`) VALUES
(1, 'Эконом', '10.00'),
(2, 'Комфорт', '15.00'),
(3, 'Детский', '7.50'),
(4, 'Эконом', '10.00'),
(5, 'Комфорт', '15.00'),
(6, 'Детский', '7.50');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Bookings`
--
ALTER TABLE `Bookings`
  ADD PRIMARY KEY (`BookingID`),
  ADD KEY `MovieID` (`MovieID`),
  ADD KEY `TicketID` (`TicketID`),
  ADD KEY `ClientID` (`ClientID`);

--
-- Индексы таблицы `ClientMovies`
--
ALTER TABLE `ClientMovies`
  ADD PRIMARY KEY (`ClientID`),
  ADD KEY `MovieID` (`MovieID`);

--
-- Индексы таблицы `Managers`
--
ALTER TABLE `Managers`
  ADD PRIMARY KEY (`ManagerID`);

--
-- Индексы таблицы `Movies`
--
ALTER TABLE `Movies`
  ADD PRIMARY KEY (`MovieID`);

--
-- Индексы таблицы `Tickets`
--
ALTER TABLE `Tickets`
  ADD PRIMARY KEY (`TicketID`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Bookings`
--
ALTER TABLE `Bookings`
  MODIFY `BookingID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `ClientMovies`
--
ALTER TABLE `ClientMovies`
  MODIFY `ClientID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `Managers`
--
ALTER TABLE `Managers`
  MODIFY `ManagerID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `Movies`
--
ALTER TABLE `Movies`
  MODIFY `MovieID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `Tickets`
--
ALTER TABLE `Tickets`
  MODIFY `TicketID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `Bookings`
--
ALTER TABLE `Bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`MovieID`) REFERENCES `Movies` (`MovieID`),
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`TicketID`) REFERENCES `Tickets` (`TicketID`),
  ADD CONSTRAINT `bookings_ibfk_3` FOREIGN KEY (`ClientID`) REFERENCES `ClientMovies` (`ClientID`);

--
-- Ограничения внешнего ключа таблицы `ClientMovies`
--
ALTER TABLE `ClientMovies`
  ADD CONSTRAINT `clientmovies_ibfk_1` FOREIGN KEY (`MovieID`) REFERENCES `Movies` (`MovieID`);
COMMIT;

 """
    return code

def var2code():
    code = """import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, QLineEdit, \
    QMessageBox, QDialog, QTableWidgetItem, QTableWidget
import mysql.connector


class ClientInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Клиентская информационная система")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.label_movies = QLabel("Фильмы в прокате:")
        layout.addWidget(self.label_movies)

        self.combo_movies = QComboBox()
        layout.addWidget(self.combo_movies)

        self.label_session_time = QLabel("Время сеанса:")
        layout.addWidget(self.label_session_time)

        self.combo_session_time = QComboBox()
        self.combo_session_time.addItems(["10:00", "14:00", "18:00", "22:00"])  # Пример времен сеансов
        layout.addWidget(self.combo_session_time)

        self.label_hall_number = QLabel("Номер зала:")
        layout.addWidget(self.label_hall_number)

        self.combo_hall_number = QComboBox()
        self.combo_hall_number.addItems(["1", "2", "3"])  # Пример номеров залов
        layout.addWidget(self.combo_hall_number)

        self.label_ticket_type = QLabel("Тип билета:")
        layout.addWidget(self.label_ticket_type)

        self.combo_ticket_type = QComboBox()
        self.combo_ticket_type.addItems(["Эконом", "Комфорт", "Детский"])
        layout.addWidget(self.combo_ticket_type)

        self.label_ticket_price = QLabel("Стоимость билета:")
        layout.addWidget(self.label_ticket_price)

        self.line_ticket_price = QLineEdit()
        self.line_ticket_price.setReadOnly(True)  # Делаем поле только для чтения
        layout.addWidget(self.line_ticket_price)

        self.btn_book_tickets = QPushButton("Забронировать билеты")
        self.btn_book_tickets.clicked.connect(self.book_tickets)
        layout.addWidget(self.btn_book_tickets)

        self.btn_buy_tickets = QPushButton("Купить билеты")
        self.btn_buy_tickets.clicked.connect(self.open_buy_tickets_dialog)
        self.btn_buy_tickets.hide()  # Скрываем кнопку покупки билетов
        layout.addWidget(self.btn_buy_tickets)

        self.btn_switch_to_manager = QPushButton("Перейти к интерфейсу менеджера")
        self.btn_switch_to_manager.clicked.connect(self.switch_to_manager)
        layout.addWidget(self.btn_switch_to_manager)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Подключение к базе данных
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="555"
        )

        # Получение списка фильмов из базы данных и заполнение ComboBox
        self.populate_movie_list()

        # Обновление стоимости билета при изменении выбранного типа билета
        self.combo_ticket_type.currentIndexChanged.connect(self.update_ticket_price)

    def populate_movie_list(self):
        try:
            mycursor = self.db_connection.cursor()
            mycursor.execute("SELECT * FROM Movies")
            movies = mycursor.fetchall()
            for movie in movies:
                self.combo_movies.addItem(movie[1], movie[0])  # Добавляем название фильма в комбобокс и сохраняем MovieID в качестве пользовательских данных
        except mysql.connector.Error as err:
            print("Ошибка при получении списка фильмов:", err)

    def update_ticket_price(self):
        ticket_types_prices = {
            "Эконом": 100,
            "Комфорт": 150,
            "Детский": 80
        }
        selected_type = self.combo_ticket_type.currentText()
        price = ticket_types_prices.get(selected_type, 0)
        self.line_ticket_price.setText(str(price))

    def book_tickets(self):
        try:
            selected_movie_id = self.combo_movies.currentData()  # Получаем MovieID выбранного фильма
            selected_time = self.combo_session_time.currentText()
            selected_hall = self.combo_hall_number.currentText()
            selected_type = self.combo_ticket_type.currentText()
            selected_price = self.line_ticket_price.text()

            # Предположим, что мы используем клиента с ID = 1 для бронирования (можно изменить на реального клиента)
            client_id = 1

            mycursor = self.db_connection.cursor()
            mycursor.execute("INSERT INTO Bookings (MovieID, SessionTime, HallNumber, TicketType, TicketPrice, ClientID) VALUES (%s, %s, %s, %s, %s, %s)",
                             (selected_movie_id, selected_time, selected_hall, selected_type, selected_price, client_id))
            self.db_connection.commit()
            QMessageBox.information(self, "Успех", "Билеты успешно забронированы!")
            self.btn_book_tickets.setEnabled(False)
            self.btn_buy_tickets.show()
        except mysql.connector.Error as err:
            print("Ошибка при бронировании билетов:", err)
            QMessageBox.critical(self, "Ошибка", "Ошибка при бронировании билетов.")

    def open_buy_tickets_dialog(self):
        dialog = BuyTicketsDialog(self.db_connection)
        dialog.exec_()

    def switch_to_manager(self):
        manager_window.show()
        self.hide()


class ManagerInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Интерфейс менеджера")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.btn_add_session = QPushButton("Добавить киносеанс")
        self.btn_add_session.clicked.connect(self.add_session)
        layout.addWidget(self.btn_add_session)

        self.btn_view_bookings = QPushButton("Просмотреть бронирования")
        self.btn_view_bookings.clicked.connect(self.view_bookings)
        layout.addWidget(self.btn_view_bookings)

        self.btn_switch_to_client = QPushButton("Перейти к клиентской системе")
        self.btn_switch_to_client.clicked.connect(self.switch_to_client)
        layout.addWidget(self.btn_switch_to_client)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Подключение к базе данных
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="555"
        )

    def add_session(self):
        dialog = AddSessionDialog()
        if dialog.exec_() == QDialog.Accepted:
            # Если диалоговое окно закрыто с результатом "Принято" (т.е. новый сеанс добавлен), обновляем список фильмов в интерфейсе клиента
            client_window.populate_movie_list()

    def view_bookings(self):
        dialog = ViewBookingsDialog(self.db_connection)
        dialog.exec_()

    def switch_to_client(self):
        client_window.show()
        self.hide()


class AddSessionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить киносеанс")

        layout = QVBoxLayout()

        self.label_movie_title = QLabel("Название фильма:")
        layout.addWidget(self.label_movie_title)

        self.line_movie_title = QLineEdit()
        layout.addWidget(self.line_movie_title)

        self.label_session_time = QLabel("Время сеанса:")
        layout.addWidget(self.label_session_time)

        self.line_session_time = QLineEdit()
        layout.addWidget(self.line_session_time)

        self.label_hall_number = QLabel("Номер зала:")
        layout.addWidget(self.label_hall_number)

        self.line_hall_number = QLineEdit()
        layout.addWidget(self.line_hall_number)

        self.btn_add_session = QPushButton("Добавить")
        self.btn_add_session.clicked.connect(self.accept)
        layout.addWidget(self.btn_add_session)

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.clicked.connect(self.reject)
        layout.addWidget(self.btn_cancel)

        self.setLayout(layout)


class ViewBookingsDialog(QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.setWindowTitle("Просмотр бронирований")
        self.db_connection = db_connection

        layout = QVBoxLayout()

        self.table_bookings = QTableWidget()
        layout.addWidget(self.table_bookings)

        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.clicked.connect(self.refresh_table)
        layout.addWidget(self.btn_refresh)

        self.setLayout(layout)

        self.refresh_table()

    def refresh_table(self):
        try:
            mycursor = self.db_connection.cursor()
            mycursor.execute("SELECT * FROM Bookings")
            bookings = mycursor.fetchall()

            self.table_bookings.setRowCount(len(bookings))
            self.table_bookings.setColumnCount(6)
            self.table_bookings.setHorizontalHeaderLabels(["Номер брони", "Номер сеанса", "Номер зала", "Тип билета", "Стоимость билета", "Куплен"])

            for row_number, booking in enumerate(bookings):
                for column_number, data in enumerate(booking):
                    self.table_bookings.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении таблицы бронирований: {err}")


class BuyTicketsDialog(QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.setWindowTitle("Покупка билетов")
        self.db_connection = db_connection

        layout = QVBoxLayout()

        self.label_booking_number = QLabel("Номер брони:")
        layout.addWidget(self.label_booking_number)

        self.line_booking_number = QLineEdit()
        layout.addWidget(self.line_booking_number)

        self.btn_search_booking = QPushButton("Найти бронь")
        self.btn_search_booking.clicked.connect(self.search_booking)
        layout.addWidget(self.btn_search_booking)

        self.table_tickets = QTableWidget()
        layout.addWidget(self.table_tickets)

        self.btn_buy_tickets = QPushButton("Купить выбранные билеты")
        self.btn_buy_tickets.clicked.connect(self.buy_tickets)
        layout.addWidget(self.btn_buy_tickets)

        self.setLayout(layout)

    def search_booking(self):
        booking_number = self.line_booking_number.text()
        try:
            mycursor = self.db_connection.cursor()
            query = ("SELECT * FROM Bookings WHERE BookingID = %s")
            mycursor.execute(query, (booking_number,))
            booking = mycursor.fetchone()

            if booking:
                self.display_tickets(booking)
            else:
                QMessageBox.warning(self, "Предупреждение", "Бронь с указанным номером не найдена.")

        except mysql.connector.Error as err:
            print("Ошибка при поиске брони:", err)
            QMessageBox.critical(self, "Ошибка", "Ошибка при поиске брони.")

    def display_tickets(self, booking):
        try:
            mycursor = self.db_connection.cursor()
            query = ("SELECT * FROM Tickets WHERE BookingID = %s")
            mycursor.execute(query, (booking[0],))
            tickets = mycursor.fetchall()

            self.table_tickets.clear()
            self.table_tickets.setRowCount(len(tickets))
            self.table_tickets.setColumnCount(4)
            self.table_tickets.setHorizontalHeaderLabels(["ID", "Тип билета", "Стоимость билета", "Куплен"])

            for row_number, ticket in enumerate(tickets):
                for column_number, data in enumerate(ticket):
                    self.table_tickets.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except mysql.connector.Error as err:
            print("Ошибка при отображении билетов:", err)
            QMessageBox.critical(self, "Ошибка", "Ошибка при отображении билетов.")

    def buy_tickets(self):
        selected_rows = self.table_tickets.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Выберите хотя бы один билет для покупки.")
            return

        booking_number = self.line_booking_number.text()
        try:
            mycursor = self.db_connection.cursor()

            for row in selected_rows:
                ticket_id = self.table_tickets.item(row.row(), 0).text()
                query = ("UPDATE Tickets SET Purchased = 1 WHERE TicketID = %s AND BookingID = %s")
                mycursor.execute(query, (ticket_id, booking_number))
                self.db_connection.commit()

            QMessageBox.information(self, "Успех", "Выбранные билеты успешно куплены.")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при покупке билетов: {err}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_window = ClientInterface()
    manager_window = ManagerInterface()
    client_window.show()
    sys.exit(app.exec_())
 """
    return code

def var20BD():
    code = """-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 13 2024 г., 04:01
-- Версия сервера: 5.7.39
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `Kolobok20`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Categories`
--

CREATE TABLE `Categories` (
  `ID` bigint(20) UNSIGNED NOT NULL,
  `CategoryName` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Categories`
--

INSERT INTO `Categories` (`ID`, `CategoryName`) VALUES
(1, 'Молочные'),
(2, 'Крупы'),
(3, 'Овощи'),
(4, 'dad'),
(5, 'dada');

-- --------------------------------------------------------

--
-- Структура таблицы `Payments`
--

CREATE TABLE `Payments` (
  `ID` bigint(20) UNSIGNED NOT NULL,
  `ShipmentNumber` int(11) DEFAULT NULL,
  `PaymentDate` date DEFAULT NULL,
  `PaymentTime` time DEFAULT NULL,
  `BankName` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TotalAmount` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Payments`
--

INSERT INTO `Payments` (`ID`, `ShipmentNumber`, `PaymentDate`, `PaymentTime`, `BankName`, `TotalAmount`) VALUES
(1, 1, '2022-03-09', '12:00:00', 'Bank A', '700'),
(2, 2, '2022-03-09', '12:30:00', 'Bank B', '3825'),
(3, 3, '2022-03-09', '13:00:00', 'Bank C', '2400'),
(4, 4, '2022-03-10', '12:30:00', 'Bank A', '750'),
(5, 5, '2022-03-09', '13:00:00', 'Bank B', '6000'),
(6, 6, '2022-03-09', '14:00:00', 'Bank C', '6750'),
(7, 7, '2022-03-10', '13:00:00', 'Bank A', '2928'),
(8, 8, '2022-03-09', '14:30:00', 'Bank B', '5940'),
(9, 9, '2022-03-10', '14:00:00', 'Bank C', '2175'),
(10, 10, '2022-03-10', '15:00:00', 'Bank A', '780');

-- --------------------------------------------------------

--
-- Структура таблицы `Products`
--

CREATE TABLE `Products` (
  `ID` bigint(20) UNSIGNED NOT NULL,
  `ProductName` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Package` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Price` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Products`
--

INSERT INTO `Products` (`ID`, `ProductName`, `Package`, `Price`) VALUES
(1, 'Молоко', '1 литр', '70'),
(2, 'Сметана', '250 гр', '85'),
(3, 'Творог', '250 гр', '120'),
(4, 'Рис', '900 гр', '120'),
(5, 'Гречка', '900 гр', '135'),
(6, 'Чечевица', '900 гр', '132'),
(7, 'Помидоры', '1 кг', '87'),
(8, 'Апельсины', '1 кг', '65'),
(9, 'fsfd', 'affa', '14214'),
(10, 'йууй', 'вфв', '231'),
(11, 'ad', 'rfd', '4141'),
(12, 'вфвы', 'аф', '321'),
(13, 'вфвф', 'выаф', '1231'),
(14, 'dad', 'adsd', '144'),
(15, 'dad', 'ad', '123');

-- --------------------------------------------------------

--
-- Структура таблицы `Suppliers`
--

CREATE TABLE `Suppliers` (
  `ID` bigint(20) UNSIGNED NOT NULL,
  `SupplierName` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `SupplierPhone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `BIK` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `CheckingAccount` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Suppliers`
--

INSERT INTO `Suppliers` (`ID`, `SupplierName`, `SupplierPhone`, `BIK`, `CheckingAccount`) VALUES
(1, 'ИП МолКом', '8(915)222-33-44', '044555555', '04455555545301'),
(2, 'ООО «Колос»', '8(996)782-33-44', '044522777', '04452277745202'),
(3, 'Овощебаза №1', '8(915)222-65-64', '044522888', '04452288845378');

-- --------------------------------------------------------

--
-- Структура таблицы `Supplies`
--

CREATE TABLE `Supplies` (
  `ID` bigint(20) UNSIGNED NOT NULL,
  `DeliveryDate` date DEFAULT NULL,
  `SupplierID` int(11) DEFAULT NULL,
  `CategoryID` int(11) DEFAULT NULL,
  `ProductID` int(11) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `Price` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Supplies`
--

INSERT INTO `Supplies` (`ID`, `DeliveryDate`, `SupplierID`, `CategoryID`, `ProductID`, `Quantity`, `Price`) VALUES
(1, '2022-03-09', 1, 1, 1, 10, '70'),
(2, '2022-03-09', 1, 1, 2, 45, '85'),
(3, '2022-03-09', 1, 1, 3, 20, '120'),
(4, '2022-03-10', 1, 1, 1, 10, '75'),
(5, '2022-03-09', 2, 2, 4, 50, '120'),
(6, '2022-03-09', 2, 2, 5, 50, '135'),
(7, '2022-03-10', 2, 2, 4, 40, '117'),
(8, '2022-03-09', 2, 2, 6, 45, '132'),
(9, '2022-03-10', 3, 3, 7, 25, '87'),
(10, '2022-03-10', 3, 3, 8, 12, '65');

-- --------------------------------------------------------

--
-- Структура таблицы `Users`
--

CREATE TABLE `Users` (
  `ID` bigint(20) UNSIGNED NOT NULL,
  `Email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Password` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Users`
--

INSERT INTO `Users` (`ID`, `Email`, `Password`) VALUES
(1, '1', '2'),
(2, 'example2@example.com', 'password2'),
(3, 'example3@example.com', 'password3');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Categories`
--
ALTER TABLE `Categories`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`);

--
-- Индексы таблицы `Payments`
--
ALTER TABLE `Payments`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`);

--
-- Индексы таблицы `Products`
--
ALTER TABLE `Products`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`);

--
-- Индексы таблицы `Suppliers`
--
ALTER TABLE `Suppliers`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`);

--
-- Индексы таблицы `Supplies`
--
ALTER TABLE `Supplies`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`);

--
-- Индексы таблицы `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Categories`
--
ALTER TABLE `Categories`
  MODIFY `ID` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `Payments`
--
ALTER TABLE `Payments`
  MODIFY `ID` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `Products`
--
ALTER TABLE `Products`
  MODIFY `ID` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT для таблицы `Suppliers`
--
ALTER TABLE `Suppliers`
  MODIFY `ID` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `Supplies`
--
ALTER TABLE `Supplies`
  MODIFY `ID` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `Users`
--
ALTER TABLE `Users`
  MODIFY `ID` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
 """
    return code

def var20code():
    code = """
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QDialog, QMessageBox, QComboBox, QListWidget,
                             QTextEdit)

import pymysql

class LoginWindow(QDialog):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 200)

        self.email_label = QLabel("Email:")
        self.email_edit = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.user_login_button = QPushButton("Вход для пользователя")
        self.accountant_login_button = QPushButton("Вход для бухгалтера")

        layout = QVBoxLayout()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.user_login_button)
        layout.addWidget(self.accountant_login_button)

        self.user_login_button.clicked.connect(self.user_login)
        self.accountant_login_button.clicked.connect(self.accountant_login)

        self.setLayout(layout)

    def user_login(self):
        email = self.email_edit.text()
        password = self.password_edit.text()

        cursor = self.connection.cursor()
        query = "SELECT * FROM Users WHERE Email=%s AND Password=%s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            self.accept()
            self.user_type = "user"
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный email или пароль")

    def accountant_login(self):
        password = self.password_edit.text()

        if password == "root":
            self.accept()
            self.user_type = "accountant"
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный пароль для бухгалтера")


class EditProductDialog(QDialog):
    def __init__(self, connection, product_id=None):
        super().__init__()
        self.connection = connection
        self.product_id = product_id

        self.setWindowTitle("Редактировать товар")
        self.setGeometry(300, 300, 300, 200)

        self.product_name_label = QLabel("Название товара:")
        self.product_name_edit = QLineEdit()
        self.product_price_label = QLabel("Цена:")
        self.product_price_edit = QLineEdit()
        self.package_label = QLabel("Упаковка:")
        self.package_edit = QLineEdit()
        self.save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()
        layout.addWidget(self.product_name_label)
        layout.addWidget(self.product_name_edit)
        layout.addWidget(self.product_price_label)
        layout.addWidget(self.product_price_edit)
        layout.addWidget(self.package_label)
        layout.addWidget(self.package_edit)
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save_product)

        self.setLayout(layout)

        if self.product_id:
            self.load_product()

    def load_product(self):
        cursor = self.connection.cursor()
        query = "SELECT ProductName, Price, Package FROM Products WHERE ID=%s"
        cursor.execute(query, (self.product_id,))
        name, price, package = cursor.fetchone()
        self.product_name_edit.setText(name)
        self.product_price_edit.setText(str(price))
        self.package_edit.setText(package)

    def save_product(self):
        name = self.product_name_edit.text()
        price = float(self.product_price_edit.text())
        package = self.package_edit.text()

        cursor = self.connection.cursor()
        if self.product_id:
            query = "UPDATE Products SET ProductName=%s, Price=%s, Package=%s WHERE ID=%s"
            cursor.execute(query, (name, price, package, self.product_id))
        else:
            query = "INSERT INTO Products (ProductName, Price, Package) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, price, package))

        self.connection.commit()
        self.accept()


class EditSupplierDialog(QDialog):
    def __init__(self, connection, supplier_id=None):
        super().__init__()
        self.connection = connection
        self.supplier_id = supplier_id

        self.setWindowTitle("Редактировать поставщика")
        self.setGeometry(300, 300, 300, 200)

        self.name_label = QLabel("Название:")
        self.name_edit = QLineEdit()
        self.contact_label = QLabel("Контактные данные:")
        self.contact_edit = QLineEdit()
        self.save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.contact_label)
        layout.addWidget(self.contact_edit)
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save_supplier)

        self.setLayout(layout)

        if self.supplier_id:
            self.load_supplier()

    def load_supplier(self):
        cursor = self.connection.cursor()
        query = "SELECT Name, Contact FROM Suppliers WHERE ID=%s"
        cursor.execute(query, (self.supplier_id,))
        name, contact = cursor.fetchone()
        self.name_edit.setText(name)
        self.contact_edit.setText(contact)

    def save_supplier(self):
        name = self.name_edit.text()
        contact = self.contact_edit.text()

        cursor = self.connection.cursor()
        if self.supplier_id:
            query = "UPDATE Suppliers SET Name=%s, Contact=%s WHERE ID=%s"
            cursor.execute(query, (name, contact, self.supplier_id))
        else:
            query = "INSERT INTO Suppliers (Name, Contact) VALUES (%s, %s)"
            cursor.execute(query, (name, contact))

        self.connection.commit()
        self.accept()


class EditEmployeeDialog(QDialog):
    def __init__(self, connection, employee_id=None):
        super().__init__()
        self.connection = connection
        self.employee_id = employee_id

        self.setWindowTitle("Редактировать сотрудника")
        self.setGeometry(300, 300, 300, 200)

        self.name_label = QLabel("Имя:")
        self.name_edit = QLineEdit()
        self.position_label = QLabel("Должность:")
        self.position_edit = QLineEdit()
        self.save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.position_label)
        layout.addWidget(self.position_edit)
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save_employee)

        self.setLayout(layout)

        if self.employee_id:
            self.load_employee()

    def load_employee(self):
        cursor = self.connection.cursor()
        query = "SELECT Name, Position FROM Employees WHERE ID=%s"
        cursor.execute(query, (self.employee_id,))
        name, position = cursor.fetchone()
        self.name_edit.setText(name)
        self.position_edit.setText(position)

    def save_employee(self):
        name = self.name_edit.text()
        position = self.position_edit.text()

        cursor = self.connection.cursor()
        if self.employee_id:
            query = "UPDATE Employees SET Name=%s, Position=%s WHERE ID=%s"
            cursor.execute(query, (name, position, self.employee_id))
        else:
            query = "INSERT INTO Employees (Name, Position) VALUES (%s, %s)"
            cursor.execute(query, (name, position))

        self.connection.commit()
        self.accept()


class AddEditCategoryDialog(QDialog):
    def __init__(self, connection, category_id=None):
        super().__init__()
        self.connection = connection
        self.category_id = category_id

        self.setWindowTitle("Добавить/Редактировать категорию")
        self.setGeometry(300, 300, 300, 200)

        self.category_name_label = QLabel("Название категории:")
        self.category_name_edit = QLineEdit()
        self.save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()
        layout.addWidget(self.category_name_label)
        layout.addWidget(self.category_name_edit)
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save_category)

        self.setLayout(layout)

        if self.category_id:
            self.load_category()

    def load_category(self):
        cursor = self.connection.cursor()
        query = "SELECT CategoryName FROM Categories WHERE ID=%s"
        cursor.execute(query, (self.category_id,))
        category_name = cursor.fetchone()[0]
        self.category_name_edit.setText(category_name)

    def save_category(self):
        category_name = self.category_name_edit.text()

        cursor = self.connection.cursor()
        if self.category_id:
            query = "UPDATE Categories SET CategoryName=%s WHERE ID=%s"
            cursor.execute(query, (category_name, self.category_id))
        else:
            query = "INSERT INTO Categories (CategoryName) VALUES (%s)"
            cursor.execute(query, (category_name,))

        self.connection.commit()
        self.accept()


class AccountantWindow(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setWindowTitle("Личный кабинет бухгалтера")
        self.setGeometry(300, 300, 600, 400)

        self.edit_category_button = QPushButton("Редактировать категории")
        self.edit_product_button = QPushButton("Редактировать товары")
        self.edit_supplier_button = QPushButton("Редактировать поставщиков")
        self.edit_employee_button = QPushButton("Редактировать сотрудников")

        layout = QVBoxLayout()
        layout.addWidget(self.edit_category_button)
        layout.addWidget(self.edit_product_button)
        layout.addWidget(self.edit_supplier_button)
        layout.addWidget(self.edit_employee_button)

        self.setLayout(layout)

        # Подключаем функции к кнопкам
        self.edit_category_button.clicked.connect(self.edit_categories)
        self.edit_product_button.clicked.connect(self.edit_products)
        self.edit_supplier_button.clicked.connect(self.edit_suppliers)
        self.edit_employee_button.clicked.connect(self.edit_employees)

    def edit_categories(self):
        dialog = AddEditCategoryDialog(self.connection)
        if dialog.exec_() == QDialog.Accepted:
            # После редактирования категории, обновляем список в QComboBox в главном окне
            self.fill_categories()

    def edit_products(self):
        dialog = EditProductDialog(self.connection)
        if dialog.exec_() == QDialog.Accepted:
            # После редактирования товара, обновляем список товаров в главном окне
            pass

    def edit_suppliers(self):
        dialog = EditSupplierDialog(self.connection)
        if dialog.exec_() == QDialog.Accepted:
            # После редактирования поставщика, обновляем список в главном окне (если он есть)
            pass

    def edit_employees(self):
        dialog = EditEmployeeDialog(self.connection)
        if dialog.exec_() == QDialog.Accepted:
            # После редактирования сотрудника, обновляем список в главном окне (если он есть)
            pass

    def fill_categories(self):
        # Здесь код для обновления списка категорий
        pass


class StoreApp(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setWindowTitle("Магазин 'Колобок'")
        self.setGeometry(100, 100, 600, 400)

        self.load_button = QPushButton("Load Products")
        self.load_button.clicked.connect(self.load_products)

        self.add_product_button = QPushButton("Добавить товар")
        self.add_product_button.clicked.connect(self.show_add_product_dialog)

        self.category_combo = QComboBox()
        self.category_combo.addItem("Все категории")
        self.category_combo.currentIndexChanged.connect(self.load_products)

        self.products_list = QListWidget()
        self.info_text_edit = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.category_combo)
        layout.addWidget(self.products_list)
        layout.addWidget(self.add_product_button)
        layout.addWidget(self.info_text_edit)

        self.setLayout(layout)

        self.fill_categories()

    def fill_categories(self):
        cursor = self.connection.cursor()
        query = "SELECT CategoryName FROM Categories ORDER BY CategoryName"
        cursor.execute(query)
        categories = cursor.fetchall()
        for category in categories:
            self.category_combo.addItem(category[0])

    def load_products(self):
        self.products_list.clear()
        cursor = self.connection.cursor()

        category_filter = self.category_combo.currentText()

        if category_filter == "Все категории":
            query = "
            SELECT Products.ProductName, Products.Price, Categories.CategoryName 
            FROM Products 
            INNER JOIN Supplies ON Products.ID = Supplies.ProductID 
            INNER JOIN Categories ON Supplies.CategoryID = Categories.ID 
            ORDER BY Products.ProductName
            "
            cursor.execute(query)
        else:
            query = "
            SELECT Products.ProductName, Products.Price, Categories.CategoryName 
            FROM Products 
            INNER JOIN Supplies ON Products.ID = Supplies.ProductID 
            INNER JOIN Categories ON Supplies.CategoryID = Categories.ID 
            WHERE Categories.CategoryName = %s
            ORDER BY Products.ProductName
            "
            cursor.execute(query, (category_filter,))

        products = cursor.fetchall()
        for product in products:
            item_text = f"{product[0]} - {product[1]} руб. ({product[2]})"
            self.products_list.addItem(item_text)

    def show_add_product_dialog(self):
        dialog = EditProductDialog(self.connection)
        if dialog.exec_() == QDialog.Accepted:
            self.load_products()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 database='Kolobok20')

    login_window = LoginWindow(connection)
    if login_window.exec_() == QDialog.Accepted:
        if login_window.user_type == "accountant":
            accountant_window = AccountantWindow(connection)
            accountant_window.show()
        else:
            main_window = StoreApp(connection)
            main_window.show()

    sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QDialog, QMessageBox, QComboBox, QListWidget,
                             QTextEdit)

import pymysql

class LoginWindow(QDialog):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 200)

        self.email_label = QLabel("Email:")
        self.email_edit = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.user_login_button = QPushButton("Вход для пользователя")
        self.accountant_login_button = QPushButton("Вход для бухгалтера")

        layout = QVBoxLayout()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.user_login_button)
        layout.addWidget(self.accountant_login_button)

        self.user_login_button.clicked.connect(self.user_login)
        self.accountant_login_button.clicked.connect(self.accountant_login)

        self.setLayout(layout)

    def user_login(self):
        email = self.email_edit.text()
        password = self.password_edit.text()

        cursor = self.connection.cursor()
        query = "SELECT * FROM Users WHERE Email=%s AND Password=%s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            self.accept()
            self.user_type = "user"
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный email или пароль")

    def accountant_login(self):
        password = self.password_edit.text()

        if password == "root":
            self.accept()
            self.user_type = "accountant"
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный пароль для бухгалтера")


class EditProductDialog(QDialog):
    def __init__(self, connection, product_id=None):
        super().__init__()
        self.connection = connection
        self.product_id = product_id

        self.setWindowTitle("Редактировать товар")
        self.setGeometry(300, 300, 300, 200)

        self.product_name_label = QLabel("Название товара:")
        self.product_name_edit = QLineEdit()
        self.product_price_label = QLabel("Цена:")
        self.product_price_edit = QLineEdit()
        self.package_label = QLabel("Упаковка:")
        self.package_edit = QLineEdit()
        self.save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()
        layout.addWidget(self.product_name_label)
        layout.addWidget(self.product_name_edit)
        layout.addWidget(self.product_price_label)
        layout.addWidget(self.product_price_edit)
        layout.addWidget(self.package_label)
        layout.addWidget(self.package_edit)
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save_product)

        self.setLayout(layout)

        if self.product_id:
            self.load_product()

    def load_product(self):
        cursor = self.connection.cursor()
        query = "SELECT ProductName, Price, Package FROM Products WHERE ID=%s"
        cursor.execute(query, (self.product_id,))
        name, price, package = cursor.fetchone()
        self.product_name_edit.setText(name)
        self.product_price_edit.setText(str(price))
        self.package_edit.setText(package)

    def save_product(self):
        name = self.product_name_edit.text()
        price = float(self.product_price_edit.text())
        package = self.package_edit.text()

        cursor = self.connection.cursor()
        if self.product_id:
            query = "UPDATE Products SET ProductName=%s, Price=%s, Package=%s WHERE ID=%s"
            cursor.execute(query, (name, price, package, self.product_id))
        else:
            query = "INSERT INTO Products (ProductName, Price, Package) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, price, package))

        self.connection.commit()
        self.accept()


class EditSupplierDialog(QDialog):
    def __init__(self, connection, supplier_id=None):
        super().__init__()
        self.connection = connection
        self.supplier_id = supplier_id

        self.setWindowTitle("Редактировать поставщика")
        self.setGeometry(300, 300, 300, 200)

        self.name_label = QLabel("Название:")
        self.name_edit = QLineEdit()
        self.contact_label = QLabel("Контактные данные:")
        self.contact_edit = QLineEdit()
        self.save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.contact_label)
        layout.addWidget(self.contact_edit)
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save_supplier)

        self.setLayout(layout)

        if self.supplier_id:
            self.load_supplier()

    def load_supplier(self):
        cursor = self.connection.cursor()
        query = "SELECT Name, Contact FROM Suppliers WHERE ID=%s"
        cursor.execute(query, (self.supplier_id,))
        name, contact = cursor.fetchone()
        self.name_edit.setText(name)
        self.contact_edit.setText(contact)

    def save_supplier(self):
        name = self.name_edit.text()
        contact = self.contact_edit.text()

        cursor = self.connection.cursor()
        if self.supplier_id:
            query = "UPDATE Suppliers SET Name=%s, Contact=%s WHERE ID=%s"
            cursor.execute(query, (name, contact, self.supplier_id))
        else:
            query = "INSERT INTO Suppliers (Name, Contact) VALUES (%s, %s)"
            cursor.execute(query, (name, contact))

        self.connection.commit()
        self.accept()


class EditEmployeeDialog(QDialog):
    def __init__(self, connection, employee_id=None):
        super().__init__()
        self.connection = connection
        self.employee_id = employee_id

        self.setWindowTitle("Редактировать сотрудника")
        self.setGeometry(300, 300, 300, 200)

        self.name_label = QLabel("Имя:")
        self.name_edit = QLineEdit()
        self.position_label = QLabel("Должность:")
        self.position_edit = QLineEdit()
        self.save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.position_label)
        layout.addWidget(self.position_edit)
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save_employee)

        self.setLayout(layout)

        if self.employee_id:
            self.load_employee()

    def load_employee(self):
        cursor = self.connection.cursor()
        query = "SELECT Name, Position FROM Employees WHERE ID=%s"
        cursor.execute(query, (self.employee_id,))
        name, position = cursor.fetchone()
        self.name_edit.setText(name)
        self.position_edit.setText(position)

    def save_employee(self):
        name = self.name_edit.text()
        position = self.position_edit.text()

        cursor = self.connection.cursor()
        if self.employee_id:
            query = "UPDATE Employees SET Name=%s, Position=%s WHERE ID=%s"
            cursor.execute(query, (name, position, self.employee_id))
        else:
            query = "INSERT INTO Employees (Name, Position) VALUES (%s, %s)"
            cursor.execute(query, (name, position))

        self.connection.commit()
        self.accept()


class AddEditCategoryDialog(QDialog):
    def __init__(self, connection, category_id=None):
        super().__init__()
        self.connection = connection
        self.category_id = category_id

        self.setWindowTitle("Добавить/Редактировать категорию")
        self.setGeometry(300, 300, 300, 200)

        self.category_name_label = QLabel("Название категории:")
        self.category_name_edit = QLineEdit()
        self.save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()
        layout.addWidget(self.category_name_label)
        layout.addWidget(self.category_name_edit)
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save_category)

        self.setLayout(layout)

        if self.category_id:
            self.load_category()

    def load_category(self):
        cursor = self.connection.cursor()
        query = "SELECT CategoryName FROM Categories WHERE ID=%s"
        cursor.execute(query, (self.category_id,))
        category_name = cursor.fetchone()[0]
        self.category_name_edit.setText(category_name)

    def save_category(self):
        category_name = self.category_name_edit.text()

        cursor = self.connection.cursor()
        if self.category_id:
            query = "UPDATE Categories SET CategoryName=%s WHERE ID=%s"
            cursor.execute(query, (category_name, self.category_id))
        else:
            query = "INSERT INTO Categories (CategoryName) VALUES (%s)"
            cursor.execute(query, (category_name,))

        self.connection.commit()
        self.accept()


class AccountantWindow(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setWindowTitle("Личный кабинет бухгалтера")
        self.setGeometry(300, 300, 600, 400)

        self.edit_category_button = QPushButton("Редактировать категории")
        self.edit_product_button = QPushButton("Редактировать товары")
        self.edit_supplier_button = QPushButton("Редактировать поставщиков")
        self.edit_employee_button = QPushButton("Редактировать сотрудников")

        layout = QVBoxLayout()
        layout.addWidget(self.edit_category_button)
        layout.addWidget(self.edit_product_button)
        layout.addWidget(self.edit_supplier_button)
        layout.addWidget(self.edit_employee_button)

        self.setLayout(layout)

        # Подключаем функции к кнопкам
        self.edit_category_button.clicked.connect(self.edit_categories)
        self.edit_product_button.clicked.connect(self.edit_products)
        self.edit_supplier_button.clicked.connect(self.edit_suppliers)
        self.edit_employee_button.clicked.connect(self.edit_employees)

    def edit_categories(self):
        dialog = AddEditCategoryDialog(self.connection)
        if dialog.exec_() == QDialog.Accepted:
            # После редактирования категории, обновляем список в QComboBox в главном окне
            self.fill_categories()

    def edit_products(self):
        dialog = EditProductDialog(self.connection)
        if dialog.exec_() == QDialog.Accepted:
            # После редактирования товара, обновляем список товаров в главном окне
            pass

    def edit_suppliers(self):
        dialog = EditSupplierDialog(self.connection)
        if dialog.exec_() == QDialog.Accepted:
            # После редактирования поставщика, обновляем список в главном окне (если он есть)
            pass

    def edit_employees(self):
        dialog = EditEmployeeDialog(self.connection)
        if dialog.exec_() == QDialog.Accepted:
            # После редактирования сотрудника, обновляем список в главном окне (если он есть)
            pass

    def fill_categories(self):
        # Здесь код для обновления списка категорий
        pass


class StoreApp(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setWindowTitle("Магазин 'Колобок'")
        self.setGeometry(100, 100, 600, 400)

        self.load_button = QPushButton("Load Products")
        self.load_button.clicked.connect(self.load_products)

        self.add_product_button = QPushButton("Добавить товар")
        self.add_product_button.clicked.connect(self.show_add_product_dialog)

        self.category_combo = QComboBox()
        self.category_combo.addItem("Все категории")
        self.category_combo.currentIndexChanged.connect(self.load_products)

        self.products_list = QListWidget()
        self.info_text_edit = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.category_combo)
        layout.addWidget(self.products_list)
        layout.addWidget(self.add_product_button)
        layout.addWidget(self.info_text_edit)

        self.setLayout(layout)

        self.fill_categories()

    def fill_categories(self):
        cursor = self.connection.cursor()
        query = "SELECT CategoryName FROM Categories ORDER BY CategoryName"
        cursor.execute(query)
        categories = cursor.fetchall()
        for category in categories:
            self.category_combo.addItem(category[0])

    def load_products(self):
        self.products_list.clear()
        cursor = self.connection.cursor()

        category_filter = self.category_combo.currentText()

        if category_filter == "Все категории":
            query = "
            SELECT Products.ProductName, Products.Price, Categories.CategoryName 
            FROM Products 
            INNER JOIN Supplies ON Products.ID = Supplies.ProductID 
            INNER JOIN Categories ON Supplies.CategoryID = Categories.ID 
            ORDER BY Products.ProductName
            "
            cursor.execute(query)
        else:
            query = "
            SELECT Products.ProductName, Products.Price, Categories.CategoryName 
            FROM Products 
            INNER JOIN Supplies ON Products.ID = Supplies.ProductID 
            INNER JOIN Categories ON Supplies.CategoryID = Categories.ID 
            WHERE Categories.CategoryName = %s
            ORDER BY Products.ProductName
            "
            cursor.execute(query, (category_filter,))

        products = cursor.fetchall()
        for product in products:
            item_text = f"{product[0]} - {product[1]} руб. ({product[2]})"
            self.products_list.addItem(item_text)

    def show_add_product_dialog(self):
        dialog = EditProductDialog(self.connection)
        if dialog.exec_() == QDialog.Accepted:
            self.load_products()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 database='Kolobok20')

    login_window = LoginWindow(connection)
    if login_window.exec_() == QDialog.Accepted:
        if login_window.user_type == "accountant":
            accountant_window = AccountantWindow(connection)
            accountant_window.show()
        else:
            main_window = StoreApp(connection)
            main_window.show()

    sys.exit(app.exec_())
 """
    return code

def var1BD():
    code = """-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 13 2024 г., 04:31
-- Версия сервера: 5.7.39
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `cinema1`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Movies`
--

CREATE TABLE `Movies` (
  `Movie_ID` int(11) NOT NULL,
  `Title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Release_Year` int(11) DEFAULT NULL,
  `Genre` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Movies`
--

INSERT INTO `Movies` (`Movie_ID`, `Title`, `Release_Year`, `Genre`) VALUES
(1, 'Белый снег', 2020, 'драма'),
(2, 'Бим', 2020, 'детектив'),
(3, 'Буран', 2021, 'драма'),
(4, 'Бухта глубокая', 2019, 'детектив');

-- --------------------------------------------------------

--
-- Структура таблицы `PromoCodes`
--

CREATE TABLE `PromoCodes` (
  `PromoCode_ID` int(11) NOT NULL,
  `User_ID` int(11) DEFAULT NULL,
  `Code` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `PromoCodes`
--

INSERT INTO `PromoCodes` (`PromoCode_ID`, `User_ID`, `Code`) VALUES
(1, 3, 'DORGFO'),
(2, 1, 'LMWUYP'),
(3, 2, 'HCUIGS'),
(4, 4, 'IVZSQM'),
(5, 5, 'SSHGTU'),
(6, 3, 'WEMGKF'),
(7, 1, 'FKRFGG'),
(8, 2, 'UQIFUU'),
(9, 4, 'RFTBHD'),
(10, 5, 'PNDKDK'),
(11, 3, 'OEIKLH'),
(12, 1, 'OEALWE'),
(13, 2, 'HIXQDP'),
(14, 4, 'QHOTHB'),
(15, 5, 'DETNNZ'),
(16, 3, 'ELKEBU'),
(17, 1, 'VPRUDW'),
(18, 2, 'BDTWOE'),
(19, 4, 'MXGEHW'),
(20, 5, 'ROPBHA'),
(21, 3, 'UNDYAA'),
(22, 1, 'ATGNQY'),
(23, 2, 'GGIIEB'),
(24, 4, 'SSMSHT'),
(25, 5, 'EZWZQG'),
(26, 3, 'MPBXZR'),
(27, 1, 'JQLSLQ'),
(28, 2, 'MSNZIZ'),
(29, 4, 'HOHQTX'),
(30, 5, 'ODJLGW');

-- --------------------------------------------------------

--
-- Структура таблицы `Sessions`
--

CREATE TABLE `Sessions` (
  `Session_ID` int(11) NOT NULL,
  `Movie_ID` int(11) DEFAULT NULL,
  `Start_DateTime` datetime DEFAULT NULL,
  `Hall` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Sessions`
--

INSERT INTO `Sessions` (`Session_ID`, `Movie_ID`, `Start_DateTime`, `Hall`) VALUES
(1, 1, '2022-03-09 10:00:00', 1),
(2, 1, '2022-03-09 10:00:00', 2),
(3, 2, '2022-03-10 16:00:00', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `Tickets`
--

CREATE TABLE `Tickets` (
  `Ticket_ID` int(11) NOT NULL,
  `Session_ID` int(11) DEFAULT NULL,
  `Seat` int(11) DEFAULT NULL,
  `User_ID` int(11) DEFAULT NULL,
  `Purchase_Date` date DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `Promo_Code` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Tickets`
--

INSERT INTO `Tickets` (`Ticket_ID`, `Session_ID`, `Seat`, `User_ID`, `Purchase_Date`, `Price`, `Promo_Code`) VALUES
(1, 1, 56, 1, '2022-03-07', '500.00', NULL),
(2, 1, 78, 2, '2022-03-07', '500.00', 1023),
(3, 2, 14, 3, '2022-03-09', '600.00', NULL),
(4, 2, 15, 3, '2022-03-09', '600.00', NULL),
(5, 3, 23, 4, '2022-03-10', '750.00', NULL),
(6, 3, 27, 5, '2022-03-05', '750.00', NULL),
(7, 3, 26, 6, '2022-03-06', '750.00', 1023);

-- --------------------------------------------------------

--
-- Структура таблицы `Users`
--

CREATE TABLE `Users` (
  `User_ID` int(11) NOT NULL,
  `Full_Name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Phone_Number` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Password` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Passport_Number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Type` enum('Client','Administrator') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `login` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Users`
--

INSERT INTO `Users` (`User_ID`, `Full_Name`, `Phone_Number`, `Password`, `Passport_Number`, `Type`, `login`) VALUES
(1, 'Иванов Иван Иванович', '8(915)222-33-44', 'password1', '42 11 567890', 'Client', ''),
(2, 'Иванов Сергей Иванович', '8(996)782-33-44', 'password3', '42 21 557894', 'Client', ''),
(3, 'Сидоров Петр Сергеевич', '8(917)998-33-23', 'password5', '40 33 678944', 'Client', ''),
(4, 'Ким Анна Витальевна', '8(915)222-65-64', 'password6', '42 10 345555', 'Client', ''),
(5, 'Ким Федор Петрович', '8(925)522-33-04', 'password7', '44 22 555666', 'Client', ''),
(6, 'root', 'root', 'root', '', 'Administrator', 'root'),
(10, 'dav', '34632463', 'da', '4142424', 'Client', ''),
(11, 'fsdfs', '2432525', 'qeqqe', '142124', 'Client', '2432525');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Movies`
--
ALTER TABLE `Movies`
  ADD PRIMARY KEY (`Movie_ID`);

--
-- Индексы таблицы `PromoCodes`
--
ALTER TABLE `PromoCodes`
  ADD PRIMARY KEY (`PromoCode_ID`),
  ADD KEY `User_ID` (`User_ID`);

--
-- Индексы таблицы `Sessions`
--
ALTER TABLE `Sessions`
  ADD PRIMARY KEY (`Session_ID`),
  ADD KEY `Movie_ID` (`Movie_ID`);

--
-- Индексы таблицы `Tickets`
--
ALTER TABLE `Tickets`
  ADD PRIMARY KEY (`Ticket_ID`),
  ADD KEY `Session_ID` (`Session_ID`),
  ADD KEY `User_ID` (`User_ID`);

--
-- Индексы таблицы `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`User_ID`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Movies`
--
ALTER TABLE `Movies`
  MODIFY `Movie_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `PromoCodes`
--
ALTER TABLE `PromoCodes`
  MODIFY `PromoCode_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT для таблицы `Sessions`
--
ALTER TABLE `Sessions`
  MODIFY `Session_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `Tickets`
--
ALTER TABLE `Tickets`
  MODIFY `Ticket_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `Users`
--
ALTER TABLE `Users`
  MODIFY `User_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `PromoCodes`
--
ALTER TABLE `PromoCodes`
  ADD CONSTRAINT `promocodes_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `Users` (`User_ID`);

--
-- Ограничения внешнего ключа таблицы `Sessions`
--
ALTER TABLE `Sessions`
  ADD CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`Movie_ID`) REFERENCES `Movies` (`Movie_ID`);

--
-- Ограничения внешнего ключа таблицы `Tickets`
--
ALTER TABLE `Tickets`
  ADD CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`Session_ID`) REFERENCES `Sessions` (`Session_ID`),
  ADD CONSTRAINT `tickets_ibfk_2` FOREIGN KEY (`User_ID`) REFERENCES `Users` (`User_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
 """
    return code

def var1code():
    code = """
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, \
    QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox
from PyQt5.QtCore import Qt
import pymysql
import random
import string

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Кинотеатр")
        self.setGeometry(100, 100, 800, 600)

        self.login_window = LoginWindow()
        self.setCentralWidget(self.login_window)

        self.login_window.login_button.clicked.connect(self.authenticate)
        self.login_window.register_button.clicked.connect(self.register)

    def authenticate(self):
        phone_number = self.login_window.phone_number_input.text()
        password = self.login_window.password_input.text()

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     database='cinema1',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Users WHERE Phone_Number = %s AND Password = %s"
                cursor.execute(sql, (phone_number, password))
                user = cursor.fetchone()

                if user:
                    if user['Type'] == 'Client':
                        self.user_id = user['User_ID']
                        self.show_movie_schedule()
                    elif user['Type'] == 'Administrator' and phone_number == 'root' and password == 'root':
                        self.show_admin_panel()
                    else:
                        QMessageBox.warning(self, "Ошибка", "Недостаточно прав для входа в админ-панель", QMessageBox.Ok)
                else:
                    QMessageBox.warning(self, "Ошибка", "Неправильный номер телефона или пароль", QMessageBox.Ok)

        finally:
            connection.close()

    def register(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.register_button.clicked.connect(self.register_user)
        self.registration_window.exec_()

    def register_user(self):
        try:
            full_name = self.registration_window.full_name_input.text()
            phone_number = self.registration_window.phone_number_input.text()
            password = self.registration_window.password_input.text()
            passport_number = self.registration_window.passport_number_input.text()

            # Debug print
            print(f"Attempting to register: {full_name}, {phone_number}, {passport_number}")

            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='',
                                         database='cinema1',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)

            with connection.cursor() as cursor:
                sql = "INSERT INTO Users (Full_Name, Phone_Number, Password, Passport_Number, Type, login) VALUES (%s, %s, %s, %s, 'Client', %s)"
                cursor.execute(sql, (full_name, phone_number, password, passport_number, phone_number))
                connection.commit()

            QMessageBox.information(self, "Успех", "Вы успешно зарегистрировались", QMessageBox.Ok)

        except Exception as e:
            print(f"Error during registration: {e}")
            QMessageBox.warning(self, "Ошибка", "Произошла ошибка при регистрации", QMessageBox.Ok)

        finally:
            connection.close()

    def show_movie_schedule(self):
        self.movie_schedule_window = MovieScheduleWindow(self.user_id)
        self.setCentralWidget(self.movie_schedule_window)

    def show_admin_panel(self):
        self.admin_panel_window = AdminPanelWindow()
        self.admin_panel_window.exec_()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.phone_number_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Войти")
        self.register_button = QPushButton("Регистрация")

        layout.addWidget(QLabel("Номер телефона:"))
        layout.addWidget(self.phone_number_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

class RegistrationWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Регистрация")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.full_name_input = QLineEdit()
        self.phone_number_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.passport_number_input = QLineEdit()

        self.register_button = QPushButton("Зарегистрироваться")

        layout.addWidget(QLabel("Полное имя:"))
        layout.addWidget(self.full_name_input)
        layout.addWidget(QLabel("Номер телефона:"))
        layout.addWidget(self.phone_number_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Номер паспорта:"))
        layout.addWidget(self.passport_number_input)
        layout.addWidget(self.register_button)

class MovieScheduleWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.movie_schedule_table = QTableWidget()
        self.movie_schedule_table.setColumnCount(4)
        self.movie_schedule_table.setHorizontalHeaderLabels(["Фильм", "Дата", "Время", "Выбрать"])
        self.movie_schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.load_movie_schedule()

        self.confirm_button = QPushButton("Подтвердить выбор")
        self.confirm_button.clicked.connect(self.confirm_selection)

        layout.addWidget(self.movie_schedule_table)
        layout.addWidget(self.confirm_button)

    def load_movie_schedule(self):
        # Очистим таблицу перед загрузкой расписания
        self.movie_schedule_table.setRowCount(0)

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     database='cinema1',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = "SELECT Movies.Title, DATE(Sessions.Start_DateTime) AS Date, TIME(Sessions.Start_DateTime) AS Time, Sessions.Session_ID FROM Movies INNER JOIN Sessions ON Movies.Movie_ID = Sessions.Movie_ID"
                cursor.execute(sql)
                movie_schedule = cursor.fetchall()

                for schedule in movie_schedule:
                    row_position = self.movie_schedule_table.rowCount()
                    self.movie_schedule_table.insertRow(row_position)
                    self.movie_schedule_table.setItem(row_position, 0, QTableWidgetItem(schedule['Title']))
                    self.movie_schedule_table.setItem(row_position, 1, QTableWidgetItem(str(schedule['Date'])))
                    self.movie_schedule_table.setItem(row_position, 2, QTableWidgetItem(str(schedule['Time'])))
                    checkbox = QCheckBox()
                    self.movie_schedule_table.setCellWidget(row_position, 3, checkbox)

        finally:
            connection.close()

    def confirm_selection(self):
        selected_sessions = []

        for row in range(self.movie_schedule_table.rowCount()):
            checkbox = self.movie_schedule_table.cellWidget(row, 3)
            if checkbox.isChecked():
                selected_sessions.append(self.movie_schedule_table.item(row, 3).text())

        if selected_sessions:
            session_id = int(selected_sessions[0])  # Пока учитываем только один выбранный сеанс
            self.select_tickets_window = TicketSelectionWindow(session_id, self.user_id)
            self.select_tickets_window.show()

class TicketSelectionWindow(QWidget):
    def __init__(self, session_id, user_id):
        super().__init__()

        self.session_id = session_id
        self.user_id = user_id

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tickets_label = QLabel("Выберите количество билетов:")
        self.tickets_input = QLineEdit()

        self.buy_button = QPushButton("Купить билеты")
        self.buy_button.clicked.connect(self.buy_tickets)

        layout.addWidget(self.tickets_label)
        layout.addWidget(self.tickets_input)
        layout.addWidget(self.buy_button)

    def buy_tickets(self):
        num_tickets = int(self.tickets_input.text())

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     database='cinema1',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Создаем билеты для пользователя
                for _ in range(num_tickets):
                    sql = "INSERT INTO Tickets (Session_ID, User_ID) VALUES (%s, %s)"
                    cursor.execute(sql, (self.session_id, self.user_id))
                    connection.commit()

                QMessageBox.information(self, "Успех", "Билеты успешно куплены", QMessageBox.Ok)

        finally:
            connection.close()

class AdminPanelWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Админ-панель")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.show_sales_button = QPushButton("Показать продажи")
        self.show_sales_button.clicked.connect(self.show_sales)

        self.generate_promo_button = QPushButton("Выдать промокоды")
        self.generate_promo_button.clicked.connect(self.generate_promo_codes)
        self.promo_codes_label = QLabel()

        layout.addWidget(self.show_sales_button)
        layout.addWidget(self.generate_promo_button)
        layout.addWidget(self.promo_codes_label)

    def show_sales(self):
        self.sales_window = SalesWindow()
        self.sales_window.exec_()

    def generate_promo_codes(self):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     database='cinema1',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Находим наиболее активных клиентов
                sql = "
                SELECT Users.User_ID, Users.Full_Name, COUNT(Tickets.Ticket_ID) AS Tickets_Count
                FROM Users
                JOIN Tickets ON Users.User_ID = Tickets.User_ID
                GROUP BY Users.User_ID
                ORDER BY Tickets_Count DESC
                LIMIT 5
                "
                cursor.execute(sql)
                top_clients = cursor.fetchall()

                # Генерируем и выдаем промокоды
                promo_codes = {}
                for client in top_clients:
                    promo_code = self.generate_promo_code()
                    promo_codes[client['User_ID']] = promo_code

                    # Сохраняем промокоды в базе данных
                    sql = "INSERT INTO PromoCodes (User_ID, Code) VALUES (%s, %s)"
                    cursor.execute(sql, (client['User_ID'], promo_code))
                    connection.commit()

                promo_codes_text = "\n".join([f"{client['Full_Name']}: {promo_codes[client['User_ID']]}" for client in top_clients])
                self.promo_codes_label.setText(f"Промокоды для топ-5 клиентов:\n{promo_codes_text}")

        finally:
            connection.close()

    def generate_promo_code(self):
        letters = string.ascii_uppercase
        return ''.join(random.choice(letters) for i in range(6))

class SalesWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Продажи")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.show_daily_sales_button = QPushButton("Показать за день")
        self.show_daily_sales_button.clicked.connect(self.show_daily_sales)

        self.show_monthly_sales_button = QPushButton("Показать за месяц")
        self.show_monthly_sales_button.clicked.connect(self.show_monthly_sales)

        self.sales_label = QLabel()

        layout.addWidget(self.show_daily_sales_button)
        layout.addWidget(self.show_monthly_sales_button)
        layout.addWidget(self.sales_label)

    def show_daily_sales(self):
        self.load_sales("day")

    def show_monthly_sales(self):
        self.load_sales("month")

    def load_sales(self, period):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     database='cinema1',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                if period == "day":
                    sql = "
                    SELECT Sessions.Session_ID, COUNT(Tickets.Ticket_ID) AS Tickets_Sold, SUM(Tickets.Price) AS Total_Sales
                    FROM Sessions
                    JOIN Tickets ON Sessions.Session_ID = Tickets.Session_ID
                    WHERE DATE(Sessions.Start_DateTime) = CURDATE()
                    GROUP BY Sessions.Session_ID
                    "
                elif period == "month":
                    sql = "
                    SELECT Sessions.Session_ID, COUNT(Tickets.Ticket_ID) AS Tickets_Sold, SUM(Tickets.Price) AS Total_Sales
                    FROM Sessions
                    JOIN Tickets ON Sessions.Session_ID = Tickets.Session_ID
                    WHERE MONTH(Sessions.Start_DateTime) = MONTH(CURDATE()) AND YEAR(Sessions.Start_DateTime) = YEAR(CURDATE())
                    GROUP BY Sessions.Session_ID
                    "

                cursor.execute(sql)
                sales_data = cursor.fetchall()

                sales_text = ""
                for sale in sales_data:
                    sales_text += f"Сеанс ID: {sale['Session_ID']}, Продано билетов: {sale['Tickets_Sold']}, Общая сумма: {sale['Total_Sales']} руб.\n"

                self.sales_label.setText(sales_text)

        except Exception as e:
            print(f"An error occurred: {e}")
            QMessageBox.warning(self, "Ошибка", "Произошла ошибка при загрузке данных", QMessageBox.Ok)

        finally:
            connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
 """
    return code

def var7BD():
    code = """-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 13 2024 г., 05:06
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `daycare_db`
--

-- --------------------------------------------------------

--
-- Структура таблицы `absences`
--

CREATE TABLE `absences` (
  `id` int NOT NULL,
  `parent_id` int DEFAULT NULL,
  `reason` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `child_groups`
--

CREATE TABLE `child_groups` (
  `id` int NOT NULL,
  `group_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `enrollments`
--

CREATE TABLE `enrollments` (
  `id` int NOT NULL,
  `parent_id` int DEFAULT NULL,
  `group_id` int DEFAULT NULL,
  `enrollment_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `parents`
--

CREATE TABLE `parents` (
  `id` int NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `privilege_category` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `parents`
--

INSERT INTO `parents` (`id`, `email`, `first_name`, `last_name`, `phone_number`, `privilege_category`) VALUES
(1, 'ivan@example.com', 'Иван', 'Иванов', '+123456789', 'Льготная категория 1'),
(2, 'petr@example.com', 'Петр', 'Петров', '+987654321', 'Льготная категория 2'),
(3, 'maria@example.com', 'Мария', 'Сидорова', '+1122334455', 'Льготная категория 3');

-- --------------------------------------------------------

--
-- Структура таблицы `payments`
--

CREATE TABLE `payments` (
  `id` int NOT NULL,
  `parent_id` int DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `privilege_categories`
--

CREATE TABLE `privilege_categories` (
  `id` int NOT NULL,
  `category_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `teachers`
--

CREATE TABLE `teachers` (
  `id` int NOT NULL,
  `teacher_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `group_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `absences`
--
ALTER TABLE `absences`
  ADD PRIMARY KEY (`id`),
  ADD KEY `parent_id` (`parent_id`);

--
-- Индексы таблицы `child_groups`
--
ALTER TABLE `child_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `group_name` (`group_name`);

--
-- Индексы таблицы `enrollments`
--
ALTER TABLE `enrollments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `parent_id` (`parent_id`),
  ADD KEY `group_id` (`group_id`);

--
-- Индексы таблицы `parents`
--
ALTER TABLE `parents`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Индексы таблицы `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `parent_id` (`parent_id`);

--
-- Индексы таблицы `privilege_categories`
--
ALTER TABLE `privilege_categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `category_name` (`category_name`);

--
-- Индексы таблицы `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `group_id` (`group_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `absences`
--
ALTER TABLE `absences`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `child_groups`
--
ALTER TABLE `child_groups`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `enrollments`
--
ALTER TABLE `enrollments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `parents`
--
ALTER TABLE `parents`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `privilege_categories`
--
ALTER TABLE `privilege_categories`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `teachers`
--
ALTER TABLE `teachers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `absences`
--
ALTER TABLE `absences`
  ADD CONSTRAINT `absences_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `parents` (`id`);

--
-- Ограничения внешнего ключа таблицы `enrollments`
--
ALTER TABLE `enrollments`
  ADD CONSTRAINT `enrollments_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `parents` (`id`),
  ADD CONSTRAINT `enrollments_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `child_groups` (`id`);

--
-- Ограничения внешнего ключа таблицы `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `parents` (`id`);

--
-- Ограничения внешнего ключа таблицы `teachers`
--
ALTER TABLE `teachers`
  ADD CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `child_groups` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
 """
    return code

def var7code():
    code = """import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTextEdit, QVBoxLayout, QTabWidget, \
    QComboBox, QMessageBox
import mysql.connector


class ParentWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Интерфейс пользователя - Родитель")
        self.setGeometry(100, 100, 600, 400)

        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(10, 10, 580, 380)

        self.profile_tab = QWidget()
        self.absence_tab = QWidget()
        self.payment_tab = QWidget()

        self.tabs.addTab(self.profile_tab, "Профиль")
        self.tabs.addTab(self.absence_tab, "Пропуска")
        self.tabs.addTab(self.payment_tab, "Оплата")

        self.init_profile_tab()
        self.init_absence_tab()
        self.init_payment_tab()

        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='daycare_db'
        )

        self.load_parent_data()  # Загрузка данных при инициализации окна

    def init_profile_tab(self):
        layout = QVBoxLayout()

        self.profile_info = QTextEdit()
        layout.addWidget(self.profile_info)

        self.edit_profile_btn = QPushButton("Редактировать профиль")
        self.edit_profile_btn.clicked.connect(self.edit_profile)
        layout.addWidget(self.edit_profile_btn)

        self.profile_tab.setLayout(layout)

    def init_absence_tab(self):
        layout = QVBoxLayout()

        self.absence_reason = QComboBox()
        self.absence_reason.addItems(["Семейные обстоятельства", "По болезни", "Другое"])
        layout.addWidget(self.absence_reason)

        self.add_absence_btn = QPushButton("Добавить пропуск")
        self.add_absence_btn.clicked.connect(self.add_absence)
        layout.addWidget(self.add_absence_btn)

        self.absence_tab.setLayout(layout)

    def init_payment_tab(self):
        layout = QVBoxLayout()

        self.payment_info = QTextEdit()
        layout.addWidget(self.payment_info)

        self.payment_tab.setLayout(layout)

    def load_parent_data(self):
        # Загрузка данных о родителе из базы данных
        query = "SELECT * FROM parents WHERE id = %s"
        parent_id = 1  # Предположим, что мы хотим загрузить данные о родителе с идентификатором 1
        with self.db.cursor() as cursor:
            cursor.execute(query, (parent_id,))
            parent_data = cursor.fetchone()

        if parent_data:
            # Отображение данных о родителе в соответствующем виджете
            self.profile_info.setText(f"Имя: {parent_data[1]}\n"
                                      f"Фамилия: {parent_data[2]}\n"
                                      f"Email: {parent_data[3]}\n"
                                      f"Телефон: {parent_data[4]}\n"
                                      f"Льготная категория: {parent_data[5]}")

    def edit_profile(self):
        # Получаем новые данные из интерфейса
        profile_text = self.profile_info.toPlainText()
        lines = profile_text.split('\n')
        new_data = {}
        for line in lines:
            key, value = line.split(': ')
            new_data[key] = value

        # Обновляем профиль в базе данных
        query = "UPDATE parents SET first_name = %s, last_name = %s, email = %s, phone_number = %s, privilege_category = %s WHERE id = %s"
        with self.db.cursor() as cursor:
            cursor.execute(query, (new_data['Имя'], new_data['Фамилия'], new_data['Email'], new_data['Телефон'],
                                   new_data['Льготная категория'],
                                   1))  # Предположим, что мы редактируем данные для родителя с id=1
        self.db.commit()
        QMessageBox.information(self, "Редактирование профиля", "Профиль успешно отредактирован")

    def add_absence(self):
        # Получаем данные из интерфейса
        reason = self.absence_reason.currentText()

        # Добавляем пропуск в базу данных
        query = "INSERT INTO absences (reason) VALUES (%s)"
        with self.db.cursor() as cursor:
            cursor.execute(query, (reason,))
        self.db.commit()
        QMessageBox.information(self, "Добавление пропуска", "Пропуск успешно добавлен")


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Интерфейс администратора")
        self.setGeometry(100, 100, 600, 400)

        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(10, 10, 580, 380)

        self.groups_tab = QWidget()
        self.teachers_tab = QWidget()
        self.enrollments_tab = QWidget()
        self.reports_tab = QWidget()

        self.tabs.addTab(self.groups_tab, "Группы")
        self.tabs.addTab(self.teachers_tab, "Воспитатели")
        self.tabs.addTab(self.enrollments_tab, "Зачисления")
        self.tabs.addTab(self.reports_tab, "Отчеты")

        self.init_groups_tab()
        self.init_teachers_tab()
        self.init_enrollments_tab()
        self.init_reports_tab()

        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='daycare_db'
        )

    def init_groups_tab(self):
        layout = QVBoxLayout()

        self.groups_list = QComboBox()
        layout.addWidget(self.groups_list)

        self.group_info = QTextEdit()
        layout.addWidget(self.group_info)

        self.add_group_btn = QPushButton("Добавить группу")
        self.add_group_btn.clicked.connect(self.add_group)
        layout.addWidget(self.add_group_btn)

        self.edit_group_btn = QPushButton("Редактировать группу")
        self.edit_group_btn.clicked.connect(self.edit_group)
        layout.addWidget(self.edit_group_btn)

        self.groups_tab.setLayout(layout)

    def init_teachers_tab(self):
        layout = QVBoxLayout()

        self.teachers_list = QComboBox()
        layout.addWidget(self.teachers_list)

        self.teacher_info = QTextEdit()
        layout.addWidget(self.teacher_info)

        self.add_teacher_btn = QPushButton("Добавить воспитателя")
        self.add_teacher_btn.clicked.connect(self.add_teacher)
        layout.addWidget(self.add_teacher_btn)

        self.edit_teacher_btn = QPushButton("Редактировать воспитателя")
        self.edit_teacher_btn.clicked.connect(self.edit_teacher)
        layout.addWidget(self.edit_teacher_btn)

        self.teachers_tab.setLayout(layout)

    def init_enrollments_tab(self):
        layout = QVBoxLayout()

        self.enrollments_list = QComboBox()
        layout.addWidget(self.enrollments_list)

        self.enrollment_info = QTextEdit()
        layout.addWidget(self.enrollment_info)

        self.enrollments_tab.setLayout(layout)

    def init_reports_tab(self):
        layout = QVBoxLayout()

        self.summary_info = QTextEdit()
        layout.addWidget(self.summary_info)

        self.generate_report_btn = QPushButton("Сформировать отчет")
        self.generate_report_btn.clicked.connect(self.generate_report)
        layout.addWidget(self.generate_report_btn)

        self.reports_tab.setLayout(layout)

    def add_group(self):
        # Получаем данные из интерфейса
        group_name = self.group_info.toPlainText()

        # Добавляем группу в базу данных
        query = "INSERT INTO groups (group_name) VALUES (%s)"
        with self.db.cursor() as cursor:
            cursor.execute(query, (group_name,))
        self.db.commit()
        QMessageBox.information(self, "Добавление группы", "Группа успешно добавлена")

    def edit_group(self):
        # Получаем данные из интерфейса
        group_name = self.group_info.toPlainText()

        # Обновляем данные группы в базе данных
        # Здесь предполагается, что мы хотим редактировать группу с определенным идентификатором
        group_id = 1  # Предположим, что мы хотим редактировать группу с идентификатором 1
        query = "UPDATE groups SET group_name = %s WHERE id = %s"
        with self.db.cursor() as cursor:
            cursor.execute(query, (group_name, group_id))
        self.db.commit()
        QMessageBox.information(self, "Редактирование группы", "Группа успешно отредактирована")

    def add_teacher(self):
        # Получаем данные из интерфейса
        teacher_name = self.teacher_info.toPlainText()

        # Добавляем воспитателя в базу данных
        query = "INSERT INTO teachers (teacher_name) VALUES (%s)"
        with self.db.cursor() as cursor:
            cursor.execute(query, (teacher_name,))
        self.db.commit()
        QMessageBox.information(self, "Добавление воспитателя", "Воспитатель успешно добавлен")

    def edit_teacher(self):
        # Получаем данные из интерфейса
        teacher_name = self.teacher_info.toPlainText()

        # Обновляем данные воспитателя в базе данных
        # Здесь предполагается, что мы хотим редактировать воспитателя с определенным идентификатором
        teacher_id = 1  # Предположим, что мы хотим редактировать воспитателя с идентификатором 1
        query = "UPDATE teachers SET teacher_name = %s WHERE id = %s"
        with self.db.cursor() as cursor:
            cursor.execute(query, (teacher_name, teacher_id))
        self.db.commit()
        QMessageBox.information(self, "Редактирование воспитателя", "Воспитатель успешно отредактирован")

    def generate_report(self):
        # Добавьте код для формирования отчета
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    parent_window = ParentWindow()
    parent_window.show()

    admin_window = AdminWindow()
    admin_window.show()

    sys.exit(app.exec_())
 """
    return code

def var9BD():
    code = """-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 13 2024 г., 05:13
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `biblioteka`
--

-- --------------------------------------------------------

--
-- Структура таблицы `4itatel`
--

CREATE TABLE `4itatel` (
  `id` int NOT NULL,
  `name` varchar(30) NOT NULL,
  `telefon` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL,
  `nomer_pasporta` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `4itatel`
--

INSERT INTO `4itatel` (`id`, `name`, `telefon`, `email`, `nomer_pasporta`) VALUES
(1, 'Иванов Иван Иванович', '8(915)222-33-44', 'ivanov@mail.ru', '12345678');

-- --------------------------------------------------------

--
-- Структура таблицы `book`
--

CREATE TABLE `book` (
  `id` int NOT NULL,
  `name` varchar(30) NOT NULL,
  `vid_izdania` varchar(30) NOT NULL,
  `category` varchar(30) NOT NULL,
  `id_inf_books` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `book`
--

INSERT INTO `book` (`id`, `name`, `vid_izdania`, `category`, `id_inf_books`) VALUES
(1, 'Базы данных', 'Учеб. пособие', 'Бакалавриат', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `inf_books`
--

CREATE TABLE `inf_books` (
  `id` int NOT NULL,
  `data_postuplenia` date NOT NULL,
  `aftor` varchar(30) NOT NULL,
  `izdatelstvo` varchar(30) NOT NULL,
  `kol_straniz` varchar(20) NOT NULL,
  `data_izdania` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `inf_books`
--

INSERT INTO `inf_books` (`id`, `data_postuplenia`, `aftor`, `izdatelstvo`, `kol_straniz`, `data_izdania`) VALUES
(1, '2020-04-08', 'Агальцов В. П. ', 'ИД «ФОРУМ»', '271', '2018-04-11');

-- --------------------------------------------------------

--
-- Структура таблицы `tranzakci`
--

CREATE TABLE `tranzakci` (
  `id` int NOT NULL,
  `id_4itatel` int NOT NULL,
  `id_books` int NOT NULL,
  `data_vuda4i` date NOT NULL,
  `data_vozrata` date NOT NULL,
  `vremi_vahlo` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `tranzakci`
--

INSERT INTO `tranzakci` (`id`, `id_4itatel`, `id_books`, `data_vuda4i`, `data_vozrata`, `vremi_vahlo`) VALUES
(1, 1, 1, '2023-04-04', '2024-04-04', '2024-02-02');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `user_name` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `roli` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `user_name`, `password`, `roli`) VALUES
(1, 'user', '123456789', '4itatel'),
(2, 'root', 'root', 'Admin');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `4itatel`
--
ALTER TABLE `4itatel`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `book`
--
ALTER TABLE `book`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_inf_books` (`id_inf_books`);

--
-- Индексы таблицы `inf_books`
--
ALTER TABLE `inf_books`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `tranzakci`
--
ALTER TABLE `tranzakci`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_4itatel` (`id_4itatel`),
  ADD KEY `id_books` (`id_books`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `4itatel`
--
ALTER TABLE `4itatel`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `book`
--
ALTER TABLE `book`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `inf_books`
--
ALTER TABLE `inf_books`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `tranzakci`
--
ALTER TABLE `tranzakci`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `book`
--
ALTER TABLE `book`
  ADD CONSTRAINT `book_ibfk_1` FOREIGN KEY (`id_inf_books`) REFERENCES `inf_books` (`id`);

--
-- Ограничения внешнего ключа таблицы `tranzakci`
--
ALTER TABLE `tranzakci`
  ADD CONSTRAINT `tranzakci_ibfk_1` FOREIGN KEY (`id_books`) REFERENCES `book` (`id`),
  ADD CONSTRAINT `tranzakci_ibfk_2` FOREIGN KEY (`id_4itatel`) REFERENCES `4itatel` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
 """
    return code

def var9code():
    code = """import mysql.connector
from tkinter import *
from datetime import datetime  # Импорт datetime добавлен здесь

# Подключение к базе данных
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='biblioteka'
)

# Создаем объект курсора для выполнения SQL-запросов
cursor = db_connection.cursor()

# Функция для отображения окна с Афишей библиотеки
def show_library_schedule():
    # Создаем окно для отображения информации из базы данных
    library_window = Tk()
    library_window.title("Афиша библиотеки")

    # Запрос к базе данных для получения информации из таблицы inf_books
    select_query = "SELECT data_postuplenia, aftor, izdatelstvo, kol_straniz, data_izdania FROM inf_books"
    cursor.execute(select_query)
    inf_books_data = cursor.fetchall()

    # Отображаем информацию из таблицы inf_books
    for data_postuplenia, aftor, izdatelstvo, kol_straniz, data_izdania in inf_books_data:
        Label(library_window, text=f"Дата поступления: {data_postuplenia}").pack()
        Label(library_window, text=f"Автор: {aftor}").pack()
        Label(library_window, text=f"Издательство: {izdatelstvo}").pack()
        Label(library_window, text=f"Количество страниц: {kol_straniz}").pack()
        Label(library_window, text=f"Дата издания: {data_izdania}").pack()
        Label(library_window, text="").pack()

    # Функция для отображения окна авторизации пользователя
    def show_user_authentication_window():
        library_window.withdraw()  # Скрыть окно с Афишей библиотеки

        def login():
            username = username_entry.get()
            password = password_entry.get()

            # Проверка аутентификации пользователя
            query = "SELECT user_name, password FROM users WHERE id = 1"  # Проверка по пользователю с ID 1
            cursor.execute(query)
            result = cursor.fetchone()

            if result and result[0] == username and result[1] == password:
                print("Аутентификация успешна. Доступ разрешен.")
                show_personal_cabinet()
            else:
                print("Ошибка аутентификации. Неверное имя пользователя или пароль.")

        auth_window = Tk()
        auth_window.title("Авторизация пользователя")

        Label(auth_window, text="Логин:").pack()
        username_entry = Entry(auth_window)
        username_entry.pack()

        Label(auth_window, text="Пароль:").pack()
        password_entry = Entry(auth_window, show="*")
        password_entry.pack()

        Button(auth_window, text="Далее", command=login).pack()

        auth_window.mainloop()

    # Функция для отображения окна личного кабинета пользователя
    def show_personal_cabinet():
        personal_cabinet_window = Tk()
        personal_cabinet_window.title("Личный кабинет пользователя")

        # Запрос к базе данных для получения информации из таблицы book
        select_books_query = "SELECT name, vid_izdania, category, id_inf_books FROM book"
        cursor.execute(select_books_query)
        book_data = cursor.fetchall()

        # Отображаем информацию из таблицы book
        for name, vid_izdania, category, id_inf_books in book_data:
            Label(personal_cabinet_window, text=f"Название: {name}").pack()
            Label(personal_cabinet_window, text=f"Вид издания: {vid_izdania}").pack()
            Label(personal_cabinet_window, text=f"Категория: {category}").pack()
            Label(personal_cabinet_window, text=f"ID информационной книги: {id_inf_books}").pack()
            Label(personal_cabinet_window, text="").pack()

        # Запрос к базе данных для получения информации из таблицы tranzakci
        select_tranzakci_query = "SELECT data_vuda4i, data_vozrata FROM tranzakci"
        cursor.execute(select_tranzakci_query)
        tranzakci_data = cursor.fetchall()

        # Отображаем информацию из таблицы tranzakci
        for data_vuda4i, data_vozrata in tranzakci_data:
            Label(personal_cabinet_window, text=f"Дата выдачи: {data_vuda4i}").pack()
            Label(personal_cabinet_window, text=f"Дата возврата: {data_vozrata}").pack()
            Label(personal_cabinet_window, text="").pack()

        personal_cabinet_window.mainloop()

    # Функция для отображения окна авторизации админа
    def show_admin_authentication_window():
        library_window.withdraw()  # Скрыть окно с Афишей библиотеки

        def admin_login():
            username = username_entry.get()
            password = password_entry.get()

            # Проверка аутентификации админа
            query = "SELECT user_name, password FROM users WHERE id = 2"  # Проверка по админу с ID 2
            cursor.execute(query)
            result = cursor.fetchone()

            if result and result[0] == username and result[1] == password:
                print("Аутентификация админа успешна. Доступ разрешен.")
                show_book_management()
            else:
                print("Ошибка аутентификации. Неверное имя пользователя или пароль.")

        admin_auth_window = Tk()
        admin_auth_window.title("Авторизация админа")

        Label(admin_auth_window, text="Логин:").pack()
        username_entry = Entry(admin_auth_window)
        username_entry.pack()

        Label(admin_auth_window, text="Пароль:").pack()
        password_entry = Entry(admin_auth_window, show="*")
        password_entry.pack()

        Button(admin_auth_window, text="Далее", command=admin_login).pack()

        admin_auth_window.mainloop()

    # Функция для отображения окна управления книгами для админа
    def show_book_management():
        book_management_window = Tk()
        book_management_window.title("Управление книгами (Администратор)")

        # Отображение информации из таблицы inf_books
        for data_postuplenia, aftor, izdatelstvo, kol_straniz, data_izdania in inf_books_data:
            Label(book_management_window, text=f"Дата поступления: {data_postuplenia}").pack()
            Label(book_management_window, text=f"Автор: {aftor}").pack()
            Label(book_management_window, text=f"Издательство: {izdatelstvo}").pack()
            Label(book_management_window, text=f"Количество страниц: {kol_straniz}").pack()
            Label(book_management_window, text=f"Дата издания: {data_izdania}").pack()
            Label(book_management_window, text="").pack()

        # Функция для сохранения изменений в информации о книге
        def save_book_changes(book_id=1):
            try:
                new_data_postuplenia = datetime.strptime(new_data_postuplenia_entry.get(), '%Y-%m-%d').date()
                new_aftor = new_aftor_entry.get()
                new_izdatelstvo = new_izdatelstvo_entry.get()
                new_kol_straniz = new_kol_straniz_entry.get()
                new_data_izdania = datetime.strptime(new_data_izdania_entry.get(), '%Y-%m-%d').date()

                update_query = "UPDATE inf_books SET data_postuplenia = %s, aftor = %s, izdatelstvo = %s, kol_straniz = %s, data_izdania = %s WHERE id = %s"
                cursor.execute(update_query, (
                    new_data_postuplenia, new_aftor, new_izdatelstvo, new_kol_straniz, new_data_izdania,
                    book_id))
                db_connection.commit()
                print("Информация о книге успешно обновлена.")
            except ValueError:
                print("Ошибка: Введенное значение даты недопустимо. Пожалуйста, введите дату в формате YYYY-MM-DD.")

        Label(book_management_window, text="Изменить информацию о книге:").pack()
        Label(book_management_window, text="Дата поступления:").pack()
        new_data_postuplenia_entry = Entry(book_management_window)
        new_data_postuplenia_entry.pack()

        Label(book_management_window, text="Автор:").pack()
        new_aftor_entry = Entry(book_management_window)
        new_aftor_entry.pack()

        Label(book_management_window, text="Издательство:").pack()
        new_izdatelstvo_entry = Entry(book_management_window)
        new_izdatelstvo_entry.pack()

        Label(book_management_window, text="Количество страниц:").pack()
        new_kol_straniz_entry = Entry(book_management_window)
        new_kol_straniz_entry.pack()

        Label(book_management_window, text="Дата издания:").pack()
        new_data_izdania_entry = Entry(book_management_window)
        new_data_izdania_entry.pack()

        Button(book_management_window, text="Изменить", command=save_book_changes).pack()

        # Отображение информации из таблицы tranzakci
        select_tranzakci_query = "SELECT vremi_vahlo FROM tranzakci"
        cursor.execute(select_tranzakci_query)
        tranzakci_data = cursor.fetchall()

        for vremi_vahlo in tranzakci_data:
            Label(book_management_window, text=f"Время взятия книги: {vremi_vahlo}").pack()
            Label(book_management_window, text="").pack()

        book_management_window.mainloop()

    # Кнопка "Добавить книгу" для пользователя
    Button(library_window, text="Добавить книгу (Пользователь)", command=show_user_authentication_window).pack()

    # Кнопка "Авторизация админа"
    Button(library_window, text="Авторизация админа", command=show_admin_authentication_window).pack()

    library_window.mainloop()

# Отображаем окно с Афишей библиотеки
show_library_schedule()

# Закрываем соединение с базой данных
cursor.close()
db_connection.close() """
    return code

def var16BD():
    code = """-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 13 2024 г., 03:58
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `var_16`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Borrowers`
--

CREATE TABLE `Borrowers` (
  `borrower_id` int NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `passport_number` varchar(20) DEFAULT NULL,
  `INN` varchar(20) DEFAULT NULL,
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Borrowers`
--

INSERT INTO `Borrowers` (`borrower_id`, `full_name`, `phone_number`, `passport_number`, `INN`, `user_id`) VALUES
(1, 'Иванов Иван Иванович', '8(915)222-33-44', '42 11 567890', '044555555', 1),
(2, 'Иванов Сергей Петрович', '8(917)998-33-23', '42 21 557894', '044555555', 2),
(3, 'Ким Анна Валерьевна', '8(915)966-33-34', '45 21 557004', '044555555', NULL),
(4, 'Борисов Борис Борисович', '8(917)998-27-28', '40 33 678944', '044555555', NULL),
(5, 'Сокол Марина Олеговна', '8(925)755-33-55', '42 10 345555', '044522777', NULL),
(6, 'Соколова Анна Петровна', '8(927)998-77-88', '44 22 555666', '044522777', NULL),
(7, 'Власюк Мария Викторовна', '8(999)022-77-02', '46 21 557766', '044522777', NULL),
(8, 'Цой Алиса Семеновна', '8(915)001-01-44', '42 33 673312', '044522777', NULL),
(9, 'Шмелева Фаина Федоровна', '8(917)998-55-60', '42 11 340005', '044522888', NULL),
(10, 'Заремба Вера Васильевна', '8(915)660-33-60', '43 22 555601', '044522888', NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `Collateral`
--

CREATE TABLE `Collateral` (
  `collateral_id` int NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `item_name` varchar(50) DEFAULT NULL,
  `document_type` varchar(50) DEFAULT NULL,
  `document_number` varchar(50) DEFAULT NULL,
  `estimated_value` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Collateral`
--

INSERT INTO `Collateral` (`collateral_id`, `category`, `item_name`, `document_type`, `document_number`, `estimated_value`) VALUES
(1, 'автомобиль', 'автомобиль', 'тех паспорт', 'A123456', '100000.00'),
(2, 'автомобиль', 'автомобиль', 'тех паспорт', 'B123456', '200000.00'),
(3, 'автомобиль', 'автомобиль', 'тех паспорт', 'C123456', '300000.00'),
(4, 'недвижимость', 'недвижимость', 'свидетельство', 'D123456', '400000.00'),
(5, 'недвижимость', 'недвижимость', 'свидетельство', 'E123456', '500000.00'),
(6, 'моб. тел', 'моб. тел', 'паспорт', 'F123456', '10000.00'),
(7, 'моб. тел', 'моб. тел', 'паспорт', 'G123456', '20000.00'),
(8, NULL, NULL, NULL, NULL, NULL),
(9, NULL, NULL, NULL, NULL, NULL),
(10, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `Loans`
--

CREATE TABLE `Loans` (
  `loan_id` int NOT NULL,
  `borrower_id` int DEFAULT NULL,
  `loan_date` date DEFAULT NULL,
  `loan_term_months` int DEFAULT NULL,
  `loan_amount` decimal(10,2) DEFAULT NULL,
  `interest_rate` decimal(5,2) DEFAULT NULL,
  `status` enum('Погашен','На рассмотрении','Получен и погашается') DEFAULT 'На рассмотрении',
  `collateral_id` int DEFAULT NULL,
  `payment_status` enum('Погашен','Просрочен') DEFAULT 'Просрочен',
  `last_payment_date` date DEFAULT NULL,
  `overdue_interest` decimal(10,2) DEFAULT NULL,
  `loan_status` enum('approved','rejected','pending') DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Loans`
--

INSERT INTO `Loans` (`loan_id`, `borrower_id`, `loan_date`, `loan_term_months`, `loan_amount`, `interest_rate`, `status`, `collateral_id`, `payment_status`, `last_payment_date`, `overdue_interest`, `loan_status`) VALUES
(1, 1, '2022-03-01', 12, '50000.00', '10.00', 'Получен и погашается', 1, 'Погашен', NULL, NULL, 'pending'),
(2, 2, '2022-03-02', 24, '150000.00', '12.00', 'Получен и погашается', 2, 'Погашен', NULL, NULL, 'pending'),
(3, 3, '2022-03-04', 18, '250000.00', '10.00', 'Получен и погашается', 3, 'Погашен', NULL, NULL, 'pending'),
(4, 4, '2022-03-02', 16, '350000.00', '12.00', 'Получен и погашается', 4, 'Погашен', NULL, NULL, 'pending'),
(5, 5, '2022-03-02', 2, '500000.00', '10.00', 'Погашен', NULL, 'Погашен', NULL, NULL, 'pending'),
(6, 6, '2022-03-04', 4, '50000.00', '12.00', 'Погашен', NULL, 'Погашен', NULL, NULL, 'pending'),
(7, 7, '2022-03-05', 14, '25000.00', '12.00', 'Получен и погашается', 5, 'Погашен', NULL, NULL, 'pending'),
(8, 8, '2022-03-01', 1, '5000.00', '12.00', 'Погашен', NULL, 'Погашен', NULL, NULL, 'pending'),
(9, 9, '2022-03-01', 1, '3000.00', '11.00', 'Погашен', NULL, 'Погашен', NULL, NULL, 'pending'),
(10, 10, '2022-03-02', 2, '15000.00', '11.00', 'Погашен', NULL, 'Погашен', NULL, NULL, 'pending');

-- --------------------------------------------------------

--
-- Структура таблицы `Payments`
--

CREATE TABLE `Payments` (
  `payment_id` int NOT NULL,
  `loan_id` int DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `payment_amount` decimal(10,2) DEFAULT NULL,
  `overdue_interest` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `Users`
--

CREATE TABLE `Users` (
  `user_id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Users`
--

INSERT INTO `Users` (`user_id`, `username`, `password`) VALUES
(1, 'User1', 'User1'),
(2, '', '');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Borrowers`
--
ALTER TABLE `Borrowers`
  ADD PRIMARY KEY (`borrower_id`),
  ADD KEY `fk_user_id` (`user_id`);

--
-- Индексы таблицы `Collateral`
--
ALTER TABLE `Collateral`
  ADD PRIMARY KEY (`collateral_id`);

--
-- Индексы таблицы `Loans`
--
ALTER TABLE `Loans`
  ADD PRIMARY KEY (`loan_id`),
  ADD KEY `borrower_id` (`borrower_id`);

--
-- Индексы таблицы `Payments`
--
ALTER TABLE `Payments`
  ADD PRIMARY KEY (`payment_id`),
  ADD KEY `loan_id` (`loan_id`);

--
-- Индексы таблицы `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Borrowers`
--
ALTER TABLE `Borrowers`
  MODIFY `borrower_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `Collateral`
--
ALTER TABLE `Collateral`
  MODIFY `collateral_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `Loans`
--
ALTER TABLE `Loans`
  MODIFY `loan_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `Payments`
--
ALTER TABLE `Payments`
  MODIFY `payment_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Users`
--
ALTER TABLE `Users`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `Borrowers`
--
ALTER TABLE `Borrowers`
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`);

--
-- Ограничения внешнего ключа таблицы `Loans`
--
ALTER TABLE `Loans`
  ADD CONSTRAINT `loans_ibfk_1` FOREIGN KEY (`borrower_id`) REFERENCES `Borrowers` (`borrower_id`);

--
-- Ограничения внешнего ключа таблицы `Payments`
--
ALTER TABLE `Payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`loan_id`) REFERENCES `Loans` (`loan_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
 """
    return

def var16code():
    code = """import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QDialog, QFormLayout, QLabel, QTextEdit
import mysql.connector

class LoanRepaymentCardWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Оплата займа с банковской карты")
        layout = QVBoxLayout()

        # Форма для ввода данных о банковской карте
        self.card_number_label = QLabel("Номер карты:")  # Метка для номера карты
        self.card_number_input = QLineEdit()  # Поле ввода для номера карты
        self.expiry_date_label = QLabel("Срок действия (ММ/ГГ):")  # Метка для срока действия
        self.expiry_date_input = QLineEdit()  # Поле ввода для срока действия
        self.cvv_label = QLabel("CVV код:")  # Метка для CVV кода
        self.cvv_input = QLineEdit()  # Поле ввода для CVV кода

        layout.addWidget(self.card_number_label)
        layout.addWidget(self.card_number_input)
        layout.addWidget(self.expiry_date_label)
        layout.addWidget(self.expiry_date_input)
        layout.addWidget(self.cvv_label)
        layout.addWidget(self.cvv_input)

        # Кнопка для подтверждения оплаты
        self.pay_button = QPushButton("Оплатить")  # Кнопка "Оплатить"
        self.pay_button.clicked.connect(self.confirm_payment)  # Подключение метода confirm_payment к событию нажатия на кнопку
        layout.addWidget(self.pay_button)

        self.setLayout(layout)

    def confirm_payment(self):
        # Получение информации о банковской карте
        card_number = self.card_number_input.text()  # Получение номера карты
        expiry_date = self.expiry_date_input.text()  # Получение срока действия
        cvv = self.cvv_input.text()  # Получение CVV кода

        # Ваш код для обработки оплаты с использованием банковской карты
        # Здесь можно добавить логику для проведения платежа с использованием API банка или платежной системы
        # В данном примере просто выведем информацию о карте
        QMessageBox.information(self, "Подтверждение оплаты", f"Оплата с карты {card_number} прошла успешно.")

class LoanHistoryWindow(QDialog):
    def __init__(self, cursor):
        super().__init__()

        self.setWindowTitle("История займов")
        layout = QVBoxLayout()

        # Set the cursor
        self.cursor = cursor

        # Получение истории займов из базы данных
        self.history_text = QTextEdit()
        self.display_loan_history()

        layout.addWidget(self.history_text)
        self.setLayout(layout)

    def display_loan_history(self):
        # Выполнение SQL-запроса для получения истории займов
        query = "SELECT borrower_id, loan_date, loan_amount, status FROM Loans"
        self.cursor.execute(query)
        loan_history_data = self.cursor.fetchall()

        # Отображение данных о займах в QTextEdit
        for loan in loan_history_data:
            borrower_id = loan[0]
            loan_date = loan[1]
            loan_amount = loan[2]
            status = loan[3]
            self.history_text.append(f"ID Заемщика: {borrower_id}\nДата займа: {loan_date}\nСумма займа: {loan_amount}\nСтатус: {status}\n")

class BorrowerDetailsWindow(QDialog):
    def __init__(self, borrower_data):
        super().__init__()

        self.setWindowTitle("Данные о заемщике")
        layout = QFormLayout()

        # Создаем метки и добавляем их в layout
        layout.addRow(QLabel("Имя:"), QLabel(borrower_data[1]))
        layout.addRow(QLabel("Фамилия:"), QLabel(borrower_data[2]))
        layout.addRow(QLabel("Телефон:"), QLabel(borrower_data[3]))
        layout.addRow(QLabel("Пасспорт:"), QLabel(borrower_data[4]))

        self.setLayout(layout)

class CalculatorWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Калькулятор")
        layout = QVBoxLayout()

        self.amount_label = QLabel("Сумма займа:")
        self.amount_input = QLineEdit()
        self.term_label = QLabel("Срок займа (в месяцах):")
        self.term_input = QLineEdit()
        self.calculate_button = QPushButton("Рассчитать")
        self.calculate_button.clicked.connect(self.calculate_loan)

        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.term_label)
        layout.addWidget(self.term_input)
        layout.addWidget(self.calculate_button)

        self.setLayout(layout)

    def calculate_loan(self):
        try:
            amount = float(self.amount_input.text())
            term = int(self.term_input.text())
            total_amount = amount * (1 + 0.1 * term)  # Простой пример расчета
            QMessageBox.information(self, "Результат расчета", f"Сумма к возврату: {total_amount:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные числовые значения.")

class LoanRepaymentWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ежемесячные выплаты по займу")
        layout = QVBoxLayout()

        # Отображение информации о ежемесячных выплатах
        self.payment_info_label = QLabel("Сумма к выплате: $100\nДата платежа: 01.04.2024")
        layout.addWidget(self.payment_info_label)

        # Кнопка подтверждения оплаты
        self.pay_button = QPushButton("Оплатить")
        self.pay_button.clicked.connect(self.confirm_payment)
        layout.addWidget(self.pay_button)

        self.setLayout(layout)

    def confirm_payment(self):
        # Ваш код для обработки оплаты
        print("Платеж успешно подтвержден.")

class LoanApplicationWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Подача заявления на займ")
        layout = QVBoxLayout()

        self.information_label = QLabel("Заполните заявление на займ:")
        self.application_text = QTextEdit()

        layout.addWidget(self.information_label)
        layout.addWidget(self.application_text)

        self.apply_button = QPushButton("Отправить заявление")
        self.apply_button.clicked.connect(self.submit_application)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def submit_application(self):
        # Здесь можно добавить код для отправки заявления на сервер или базу данных
        application_text = self.application_text.toPlainText()
        QMessageBox.information(self, "Заявление отправлено", "Ваше заявление на займ отправлено.")

class BorrowerInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Интерфейс заемщика")
        self.setGeometry(100, 100, 400, 300)

        # Подключение к базе данных
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="var_16"
        )
        self.cursor = self.db_connection.cursor()

        layout = QVBoxLayout()

        # Логин
        self.login_label = QLabel("Логин:")
        self.login_input = QLineEdit()

        # Пароль
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Скрытие введенных символов

        # Кнопки для входа и регистрации
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)
        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self.register)

        layout.addWidget(self.login_label)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

        # Кнопка для открытия калькулятора
        self.calculator_button = QPushButton("Калькулятор")
        self.calculator_button.clicked.connect(self.open_calculator)
        layout.addWidget(self.calculator_button)

        # Кнопка для открытия окна подачи заявления
        self.application_button = QPushButton("Подать заявление")
        self.application_button.clicked.connect(self.open_application)
        layout.addWidget(self.application_button)

        self.repayment_button = QPushButton("Оплатить с карты")
        self.repayment_button.clicked.connect(self.open_repayment_card_window)
        layout.addWidget(self.repayment_button)

        self.setLayout(layout)

        self.history_button = QPushButton("История займов")
        self.history_button.clicked.connect(self.open_loan_history_window)
        layout.addWidget(self.history_button)

    def open_calculator(self):
        calculator_window = CalculatorWindow()
        calculator_window.exec_()

    def open_application(self):
        application_window = LoanApplicationWindow()
        application_window.exec_()

    def open_repayment_card_window(self):
        repayment_card_window = LoanRepaymentCardWindow()
        repayment_card_window.exec_()

    def open_loan_history_window(self):
        history_window = LoanHistoryWindow(self.cursor)  # Pass the cursor object
        history_window.exec_()

    def login(self):
        username = self.login_input.text()
        password = self.password_input.text()

        # Выполнение SQL-запроса для проверки логина и пароля
        query = "SELECT * FROM Users WHERE username = %s AND password = %s"
        values = (username, password)
        self.cursor.execute(query, values)
        user = self.cursor.fetchone()

        if user:
            # Получение идентификатора пользователя по имени пользователя
            user_id_query = "SELECT user_id FROM Users WHERE username = %s"
            self.cursor.execute(user_id_query, (username,))
            user_id = self.cursor.fetchone()[0]

            # Запрос данных о заемщике на основе идентификатора пользователя
            borrower_query = "SELECT * FROM Borrowers WHERE user_id = %s"
            self.cursor.execute(borrower_query, (user_id,))
            borrower_data = self.cursor.fetchone()

            # Создание и отображение окна с данными о заемщике
            borrower_details_window = BorrowerDetailsWindow(borrower_data)
            borrower_details_window.exec_()

            # Показать основной интерфейс после успешной авторизации
            self.show_main_interface(username)
        else:
            QMessageBox.warning(self, "Ошибка авторизации", "Неправильный логин или пароль.")

    def register(self):
        username = self.login_input.text()
        password = self.password_input.text()

        # Проверка наличия пользователя с таким же логином в базе данных
        query = "SELECT * FROM Users WHERE username = %s"
        values = (username,)
        self.cursor.execute(query, values)
        existing_user = self.cursor.fetchone()

        if existing_user:
            QMessageBox.warning(self, "Ошибка регистрации", "Пользователь с таким логином уже существует.")
        else:
            # Регистрация нового пользователя и заемщика
            query = "INSERT INTO Users (username, password) VALUES (%s, %s)"
            values = (username, password)
            self.cursor.execute(query, values)
            self.db_connection.commit()
            QMessageBox.information(self, "Успешная регистрация", "Пользователь успешно зарегистрирован.")
            # Показать основной интерфейс после успешной регистрации
            self.show_main_interface(username)

    def show_main_interface(self, username):
        # Скрыть окно входа и показать основной интерфейс
        self.hide()
        main_interface = MainInterface(username)
        main_interface.show()

class MainInterface(QWidget):
    def __init__(self, username):
        super().__init__()

        self.setWindowTitle("Главный интерфейс")
        self.setGeometry(100, 100, 400, 300)

        self.username_label = QLabel(f"Добро пожаловать, {username}!")
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        self.setLayout(layout)

class OperatorDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Панель оператора")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()

        self.application_list_label = QLabel("Список заявлений заемщиков:")
        layout.addWidget(self.application_list_label)

        # Placeholder for the application list (could be a table, list view, etc.)
        self.application_list = QTextEdit()
        layout.addWidget(self.application_list)

        # Buttons for approving and rejecting applications
        self.approve_button = QPushButton("Одобрить заявление")
        self.reject_button = QPushButton("Отклонить заявление")

        self.approve_button.clicked.connect(self.approve_application)
        self.reject_button.clicked.connect(self.reject_application)

        layout.addWidget(self.approve_button)
        layout.addWidget(self.reject_button)

        self.setLayout(layout)

    def approve_application(self):
        # Placeholder method for approving an application
        QMessageBox.information(self, "Одобрение заявления", "Заявление успешно одобрено.")

    def reject_application(self):
        # Placeholder method for rejecting an application
        QMessageBox.information(self, "Отклонение заявления", "Заявление успешно отклонено.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    borrower_interface = BorrowerInterface()
    operator_dashboard = OperatorDashboard()  # Создание объекта интерфейса оператора
    borrower_interface.show()  # Показ интерфейса заемщика
    operator_dashboard.show()  # Показ интерфейса оператора
    sys.exit(app.exec_())  # Выход из приложения при закрытии всех окон

 """
    return code

def var23BD():
    code = """-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 13 2024 г., 05:18
-- Версия сервера: 5.7.39
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `OnlineClothingStore`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Customers`
--

CREATE TABLE `Customers` (
  `ID` int(11) NOT NULL,
  `FirstName` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `LastName` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Password` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Customers`
--

INSERT INTO `Customers` (`ID`, `FirstName`, `LastName`, `Email`, `Phone`, `Password`) VALUES
(1, 'Марина', 'Дбар', 'User1@mail.ru', '8(915)222-33-44', '123456'),
(2, 'Олег', 'Шкуратов', 'User2@yandex.ru', '8(915)222-33-44', 'password'),
(3, 'Федор', 'Ким', 'User3@mail.ru', '8(915)222-33-44', 'abc123'),
(4, 'Петр', 'Сидоров', 'User4@yandex.ru', '8(915)222-33-44', 'qwerty'),
(5, 'Марина', 'Некрасова', 'User5@mail.ru', '8(996)782-33-44', 'letmein'),
(6, 'Светлана', 'Королева', 'User6@yandex.ru', '8(996)782-33-44', 'football'),
(7, 'Маргарита', 'Бойко', 'User7@mail.ru', '8(996)782-33-44', 'admin'),
(8, 'Алла', 'Пак', 'User8@mail.ru', '8(996)782-33-44', 'welcome'),
(9, 'Жанна', 'Серова', 'User9@mail.ru', '8(915)222-65-64', 'hello');

-- --------------------------------------------------------

--
-- Структура таблицы `OrderDetails`
--

CREATE TABLE `OrderDetails` (
  `ID` int(11) NOT NULL,
  `OrderID` int(11) DEFAULT NULL,
  `ProductID` int(11) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `OrderAmount` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `OrderDetails`
--

INSERT INTO `OrderDetails` (`ID`, `OrderID`, `ProductID`, `Quantity`, `OrderAmount`) VALUES
(1, 1, 1, 2, '7400.00'),
(2, 2, 6, 1, '1350.00'),
(3, 3, 7, 3, '18000.00'),
(4, 4, 8, 2, '5600.00'),
(5, 5, 9, 1, '4000.00'),
(6, 6, 10, 1, '2800.00');

-- --------------------------------------------------------

--
-- Структура таблицы `Orders`
--

CREATE TABLE `Orders` (
  `ID` int(11) NOT NULL,
  `OrderNumber` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `OrderDate` date DEFAULT NULL,
  `PaymentMethod` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ShippingAddress` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `CustomerID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Orders`
--

INSERT INTO `Orders` (`ID`, `OrderNumber`, `OrderDate`, `PaymentMethod`, `ShippingAddress`, `CustomerID`) VALUES
(1, '001', '2024-04-13', 'Карта', 'ул. Ленина, 10', 1),
(2, '002', '2024-04-14', 'Наличные', 'ул. Гагарина, 5', 2),
(3, '003', '2024-04-14', 'Карта', 'ул. Пушкина, 20', 3),
(4, '004', '2024-04-15', 'Карта', 'ул. Кирова, 15', 4),
(5, '005', '2024-04-16', 'Карта', 'ул. Советская, 8', 5),
(6, '006', '2024-04-17', 'Наличные', 'ул. Ленина, 10', 6),
(7, 'ORD123456', '2024-04-13', 'Cash', 'faafafaf', 1),
(8, 'ORD123456', '2024-04-13', 'Card', 'gggggg', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `Products`
--

CREATE TABLE `Products` (
  `ID` int(11) NOT NULL,
  `Category` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `Sizes` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Color` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Model` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Products`
--

INSERT INTO `Products` (`ID`, `Category`, `Name`, `Quantity`, `Price`, `Sizes`, `Color`, `Model`) VALUES
(1, 'Обувь', 'Туфли', 10, '7000.00', '35-42', 'Белый', 'Модель 1'),
(2, 'Обувь', 'Сандалии', 45, '1500.00', '35-42', 'Серый', 'Модель 2'),
(3, 'Обувь', 'Кеды', 20, '3500.00', '37-46', 'Серый', 'Модель 3'),
(4, 'Обувь', 'Туфли', 10, '7200.00', '35-42', 'Черный', 'Модель 4'),
(5, 'Одежда', 'Толстовка', 50, '3700.00', '42-54', 'Белый', 'Модель 5'),
(6, 'Одежда', 'Футболка', 50, '1350.00', '42-54', 'Белый', 'Модель 6'),
(7, 'Одежда', 'Толстовка', 40, '6000.00', '42-54', 'Синий', 'Модель 7'),
(8, 'Одежда', 'Майка', 45, '700.00', '42-54', 'Розовый', 'Модель 8'),
(9, 'Аксессуар', 'Сумочка', 25, '4000.00', NULL, 'Белый', 'Модель 9'),
(10, 'Аксессуар', 'Очки', 12, '2800.00', NULL, 'Черный', 'Модель 10');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Customers`
--
ALTER TABLE `Customers`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `OrderDetails`
--
ALTER TABLE `OrderDetails`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `OrderID` (`OrderID`),
  ADD KEY `ProductID` (`ProductID`);

--
-- Индексы таблицы `Orders`
--
ALTER TABLE `Orders`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `CustomerID` (`CustomerID`);

--
-- Индексы таблицы `Products`
--
ALTER TABLE `Products`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Customers`
--
ALTER TABLE `Customers`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `OrderDetails`
--
ALTER TABLE `OrderDetails`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `Orders`
--
ALTER TABLE `Orders`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `Products`
--
ALTER TABLE `Products`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `OrderDetails`
--
ALTER TABLE `OrderDetails`
  ADD CONSTRAINT `orderdetails_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `Orders` (`ID`),
  ADD CONSTRAINT `orderdetails_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `Products` (`ID`);

--
-- Ограничения внешнего ключа таблицы `Orders`
--
ALTER TABLE `Orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `Customers` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
 """
    return code

def var23code():
    code = """import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QDialogButtonBox, QInputDialog
import pymysql

class LoginDialog(QDialog):
    def __init__(self, db, cursor):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 200)

        self.db = db
        self.cursor = cursor

        self.email_label = QLabel("Username:")
        self.email_edit = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.register_button)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def get_login_info(self):
        username = self.email_edit.text()
        password = self.password_edit.text()
        return username, password

    def register(self):
        register_dialog = RegisterDialog(self.db, self.cursor)
        if register_dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(self, "Registration", "Registration successful. You can now login.")

    def authenticate(self, username, password):
        # Check if the entered username and password are for admin
        if username == "admin" and password == "admin":
            return True
        else:
            # Perform authentication - query your database
            try:
                query = "SELECT * FROM Customers WHERE Email = %s AND Password = %s"
                self.cursor.execute(query, (username, password))
                result = self.cursor.fetchone()
                if result:
                    return True
                else:
                    return False
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                return False

    def open_login_dialog(self):
        login_dialog = LoginDialog(self.db, self.cursor)
        if login_dialog.exec_() == QDialog.Accepted:
            username, password = login_dialog.get_login_info()
            if login_dialog.authenticate(username, password):
                if username == "admin" and password == "admin":
                    self.open_manager_interface()  # Открыть интерфейс менеджера
                else:
                    QMessageBox.information(self, "Login", "Logged in successfully as a regular user.")
            else:
                QMessageBox.warning(self, "Login", "Authentication failed.")

        


class RegisterDialog(QDialog):
    def __init__(self, db, cursor):
        super().__init__()
        self.setWindowTitle("Register")
        self.setFixedSize(300, 250)

        self.db = db
        self.cursor = cursor

        self.first_name_label = QLabel("First Name:")
        self.first_name_edit = QLineEdit()
        self.last_name_label = QLabel("Last Name:")
        self.last_name_edit = QLineEdit()
        self.email_label = QLabel("Email:")
        self.email_edit = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.phone_label = QLabel("Phone:")
        self.phone_edit = QLineEdit()

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.first_name_label)
        layout.addWidget(self.first_name_edit)
        layout.addWidget(self.last_name_label)
        layout.addWidget(self.last_name_edit)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_edit)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def get_registration_info(self):
        first_name = self.first_name_edit.text()
        last_name = self.last_name_edit.text()
        email = self.email_edit.text()
        password = self.password_edit.text()
        phone = self.phone_edit.text()
        return first_name, last_name, email, password, phone

    def save_user(self, first_name, last_name, email, password, phone):
        try:
            query = "INSERT INTO Customers (FirstName, LastName, Email, Password, Phone) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (first_name, last_name, email, password, phone))
            self.db.commit()
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return False


class ClientInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Online Clothing Store - Client Interface")
        self.setGeometry(100, 100, 800, 600)

        # Establish connection to the database
        self.db = pymysql.connect(host="localhost", user="root", password="", database="OnlineClothingStore")
        self.cursor = self.db.cursor()

        # Create main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Category selection
        self.category_label = QLabel("Select Category:")
        self.category_combo_box = QComboBox()
        self.main_layout.addWidget(self.category_label)
        self.main_layout.addWidget(self.category_combo_box)

        # Products table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(4)
        self.products_table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Quantity"])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_layout.addWidget(self.products_table)

        # Buttons layout
        self.buttons_layout = QHBoxLayout()
        self.main_layout.addLayout(self.buttons_layout)

        # Add to cart button
        self.add_to_cart_button = QPushButton("Add to Cart")
        self.add_to_cart_button.clicked.connect(self.add_to_cart)
        self.buttons_layout.addWidget(self.add_to_cart_button)

        # View cart button
        self.view_cart_button = QPushButton("View Cart")
        self.view_cart_button.clicked.connect(self.view_cart)
        self.buttons_layout.addWidget(self.view_cart_button)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.open_login_dialog)
        self.buttons_layout.addWidget(self.login_button)

        # Initialize cart
        self.cart = []

        # Load categories
        self.load_categories()

    def open_login_dialog(self):
        login_dialog = LoginDialog(self.db, self.cursor)
        if login_dialog.exec_() == QDialog.Accepted:
            username, password = login_dialog.get_login_info()
            if login_dialog.authenticate(username, password):
                if username == "admin" and password == "admin":
                    self.hide()  # Скрываем основное окно
                    manager_interface = ManagerInterface()  # Создаем экземпляр интерфейса менеджера
                    manager_interface.show()  # Отображаем интерфейс менеджера
                else:
                    QMessageBox.information(self, "Login", "Logged in successfully as a regular user.")
            else:
                QMessageBox.warning(self, "Login", "Authentication failed.")



    def load_categories(self):
        try:
            query = "SELECT DISTINCT Category FROM Products"
            self.cursor.execute(query)
            categories = self.cursor.fetchall()
            for category in categories:
                self.category_combo_box.addItem(category[0])
            self.category_combo_box.currentIndexChanged.connect(self.load_products)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def load_products(self):
        category = self.category_combo_box.currentText()
        try:
            query = "SELECT ID, Name, Price, Quantity FROM Products WHERE Category = %s"
            self.cursor.execute(query, (category,))
            products = self.cursor.fetchall()
            self.products_table.setRowCount(len(products))
            for i, product in enumerate(products):
                for j in range(4):
                    self.products_table.setItem(i, j, QTableWidgetItem(str(product[j])))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def add_to_cart(self):
        selected_rows = self.products_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Error", "Please select a product.")
            return

        login_dialog = LoginDialog(self.db, self.cursor)
        if login_dialog.exec_() == QDialog.Accepted:
            email, password = login_dialog.get_login_info()
            # Check authentication - perform your authentication logic here
            if self.authenticate(email, password):
                for row in selected_rows:
                    product_id = self.products_table.item(row.row(), 0).text()
                    product_name = self.products_table.item(row.row(), 1).text()
                    product_price = float(self.products_table.item(row.row(), 2).text())
                    self.cart.append((product_id, product_name, product_price))
                QMessageBox.information(self, "Success", "Product(s) added to cart.")
            else:
                QMessageBox.warning(self, "Error", "Authentication failed.")


    def view_cart(self):
        if not self.cart:
            QMessageBox.information(self, "Cart", "Your cart is empty.")
            return

        cart_info = "Your Cart:\n"
        total_price = 0
        for item in self.cart:
            cart_info += f"{item[1]} - ${item[2]}\n"
            total_price += item[2]
        cart_info += f"\nTotal Price: ${total_price}"

        address, ok = QInputDialog.getText(self, "Delivery Address", "Enter delivery address:")
        if ok:
            cart_info += f"\nDelivery Address: {address}"

            payment_method, ok = QInputDialog.getItem(self, "Payment Method", "Select Payment Method:",
                                                      ("Cash", "Card"), 0, False)
            if ok:
                cart_info += f"\nPayment Method: {payment_method}"

                # Insert order into database
                if self.insert_order(address, payment_method):
                    QMessageBox.information(self, "Cart", "Order placed successfully.")
                    self.cart = []  # Clear cart after successful order
                else:
                    QMessageBox.critical(self, "Error", "Failed to place order.")

        QMessageBox.information(self, "Cart", cart_info)

    def authenticate(self, email, password):
        # Perform authentication - query your database
        try:
            query = "SELECT * FROM Customers WHERE Email = %s AND Password = %s"
            self.cursor.execute(query, (email, password))
            result = self.cursor.fetchone()
            if result:
                return True
            else:
                return False
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return False

    def insert_order(self, address, payment_method):
        # Insert order into database
        try:
            customer_id = 1  # Replace with actual customer ID after implementing user authentication
            query = "INSERT INTO Orders (OrderNumber, OrderDate, PaymentMethod, ShippingAddress, CustomerID) " \
                    "VALUES (%s, NOW(), %s, %s, %s)"
            self.cursor.execute(query, (self.generate_order_number(), payment_method, address, customer_id))
            self.db.commit()
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return False

    def generate_order_number(self):
        # Generate a unique order number (You can implement your own logic here)
        return "ORD123456"

class ManagerInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Online Clothing Store - Manager Interface")
        self.setGeometry(100, 100, 800, 600)

        # Establish connection to the database
        self.db = pymysql.connect(host="localhost", user="root", password="", database="OnlineClothingStore")
        self.cursor = self.db.cursor()

        # Create main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Placeholder widgets for manager interface
        self.manager_label = QLabel("Manager Interface - Work in Progress")
        self.main_layout.addWidget(self.manager_label)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_interface = ClientInterface()
    manager_interface = ManagerInterface()
    client_interface.show()
    sys.exit(app.exec_())

 """
    return code

def var13BD():
    code = """-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 13 2024 г., 04:29
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `B13`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Admin`
--

CREATE TABLE `Admin` (
  `id` int NOT NULL,
  `login` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Admin`
--

INSERT INTO `Admin` (`id`, `login`, `password`) VALUES
(1, 'root', 'root');

-- --------------------------------------------------------

--
-- Структура таблицы `Category`
--

CREATE TABLE `Category` (
  `id` int NOT NULL,
  `name_category` varchar(50) NOT NULL,
  `id_Position` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Category`
--

INSERT INTO `Category` (`id`, `name_category`, `id_Position`) VALUES
(1, 'Лечение зубов', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `Doctor`
--

CREATE TABLE `Doctor` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `patronymic` varchar(50) NOT NULL,
  `education` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `id_Category` int NOT NULL,
  `id_UnderCotegor` int NOT NULL,
  `id_Position` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Doctor`
--

INSERT INTO `Doctor` (`id`, `name`, `fname`, `patronymic`, `education`, `email`, `password`, `id_Category`, `id_UnderCotegor`, `id_Position`) VALUES
(1, 'Иванвывававаdsd', 'Ивановв', 'Иванович', 'выввы', 'shamil', 'shamil', 1, 1, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `Position`
--

CREATE TABLE `Position` (
  `id` int NOT NULL,
  `name_position` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Position`
--

INSERT INTO `Position` (`id`, `name_position`) VALUES
(1, 'Терапевт');

-- --------------------------------------------------------

--
-- Структура таблицы `Service`
--

CREATE TABLE `Service` (
  `id` int NOT NULL,
  `kod_servise` int NOT NULL,
  `services` varchar(50) NOT NULL,
  `price` int NOT NULL,
  `id_Category` int NOT NULL,
  `id_UnderCotegor` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Service`
--

INSERT INTO `Service` (`id`, `kod_servise`, `services`, `price`, `id_Category`, `id_UnderCotegor`) VALUES
(1, 9901, 'Филтек Z260', 2000, 1, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `UnderCotegor`
--

CREATE TABLE `UnderCotegor` (
  `id` int NOT NULL,
  `name_under_cotegor` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `UnderCotegor`
--

INSERT INTO `UnderCotegor` (`id`, `name_under_cotegor`) VALUES
(1, 'Лечение Кариеса');

-- --------------------------------------------------------

--
-- Структура таблицы `Work_schedule`
--

CREATE TABLE `Work_schedule` (
  `id` int NOT NULL,
  `day_of_work` date NOT NULL,
  `shift` varchar(50) NOT NULL,
  `time` text NOT NULL,
  `id_Doctor` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Work_schedule`
--

INSERT INTO `Work_schedule` (`id`, `day_of_work`, `shift`, `time`, `id_Doctor`) VALUES
(1, '2024-04-02', 'Дневная Смена', '09:00-18:01', 1);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Admin`
--
ALTER TABLE `Admin`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `Category`
--
ALTER TABLE `Category`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_Position` (`id_Position`);

--
-- Индексы таблицы `Doctor`
--
ALTER TABLE `Doctor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_Category` (`id_Category`),
  ADD KEY `id_UnderCotegor` (`id_UnderCotegor`),
  ADD KEY `id_Position` (`id_Position`);

--
-- Индексы таблицы `Position`
--
ALTER TABLE `Position`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `Service`
--
ALTER TABLE `Service`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_UnderCotegor` (`id_UnderCotegor`),
  ADD KEY `id_Category` (`id_Category`);

--
-- Индексы таблицы `UnderCotegor`
--
ALTER TABLE `UnderCotegor`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `Work_schedule`
--
ALTER TABLE `Work_schedule`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_Doctor` (`id_Doctor`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Admin`
--
ALTER TABLE `Admin`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `Category`
--
ALTER TABLE `Category`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `Doctor`
--
ALTER TABLE `Doctor`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `Position`
--
ALTER TABLE `Position`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `Service`
--
ALTER TABLE `Service`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `UnderCotegor`
--
ALTER TABLE `UnderCotegor`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `Work_schedule`
--
ALTER TABLE `Work_schedule`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `Category`
--
ALTER TABLE `Category`
  ADD CONSTRAINT `category_ibfk_1` FOREIGN KEY (`id_Position`) REFERENCES `Position` (`id`);

--
-- Ограничения внешнего ключа таблицы `Doctor`
--
ALTER TABLE `Doctor`
  ADD CONSTRAINT `doctor_ibfk_1` FOREIGN KEY (`id_Category`) REFERENCES `Category` (`id`),
  ADD CONSTRAINT `doctor_ibfk_2` FOREIGN KEY (`id_UnderCotegor`) REFERENCES `UnderCotegor` (`id`),
  ADD CONSTRAINT `doctor_ibfk_3` FOREIGN KEY (`id_Position`) REFERENCES `Position` (`id`);

--
-- Ограничения внешнего ключа таблицы `Service`
--
ALTER TABLE `Service`
  ADD CONSTRAINT `service_ibfk_1` FOREIGN KEY (`id_Category`) REFERENCES `Category` (`id`),
  ADD CONSTRAINT `service_ibfk_2` FOREIGN KEY (`id_UnderCotegor`) REFERENCES `UnderCotegor` (`id`);

--
-- Ограничения внешнего ключа таблицы `Work_schedule`
--
ALTER TABLE `Work_schedule`
  ADD CONSTRAINT `work_schedule_ibfk_1` FOREIGN KEY (`id_Doctor`) REFERENCES `Doctor` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
 """
    return code

def var13code():
    code = """#База данных
import pymysql

class database:
    def __init__(self, host, user, password, database):
        try:
            self.connection = pymysql.connect(host=host, user=user, password=password, database=database)
            self.cursor = self.connection.cursor()
        except pymysql.Error as e:
            print(f"Error connecting to database: {e}")

    def getDoctorInfo(self, doctor_id=1):
        query = "SELECT * FROM Doctor WHERE id = %s"
        self.cursor.execute(query, (doctor_id,))
        doctor = self.cursor.fetchone()
        columns = [column[0] for column in self.cursor.description]
        return {columns[i]: doctor[i] for i in range(len(columns))}

    def updateDoctorInfo(self, doctor_id=1, **kwargs):
        columns = ', '.join([f"{key} = %s" for key in kwargs.keys()])
        values = tuple(kwargs.values())
        query = f"UPDATE Doctor SET {columns} WHERE id = %s"
        self.cursor.execute(query, values + (doctor_id,))
        self.connection.commit()

    def getWorkSchedule(self, doctor_id):
        cursor = self.db.cursor
        cursor.execute("SELECT day_of_work, shift, time FROM Work_schedule WHERE id_Doctor = %s", (doctor_id,))
        schedule = cursor.fetchall()
        return schedule

    def getAllCategories(self):
        cursor = self.cursor
        cursor.execute("SELECT name_category FROM Category")
        categories = cursor.fetchall()
        return [category[0] for category in categories]

    def getAllUnderCategories(self):
        cursor = self.cursor
        cursor.execute("SELECT name_under_cotegor FROM UnderCotegor")
        under_categories = cursor.fetchall()
        return [under_category[0] for under_category in under_categories]


-------------------------------------------------------------------------------------------
#Main
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox,QTableWidgetItem, QTableWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from database import database


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('untitled.ui', self)
        self.db = database(host='localhost', user='root', password='', database='B13')
        self.btnSave.clicked.connect(self.saveDoctorInfo)
        self.pushButton.clicked.connect(self.showWorkSchedule)
        self.loadDoctorInfo()

    def getCategoryName(self, category_id):
        cursor = self.db.cursor
        cursor.execute("SELECT name_category FROM Category WHERE id = %s", (category_id,))
        category = cursor.fetchone()
        return category[0] if category else ""

    def getUnderCategoryName(self, under_category_id):
        cursor = self.db.cursor
        cursor.execute("SELECT name_under_cotegor FROM UnderCotegor WHERE id = %s", (under_category_id,))
        under_category = cursor.fetchone()
        return under_category[0] if under_category else ""

    def getPositionName(self, position_id):
        cursor = self.db.cursor
        cursor.execute("SELECT name_position FROM Position WHERE id = %s", (position_id,))
        position = cursor.fetchone()
        return position[0] if position else ""

    def loadDoctorInfo(self):
        doctor = self.db.getDoctorInfo(1)

        layout = QVBoxLayout()

        # Получаем названия столбцов из таблицы Doctor
        cursor = self.db.cursor
        cursor.execute("SHOW COLUMNS FROM Doctor")
        columns = [column[0] for column in cursor.fetchall()]

        self.lineEdits = []
        self.columns = columns  # Сохраняем имена столбцов для последующего использования

        for column in columns:
            lineEdit = QLineEdit()

            if column == 'id_Category':
                lineEdit.setText(self.getCategoryName(doctor[column]))
            elif column == 'id_UnderCotegor':
                lineEdit.setText(self.getUnderCategoryName(doctor[column]))
            elif column == 'id_Position':
                lineEdit.setText(self.getPositionName(doctor[column]))
            else:
                lineEdit.setText(str(doctor[column]))

            layout.addWidget(QLabel(column.capitalize()))
            layout.addWidget(lineEdit)
            self.lineEdits.append(lineEdit)

        self.scrollAreaWidgetContents.setLayout(layout)

    def saveDoctorInfo(self):
        doctor_data = {}
        for lineEdit, column in zip(self.lineEdits, self.columns):
            # Игнорируем столбцы, которые не должны изменяться
            if column in ['id_Position', 'id_UnderCotegor', 'id_Category']:
                continue

            doctor_data[column] = lineEdit.text()

        self.db.updateDoctorInfo(1, **doctor_data)

        # Показать сообщение об успешном сохранении
        QMessageBox.information(self, 'Сохранение', 'Данные успешно сохранены!')

    def showWorkSchedule(self):
        cursor = self.db.cursor
        cursor.execute("SELECT * FROM Work_schedule WHERE id_Doctor = %s", (1,))
        data = cursor.fetchall()

        # Форматирование данных в красивый текст
        text_data = "Расписание работы:\n\n"

        for row_data in data:
            text_data += f"Day of Work: {row_data[1]}\n"
            text_data += f"Shift: {row_data[2]}\n"
            text_data += f"Time: {row_data[3]}\n\n"

        # Показать данные в виде текста через QMessageBox
        QMessageBox.information(self, 'Расписание работы', text_data, QMessageBox.Ok)


class AuthWindow(QMainWindow):
    closeSignal = pyqtSignal()

    def __init__(self):
        super(AuthWindow, self).__init__()
        loadUi('Avto.ui', self)

        self.pushButton.clicked.connect(self.check_login)

    def check_login(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()

        # Подключение к базе данных
        db = database(host='localhost', user='root', password='', database='B13')
        cursor = db.cursor

        # Поиск в таблице Admin
        cursor.execute("SELECT * FROM Admin WHERE login = %s AND password = %s", (login, password))
        admin = cursor.fetchone()

        if admin and login == 'root' and password == 'root':
            # Отправляем сигнал о закрытии текущего окна
            self.closeSignal.emit()
            # Открываем окно Admin
            self.admin_window = AdminWindow()
            self.admin_window.show()

        else:
            # Поиск в таблице Doctor
            cursor.execute("SELECT * FROM Doctor WHERE email = %s AND password = %s", (login, password))
            doctor = cursor.fetchone()

            if doctor:
                # Отправляем сигнал о закрытии текущего окна
                self.closeSignal.emit()
                # Открываем главное окно
                self.main_window = MainWindow()
                self.main_window.show()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль', QMessageBox.Ok)


class AdminWindow(QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        loadUi('Admin.ui', self)
        self.db = database(host='localhost', user='root', password='', database='B13')

        # Загрузка данных в комбобоксы
        self.loadCategoryAndUnderCategory()
        self.loadServices()

        # Привязка кнопок
        self.btnSaveService.clicked.connect(self.saveServiceChanges)
        self.btnDeleteService.clicked.connect(self.deleteService)
        self.comboBoxServices.currentIndexChanged.connect(self.loadSelectedServiceInfo)

    def loadCategoryAndUnderCategory(self):
        categories = self.db.getAllCategories()
        under_categories = self.db.getAllUnderCategories()

        self.comboBoxCategory.clear()
        self.comboBoxUnderCategory.clear()

        self.comboBoxCategory.addItems(categories)
        self.comboBoxUnderCategory.addItems(under_categories)

    def loadServices(self):
        services = self.db.getAllServicesNames()
        self.comboBoxServices.clear()
        self.comboBoxServices.addItems(services)

    def loadSelectedServiceInfo(self):
        service_name = self.comboBoxServices.currentText()
        service_id = self.db.getServiceIdByName(service_name)

        self.loadServiceInfo(service_id)

    def loadServiceInfo(self, service_id):
        cursor = self.db.cursor
        cursor.execute("SELECT * FROM Service WHERE id = %s", (service_id,))
        service = cursor.fetchone()

        if service:
            self.lineEditServiceName.setText(service[2])
            self.spinBoxServicePrice.setValue(service[3])
            self.comboBoxCategory.setCurrentIndex(self.comboBoxCategory.findText(self.getCategoryName(service[4])))
            self.comboBoxUnderCategory.setCurrentIndex(
                self.comboBoxUnderCategory.findText(self.getUnderCategoryName(service[5])))

    def editService(self, service_id):
        service_name = self.lineEditServiceName.text()
        service_price = self.spinBoxServicePrice.value()
        category_id = self.comboBoxCategory.currentIndex() + 1
        under_category_id = self.comboBoxUnderCategory.currentIndex() + 1

        cursor = self.db.cursor
        cursor.execute(
            "UPDATE Service SET services = %s, price = %s, id_Category = %s, id_UnderCotegor = %s WHERE id = %s",
            (service_name, service_price, category_id, under_category_id, service_id))
        self.db.connection.commit()

    def deleteService(self):
        service_name = self.comboBoxServices.currentText()
        service_id = self.db.getServiceIdByName(service_name)

        cursor = self.db.cursor
        cursor.execute("DELETE FROM Service WHERE id = %s", (service_id,))
        self.db.connection.commit()

        self.loadServices()
        QMessageBox.information(self, 'Удаление', 'Услуга успешно удалена!')

    def saveServiceChanges(self):
        service_name = self.comboBoxServices.currentText()
        service_id = self.db.getServiceIdByName(service_name)

        self.editService(service_id)
        self.loadServices()
        QMessageBox.information(self, 'Сохранение', 'Изменения успешно сохранены!')

    def getCategoryName(self, category_id):
        cursor = self.db.cursor
        cursor.execute("SELECT name_category FROM Category WHERE id = %s", (category_id,))
        category = cursor.fetchone()
        return category[0] if category else ""

    def getUnderCategoryName(self, under_category_id):
        cursor = self.db.cursor
        cursor.execute("SELECT name_under_cotegor FROM UnderCotegor WHERE id = %s", (under_category_id,))
        under_category = cursor.fetchone()
        return under_category[0] if under_category else ""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth_window = AuthWindow()
    auth_window.show()
    auth_window.closeSignal.connect(auth_window.close)
    sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox,QTableWidgetItem, QTableWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from database import database


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('untitled.ui', self)
        self.db = database(host='localhost', user='root', password='', database='B13')
        self.btnSave.clicked.connect(self.saveDoctorInfo)
        self.pushButton.clicked.connect(self.showWorkSchedule)
        self.loadDoctorInfo()

    def getCategoryName(self, category_id):
        cursor = self.db.cursor
        cursor.execute("SELECT name_category FROM Category WHERE id = %s", (category_id,))
        category = cursor.fetchone()
        return category[0] if category else ""

    def getUnderCategoryName(self, under_category_id):
        cursor = self.db.cursor
        cursor.execute("SELECT name_under_cotegor FROM UnderCotegor WHERE id = %s", (under_category_id,))
        under_category = cursor.fetchone()
        return under_category[0] if under_category else ""

    def getPositionName(self, position_id):
        cursor = self.db.cursor
        cursor.execute("SELECT name_position FROM Position WHERE id = %s", (position_id,))
        position = cursor.fetchone()
        return position[0] if position else ""

    def loadDoctorInfo(self):
        doctor = self.db.getDoctorInfo(1)

        layout = QVBoxLayout()

        # Получаем названия столбцов из таблицы Doctor
        cursor = self.db.cursor
        cursor.execute("SHOW COLUMNS FROM Doctor")
        columns = [column[0] for column in cursor.fetchall()]

        self.lineEdits = []
        self.columns = columns  # Сохраняем имена столбцов для последующего использования

        for column in columns:
            lineEdit = QLineEdit()

            if column == 'id_Category':
                lineEdit.setText(self.getCategoryName(doctor[column]))
            elif column == 'id_UnderCotegor':
                lineEdit.setText(self.getUnderCategoryName(doctor[column]))
            elif column == 'id_Position':
                lineEdit.setText(self.getPositionName(doctor[column]))
            else:
                lineEdit.setText(str(doctor[column]))

            layout.addWidget(QLabel(column.capitalize()))
            layout.addWidget(lineEdit)
            self.lineEdits.append(lineEdit)

        self.scrollAreaWidgetContents.setLayout(layout)

    def saveDoctorInfo(self):
        doctor_data = {}
        for lineEdit, column in zip(self.lineEdits, self.columns):
            # Игнорируем столбцы, которые не должны изменяться
            if column in ['id_Position', 'id_UnderCotegor', 'id_Category']:
                continue

            doctor_data[column] = lineEdit.text()

        self.db.updateDoctorInfo(1, **doctor_data)

        # Показать сообщение об успешном сохранении
        QMessageBox.information(self, 'Сохранение', 'Данные успешно сохранены!')

    def showWorkSchedule(self):
        cursor = self.db.cursor
        cursor.execute("SELECT * FROM Work_schedule WHERE id_Doctor = %s", (1,))
        data = cursor.fetchall()

        # Форматирование данных в красивый текст
        text_data = "Расписание работы:\n\n"

        for row_data in data:
            text_data += f"Day of Work: {row_data[1]}\n"
            text_data += f"Shift: {row_data[2]}\n"
            text_data += f"Time: {row_data[3]}\n\n"

        # Показать данные в виде текста через QMessageBox
        QMessageBox.information(self, 'Расписание работы', text_data, QMessageBox.Ok)


class AuthWindow(QMainWindow):
    closeSignal = pyqtSignal()

    def __init__(self):
        super(AuthWindow, self).__init__()
        loadUi('Avto.ui', self)

        self.pushButton.clicked.connect(self.check_login)

    def check_login(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()

        # Подключение к базе данных
        db = database(host='localhost', user='root', password='', database='B13')
        cursor = db.cursor

        # Поиск в таблице Admin
        cursor.execute("SELECT * FROM Admin WHERE login = %s AND password = %s", (login, password))
        admin = cursor.fetchone()

        if admin and login == 'root' and password == 'root':
            # Отправляем сигнал о закрытии текущего окна
            self.closeSignal.emit()
            # Открываем окно Admin
            self.admin_window = AdminWindow()
            self.admin_window.show()

        else:
            # Поиск в таблице Doctor
            cursor.execute("SELECT * FROM Doctor WHERE email = %s AND password = %s", (login, password))
            doctor = cursor.fetchone()

            if doctor:
                # Отправляем сигнал о закрытии текущего окна
                self.closeSignal.emit()
                # Открываем главное окно
                self.main_window = MainWindow()
                self.main_window.show()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль', QMessageBox.Ok)


class AdminWindow(QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        loadUi('Admin.ui', self)
        self.db = database(host='localhost', user='root', password='', database='B13')

        # Загрузка данных в комбобоксы
        self.loadCategoryAndUnderCategory()
        self.loadServices()

        # Привязка кнопок
        self.btnSaveService.clicked.connect(self.saveServiceChanges)
        self.btnDeleteService.clicked.connect(self.deleteService)
        self.comboBoxServices.currentIndexChanged.connect(self.loadSelectedServiceInfo)

    def loadCategoryAndUnderCategory(self):
        try:
            categories = self.db.getAllCategories()
            under_categories = self.db.getAllUnderCategories()

            self.comboBoxCategory.clear()
            self.comboBoxUnderCategory.clear()

            self.comboBoxCategory.addItems(categories)
            self.comboBoxUnderCategory.addItems(under_categories)
        except Exception as e:
            print(f"Error loading categories and undercategories: {e}")

    def loadServices(self):
        try:
            services = self.db.getAllServicesNames()
            self.comboBoxServices.clear()
            self.comboBoxServices.addItems(services)
        except Exception as e:
            print(f"Error loading services: {e}")

    def loadSelectedServiceInfo(self):
        try:
            service_name = self.comboBoxServices.currentText()
            service_id = self.db.getServiceIdByName(service_name)

            self.loadServiceInfo(service_id)
        except Exception as e:
            print(f"Error loading selected service info: {e}")

    def loadServiceInfo(self, service_id):
        try:
            cursor = self.db.cursor
            cursor.execute("SELECT * FROM Service WHERE id = %s", (service_id,))
            service = cursor.fetchone()

            if service:
                self.lineEditServiceName.setText(service[2])
                self.spinBoxServicePrice.setValue(service[3])
                self.comboBoxCategory.setCurrentIndex(self.comboBoxCategory.findText(self.getCategoryName(service[4])))
                self.comboBoxUnderCategory.setCurrentIndex(
                    self.comboBoxUnderCategory.findText(self.getUnderCategoryName(service[5])))

        except Exception as e:
            print(f"Error loading service info: {e}")

    def editService(self, service_id):
        try:
            service_name = self.lineEditServiceName.text()
            service_price = self.spinBoxServicePrice.value()
            category_id = self.comboBoxCategory.currentIndex() + 1
            under_category_id = self.comboBoxUnderCategory.currentIndex() + 1

            cursor = self.db.cursor
            cursor.execute(
                "UPDATE Service SET services = %s, price = %s, id_Category = %s, id_UnderCotegor = %s WHERE id = %s",
                (service_name, service_price, category_id, under_category_id, service_id))
            self.db.connection.commit()

        except Exception as e:
            print(f"Error editing service: {e}")

    def deleteService(self):
        try:
            service_name = self.comboBoxServices.currentText()
            service_id = self.db.getServiceIdByName(service_name)

            cursor = self.db.cursor
            cursor.execute("DELETE FROM Service WHERE id = %s", (service_id,))
            self.db.connection.commit()

            self.loadServices()
            QMessageBox.information(self, 'Удаление', 'Услуга успешно удалена!')

        except Exception as e:
            print(f"Error deleting service: {e}")

    def saveServiceChanges(self):
        try:
            service_name = self.comboBoxServices.currentText()
            service_id = self.db.getServiceIdByName(service_name)

            self.editService(service_id)
            self.loadServices()
            QMessageBox.information(self, 'Сохранение', 'Изменения успешно сохранены!')

        except Exception as e:
            print(f"Error saving service changes: {e}")

    def getCategoryName(self, category_id):
        try:
            cursor = self.db.cursor
            cursor.execute("SELECT name_category FROM Category WHERE id = %s", (category_id,))
            category = cursor.fetchone()
            return category[0] if category else ""
        except Exception as e:
            print(f"Error getting category name: {e}")

    def getUnderCategoryName(self, under_category_id):
        try:
            cursor = self.db.cursor
            cursor.execute("SELECT name_under_cotegor FROM UnderCotegor WHERE id = %s", (under_category_id,))
            under_category = cursor.fetchone()
            return under_category[0] if under_category else ""
        except Exception as e:
            print(f"Error getting undercategory name: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth_window = AuthWindow()
    auth_window.show()
    auth_window.closeSignal.connect(auth_window.close)
    sys.exit(app.exec_())


-----------------------------------------------------------------------------------------------


#Untitle.ui

<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPushButton" name="btnSave">
    <property name="geometry">
     <rect>
      <x>180</x>
      <y>250</y>
      <width>191</width>
      <height>61</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>13</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Сохранить изменение</string>
    </property>
   </widget>
   <widget class="QScrollArea" name="scrollAreaWidgetContents_2">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>0</y>
      <width>461</width>
      <height>251</height>
     </rect>
    </property>
    <property name="widgetResizable">
     <bool>true</bool>
    </property>
    <widget class="QWidget" name="scrollAreaWidgetContents">
     <property name="geometry">
      <rect>
       <x>0</x>
       <y>0</y>
       <width>459</width>
       <height>249</height>
      </rect>
     </property>
    </widget>
   </widget>
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>320</y>
      <width>191</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>10</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Посмотреть свое рассписание</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>22</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>

------------------------------------------------------------------------------
#Avto.ui
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>360</x>
      <y>40</y>
      <width>26</width>
      <height>8</height>
     </rect>
    </property>
    <property name="text">
     <string>TextLabel</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="lineEdit">
    <property name="geometry">
     <rect>
      <x>320</x>
      <y>100</y>
      <width>113</width>
      <height>20</height>
     </rect>
    </property>
   </widget>
   <widget class="QLineEdit" name="lineEdit_2">
    <property name="geometry">
     <rect>
      <x>320</x>
      <y>140</y>
      <width>113</width>
      <height>20</height>
     </rect>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>330</x>
      <y>180</y>
      <width>75</width>
      <height>23</height>
     </rect>
    </property>
    <property name="text">
     <string>PushButton</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>22</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
-----------------------------------------------------------------------------------------------------------------------
#Admin.ui
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QComboBox" name="comboBoxCategory">
    <property name="geometry">
     <rect>
      <x>250</x>
      <y>20</y>
      <width>201</width>
      <height>22</height>
     </rect>
    </property>
   </widget>
   <widget class="QWidget" name="verticalLayoutWidget">
    <property name="geometry">
     <rect>
      <x>80</x>
      <y>60</y>
      <width>561</width>
      <height>191</height>
     </rect>
    </property>
    <layout class="QVBoxLayout" name="verticalLayout"/>
   </widget>
   <widget class="QPushButton" name="pushButton1">
    <property name="geometry">
     <rect>
      <x>310</x>
      <y>310</y>
      <width>75</width>
      <height>23</height>
     </rect>
    </property>
    <property name="text">
     <string>PushButton</string>
    </property>
   </widget>
   <widget class="QComboBox" name="comboBoxUnderCategory">
    <property name="geometry">
     <rect>
      <x>510</x>
      <y>30</y>
      <width>201</width>
      <height>22</height>
     </rect>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>22</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
 """
    return code

def var21BD():
    code = """-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 13 2024 г., 06:07
-- Версия сервера: 5.7.39
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `susek`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Banks`
--

CREATE TABLE `Banks` (
  `Bank_ID` int(11) NOT NULL,
  `Bank_Name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Banks`
--

INSERT INTO `Banks` (`Bank_ID`, `Bank_Name`) VALUES
(1, 'Банк 1'),
(2, 'Банк 2');

-- --------------------------------------------------------

--
-- Структура таблицы `Buyers`
--

CREATE TABLE `Buyers` (
  `Buyer_ID` int(11) NOT NULL,
  `Name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `BIK` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Account` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Buyers`
--

INSERT INTO `Buyers` (`Buyer_ID`, `Name`, `Phone`, `BIK`, `Account`) VALUES
(1, 'ИП МолКом', '8(915)222-33-44', '044555555', '04455555545301'),
(2, 'ООО \"Колос\"', '8(996)782-33-44', '044522777', '04452277745202'),
(3, 'Овощебаза №1', '8(915)222-65-64', '044522888', '04452288845378');

-- --------------------------------------------------------

--
-- Структура таблицы `Categories`
--

CREATE TABLE `Categories` (
  `Category_ID` int(11) NOT NULL,
  `Category` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Categories`
--

INSERT INTO `Categories` (`Category_ID`, `Category`) VALUES
(1, 'Молочные'),
(2, 'Крупы'),
(3, 'Овощи');

-- --------------------------------------------------------

--
-- Структура таблицы `Payments`
--

CREATE TABLE `Payments` (
  `Payment_ID` int(11) NOT NULL,
  `Payment_Number` int(11) DEFAULT NULL,
  `Payment_Date` date DEFAULT NULL,
  `Payment_Time` time DEFAULT NULL,
  `Bank_ID` int(11) DEFAULT NULL,
  `Total_Amount` decimal(10,2) DEFAULT NULL,
  `Buyer_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Payments`
--

INSERT INTO `Payments` (`Payment_ID`, `Payment_Number`, `Payment_Date`, `Payment_Time`, `Bank_ID`, `Total_Amount`, `Buyer_ID`) VALUES
(1, 1, '2022-03-09', '12:00:00', 1, '700.00', 1),
(2, 2, '2022-03-09', '12:30:00', 1, '382.00', 2),
(3, 3, '2022-03-10', '13:00:00', 1, '200.00', 3),
(4, 4, '2022-03-10', '13:30:00', 2, '150.00', 3);

-- --------------------------------------------------------

--
-- Структура таблицы `Products`
--

CREATE TABLE `Products` (
  `Product_ID` int(11) NOT NULL,
  `Name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `Packaging` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Category_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Products`
--

INSERT INTO `Products` (`Product_ID`, `Name`, `Price`, `Packaging`, `Category_ID`) VALUES
(1, 'Молоко', '70.00', '1 литр', 1),
(2, 'Сметана', '85.00', '250 гр', 1),
(3, 'Творог', '120.00', '250 гр', 1),
(4, 'Рис', '120.00', '900 гр', 2),
(5, 'Гречка', '135.00', '900 гр', 2),
(6, 'Чечевица', '132.00', '900 гр', 2),
(7, 'Помидоры', '87.00', 'кг', 3),
(8, 'Апельсины', '65.00', 'кг', 3);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Banks`
--
ALTER TABLE `Banks`
  ADD PRIMARY KEY (`Bank_ID`);

--
-- Индексы таблицы `Buyers`
--
ALTER TABLE `Buyers`
  ADD PRIMARY KEY (`Buyer_ID`);

--
-- Индексы таблицы `Categories`
--
ALTER TABLE `Categories`
  ADD PRIMARY KEY (`Category_ID`);

--
-- Индексы таблицы `Payments`
--
ALTER TABLE `Payments`
  ADD PRIMARY KEY (`Payment_ID`),
  ADD KEY `Bank_ID` (`Bank_ID`),
  ADD KEY `Buyer_ID` (`Buyer_ID`);

--
-- Индексы таблицы `Products`
--
ALTER TABLE `Products`
  ADD PRIMARY KEY (`Product_ID`),
  ADD KEY `Category_ID` (`Category_ID`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Banks`
--
ALTER TABLE `Banks`
  MODIFY `Bank_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `Buyers`
--
ALTER TABLE `Buyers`
  MODIFY `Buyer_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `Categories`
--
ALTER TABLE `Categories`
  MODIFY `Category_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `Payments`
--
ALTER TABLE `Payments`
  MODIFY `Payment_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `Products`
--
ALTER TABLE `Products`
  MODIFY `Product_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `Payments`
--
ALTER TABLE `Payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`Bank_ID`) REFERENCES `Banks` (`Bank_ID`),
  ADD CONSTRAINT `payments_ibfk_2` FOREIGN KEY (`Buyer_ID`) REFERENCES `Buyers` (`Buyer_ID`);

--
-- Ограничения внешнего ключа таблицы `Products`
--
ALTER TABLE `Products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`Category_ID`) REFERENCES `Categories` (`Category_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
 """
    return code

def var21code():
    code = """import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTextEdit, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QInputDialog
from PyQt5.QtCore import Qt
import pymysql


class BuyerInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Интерфейс покупателя')

        layout = QVBoxLayout()

        self.email_label = QLabel('Email:')
        self.email_input = QLineEdit()

        self.login_button = QPushButton('Войти')
        self.login_button.clicked.connect(self.login)

        self.info_label = QLabel('Информация о товарах:')
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)

        self.order_button = QPushButton('Заказать товары')
        self.order_button.clicked.connect(self.order_products)

        self.receipt_button = QPushButton('Просмотр квитанции на оплату')
        self.receipt_button.clicked.connect(self.view_receipt)

        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.info_label)
        layout.addWidget(self.info_text)
        layout.addWidget(self.order_button)
        layout.addWidget(self.receipt_button)

        self.setLayout(layout)

        self.db = pymysql.connect(host="localhost", user="root", password="", database="susek")
        self.cursor = self.db.cursor()

    def login(self):
        # Реализация входа пользователя по email
        email = self.email_input.text()
        if email:
            QMessageBox.information(self, 'Вход выполнен', 'Вы успешно вошли в личный кабинет!')
            self.fetch_product_info()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите email.')

    def fetch_product_info(self):
        # Получение информации о товарах из базы данных
        try:
            query = "SELECT category, name, quantity FROM products ORDER BY category, name"
            self.cursor.execute(query)
            products = self.cursor.fetchall()

            info = ""
            current_category = ""
            for product in products:
                category, name, quantity = product
                if category != current_category:
                    info += f"\n{category}:\n"
                    current_category = category
                info += f"{name}: {quantity} шт.\n"

            self.info_text.setText(info)
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка при получении информации о товарах: {str(e)}')

    def order_products(self):
        # Реализация заказа товаров
        selected_products = self.info_text.toPlainText()
        if selected_products:
            QMessageBox.information(self, 'Заказ товаров', 'Товары успешно заказаны!')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Выберите товары для заказа.')

    def view_receipt(self):
        # Реализация просмотра квитанции на оплату
        receipt_number = self.receipt_input.text()
        if receipt_number:
            QMessageBox.information(self, 'Квитанция на оплату', f'Квитанция №{receipt_number} успешно просмотрена!')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Введите номер квитанции.')


class AccountantInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Интерфейс бухгалтера')

        layout = QVBoxLayout()

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('root')

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('root')
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Войти')
        self.login_button.clicked.connect(self.login)


        self.add_category_button = QPushButton('Добавить категорию товаров')
        self.add_category_button.clicked.connect(self.add_category)

        self.add_product_button = QPushButton('Добавить товар')
        self.add_product_button.clicked.connect(self.add_product)

        self.add_buyer_button = QPushButton('Добавить покупателя')
        self.add_buyer_button.clicked.connect(self.add_buyer)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(3)
        self.orders_table.setHorizontalHeaderLabels(['ID', 'Товар', 'Количество'])

        self.summary_info_label = QLabel('Сводная информация о заказах:')
        self.summary_info_text = QTextEdit()
        self.summary_info_text.setReadOnly(True)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.add_category_button)
        layout.addWidget(self.add_product_button)
        layout.addWidget(self.add_buyer_button)
        layout.addWidget(self.orders_table)
        layout.addWidget(self.summary_info_label)
        layout.addWidget(self.summary_info_text)

        self.setLayout(layout)

        self.db = pymysql.connect(host="localhost", user="root", password="", database="susek")
        self.cursor = self.db.cursor()

    def login(self):
        # Реализация входа бухгалтера
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            QMessageBox.information(self, 'Вход выполнен', 'Вы успешно вошли в личный кабинет бухгалтера!')
            self.fetch_orders_info()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите имя пользователя и пароль.')

    def fetch_orders_info(self):
        # Получение информации о заказах из базы данных
        try:
            query = "SELECT * FROM orders"
            self.cursor.execute(query)
            orders = self.cursor.fetchall()

            self.orders_table.setRowCount(len(orders))
            for i, order in enumerate(orders):
                order_id, product_name, quantity = order
                self.orders_table.setItem(i, 0, QTableWidgetItem(str(order_id)))
                self.orders_table.setItem(i, 1, QTableWidgetItem(product_name))
                self.orders_table.setItem(i, 2, QTableWidgetItem(str(quantity)))
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка при получении информации о заказах: {str(e)}')

    def add_category(self):
        # Реализация добавления категории товаров
        category_name, ok = QInputDialog.getText(self, 'Добавление категории', 'Введите название категории:')
        if ok:
            try:
                query = f"INSERT INTO categories (name) VALUES ('{category_name}')"
                self.cursor.execute(query)
                self.db.commit()
                QMessageBox.information(self, 'Добавление категории', f'Категория "{category_name}" успешно добавлена!')
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Ошибка при добавлении категории: {str(e)}')

    def add_product(self):
        # Реализация добавления товара
        product_name, ok = QInputDialog.getText(self, 'Добавление товара', 'Введите название товара:')
        if ok:
            try:
                query = f"INSERT INTO products (name) VALUES ('{product_name}')"
                self.cursor.execute(query)
                self.db.commit()
                QMessageBox.information(self, 'Добавление товара', f'Товар "{product_name}" успешно добавлен!')
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Ошибка при добавлении товара: {str(e)}')


    def add_buyer(self):
        # Реализация добавления покупателя
        buyer_name, ok = QInputDialog.getText(self, 'Добавление покупателя', 'Введите имя покупателя:')
        if ok:
            try:
                query = f"INSERT INTO buyers (name) VALUES ('{buyer_name}')"
                self.cursor.execute(query)
                self.db.commit()
                QMessageBox.information(self, 'Добавление покупателя', f'Покупатель "{buyer_name}" успешно добавлен!')
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Ошибка при добавлении покупателя: {str(e)}')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Система мелкооптового магазина «Сусек»')

        self.buyer_interface = BuyerInterface()
        self.accountant_interface = AccountantInterface()

        self.tabs = QComboBox()
        self.tabs.addItems(['Интерфейс покупателя', 'Интерфейс бухгалтера'])
        self.tabs.currentIndexChanged.connect(self.switch_tab)

        self.setCentralWidget(self.buyer_interface)

        self.statusBar().showMessage('Готово')

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.buyer_interface)
        self.layout.addWidget(self.accountant_interface)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def switch_tab(self, i):
        if i == 0:
            self.setCentralWidget(self.buyer_interface)
        elif i == 1:
            self.setCentralWidget(self.accountant_interface)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
 """
    return code

def var17code():
    code = """импорты:
mysql.connector 
datetime
PyQt5
PyQt5-tools


import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QInputDialog, QTextEdit
import mysql.connector

class AddRealEstateWindow(QDialog):
    def __init__(self, taxpayer_id, cursor):
        super().__init__()
        self.setWindowTitle("Добавление недвижимого имущества")
        self.taxpayer_id = taxpayer_id
        self.cursor = cursor
        self.layout = QVBoxLayout()

        # Создаем виджеты для ввода информации о недвижимости
        self.address_label = QLabel("Адрес:")
        self.address_input = QLineEdit()
        self.layout.addWidget(self.address_label)
        self.layout.addWidget(self.address_input)

        self.rooms_label = QLabel("Количество комнат:")
        self.rooms_input = QLineEdit()
        self.layout.addWidget(self.rooms_label)
        self.layout.addWidget(self.rooms_input)

        self.area_label = QLabel("Площадь:")
        self.area_input = QLineEdit()
        self.layout.addWidget(self.area_label)
        self.layout.addWidget(self.area_input)

        self.cadastre_label = QLabel("Кадастровый номер:")
        self.cadastre_input = QLineEdit()
        self.layout.addWidget(self.cadastre_label)
        self.layout.addWidget(self.cadastre_input)

        self.appraisal_label = QLabel("Оценочная стоимость:")
        self.appraisal_input = QLineEdit()
        self.layout.addWidget(self.appraisal_label)
        self.layout.addWidget(self.appraisal_input)

        # Кнопка для добавления недвижимости
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_real_estate)
        self.layout.addWidget(self.add_button)

        self.setLayout(self.layout)

    def add_real_estate(self):
        address = self.address_input.text()
        rooms = self.rooms_input.text()
        area = self.area_input.text()
        cadastre_number = self.cadastre_input.text()
        appraisal_value = self.appraisal_input.text()

        # Вставляем информацию о недвижимости в базу данных
        query = "
            INSERT INTO RealEstate (taxpayer_id, Address, Rooms, Area, CadastreNumber, AppraisalValue)
            VALUES (%s, %s, %s, %s, %s, %s)
        "
        values = (self.taxpayer_id, address, rooms, area, cadastre_number, appraisal_value)
        self.cursor.execute(query, values)
        self.cursor.commit()

        QMessageBox.information(self, "Успех", "Недвижимость успешно добавлена.")
        self.close()

class PersonalInfoWindow(QDialog):
    def __init__(self, taxpayer_id, cursor):
        super().__init__()
        self.setWindowTitle("Личная информация")
        self.taxpayer_id = taxpayer_id
        self.layout = QVBoxLayout()
        self.cursor = cursor  # Сохраняем экземпляр курсора

        # Получаем информацию о налогоплательщике из базы данных
        self.taxpayer_info = self.get_taxpayer_info()

        # Отображаем информацию о налогоплательщике
        self.display_info()

        # Кнопка для сохранения изменений
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def get_taxpayer_info(self):
        # Получение информации о налогоплательщике из базы данных
        query = "SELECT Fullname, Passport, SNILS, Address FROM Taxpayers WHERE taxpayer_id = %s"
        self.cursor.execute(query, (self.taxpayer_id,))
        taxpayer_info = self.cursor.fetchone()
        return taxpayer_info

    def display_info(self):
        # Отображаем информацию о налогоплательщике в виде меток и полей для ввода
        labels = ["ФИО:", "Паспорт:", "СНИЛС:", "Адрес:"]
        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            info = QLineEdit(str(self.taxpayer_info[i]))
            info.setReadOnly(False)  # Разрешить редактирование
            self.layout.addWidget(label)
            self.layout.addWidget(info)

    def save_changes(self):
        # Ваш код для сохранения изменений в базе данных
        QMessageBox.information(self, "Успех", "Изменения сохранены.")

class TaxBillingWindow(QDialog):
    def __init__(self, taxpayer_id, cursor):
        super().__init__()
        self.setWindowTitle("Просмотр начислений и формирование квитанции на оплату налога")
        self.taxpayer_id = taxpayer_id
        self.cursor = cursor
        self.layout = QVBoxLayout()

        # Отображение начислений налога и пени
        self.display_tax_and_penalty()

        # Кнопка для формирования квитанции на оплату
        self.generate_receipt_button = QPushButton("Сформировать квитанцию на оплату")
        self.generate_receipt_button.clicked.connect(self.generate_receipt)
        self.layout.addWidget(self.generate_receipt_button)

        self.setLayout(self.layout)

    def display_tax_and_penalty(self):
        # Получение начислений налога и пени из базы данных
        query = "
            SELECT TaxAmount, PenaltyAmount FROM TaxBilling 
            WHERE taxpayer_id = %s
        "
        self.cursor.execute(query, (self.taxpayer_id,))
        tax_billing_info = self.cursor.fetchone()

        # Отображение начислений налога и пени
        tax_amount_label = QLabel(f"Сумма налога: {tax_billing_info[0]}")
        penalty_amount_label = QLabel(f"Сумма пени: {tax_billing_info[1]}")
        self.layout.addWidget(tax_amount_label)
        self.layout.addWidget(penalty_amount_label)

    def generate_receipt(self):
        # Ваш код для формирования квитанции на оплату
        QMessageBox.information(self, "Успех", "Квитанция на оплату сформирована.")

class TaxpayerInterface(QDialog):
    def __init__(self, cursor=None):
        super().__init__()

        self.setWindowTitle("Интерфейс налогоплательщика")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.snils_label = QLabel("СНИЛС:")
        self.snils_input = QLineEdit()
        layout.addWidget(self.snils_label)
        layout.addWidget(self.snils_input)

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.add_real_estate_button = QPushButton("Добавить недвижимость")
        self.add_real_estate_button.clicked.connect(self.open_add_real_estate_window)
        layout.addWidget(self.add_real_estate_button)

        # Add tax calculator button
        self.calculate_tax_button = QPushButton("Рассчитать налог")
        self.calculate_tax_button.clicked.connect(self.calculate_tax)
        layout.addWidget(self.calculate_tax_button)

        # Add tax billing button
        self.view_tax_billing_button = QPushButton("Просмотр начислений и формирование квитанции на оплату")
        self.view_tax_billing_button.clicked.connect(self.open_tax_billing_window)
        layout.addWidget(self.view_tax_billing_button)

        self.setLayout(layout)

        # Check if cursor is provided
        if cursor is not None:
            self.cursor = cursor

        # Подключение к базе данных (если курсор не был предоставлен)
        if not hasattr(self, 'cursor'):
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="var_17"
            )
            self.cursor = self.db_connection.cursor()


    def open_add_real_estate_window(self):
        add_real_estate_window = AddRealEstateWindow(self.taxpayer_id, self.cursor)
        add_real_estate_window.exec_()

    def login(self):
        snils = self.snils_input.text()
        password = self.password_input.text()

        query = "SELECT * FROM Taxpayers WHERE snils = %s AND password = %s"
        values = (snils, password)
        self.cursor.execute(query, values)
        taxpayer = self.cursor.fetchone()

        if taxpayer:
            QMessageBox.information(self, "Успешный вход", "Добро пожаловать!")
            self.taxpayer_id = taxpayer[0]  # Set the taxpayer_id attribute
            self.open_personal_info_window(self.taxpayer_id)
        else:
            QMessageBox.warning(self, "Ошибка входа", "Неправильный СНИЛС или пароль.")

    def register(self):
        snils = self.snils_input.text()
        password = self.password_input.text()

        # Проверяем, есть ли уже такой пользователь в БД
        query = "SELECT * FROM Taxpayers WHERE snils = %s"
        values = (snils,)
        self.cursor.execute(query, values)
        existing_taxpayer = self.cursor.fetchone()

        if existing_taxpayer:
            QMessageBox.warning(self, "Ошибка регистрации", "Пользователь с таким СНИЛС уже существует.")
        else:
            # Регистрация нового пользователя
            query = "INSERT INTO Taxpayers (snils, password) VALUES (%s, %s)"
            values = (snils, password)
            self.cursor.execute(query, values)
            self.db_connection.commit()
            QMessageBox.information(self, "Успешная регистрация", "Пользователь успешно зарегистрирован.")

    def open_personal_info_window(self, taxpayer_id):
        personal_info_window = PersonalInfoWindow(taxpayer_id, self.cursor)
        personal_info_window.exec_()

    def calculate_tax(self):
        # Create a dialog window to get user income
        income, ok = QInputDialog.getDouble(self, "Введите доход", "Введите ваш годовой доход:", 0, 0, 1000000, 2)
        if ok:
            tax_amount = self.calculate_tax_amount(income)
            QMessageBox.information(self, "Сумма налога", f"Сумма налога к уплате: {tax_amount:.2f}")

    def calculate_tax_amount(self, income):
        # Example tax calculation
        tax_rate = 0.15
        deduction = 5000
        taxable_income = income - deduction
        if taxable_income <= 0:
            return 0
        else:
            tax_amount = taxable_income * tax_rate
            return tax_amount

    def open_tax_billing_window(self):
        tax_billing_window = TaxBillingWindow(self.taxpayer_id, self.cursor)
        tax_billing_window.exec_()


class TaxInspectorInterface(QDialog):
    def __init__(self, cursor):
        super().__init__()

        self.setWindowTitle("Интерфейс инспектора информационной системы налоговой службы")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.taxpayer_label = QLabel("ID налогоплательщика:")
        self.taxpayer_input = QLineEdit()
        layout.addWidget(self.taxpayer_label)
        layout.addWidget(self.taxpayer_input)

        self.search_button = QPushButton("Поиск")
        self.search_button.clicked.connect(self.search_taxpayer)
        layout.addWidget(self.search_button)

        self.taxpayer_info_label = QLabel("Информация о налогоплательщике:")
        layout.addWidget(self.taxpayer_info_label)

        self.taxpayer_info_text = QTextEdit()
        self.taxpayer_info_text.setReadOnly(True)
        layout.addWidget(self.taxpayer_info_text)

        # Кнопка для получения сводной информации
        self.summary_info_button = QPushButton("Получить сводную информацию")
        self.summary_info_button.clicked.connect(self.get_summary_info)
        layout.addWidget(self.summary_info_button)

        self.summary_info_text = QTextEdit()
        self.summary_info_text.setReadOnly(True)
        layout.addWidget(self.summary_info_text)

        self.setLayout(layout)

        self.cursor = cursor  # Store the cursor

    def search_taxpayer(self):
        taxpayer_id = self.taxpayer_input.text()
        query = "SELECT * FROM Taxpayers WHERE taxpayer_id = %s"
        self.cursor.execute(query, (taxpayer_id,))
        taxpayer_info = self.cursor.fetchone()
        if taxpayer_info:
            self.display_taxpayer_info(taxpayer_info)
        else:
            QMessageBox.warning(self, "Поиск", "Налогоплательщик с указанным ID не найден.")

    def display_taxpayer_info(self, taxpayer_info):
        # Display taxpayer information
        info_text = f"ID: {taxpayer_info[0]}\n"
        info_text += f"ФИО: {taxpayer_info[1]}\n"
        info_text += f"Паспорт: {taxpayer_info[2]}\n"
        info_text += f"СНИЛС: {taxpayer_info[3]}\n"
        info_text += f"Адрес: {taxpayer_info[4]}\n"
        self.taxpayer_info_text.setPlainText(info_text)

    def get_summary_info(self):
        taxpayer_id = self.taxpayer_input.text()
        query = "
            SELECT r.Address, r.Rooms, COUNT(t.taxpayer_id) AS NumTaxpayers
            FROM RealEstate r
            LEFT JOIN Taxpayers t ON r.taxpayer_id = t.taxpayer_id
            WHERE r.taxpayer_id = %s
            GROUP BY r.Address, r.Rooms
            ORDER BY r.Address ASC, r.Rooms ASC
        "
        self.cursor.execute(query, (taxpayer_id,))
        summary_info = "Сводная информация:\n\n"

        for row in self.cursor.fetchall():
            address = row[0]
            rooms = row[1]
            num_taxpayers = row[2]
            summary_info += f"Адрес: {address}, Количество комнат: {rooms}, Количество налогоплательщиков: {num_taxpayers}\n"

        self.summary_info_text.setPlainText(summary_info)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = QDialog()
    layout = QVBoxLayout()

    taxpayer_button = QPushButton("Налогоплательщик")
    inspector_button = QPushButton("Инспектор")
    layout.addWidget(taxpayer_button)
    layout.addWidget(inspector_button)

    login_window.setLayout(layout)

    # Connect the signals after defining the cursor
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="var_17"
    )
    cursor = db_connection.cursor()

    taxpayer_button.clicked.connect(lambda: open_window(TaxpayerInterface, cursor))
    inspector_button.clicked.connect(lambda: open_window(TaxInspectorInterface, cursor))

    # Define the open_window function
    def open_window(window_class, cursor=None):
        if cursor is None:
            window = window_class()
        else:
            window = window_class(cursor)
        if hasattr(window, 'get_summary_info'):  # Check if the window has the get_summary_info method
            window.get_summary_info()  # Call the method only if it exists
        window.exec_()

    login_window.exec_()
    sys.exit(app.exec_())
 """
    return code

def var17BD():
    code = """-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 13 2024 г., 06:35
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `var_17`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Taxpayers`
--

CREATE TABLE `Taxpayers` (
  `taxpayer_id` int NOT NULL,
  `Fullname` varchar(255) DEFAULT NULL,
  `Passport` varchar(20) DEFAULT NULL,
  `SNILS` varchar(20) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Taxpayers`
--

INSERT INTO `Taxpayers` (`taxpayer_id`, `Fullname`, `Passport`, `SNILS`, `Address`, `Password`) VALUES
(1, 'Иванов Иван Иванович', '1234567890', '123-456-789 01', 'Ул. Текстильщиков дом 25 кв 15', 'password1'),
(2, 'Иванов Сергей Петрович', '2345678901', '234-567-890 02', 'Ул. Ак. Скрябина дом 51 кв 23', 'password2'),
(3, 'Ким Анна Валерьевна', '3456789012', '345-678-901 03', 'Ул. Текстильщиков дом 18 кв 22', 'password3'),
(4, 'Борисов Борис Борисович', '4567890123', '456-789-012 04', 'Ул. Ак. Скрябина дом 5 кв 14', 'password4'),
(5, 'Сокол Марина Олеговна', '5678901234', '567-890-123 05', 'Ул. Текстильщиков дом 5 кв 14', 'password5'),
(6, 'Соколова Анна Петровна', '6789012345', '678-901-234 06', 'Ул. Луговая дом 25', 'password6'),
(7, 'Власюк Мария Викторовна', '7890123456', '789-012-345 07', 'Ул. Луговая дом 27', 'password7'),
(8, 'Цой Алиса Семеновна', '8901234567', '890-123-456 08', 'Ул. Луговая дом 34', 'password8'),
(9, 'Шмелева Фаина Федоровна', '9012345678', '901-234-567 09', 'Ул. Ак. Скрябина дом 5 кв 16', 'password9'),
(10, 'Заремба Вера Васильевна', '0123456789', '012-345-678 10', 'Ул. Текстильщиков дом 5 кв 17', 'password10');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Taxpayers`
--
ALTER TABLE `Taxpayers`
  ADD PRIMARY KEY (`taxpayer_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Taxpayers`
--
ALTER TABLE `Taxpayers`
  MODIFY `taxpayer_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
 """
    return code



