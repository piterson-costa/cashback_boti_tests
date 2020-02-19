virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
source venv/bin/activate
cd api
flask run

