from flask import Flask, render_template, request, jsonify
import json
import subprocess
import socket
import os
import threading
import psutil

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    port = s.getsockname()[1]
    s.close()
    return port

app = Flask(__name__)

JSON_FILE_PATH = 'unix.json'

def is_process_running(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            return proc
    return None

def kill_process(proc):
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except psutil.TimeoutExpired:
        proc.kill()

def restart_index_exe():
    proc = is_process_running('index.exe')
    if proc:
        kill_process(proc)
    subprocess.Popen(['./index.exe'])

@app.route('/start', methods=['POST'])
def start_program():
    restart_index_exe()
    return jsonify({'message': 'Program restarted successfully'})

@app.route('/stop', methods=['POST'])
def start_program1():
    file_path = 'app.aa'

    try:
        os.remove(file_path)
        print(f"Файл '{file_path}' успішно видалено.")
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено.")
    except PermissionError:
        print(f"Немає прав для видалення файлу '{file_path}'.")
    except Exception as e:
        print(f"Виникла помилка при видаленні файлу '{file_path}': {e}")

    return jsonify({'message': 'Program restarted successfully'})

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/c')
def index1():
    return render_template('index.html')

@app.route('/add_data', methods=['POST'])
def add_data():
    key = request.form['key']
    value = request.form['value']

    key = key.encode('utf-8', 'ignore').decode('utf-8')
    value = value.encode('utf-8', 'ignore').decode('utf-8')

    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)

    data[key] = value

    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return jsonify({'message': 'Data added successfully'})

@app.route('/get_data', methods=['GET'])
def get_data():
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return jsonify(data)

@app.route('/delete_data', methods=['POST'])
def delete_data():
    key = request.json['key']

    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if key in data:
        del data[key]

        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return jsonify({'message': f'Data with key {key} deleted successfully'})
    else:
        return jsonify({'message': f'Key {key} not found'})

def run_flask_app(port):
    app.run(port=port)

def run_exe():
    subprocess.run(['./ACWA.exe'])

if __name__ == '__main__':
    port = find_free_port()

    content = f'''name = Hot keys
window_h = 800
window_w = 1000
html = <style>iframe{{position: fixed;height: 100%;width: 100%;top: 0%;left: 0%;}}</style><iframe src="http://127.0.0.1:{port}" frameborder="0"></iframe>
'''

    with open('start.article', 'w', encoding='utf-8') as file:
        file.write(content)

    try:
        flask_thread = threading.Thread(target=run_flask_app, args=(port,))
        flask_thread.start()

        run_exe()

    finally:
        os._exit(0)
