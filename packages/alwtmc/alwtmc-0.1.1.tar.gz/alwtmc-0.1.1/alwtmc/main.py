import os.path
import sys

from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import QTimer, QThreadPool, QRunnable, pyqtSignal, QObject
import subprocess
import shlex
import json

class Signals(QObject):
    output = pyqtSignal(str, str)

class ALWTMC(QMainWindow):
    def __init__(self):
        super().__init__()

        if not os.path.exists("config.json"):
            print("Need config.json in the current directory")
            sys.exit(-1)

        self.jobs = self.read_jobs_from_config('config.json')

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('ALWTMC')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.job_widgets = {}
        for job in self.jobs:
            job_label = QLabel(f'{job["job_name"]}')
            job_label.setFont(QFont("Arial", 8))
            job_status_label = QLabel(f'Refresh Interval: {job["refresh_interval"]}, Remaining: {job["refresh_interval"]}')
            job_status_label.setFont(QFont("Arial", 6))
            job_output = QTextEdit()


            if 'output_height' in job:
                font_metrics = QFontMetrics(job_output.font())
                linespace = font_metrics.lineSpacing() * int(job['output_height'])
                job_output.setMaximumHeight(linespace)

            self.job_widgets[job["job_name"]] = {"label": job_label, "status_label": job_status_label, "output": job_output}
            layout2 = QHBoxLayout()
            layout2.addWidget(job_label)
            layout2.addWidget(job_status_label)

            widget1 = QWidget()
            widget1.setLayout(layout2)

            layout3 = QVBoxLayout()
            layout3.setContentsMargins(0, 0, 0, 0)  # Remove any margins
            layout3.addWidget(widget1)
            layout3.addWidget(job_output)

            card_widget = QWidget()  # This will be our "card"
            card_widget.setLayout(layout3)

            self.layout.addWidget(card_widget)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stopTimer)

        self.layout.addWidget(self.stop_button)

        self.timer = QTimer()
        self.timer.timeout.connect(self.refreshOutput)
        self.timer.start(1000)

        self.thread_pool = QThreadPool()

        self.refreshOutput()

    def read_jobs_from_config(self, filename):
        with open(filename, 'r') as f:
            config = json.load(f)
            return config['jobs']

    def refreshOutput(self):
        worker = RefreshWorker(self.jobs)
        worker.signals.output.connect(self.updateJobOutput)
        self.thread_pool.start(worker)

        for job in self.jobs:
            remaining = int(self.job_widgets[job["job_name"]]["status_label"].text().split(':')[-1].strip())
            if remaining > 0:
                self.job_widgets[job["job_name"]]["status_label"].setText(self.job_widgets[job["job_name"]]["status_label"].text().split(':')[0] + f': {job["refresh_interval"]}, Remaining: {remaining - 1}')
            else:
                self.job_widgets[job["job_name"]]["status_label"].setText(self.job_widgets[job["job_name"]]["status_label"].text().split(':')[0] + f': {job["refresh_interval"]}, Remaining: {job["refresh_interval"]}')

    def updateJobOutput(self, job_name, output):
        self.job_widgets[job_name]["output"].setPlainText(output)

    def stopTimer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.stop_button.setText('Resume')
        else:
            self.timer.start(1000)
            self.stop_button.setText('Stop')


class RefreshWorker(QRunnable):
    def __init__(self, jobs):
        super().__init__()
        self.jobs = jobs
        self.signals = Signals()

    def run(self):
        for job in self.jobs:
            try:
                output = subprocess.check_output(shlex.split(job["command"]), universal_newlines=True)
                self.signals.output.emit(job["job_name"], output)
            except subprocess.CalledProcessError as e:
                print(e)


def main():
    app = QApplication(sys.argv)
    ex = ALWTMC()
    ex.show()
    sys.exit(app.exec_())