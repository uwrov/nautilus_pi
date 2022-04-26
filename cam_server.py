import socket
import time
import picamera

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('wb')
try:
    print("start recording")
    camera.start_recording(connection, format='h264')
except:
    print("stop recording - exception")
    connection.close()
    server_socket.close()
finally:
    print("stop recording - correct")
    connection.close()
    server_socket.close()
