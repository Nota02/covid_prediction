# COVID-19 Prediction App

**Приложение для прогноза новых случаев COVID-19 по странам и датам.**  
Бэкенд (FastAPI) и фронтенд (Streamlit).

---

### 1. Backend (FastAPI, отдельный сервер)

> Требования: Python 3.11+, pip, venv, права sudo

#### Установка и запуск 

git clone https://github.com/Nota02/covid_prediction.git
cd covid_prediction
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# model.pkl должен быть загружен отдельно - https://drive.google.com/file/d/1_EMmoB2qwy-tAM_n-MrkgM6CMarRqmOq/view?usp=drive_link 
uvicorn main:app --host 0.0.0.0 --port 8000

Создайте файл /etc/systemd/system/covid_api.service
[Unit]
Description=COVID Prediction FastAPI service
After=network.target

[Service]
User=nota                        # <-- пользователь Linux
Group=nota                       # <-- группа
WorkingDirectory=/home/nota/covid_prediction   # <-- путь к проекту!
Environment="PATH=/home/nota/covid_prediction/venv/bin"
ExecStart=/home/nota/covid_prediction/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

###Запуск
sudo systemctl daemon-reload
sudo systemctl start covid_api
sudo systemctl enable covid_api
sudo systemctl status covid_api

### 2. Frontend (Streamlit)
--------------
Локальный запуск
--------------
git clone https://github.com/Nota02/covid_prediction.git
cd covid_prediction
Необходимо изменить адрес api сервера в файле app.py
pip install -r requirements.txt
streamlit run app.py
--------------
Облачный запуск (Streamlit Cloud)
--------------
Перейдите на streamlit.io/cloud, подключите свой репозиторий.
Укажи файл запуска: app.py

### 3. Использование
1) Откройте Streamlit (например, https://covidprediction-m4rggztwkk2heax32nq6md.streamlit.app/)
2) Выберите страну и дату для прогноза.
3) Нажмите "Предсказать и показать на карте".
4) Прогноз появится, точка отобразится на карте.



