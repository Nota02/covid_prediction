# COVID-19 Prediction App

**Приложение для прогноза новых случаев COVID-19 по странам и датам.**  
Бэкенд (FastAPI) и фронтенд (Streamlit).

---

### 1. Backend (FastAPI, отдельный сервер)

> Требования: Python 3.11+, pip, venv, права sudo

#### Установка и запуск 

1) git clone https://github.com/Nota02/covid_prediction.git
2) cd covid_prediction
3) python3 -m venv venv
4) source venv/bin/activate
5) pip install -r requirements.txt
6) model.pkl должен быть загружен отдельно - https://drive.google.com/file/d/1_EMmoB2qwy-tAM_n-MrkgM6CMarRqmOq/view?usp=drive_link 
7) uvicorn main:app --host 0.0.0.0 --port 8000 - ручной запуск

Автоматический Запуск
1) Перенесите файл covid_api.service в /etc/systemd/system/covid_api.service 
2) sudo systemctl daemon-reload
3) sudo systemctl start covid_api
4) sudo systemctl enable covid_api
5) sudo systemctl status covid_api

### 2. Frontend (Streamlit)
--------------
Локальный запуск
--------------
1) git clone https://github.com/Nota02/covid_prediction.git
2) cd covid_prediction
3) Необходимо изменить адрес api сервера в файле app.py
4) pip install -r requirements.txt
5) streamlit run app.py
--------------
Облачный запуск (Streamlit Cloud)
--------------
1) Перейдите на streamlit.io/cloud, подключите свой репозиторий.
2) Укажите файл запуска: app.py

### 3. Использование
1) Откройте Streamlit (например, https://covidprediction-m4rggztwkk2heax32nq6md.streamlit.app/)
2) Выберите страну и дату для прогноза.
3) Нажмите "Предсказать и показать на карте".
4) Прогноз появится, точка отобразится на карте.



