from PyQt5 import QtWidgets, QtCore, QtNetwork, QtGui
import configparser
import json


config = configparser.RawConfigParser()
config.read('.settings.ini')
TOKEN = config.get("settings", "token")
CITY = "Saint Petersburg"


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.resize(400, 300)
        self.manager = None
        self.weatherData = None
        self.setupUI()
        self.getWeather()

    def setupUI(self):
        # Set up the UI
        widget = QtWidgets.QWidget()

        cityLabel = QtWidgets.QLabel(f"City: {CITY}")
        cityLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        cityLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)

        self.tempLabel = QtWidgets.QLabel()
        self.tempLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.tempLabel.setFont(QtGui.QFont("sans-serif", 22, QtGui.QFont.Bold))
        self.tempLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)

        self.iconLabel = QtWidgets.QLabel()
        self.iconLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.iconLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)

        self.descLabel = QtWidgets.QLabel()
        self.descLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        self.descLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.descLabel.setFont(QtGui.QFont("sans-serif", 20))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(cityLabel)
        layout.addStretch()
        layout.addWidget(self.iconLabel)
        layout.addWidget(self.descLabel)
        layout.addWidget(self.tempLabel)
        layout.addStretch()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        quitAction = QtWidgets.QAction(self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(self.close)
        quitAction.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.addAction(quitAction)

    def getWeatherIcon(self, icon: str):
        url = QtCore.QUrl(f"http://openweathermap.org/img/wn/{icon}@2x.png")
        self.manager = QtNetwork.QNetworkAccessManager()
        self.manager.finished.connect(self.showWeatherIcon)
        self.manager.get(QtNetwork.QNetworkRequest(url))
    
    def showWeatherIcon(self, response: QtNetwork.QNetworkReply):
        # Show the weather icon
        if response.error():
            print(response.errorString())
            return
        icon = QtGui.QImage()
        icon.loadFromData(response.readAll())
        self.iconLabel.setPixmap(QtGui.QPixmap(icon))
        self.manager.deleteLater()

    def getWeather(self):
        # Send API request to openweathermap.org
        city = "Saint Petersburg"  # We can change this to any city, e.g. "London"
        url = QtCore.QUrl(f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={TOKEN}&units=metric")
        self.manager = QtNetwork.QNetworkAccessManager()
        self.manager.finished.connect(self.showWeather)
        self.manager.get(QtNetwork.QNetworkRequest(url))
    
    def showWeather(self, response: QtNetwork.QNetworkReply):
        # Show the weather data
        if response.error():
            print(response.errorString())
            return
        self.weatherData = json.loads(response.readAll().data().decode("utf-8"))
        self.manager.deleteLater()
        self.getWeatherIcon(self.weatherData["weather"][0]["icon"])
        temperature = round(self.weatherData["main"]["temp"])
        self.tempLabel.setText(f"{temperature}°C")
        self.descLabel.setText(self.weatherData["weather"][0]["main"])
