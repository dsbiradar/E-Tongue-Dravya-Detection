import os
import time
import joblib
import serial
import threading
import numpy as np
import serial.tools.list_ports

from datetime import datetime
from collections import deque
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)
app.config["SECRET_KEY"] = "etongue_liquid_secret"

# Explicitly configure python-engineio with threading mode (avoiding eventlet)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading",
    ping_timeout=20,
    ping_interval=25,
    always_connect=True
)

SERIAL_PORT = "COM3"
BAUD_RATE = 9600
TIMEOUT = 1

serial_conn = None
serial_thread = None
is_reading = False
connection_status = False
reading_history = deque(maxlen=50)

DRAVYA_INFO = {
    "Aloevera": {
        "color": "#22c55e",
        "sanskrit": "Kumari",
        "taste": "Mild Bitter",
        "property": "Cooling, Soothing",
        "use": "Digestion, Skin care, General wellness",
        "rasa": "Tikta, Madhura",
        "guna": "Snigdha, Sara"
    },
    "Amla": {
        "color": "#84cc16",
        "sanskrit": "Amalaki",
        "taste": "Sour-Astringent",
        "property": "Antioxidant, Rejuvenating",
        "use": "Immunity, Digestion, Vitamin C support",
        "rasa": "Amla, Kashaya",
        "guna": "Laghu, Ruksha"
    },
    "Giloy": {
        "color": "#0ea5e9",
        "sanskrit": "Guduchi",
        "taste": "Bitter",
        "property": "Immunity Support, Antipyretic",
        "use": "Fever, Immunity, General weakness",
        "rasa": "Tikta, Kashaya",
        "guna": "Laghu, Snigdha"
    }
}


def load_model():
    model_path = os.path.join(BASE_DIR, "best_dravya_model.pkl")
    dataset_path = os.path.join(BASE_DIR, "real_dravya_dataset.csv")
    try:
        m = joblib.load(model_path)
        print("Model loaded:", model_path)
        if hasattr(m, "classes_"):
            print("Model classes:", list(m.classes_))
        return m
    except Exception as e:
        print("Model load error:", e)
        if os.path.exists(dataset_path):
            print("Auto-training model from dataset to resolve version mismatch...")
            try:
                import pandas as pd
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.model_selection import train_test_split

                df = pd.read_csv(dataset_path)
                X = df[["pH", "TDS", "EC"]]
                y = df["Label"]
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42, stratify=y
                )
                m = RandomForestClassifier(n_estimators=200, random_state=42)
                m.fit(X_train, y_train)
                joblib.dump(m, model_path)
                print("Model auto-trained and saved to:", model_path)
                return m
            except Exception as train_err:
                print("Auto-training failed:", train_err)
                return None
        return None


model = load_model()


def emit_status(connected, message):
    socketio.emit("connection_status", {
        "connected": connected,
        "port": SERIAL_PORT,
        "baud": BAUD_RATE,
        "message": message
    })


def parse_serial_line(line: str):
    line = line.strip()
    if not line:
        return None

    parts = line.split(",")
    if len(parts) < 3:
        return None

    try:
        pH = float(parts[0].strip())
        TDS = float(parts[1].strip())
        EC = float(parts[2].strip())

        if 0 < pH < 14 and 0 <= TDS < 10000 and 0 <= EC < 10000:
            return pH, TDS, EC
    except ValueError:
        return None

    return None


def predict_dravya(pH: float, TDS: float, EC: float):
    global model
    if model is None:
        model = load_model()
        if model is None:
            return None

    try:
        import pandas as pd
        x = pd.DataFrame([[pH, TDS, EC]], columns=["pH", "TDS", "EC"])
    except Exception:
        x = np.array([[pH, TDS, EC]])

    pred = model.predict(x)[0]

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(x)[0]
        classes = list(model.classes_)
        prob_dict = {cls: round(float(p) * 100, 2) for cls, p in zip(classes, probs)}
        confidence = round(float(max(probs)) * 100, 2)
    else:
        classes = list(model.classes_) if hasattr(model, "classes_") else [pred]
        prob_dict = {cls: 0.0 for cls in classes}
        prob_dict[pred] = 100.0
        confidence = 100.0

    info = DRAVYA_INFO.get(pred, {
        "color": "#64748b",
        "sanskrit": "-",
        "taste": "-",
        "property": "-",
        "use": "-",
        "rasa": "-",
        "guna": "-"
    })

    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "pH": round(pH, 2),
        "TDS": round(TDS, 2),
        "EC": round(EC, 2),
        "prediction": pred,
        "confidence": confidence,
        "probabilities": prob_dict,
        "info": info
    }


def serial_reader():
    global serial_conn, is_reading, connection_status

    print(f"Connecting to {SERIAL_PORT} @ {BAUD_RATE}...")
    try:
        serial_conn = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        time.sleep(2)
        serial_conn.reset_input_buffer()

        connection_status = True
        print("Connected to serial port")
        emit_status(True, f"Connected to {SERIAL_PORT} @ {BAUD_RATE}")

        while is_reading:
            try:
                raw = serial_conn.readline()
                if not raw:
                    continue

                line = raw.decode("utf-8", errors="ignore").strip()
                if not line:
                    continue

                print("RAW:", repr(line))
                parsed = parse_serial_line(line)

                if parsed:
                    pH, TDS, EC = parsed
                    print("PARSED:", pH, TDS, EC)
                    result = predict_dravya(pH, TDS, EC)

                    if result:
                        reading_history.appendleft(result)
                        socketio.emit("new_reading", result)
                        emit_status(True, "Receiving continuous data")
                        print("PREDICTED:", result["prediction"], result["confidence"])
                else:
                    print("UNPARSED:", repr(line))
                    socketio.emit("serial_log", {
                        "line": line,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })

            except serial.SerialException as e:
                print("Serial read error:", e)
                emit_status(False, f"Read error: {str(e)}")
                break
            except Exception as e:
                print("Serial loop error:", e)
                socketio.emit("error", {"message": str(e)})
                time.sleep(0.05)

    except serial.SerialException as e:
        print("Cannot open serial:", e)
        emit_status(False, f"Cannot open {SERIAL_PORT}: {str(e)}")

    finally:
        try:
            if serial_conn and serial_conn.is_open:
                serial_conn.close()
        except Exception:
            pass

        serial_conn = None
        connection_status = False
        is_reading = False
        print("Serial connection closed")
        emit_status(False, "Serial connection closed")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/status")
def api_status():
    ports = [p.device for p in serial.tools.list_ports.comports()]
    return jsonify({
        "connected": connection_status,
        "is_reading": is_reading,
        "port": SERIAL_PORT,
        "baud": BAUD_RATE,
        "available_ports": ports,
        "history_count": len(reading_history),
        "model_loaded": model is not None,
        "model_classes": list(model.classes_) if model is not None and hasattr(model, "classes_") else []
    })


@app.route("/api/history")
def api_history():
    return jsonify({"history": list(reading_history), "count": len(reading_history)})


@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        data = request.get_json() or {}
        pH = float(data.get("pH", 7.0))
        TDS = float(data.get("TDS", 600.0))
        EC = float(data.get("EC", 50.0))

        result = predict_dravya(pH, TDS, EC)
        if result:
            reading_history.appendleft(result)
            socketio.emit("new_reading", result)
            return jsonify({"success": True, "result": result})

        return jsonify({"success": False, "error": "Prediction failed"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/clear_history", methods=["POST"])
def api_clear_history():
    reading_history.clear()
    socketio.emit("history_cleared", {})
    return jsonify({"success": True})


@app.route("/api/start_serial", methods=["POST"])
def api_start_serial():
    global serial_thread, is_reading
    if not is_reading:
        is_reading = True
        serial_thread = threading.Thread(target=serial_reader, daemon=True)
        serial_thread.start()
        socketio.emit("serial_control", {"status": "started"})
        return jsonify({"success": True, "status": "started"})
    return jsonify({"success": True, "status": "already_running"})


@app.route("/api/stop_serial", methods=["POST"])
def api_stop_serial():
    global is_reading, serial_conn
    is_reading = False
    try:
        if serial_conn and serial_conn.is_open:
            serial_conn.close()
    except Exception:
        pass
    socketio.emit("serial_control", {"status": "stopped"})
    return jsonify({"success": True, "status": "stopped"})


@socketio.on("connect")
def on_connect():
    print("Client connected")
    emit("connection_status", {
        "connected": connection_status,
        "port": SERIAL_PORT,
        "baud": BAUD_RATE,
        "message": "Connected to server"
    })
    emit("history_data", {"history": list(reading_history)})
    emit("model_info", {
        "loaded": model is not None,
        "classes": list(model.classes_) if model is not None and hasattr(model, "classes_") else []
    })


@socketio.on("disconnect")
def on_disconnect():
    print("Client disconnected")


@socketio.on("start_serial")
def on_start_serial():
    global serial_thread, is_reading
    print("START_SERIAL event received")

    if not is_reading:
        is_reading = True
        serial_thread = threading.Thread(target=serial_reader, daemon=True)
        serial_thread.start()
        emit("serial_control", {"status": "started"})
        print("Serial thread started")
    else:
        emit("serial_control", {"status": "already_running"})
        print("Serial already running")


@socketio.on("stop_serial")
def on_stop_serial():
    global is_reading, serial_conn
    print("STOP_SERIAL event received")
    is_reading = False

    try:
        if serial_conn and serial_conn.is_open:
            serial_conn.close()
    except Exception:
        pass

    emit("serial_control", {"status": "stopped"})


@socketio.on("manual_predict")
def on_manual_predict(data):
    try:
        pH = float(data.get("pH", 7.0))
        TDS = float(data.get("TDS", 600.0))
        EC = float(data.get("EC", 50.0))

        result = predict_dravya(pH, TDS, EC)
        if result:
            reading_history.appendleft(result)
            socketio.emit("new_reading", result)
        else:
            emit("error", {"message": "Prediction failed"})
    except Exception as e:
        emit("error", {"message": str(e)})


def free_port(port: int):
    """
    Terminates any lingering background process holding the port on Windows,
    so restarting the app never fails with 'address already in use'.
    """
    import subprocess
    current_pid = os.getpid()
    try:
        res = subprocess.run("netstat -ano", shell=True, capture_output=True, text=True)
        pids = set()
        for line in res.stdout.splitlines():
            line = line.strip()
            if f":{port}" in line and "LISTENING" in line:
                parts = line.split()
                if len(parts) >= 5:
                    try:
                        pid = int(parts[-1])
                        if pid > 0 and pid != current_pid:
                            pids.add(pid)
                    except ValueError:
                        pass
        for pid in pids:
            print(f"[Port Manager] Freeing port {port} from background process (PID: {pid})...")
            subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True)
        if pids:
            time.sleep(1)
    except Exception:
        pass


def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def get_available_port(preferred_port: int = 5000, max_tries: int = 10) -> int:
    free_port(preferred_port)
    if not is_port_in_use(preferred_port):
        return preferred_port

    for p in range(preferred_port + 1, preferred_port + max_tries):
        free_port(p)
        if not is_port_in_use(p):
            print(f"[Port Manager] Preferred port {preferred_port} unavailable, using port {p}")
            return p
    return preferred_port


if __name__ == "__main__":
    PORT = get_available_port(5000)

    print("=" * 60)
    print(" E-Tongue Liquid Detection System")
    print("=" * 60)
    print(f" Serial Port : {SERIAL_PORT}")
    print(f" Baud Rate   : {BAUD_RATE}")
    print(f" Model Path  : {os.path.join(BASE_DIR, 'best_dravya_model.pkl')}")
    print(f" Index URL   : http://127.0.0.1:{PORT}")
    print(f" Dashboard   : http://127.0.0.1:{PORT}/dashboard")
    print("=" * 60)

    try:
        socketio.run(
            app,
            host="0.0.0.0",
            port=PORT,
            debug=False,
            use_reloader=False,
            allow_unsafe_werkzeug=True
        )
    except OSError as e:
        if "10048" in str(e) or "Address already in use" in str(e):
            print(f"\n[Port Manager] Port {PORT} still busy. Freeing and retrying...")
            free_port(PORT)
            socketio.run(
                app,
                host="0.0.0.0",
                port=PORT,
                debug=False,
                use_reloader=False,
                allow_unsafe_werkzeug=True
            )
        else:
            raise e