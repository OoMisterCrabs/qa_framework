## 1️ Install dependencies

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## 2️ Launch tests

```bash
python -m pytest tests/ -v
```

## 3️ Launch tests with Allure report

```bash
python -m pytest tests/ -v --alluredir=allure-results
allure serve allure-results
```

## 4️ Launch tests headed (with browser UI)

```bash
python -m pytest tests/ -v --headed
```

## 5️ Relaunch failed tests

```bash
pip install pytest-rerunfailures
python -m pytest tests/ --reruns 2 -v --alluredir=allure-results
```