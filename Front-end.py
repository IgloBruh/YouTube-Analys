import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QLineEdit, QWidget, QTextBrowser, QMessageBox, QTextEdit
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
            # Создаем YouTube Data API клиент
            api_key = 'AIzaSyBHouVubyJV00ehrCoGSFGoyIxGZjl4pFA'
            youtube = build('youtube', 'v3', developerKey=api_key)

            # Получаем статистику канала
            response = youtube.channels().list(
                part='statistics',
                id=channel_id
            ).execute()
            # Получаем количество подписок и сумму просмотров
            sub_count = response['items'][0]['statistics']['subscriberCount']
            view_count = response['items'][0]['statistics']['viewCount']
            
            # Получаем среднее количество просмотров
            video_response = youtube.videos().list(
                part='statistics',
                chart='mostPopular',
                maxResults=10
            ).execute()

            total_views = 0
            total_likes = 0
            most_viewed_videos = []
            
            # Получаем список видео канала
            video_response = youtube.search().list(
                part='id',
                channelId=channel_id,
                maxResults=10
            ).execute()

            # Получаем статистику для каждого видео
            for item in video_response.get('items', []):
                if 'videoId' in item['id']:
                    video_id = item['id']['videoId']
                    video_info = youtube.videos().list(
                        part='statistics, snippet',
                        id=video_id
                    ).execute()
                    if video_info.get('items'):
                        title = video_info['items'][0]['snippet']['title']
                        views = video_info['items'][0]['statistics']['viewCount']
                        likes = video_info['items'][0]['statistics']['likeCount']
                        most_viewed_videos.append(title)
                        total_views += int(views)
                        total_likes += int(likes)

            average_views = total_views / len(video_response.get('items', []))
            
            video_ids = []
            video_views = []
            for item in video_response.get('items', []):
                if 'videoId' in item['id']:
                    video_info = youtube.videos().list(
                        part='statistics, snippet',
                        id=item['id']['videoId']
                    ).execute()
                    video_ids.append(video_info['items'][0]['snippet']['title'])
                    if video_info.get('items'):
                        views = video_info['items'][0]['statistics']['viewCount']
                        video_views.append(views)

            # Create a bar graph
            plt.title('Views of the Last 10 Videos')
            plt.xlabel('Video ID')
            plt.ylabel('Views')
            plt.plot(video_ids, video_views, marker='o', markersize=7)
            plt.show()
            
            # Выводим результаты
            vbox.addWidget(QLabel(f'Количество подписок: {sub_count}'))
            vbox.addWidget(QLabel(f'Среднее количество просмотров: {average_views}'))
            vbox.addWidget(QLabel(f'Сумма просмотров: {total_views}'))
            vbox.addWidget(QLabel(f'Сумма лайков: {total_likes}'))
            vbox.addWidget(QLabel('Самые просматриваемые видео:'))
            for video in most_viewed_videos:
                vbox.addWidget(QLabel(video))
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
    ex.resize(500, 500)
    ex.show()
    sys.exit(app.exec_())
