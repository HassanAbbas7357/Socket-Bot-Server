const express = require("express");
const app = express();
const http = require("http");
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

// PORT
const PORT = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.send("SOkcetServer");
});

let bots = [];
let controllerClient;

let workingBots = [];
let beforeBots;

io.on("connection", (socket) => {
  socket.on("connected_bot", (bot_name) => {
    if (bot_name === "beforeBots") {
      beforeBots = {
        botName: bot_name,
        socketId: socket.id,
      };
    } else {
      let dic = {
        botName: bot_name,
        socketId: socket.id,
      };
      bots.push(dic);
    }
  });

  socket.on("connected_controllerClient", (controllerName) => {
    controllerClient = {
      botName: controllerName,
      socketId: socket.id,
    };
  });

  socket.on("start_bots", () => {
    io.to(beforeBots.socketId).emit("beforeBotsStart");
  });

  socket.on("beforeBotsStartCompleted", () => {
    console.log("starting bots");
    bots.map((x) => {
      io.to(x.socketId).emit("start_self", x);
    });
  });

  socket.on("start_self_ok", (data) => {
    workingBots.push(data);
    console.log("bot started working", data);
  });

  socket.on("task_completed", (data) => {
    workingBots = workingBots.filter((x) => {
      if (x.socketId !== data.socketId) {
        return x;
      }
    });
    if (workingBots.length == 0 || workingBots === {}) {
      io.to(controllerClient.socketId).emit("TasksCompletedSuccess", bots);
    }
  });

  socket.on("disconnect", () => {
    console.log("user disconnected");
  });
});

server.listen(PORT, () => {
  console.log(`listening on ${PORT}`);
});
