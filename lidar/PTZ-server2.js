const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);
const spawn = require('child_process').spawn;
const Gpio = require('onoff').Gpio;
const fs = require('fs');

// Set up PTZ module control pins
const panPin = new Gpio(17, 'out');
const tiltPin = new Gpio(23, 'out');
const zoomPin = new Gpio(24, 'out');

// Set up video streaming
let videoStream;
let isRecording = false;
let isStreaming = false;

// Set up still image capture
let stillImageCapture;

// Start video streaming
function startStreaming() {
  if (!isStreaming) {
    isStreaming = true;
    videoStream = spawn('raspivid', ['-o', '-', '-t', '0', '-w', '640', '-h', '480', '-fps', '30']);
    videoStream.stdout.on('data', (data) => {
      io.emit('video', data);
    });
  }
}

// Stop video streaming
function stopStreaming() {
  if (isStreaming) {
    isStreaming = false;
    videoStream.kill();
  }
}

// Start recording
function startRecording() {
  if (!isRecording) {
    isRecording = true;
    const recordStream = spawn('raspivid', ['-o', 'record.h264', '-t', '0', '-w', '640', '-h', '480', '-fps', '30']);
    recordStream.stdout.on('data', (data) => {
      fs.appendFile('record.h264', data, (err) => {
        if (err) {
          console.log(err);
        }
      });
    });
  }
}

// Stop recording
function stopRecording() {
  if (isRecording) {
    isRecording = false;
    const recordStream = spawn('killall', ['raspivid']);
  }
}

// Take still image
function takeStillImage() {
  stillImageCapture = spawn('raspistill', ['-o', 'still.jpg', '-w', '640', '-h', '480']);
}

// PTZ module control
function controlPTZ(direction) {
  switch (direction) {
    case 'up':
      tiltPin.writeSync(1);
      break;
    case 'down':
      tiltPin.writeSync(0);
      break;
    case 'left':
      panPin.writeSync(1);
      break;
    case 'right':
      panPin.writeSync(0);
      break;
    case 'zoomIn':
      zoomPin.writeSync(1);
      break;
    case 'zoomOut':
      zoomPin.writeSync(0);
      break;
  }
}

// Set up socket.io connections
io.on('connection', (socket) => {
  console.log('Client connected');

  // Start video streaming when client connects
  startStreaming();

  // Handle client disconnection
  socket.on('disconnect', () => {
    console.log('Client disconnected');
    stopStreaming();
  });

  // Handle PTZ control
  socket.on('ptz', (direction) => {
    controlPTZ(direction);
  });

  // Handle recording
  socket.on('record', (action) => {
    if (action === 'start') {
      startRecording();
    } else if (action === 'stop') {
      stopRecording();
    }
  });

  // Handle still image capture
  socket.on('still', () => {
    takeStillImage();
  });
});

// Set up express routes
app.use(express.static(__dirname + '/public'));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// Start server
http.listen(3000, () => {
  console.log('Server listening on port 3000');
});

