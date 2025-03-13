import { useState, useRef, useEffect } from "react";
// import Header from './components/Header'
import VideoFeed from "./components/VideoFeed";
import Controls from "./components/Controls";
import Footer from "./components/Footer";
import "./App.css";
import io from "socket.io-client";

function App() {
  const [isRunning, setIsRunning] = useState(false);
  const [mode, setMode] = useState("cursor"); // 'cursor' or 'wheel'
  const [sensitivity, setSensitivity] = useState(5);
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const canvasRef = useRef(null);
  // const photoRef = useRef(null);
  const socketRef = useRef(null);

  // function simulateMouseMove(x, y) {
  //   let event = new MouseEvent("mousemove", {
  //     clientX: x,
  //     clientY: y,
  //     bubbles: true,
  //     cancelable: true,
  //     view: window,
  //   });
  //   document.dispatchEvent(event);
  // }

  // function moveCursor(action) {
  //   let step = 20; // Mức độ di chuyển chuột
  //   let cursorX = window.innerWidth / 2; // Vị trí hiện tại của chuột
  //   let cursorY = window.innerHeight / 2;

  //   switch (action) {
  //     case "move_left":
  //       cursorX -= step;
  //       break;
  //     case "move_right":
  //       cursorX += step;
  //       break;
  //     case "move_up":
  //       cursorY -= step;
  //       break;
  //     case "move_down":
  //       cursorY += step;
  //       break;
  //     case "stay":
  //     default:
  //       return; // Không di chuyển chuột
  //   }

  //   simulateMouseMove(cursorX, cursorY);
  // }

  // const setupVoiceRecognition = () => {
  //   const SpeechRecognition =
  //     window.SpeechRecognition || window.webkitSpeechRecognition;
  //   if (!SpeechRecognition) {
  //     console.error("Speech Recognition is not supported in this browser.");
  //     return;
  //   }

  //   const recognition = new SpeechRecognition();
  //   recognition.continuous = true;
  //   recognition.lang = "en-US";

  //   recognition.onresult = (event) => {
  //     const transcript = event.results[event.results.length - 1][0].transcript
  //       .trim()
  //       .toLowerCase();
  //     console.log("Voice Command:", transcript);

  //     if (transcript.includes("start camera")) {
  //       if (isRunning === false) toggleTracking();
  //     } else if (transcript.includes("stop camera")) {
  //       if (isRunning === true) toggleTracking();
  //     }
  //   };

  //   recognition.onerror = (event) => {
  //     console.error("Speech recognition error:", event.error);
  //   };

  //   recognition.start();
  // };

  const startWebcam = async () => {
    try {
      if (!socketRef.current) {
        socketRef.current = io.connect("http://127.0.0.1:5000");
        socketRef.current.on("connect", () => {
          console.log("Connected to the server", socketRef.current.connected);
        });
      }

      const canvas = canvasRef.current;
      const context = canvas.getContext("2d");
      const video = videoRef.current;
      video.width = 400;
      video.height = 300;

      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
      }

      const FPS = 10;
      setInterval(() => {
        const width = video.width;
        const height = video.height;
        context.drawImage(video, 0, 0, width, height);
        const data = canvas.toDataURL("image/jpeg", 0.5);
        context.clearRect(0, 0, width, height);
        socketRef.current.emit("image", { image: data, mode: mode });
      }, 1000 / FPS);

      socketRef.current.on("head_pose", function (data) {
        console.log(data.direction, data.mouse_action, data.mode);
        // moveCursor(data.mouse_action);
      });
    } catch (err) {
      console.error("Error accessing webcam:", err);
      alert(
        "Unable to access webcam. Please ensure you have granted permission."
      );
    }
  };

  const stopWebcam = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      if (videoRef.current) {
        videoRef.current.srcObject = null;
      }
      streamRef.current = null;
    }

    // Hủy WebSocket nếu có kết nối
    if (socketRef.current) {
      // clearInterval(socketRef.current.imageInterval); // Dừng gửi ảnh
      socketRef.current.disconnect();
      socketRef.current = null;
    }

    // Xóa bỏ tất cả các bộ đếm thời gian để tránh thực hiện setInterval không cần thiết
    const intervalId = window.setInterval(function () {},
    Number.MAX_SAFE_INTEGER);
    for (let i = 1; i <= intervalId; i++) {
      window.clearInterval(i);
    }

    // Reset canvas và photo về trạng thái ban đầu
    if (canvasRef.current) {
      const context = canvasRef.current.getContext("2d");
      context.clearRect(
        0,
        0,
        canvasRef.current.width,
        canvasRef.current.height
      );
    }
    // if (photoRef.current) {
    //   photoRef.current.setAttribute("src", ""); // Xóa ảnh hiển thị
    // }
  };

  const toggleTracking = () => {
    if (!isRunning) {
      startWebcam();
    } else {
      stopWebcam();
    }
    setIsRunning(!isRunning);
  };

  useEffect(() => {
    // setupVoiceRecognition();
    return () => {
      stopWebcam();
    };
  }, []);

  useEffect(() => {
    const intervalId = window.setInterval(function () {},
    Number.MAX_SAFE_INTEGER);
    for (let i = 1; i <= intervalId; i++) {
      window.clearInterval(i);
    }

    if (isRunning === true) {
      startWebcam();
    }
  }, [mode]);

  return (
    <div className="container">
      {/* <Header /> */}

      <main>
        <VideoFeed
          videoRef={videoRef}
          isRunning={isRunning}
          canvasRef={canvasRef}
        />

        <Controls
          isRunning={isRunning}
          toggleTracking={toggleTracking}
          mode={mode}
          setMode={setMode}
          sensitivity={sensitivity}
          setSensitivity={setSensitivity}
        />
        {/* <div className="video">
          <img alt="" ref={photoRef} id="photo" width="400" height="300" />
        </div> */}
      </main>

      <Footer isRunning={isRunning} mode={mode} />
    </div>
  );
}

export default App;
