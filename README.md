# Air Quality Tiantan Station Dashboard ✨

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app in local
```
edit dashboard.py
change pd.read_csv("dashboard/main_data.csv") to pd.read_csv("main_data.csv")
save
streamlit run dashboard.py
```

## Run steamlit app
```
streamlit run dashboard.py
```
