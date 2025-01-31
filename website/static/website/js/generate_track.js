let currentlyPlaying = null;
let prevPlayButton = null;
const play_icon = `
    <svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M27.9111 12.8355L3.59188 0.294005C3.23314 0.10849 2.82214 0.00711601 2.40136 0.00036115C1.98059 -0.00639371 1.56531 0.0817157 1.19845 0.255582C0.833542 0.424533 0.529555 0.673458 0.318609 0.976051C0.107663 1.27864 -0.00240419 1.62366 3.98326e-05 1.97465V27.0576C-0.00240419 27.4086 0.107663 27.7536 0.318609 28.0562C0.529555 28.3588 0.833542 28.6077 1.19845 28.7767C1.56531 28.9505 1.98059 29.0387 2.40136 29.0319C2.82214 29.0251 3.23314 28.9238 3.59188 28.7383L27.9111 16.1968C28.2534 16.0214 28.5364 15.7746 28.7327 15.4802C28.9291 15.1859 29.0323 14.8539 29.0323 14.5161C29.0323 14.1784 28.9291 13.8464 28.7327 13.552C28.5364 13.2577 28.2534 13.0109 27.9111 12.8355ZM26.8545 14.7396L2.53188 27.281C2.47938 27.3076 2.41928 27.3217 2.35803 27.3217C2.29678 27.3217 2.23668 27.3076 2.18418 27.281C2.1333 27.2601 2.09047 27.2275 2.06061 27.187C2.03074 27.1465 2.01507 27.0996 2.01539 27.0519V1.97465C2.01507 1.92693 2.03074 1.88011 2.06061 1.83957C2.09047 1.79904 2.1333 1.76644 2.18418 1.74553C2.23879 1.71986 2.30059 1.70708 2.36309 1.70853C2.423 1.71034 2.48126 1.72557 2.53188 1.75265L26.8545 14.2927C26.9007 14.3156 26.939 14.3482 26.9656 14.3874C26.9922 14.4266 27.0063 14.471 27.0063 14.5161C27.0063 14.5613 26.9922 14.6057 26.9656 14.6449C26.939 14.6841 26.9007 14.7167 26.8545 14.7396Z" fill="#ECECEC"/>
    </svg>`;
const pause_icon = `
    <svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M27.5581 0H20.5814C19.9338 0 19.3127 0.235372 18.8547 0.654336C18.3968 1.0733 18.1395 1.64154 18.1395 2.23404V27.766C18.1395 28.3585 18.3968 28.9267 18.8547 29.3457C19.3127 29.7646 19.9338 30 20.5814 30H27.5581C28.2058 30 28.8269 29.7646 29.2848 29.3457C29.7427 28.9267 30 28.3585 30 27.766V2.23404C30 1.64154 29.7427 1.0733 29.2848 0.654336C28.8269 0.235372 28.2058 0 27.5581 0ZM27.907 27.766C27.907 27.8506 27.8702 27.9318 27.8048 27.9916C27.7394 28.0515 27.6507 28.0851 27.5581 28.0851H20.5814C20.4889 28.0851 20.4001 28.0515 20.3347 27.9916C20.2693 27.9318 20.2326 27.8506 20.2326 27.766V2.23404C20.2326 2.1494 20.2693 2.06822 20.3347 2.00837C20.4001 1.94852 20.4889 1.91489 20.5814 1.91489H27.5581C27.6507 1.91489 27.7394 1.94852 27.8048 2.00837C27.8702 2.06822 27.907 2.1494 27.907 2.23404V27.766ZM9.4186 0H2.44186C1.79424 0 1.17314 0.235372 0.715204 0.654336C0.257267 1.0733 0 1.64154 0 2.23404V27.766C0 28.3585 0.257267 28.9267 0.715204 29.3457C1.17314 29.7646 1.79424 30 2.44186 30H9.4186C10.0662 30 10.6873 29.7646 11.1453 29.3457C11.6032 28.9267 11.8605 28.3585 11.8605 27.766V2.23404C11.8605 1.64154 11.6032 1.0733 11.1453 0.654336C10.6873 0.235372 10.0662 0 9.4186 0ZM9.76744 27.766C9.76744 27.8506 9.73069 27.9318 9.66527 27.9916C9.59985 28.0515 9.51112 28.0851 9.4186 28.0851H2.44186C2.34934 28.0851 2.26061 28.0515 2.19519 27.9916C2.12978 27.9318 2.09302 27.8506 2.09302 27.766V2.23404C2.09302 2.1494 2.12978 2.06822 2.19519 2.00837C2.26061 1.94852 2.34934 1.91489 2.44186 1.91489H9.4186C9.51112 1.91489 9.59985 1.94852 9.66527 2.00837C9.73069 2.06822 9.76744 2.1494 9.76744 2.23404V27.766Z" fill="#ECECEC"/>
    </svg>`;

function generate_track(track) {
  let isPlaying = false;
  const parentElement = document.createElement("div");
  const prompt = document.createElement("p");
  const audioPlayer = document.createElement("div");
  const seekBar = document.createElement("input");
  const playButton = document.createElement("button");
  const duration = document.createElement("p");
  const currentDuration = document.createElement("span");
  const totalDuration = document.createElement("span");
  const waveform = document.createElement("div");
  waveform.id = "waveform";

  const wavesurfer = WaveSurfer.create({
    container: waveform,
    waveColor: "#ececec",
    progressColor: "cyan",
    barWidth: 2,
    responsive: true,
    height: 50,
    barRadius: 3,
    cursorWidth: 2,
    cursorColor: "cyan",
    normalize: true,
  });

  fetch(`/api/track/${track.id}`, { method: "GET" })
    .then((response) => response.blob())
    .then((blob) => {
      wavesurfer.loadBlob(blob);
    })
    .catch((error) => {
      console.log(error);
    });

  parentElement.className = "audioPlayerParent";

  prompt.className = "normal-text";
  prompt.innerHTML = track.prompt;
  parentElement.appendChild(prompt);

  audioPlayer.className = "audio-player";

  seekBar.type = "range";
  seekBar.min = 0;
  seekBar.max = 100;
  seekBar.value = 0;
  seekBar.step = 1;
  seekBar.style.display = "none";
  audioPlayer.appendChild(seekBar);

  playButton.className = "buttonReset normal-text";
  playButton.innerHTML = play_icon;
  playButton.addEventListener("click", () => {
    if (currentlyPlaying != null) {
      currentlyPlaying.pause();
      prevPlayButton.innerHTML = play_icon;
    }
    if (!isPlaying || currentlyPlaying != wavesurfer) {
      currentlyPlaying = wavesurfer;
      prevPlayButton = playButton;
      playButton.innerHTML = pause_icon;
      wavesurfer.play();
      isPlaying = true;
    } else {
      playButton.innerHTML = play_icon;
      wavesurfer.pause();
      isPlaying = false;
      currentlyPlaying = null;
    }
  });
  audioPlayer.appendChild(playButton);

  wavesurfer.on("ready", () => {
    var duration = wavesurfer.getDuration();
    var minutes = parseInt(duration / 60, 10);
    var seconds = parseInt(duration % 60);
    totalDuration.innerHTML =
      "/" + minutes + ":" + seconds.toString().padStart(2, "0");

    wavesurfer.on("seek", (progress) => {
      var currentTime = progress * duration;
      var minutes = parseInt(currentTime / 60, 10);
      var seconds = parseInt(currentTime % 60);
      currentDuration.innerHTML =
        minutes + ":" + seconds.toString().padStart(2, "0");

      if (Math.round(currentTime) == Math.round(wavesurfer.getDuration())) {
        prevPlayButton.innerHTML = play_icon;
        wavesurfer.seekTo(0);
        isPlaying = false;
        wavesurfer.pause();
      }
    });

    wavesurfer.on("audioprocess", () => {
      var currentTime = wavesurfer.getCurrentTime();
      var minutes = parseInt(currentTime / 60, 10);
      var seconds = parseInt(currentTime % 60);
      currentDuration.innerHTML =
        minutes + ":" + seconds.toString().padStart(2, "0");

      if (Math.round(currentTime) == Math.round(wavesurfer.getDuration())) {
        prevPlayButton.innerHTML = play_icon;
        wavesurfer.seekTo(0);
        isPlaying = false;
        wavesurfer.pause();
      }
    });
  });

  duration.className = "normal-text duration";

  currentDuration.innerHTML = "0:00";
  duration.appendChild(currentDuration);

  const durationTime = wavesurfer.getDuration();
  const minutes = parseInt(durationTime / 60, 10);
  const seconds = parseInt(durationTime % 60);
  totalDuration.innerHTML = `/${minutes}:${seconds
    .toString()
    .padStart(2, "0")}`;
  duration.appendChild(totalDuration);

  audioPlayer.appendChild(duration);
  audioPlayer.appendChild(waveform);

  parentElement.appendChild(audioPlayer);

  return parentElement;
}
