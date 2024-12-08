from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# In-memory store for tasks
tasks = []

class ToDoHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':  # Handle root path
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Welcome to the To-Do App</h1><p>Use the following endpoints:</p><ul><li><b>GET /tasks</b>: View tasks</li><li><b>POST /tasks</b>: Add a task</li><li><b>DELETE /tasks/&lt;id&gt;</b>: Delete a task</li></ul>")
        elif self.path == '/tasks':  # Handle /tasks path
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(tasks).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_data = json.loads(post_data.decode('utf-8'))

            # Add new task to the list
            task = task_data.get("task")
            if task:
                tasks.append({"task": task})
                self.send_response(201)
                self.end_headers()
                self.wfile.write(b'Task added successfully')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing task description')

    def do_DELETE(self):
        if self.path.startswith('/tasks/'):
            try:
                task_id = int(self.path.split('/')[-1])
                if 0 <= task_id < len(tasks):
                    tasks.pop(task_id)
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'Task deleted successfully')
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'Task not found')
            except ValueError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid task ID')
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=ToDoHTTPRequestHandler, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
