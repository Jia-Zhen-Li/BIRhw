1.install pip packages
pip install -r requirements.txt

2. install chromium-chromedriver

- Ubuntu or Linux
  apt install chromium-chromedriver

- Windows
  a. go to the url: "https://chromedriver.chromium.org/getting-started" dowmload chromedriver
  b. then change the permission of chromedriver
     chmod 755 "chromedriver"

3.run on the server
python manage.py runserver
