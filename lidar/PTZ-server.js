const express = require('express');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);
const raspivid = require('raspivid');
const Gpio = require('onoff').Gpio;
const fs = require('fs');

// Set up PTZ module GPIO pins
const up = new Gpio(17, 'out');
const down = new Gpio(22, 'out');
const leftRight = new Gpio(23, 'out');

// Set up camera
const camera = new raspivid({
  width: 640,
  height: 480,
  framerate: 30,
  bitrate: 1000000,
  timeout: 0
});

// Stream video from camera
app.get('/stream', (req, res) => {
  camera.pipe(res);
});

// Set up socket.io connection for PTZ control and recording
io.on('connection', (socket) => {
  console.log('Client connected');

  // PTZ control
  socket.on('move', (direction) => {
    switch (direction) {
      case 'up':
        up.writeSync(1);
        setTimeout(() => {
          up.writeSync(0);
        }, 500);
        break;
      case 'down':
        down.writeSync(1);
        setTimeout(() => {
          down.writeSync(0);
        }, 500);
        break;
      case 'left':
        leftRight.writeSync(1);
        setTimeout(() => {
          leftRight.writeSync(0);
        }, 500);
        break;
      case 'right':
        leftRight.writeSync(0);
        setTimeout(() => {
          leftRight.writeSync(1);
        }, 500);
        break;
    }
  });

  // Recording
  let recording = false;
  let videoStream;
  socket.on('record', () => {
    if (!recording) {
      recording = true;
      videoStream = fs.createWriteStream(`video-${Date.now()}.h264`);
      camera.pipe(videoStream);
    } else {
      recording = false;
      camera.unpipe(videoStream);
      videoStream.end();
    }
  });

  // Still image
  socket.on('still', () => {
    const stillImage = fs.createWriteStream(`image-${Date.now()}.jpg`);
    camera.once('data', (data) => {
      stillImage.write(data);
      stillImage.end();
    });
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

// Serve index.html
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// Start server
server.listen(3000, () => {
  console.log('Server listening on port 3000');
});
