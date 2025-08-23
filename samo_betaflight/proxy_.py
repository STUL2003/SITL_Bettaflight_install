#!/usr/bin/env python3
import socket
import threading
import argparse
import time

class Forward:
    def __init__(self, host, port, listen_host='127.0.0.1', listen_port=5765):
        self.host = host
        self.port = port
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.backend_sock = None
        self.frontends = []  
        self.lock = threading.Lock()
        self.running = True

    def start(self):
        self._connect_backend()
        threading.Thread(target=self._backend_reader, daemon=True).start()
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((self.listen_host, self.listen_port))
        srv.listen(8)
        try:
            while self.running:
                try:
                    client, addr = srv.accept()
                except KeyboardInterrupt:
                    break
                with self.lock:
                    self.frontends.append(client)
                threading.Thread(target=self._frontend_handler, args=(client, addr), daemon=True).start()
        finally:
            self.shutdown()
            srv.close()

    def _connect_backend(self):
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5.0)
                s.connect((self.host, self.port))
                s.settimeout(None)
                self.backend_sock =s
                return
            except Exception as e:
                time.sleep(1.0)

    def _backend_reader(self):
        # read from backend and broadcast to frontends
        while self.running:
            if not self.backend_sock:
                self._connect_backend()
                continue
            try:
                data = self.backend_sock.recv(4096)
                if not data:
                    try:
                        self.backend_sock.close()
                    except:
                        pass
                    self.backend_sock = None
                    # notify frontends? for now just continue and reconnect
                    time.sleep(0.5)
                    continue
                # broadcast
                with self.lock:
                    to_remove = []
                    for f in self.frontends:
                        try:
                            f.sendall(data)
                        except Exception:
                            to_remove.append(f)
                    for r in to_remove:
                        try:
                            r.close()
                        except:
                            pass
                        if r in self.frontends: self.frontends.remove(r)
            except Exception as e:
                try:
                    self.backend_sock.close()
                except:
                    pass
                self.backend_sock = None
                time.sleep(0.5)

    def _frontend_handler(self, client, addr):

        while self.running:
            data = client.recv(4096)
            if not data:
                break
            # forward to backend (if connected)
            if self.backend_sock:
                try:
                    self.backend_sock.sendall(data)
                except Exception as e:
                    # try to reconnect backend
                    try:
                        self.backend_sock.close()
                    except:
                        pass
                    self.backend_sock = None
            else:
                # backend not connected; ignore or buffer (we ignore)
                pass
        

    def shutdown(self):
        self.running = False
        print("[MUX] shutting down")
        try:
            if self.backend_sock:
                self.backend_sock.close()
        except:
            pass
        with self.lock:
            for f in list(self.frontends):
                try:
                    f.close()
                except:
                    pass
            self.frontends.clear()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--backend-host", default="127.0.0.1")
    p.add_argument("--backend-port", type=int, default=5761)
    p.add_argument("--listen-host", default="127.0.0.1")
    p.add_argument("--listen-port", type=int, default=5765)
    args = p.parse_args()
    m = Forward(args.backend_host, args.backend_port, args.listen_host, args.listen_port)
    try:
        m.start()
    except KeyboardInterrupt:
        m.shutdown()