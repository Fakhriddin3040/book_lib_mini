For running with docker, you need only docker and
network connection.

If you have this requirements, you can easily run
this program with docker, when you does not have
python.

Lest goeeee:
    1. Download this app, or clone it from git:
        git clone https://github.com/Fakhriddin3040/book_lib_mini.git
    2. Enter the directory on terminal.
    3. Run:
       1. docker compose build
       2. docker compose up -d
       3. docker compose exec -it app sh
       4. python3 main.py

Thats all.
If you want to stop docker services, just run
docker compose down.