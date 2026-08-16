import tkinter as tk
from tkinter import messagebox
import socket
import threading

APP_NAME = "Kasim USB"
DEFAULT_PORT = 32038

server_socket = None
running = False


def get_local_ip():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except Exception:
        return "127.0.0.1"


def start_server():
    global server_socket, running

    if running:
        return

    try:
        port = int(port_entry.get())

        if not 1 <= port <= 65535:
            raise ValueError

        ip = get_local_ip()

        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        server_socket.bind(("0.0.0.0", port))
        server_socket.listen(5)

        running = True

        ip_value.config(text=ip)
        port_value.config(text=str(port))

        status_label.config(
            text="● Server Running",
            fg="#16a34a"
        )

        start_button.config(state="disabled")
        stop_button.config(state="normal")

        threading.Thread(
            target=accept_connections,
            daemon=True
        ).start()

    except ValueError:
        messagebox.showerror(
            "Kasim USB",
            "Please enter a valid port number."
        )

    except Exception as error:
        messagebox.showerror(
            "Kasim USB",
            "Server start failed:\n" + str(error)
        )


def accept_connections():
    while running:
        try:
            client, address = server_socket.accept()
            client.close()
        except Exception:
            break


def stop_server():
    global server_socket, running

    running = False

    try:
        if server_socket:
            server_socket.close()
    except Exception:
        pass

    server_socket = None

    status_label.config(
        text="● Server Stopped",
        fg="#dc2626"
    )

    start_button.config(state="normal")
    stop_button.config(state="disabled")


def copy_ip():
    ip = ip_value.cget("text")

    if ip != "---":
        root.clipboard_clear()
        root.clipboard_append(ip)
        root.update()

        status_label.config(
            text="✓ IP Address Copied",
            fg="#2563eb"
        )


def copy_port():
    port = port_value.cget("text")

    if port != "---":
        root.clipboard_clear()
        root.clipboard_append(port)
        root.update()

        status_label.config(
            text="✓ Port Number Copied",
            fg="#2563eb"
        )


def on_close():
    stop_server()
    root.destroy()


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title(APP_NAME)
root.geometry("460x500")
root.resizable(False, False)
root.configure(bg="#f4f6f8")


# =========================
# HEADER
# =========================

header = tk.Frame(
    root,
    bg="#111827",
    height=90
)

header.pack(fill="x")


title = tk.Label(
    header,
    text="KASIM USB",
    font=("Segoe UI", 24, "bold"),
    fg="white",
    bg="#111827"
)

title.pack(pady=(20, 0))


subtitle = tk.Label(
    header,
    text="USB Port Redirector",
    font=("Segoe UI", 10),
    fg="#cbd5e1",
    bg="#111827"
)

subtitle.pack()


# =========================
# MAIN AREA
# =========================

main = tk.Frame(
    root,
    bg="#f4f6f8"
)

main.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=25
)


# =========================
# IP ADDRESS
# =========================

tk.Label(
    main,
    text="IP ADDRESS",
    font=("Segoe UI", 10, "bold"),
    bg="#f4f6f8",
    fg="#475569"
).pack(anchor="w")


ip_frame = tk.Frame(
    main,
    bg="white",
    highlightbackground="#d1d5db",
    highlightthickness=1
)

ip_frame.pack(
    fill="x",
    pady=(5, 18)
)


ip_value = tk.Label(
    ip_frame,
    text="---",
    font=("Consolas", 16, "bold"),
    bg="white",
    fg="#111827"
)

ip_value.pack(
    side="left",
    padx=15,
    pady=12
)


copy_ip_button = tk.Button(
    ip_frame,
    text="COPY IP",
    command=copy_ip,
    font=("Segoe UI", 9, "bold"),
    bg="#e5e7eb",
    fg="#111827",
    relief="flat",
    cursor="hand2"
)

copy_ip_button.pack(
    side="right",
    padx=10,
    pady=8
)


# =========================
# PORT
# =========================

tk.Label(
    main,
    text="PORT NUMBER",
    font=("Segoe UI", 10, "bold"),
    bg="#f4f6f8",
    fg="#475569"
).pack(anchor="w")


port_frame = tk.Frame(
    main,
    bg="white",
    highlightbackground="#d1d5db",
    highlightthickness=1
)

port_frame.pack(
    fill="x",
    pady=(5, 18)
)


port_entry = tk.Entry(
    port_frame,
    font=("Consolas", 15, "bold"),
    relief="flat",
    bg="white",
    fg="#111827"
)

port_entry.insert(
    0,
    str(DEFAULT_PORT)
)

port_entry.pack(
    side="left",
    padx=15,
    pady=10,
    fill="x",
    expand=True
)


port_value = tk.Label(
    port_frame,
    text="---",
    font=("Consolas", 15, "bold"),
    bg="white",
    fg="#111827"
)

port_value.pack(
    side="left",
    padx=10
)


copy_port_button = tk.Button(
    port_frame,
    text="COPY",
    command=copy_port,
    font=("Segoe UI", 9, "bold"),
    bg="#e5e7eb",
    fg="#111827",
    relief="flat",
    cursor="hand2"
)

copy_port_button.pack(
    side="right",
    padx=10,
    pady=8
)


# =========================
# START BUTTON
# =========================

start_button = tk.Button(
    main,
    text="START SERVER",
    command=start_server,
    font=("Segoe UI", 12, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    height=2
)

start_button.pack(
    fill="x",
    pady=(5, 10)
)


# =========================
# STOP BUTTON
# =========================

stop_button = tk.Button(
    main,
    text="STOP SERVER",
    command=stop_server,
    font=("Segoe UI", 11, "bold"),
    bg="#e5e7eb",
    fg="#374151",
    relief="flat",
    cursor="hand2",
    state="disabled",
    height=2
)

stop_button.pack(
    fill="x"
)


# =========================
# STATUS
# =========================

status_label = tk.Label(
    main,
    text="● Server Stopped",
    font=("Segoe UI", 10, "bold"),
    bg="#f4f6f8",
    fg="#dc2626"
)

status_label.pack(
    pady=18
)


root.protocol(
    "WM_DELETE_WINDOW",
    on_close
)

root.mainloop()
