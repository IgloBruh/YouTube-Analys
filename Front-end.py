import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QLineEdit, QWidget
from googleapiclient.discovery import build
import matplotlib.pyplot as plt


class YouTubeStatisticsApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Statistics')
        self.label = QLabel('Введите ID вашего YouTube канала:')
        self.input_field = QLineEdit()
        self.button = QPushButton('Получить статистику')
        self.button.clicked.connect(self.get_statistics)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.input_field)
        vbox.addWidget(self.button)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
    
    def get_statistics(self):
        
        vbox = QVBoxLayout()
        widget = QWidget()
        channel_id = self.input_field.text()  # UCzB2V3zc2E4dy3-nxJoD0Yg
        
        try:

            api_key = 'AIzaSyDymq50UAPwQhoF3b34mseT9kDNS19fB6c'
            youtube = build('youtube', 'v3', developerKey=api_key)

            # Получаем статистику канала
            response = youtube.channels().list(
                part='statistics',
                id=channel_id
            ).execute()
            # Получаем количество подписок и сумму просмотров
            sub_count = response['items'][0]['statistics']['subscriberCount']


            total_views = 0
            total_likes = 0
            video_idis = []
            
            # Получаем список видео канала
            video_response = youtube.search().list(
                part='id',
                channelId=channel_id,
                maxResults=50
            ).execute()
            nextPage = video_response.get('nextPageToken')
            
            while nextPage:
                for item in video_response.get('items', []):
                    if 'videoId' in item['id']:
                        video_id = item['id']['videoId']
                        video_idis.append(video_id)
                video_response = youtube.search().list(
                    part='id',
                    channelId=channel_id,
                    maxResults=50,
                    pageToken=nextPage
                ).execute()
                nextPage = video_response.get('nextPageToken')
            
            for video_id in video_idis:
                video_info = youtube.videos().list(
                    part='statistics, snippet',
                    id=video_id
                ).execute()
                if video_info.get('items'):
                    views = video_info['items'][0]['statistics']['viewCount']
                    likes = video_info['items'][0]['statistics']['likeCount']
                    total_views += int(views)
                    total_likes += int(likes)

            average_views = total_views / len(video_idis)
            
            video_titles = []
            video_views = []
            
            for video_id in video_idis:
                video_info = youtube.videos().list(
                        part='statistics, snippet',
                        id=video_id
                    ).execute()
                video_views.append(int(video_info['items'][0]['statistics']['viewCount']))
                video_titles.append(video_info['items'][0]['snippet']['title'])

            # Create a bar graph
            plt.title('Views of the Last 10 Videos')
            plt.xlabel('Video ID')
            plt.ylabel('Views')
            plt.bar(video_titles[:10], video_views[:10])
            plt.legend()
            plt.show()
            
            # Выводим результаты
            vbox.addWidget(QLabel(f'Количество подписок: {sub_count}'))
            vbox.addWidget(QLabel(f'Среднее количество просмотров: {average_views}'))
            vbox.addWidget(QLabel(f'Сумма просмотров: {total_views}'))
            vbox.addWidget(QLabel(f'Сумма лайков: {total_likes}'))
            widget.setLayout(vbox)
            self.setCentralWidget(widget)
            return 0
        except:
            vbox.addWidget(QLabel(f'Неверный ID канала youtube'))
            
            self.input_field = QLineEdit()
            self.button = QPushButton('Получить статистику')
            self.button.clicked.connect(self.get_statistics)
            
            vbox.addWidget(self.input_field)
            vbox.addWidget(self.button)
            
            widget.setLayout(vbox)
            self.setCentralWidget(widget)
            
            return 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubeStatisticsApp()
    ex.resize(300, 300)
    ex.show()
    sys.exit(app.exec_())
