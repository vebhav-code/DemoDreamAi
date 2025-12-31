let streamVideos = {};

fetch("../data/Streams.json")
  .then(res => res.json())
  .then(data => streamVideos = data)
  .catch(err => console.error("Failed to load video list:", err));

function loadStreamVideo(streamName) {
    const section = document.getElementById("videoSection");
    const iframe = document.getElementById("streamVideo");

    if (streamName && streamVideos[streamName]) {
        iframe.src = streamVideos[streamName];
        section.style.display = "block";
    } else {
        iframe.src = "";
        section.style.display = "none";
    }
}

window.loadStreamVideo = loadStreamVideo;
