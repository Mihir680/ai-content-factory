import { useState, useEffect, useRef } from "react";

import jsPDF from "jspdf";
import { Document, Packer, Paragraph, TextRun } from "docx";
import JSZip from "jszip";
import { saveAs } from "file-saver";
import SummaryCard from "../components/SummaryCard";


import toast from "react-hot-toast";

import api from "../services/api";

import Header from "../components/Header";
import TopicInput from "../components/TopicInput";
import ResultCard from "../components/ResultCard";

function Home() {
  const [topic, setTopic] = useState("");
  const [history, setHistory] = useState<any[]>([]);

const loadHistory = async () => {
  try {
    const res = await api.get("/history");

    setHistory(Array.isArray(res.data) ? res.data : []);

  } catch (err) {
    console.log(err);
    setHistory([]);
  }
};

useEffect(() => {
  loadHistory();
}, []);

  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);

  const [thumbnailPrompt, setThumbnailPrompt] = useState("");
  const [thumbnailImage, setThumbnailImage] = useState("");
  const [language, setLanguage] = useState("English");
  const [platform, setPlatform] = useState("YouTube");
const [tone, setTone] = useState("Professional");
  const [length, setLength] = useState("5 Minutes");
  const [visualStyle, setVisualStyle] = useState("real");


  const generate = async () => {
    if (!topic.trim()) {
      toast.error("Please enter a topic");
      return;
    }

  setLoading(true);

try {
  const { data } = await api.post("/generate", {
    topic,
    language,
    platform,
    tone,
    length,
  });

  setData(data);


setData(data);

// Reload history from database
await loadHistory();

toast.success("Content Generated Successfully!");

  toast.success("Content generated successfully!");
} catch (err: any) {
  console.error(err);

  toast.error(
    err.response?.data?.detail ||
      err.response?.data?.message ||
      "Failed to generate content"
  );
} finally {
  setLoading(false);
}
};

  const generateThumbnailPrompt = async () => {
    if (!topic.trim()) {
      toast.error("Please enter a topic");
      return;
    }

    try {
      const res = await api.post("/thumbnail-image", {
        topic,
      });console.log(res.data);
console.log(res.data.prompt);

      setThumbnailPrompt(res.data.prompt);

      if (!res.data.prompt) {
  toast.error("Prompt not generated");
  return;
}

const imageUrl =
  "https://image.pollinations.ai/prompt/" +
  encodeURIComponent(res.data.prompt);

      setThumbnailImage(imageUrl);

      toast.success("AI Thumbnail Generated!");
    } catch (err: any) {
      console.error(err);

      toast.error(
        err.response?.data?.detail ||
          err.response?.data ||
          err.message
      );
    }
  };
    const downloadPDF = () => {
    if (!data) return;

    const pdf = new jsPDF();

    pdf.setFontSize(20);
    pdf.text("AI Content Factory", 20, 20);

    let y = 35;

    const sections = [
      ["SCRIPT", data.script],
      ["SEO", data.seo],
      ["DESCRIPTION", data.description],
      ["HASHTAGS", data.hashtags],
      ["THUMBNAIL", data.thumbnail],
    ];

    sections.forEach(([title, content]) => {
      if (y > 250) {
        pdf.addPage();
        y = 20;
      }

      pdf.setFont("helvetica", "bold");
      pdf.text(title as string, 20, y);

      y += 8;

      pdf.setFont("helvetica", "normal");

      const lines = pdf.splitTextToSize(
        String(content),
        170
      );

      pdf.text(lines, 20, y);

      y += lines.length * 6 + 12;
    });

    pdf.save("AI_Content_Factory.pdf");
  };

  const downloadDOCX = async () => {
    if (!data) return;

    const doc = new Document({
      sections: [
        {
          children: [
            new Paragraph({
              children: [
                new TextRun({
                  text: "AI Content Factory",
                  bold: true,
                  size: 36,
                }),
              ],
            }),

            new Paragraph(" "),

            new Paragraph({
              children: [
                new TextRun({
                  text: "SCRIPT",
                  bold: true,
                }),
              ],
            }),

            new Paragraph(data.script),

            new Paragraph(" "),

            new Paragraph({
              children: [
                new TextRun({
                  text: "SEO",
                  bold: true,
                }),
              ],
            }),

            new Paragraph(data.seo),

            new Paragraph(" "),

            new Paragraph({
              children: [
                new TextRun({
                  text: "DESCRIPTION",
                  bold: true,
                }),
              ],
            }),

            new Paragraph(data.description),

            new Paragraph(" "),

            new Paragraph({
              children: [
                new TextRun({
                  text: "HASHTAGS",
                  bold: true,
                }),
              ],
            }),

            new Paragraph(data.hashtags),

            new Paragraph(" "),

            new Paragraph({
              children: [
                new TextRun({
                  text: "THUMBNAIL PROMPT",
                  bold: true,
                }),
              ],
            }),

            new Paragraph(data.thumbnail),
          ],
        },
      ],
    });

    const blob = await Packer.toBlob(doc);

    saveAs(blob, "AI_Content_Factory.docx");
  };

  const copyAll = () => {
  if (!data) return;
  

  const text = `
========================
SCRIPT
========================

${data.script}

========================
SEO
========================

${data.seo}

========================
DESCRIPTION
========================

${data.description}

========================
HASHTAGS
========================

${data.hashtags}

========================
THUMBNAIL PROMPT
========================

${data.thumbnail}
`;

  navigator.clipboard.writeText(text);

  toast.success("Everything copied successfully!");
};
  const [videoLoading, setVideoLoading] = useState(false);
  const [uploadingYoutube, setUploadingYoutube] = useState(false);
  const [generatedVideo, setGeneratedVideo] = useState<any>(null);
  const [videoTimestamp, setVideoTimestamp] = useState(Date.now());
  const videoRef = useRef<HTMLVideoElement>(null);

  const unmuteAndPlayVideo = () => {
    if (videoRef.current) {
      videoRef.current.muted = false;
      videoRef.current.volume = 1.0;
      videoRef.current.play().catch(() => {});
      toast.success("🔊 Full Voiceover Sound Unmuted!");
    }
  };


  const generateFullVideo = async () => {
    if (!topic.trim()) {
      toast.error("Please enter a topic first");
      return;
    }

    setVideoLoading(true);
    toast.loading("🎬 Rendering AI Video with Moving Scenes & Voiceover...", { id: "video-toast" });

    try {
      const res = await api.post(
        "/generate-pipeline",
        {
          topic,
          language,
          platform,
          tone,
          length,
          visual_style: visualStyle,

          auto_upload: false,
        },
        { timeout: 300000 }
      );


      if (res.data && res.data.result) {
        setVideoTimestamp(Date.now());
        setGeneratedVideo(res.data.result);
        toast.success("🎉 Dynamic AI Video & SRT Subtitles Rendered!", { id: "video-toast" });
      }
    } catch (err: any) {

      console.error(err);
      toast.error(err.response?.data?.detail || "Video Generation Failed", { id: "video-toast" });
    } finally {
      setVideoLoading(false);
    }
  };

  const manualUploadYouTube = async () => {
    if (!generatedVideo) return;

    setUploadingYoutube(true);
    toast.loading("📤 Uploading video to YouTube...", { id: "yt-upload-toast" });

    try {
      const res = await api.post(
        "/upload-youtube",
        {
          video_path: generatedVideo.video_path,
          title: generatedVideo.title || topic,
          description: generatedVideo.description || topic,
          privacy_status: "private",
        },
        { timeout: 180000 }
      );

      if (res.data && res.data.upload_result) {
        const videoId = res.data.upload_result.video_id;
        const ytUrl = `https://youtube.com/watch?v=${videoId}`;
        toast.success(`🎉 Video Uploaded to YouTube! (ID: ${videoId})`, { id: "yt-upload-toast" });
        setGeneratedVideo((prev: any) => ({ ...prev, youtube_url: ytUrl }));
      }
    } catch (err: any) {
      console.error(err);
      toast.error(err.response?.data?.detail || "YouTube Upload Failed", { id: "yt-upload-toast" });
    } finally {
      setUploadingYoutube(false);
    }
  };


  const downloadZIP = async () => {
    if (!data) return;

    const zip = new JSZip();

    zip.file("script.txt", data.script);
    zip.file("seo.txt", data.seo);
    zip.file("description.txt", data.description);
    zip.file("hashtags.txt", data.hashtags);
    zip.file("thumbnail_prompt.txt", data.thumbnail);

    if (thumbnailPrompt) {
      zip.file("ai_image_prompt.txt", thumbnailPrompt);
    }

    const blob = await zip.generateAsync({
      type: "blob",
    });

    saveAs(blob, "AI_Content_Factory.zip");

    toast.success("ZIP Downloaded Successfully!");
  };


  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <div className="max-w-7xl mx-auto p-10">

        <Header />

        {/* Recent Topics */}

        <div className="mt-8 mb-8">

          <h2 className="text-2xl font-bold mb-4">
            🕘 Recent Topics
          </h2>

          <div className="flex flex-wrap gap-3">

            {history.slice(0, 5).map((item, index) => (

              <button
                key={index}
                onClick={() => {
                  setTopic(item.topic);

                  setData({
                    script: item.script,
                    seo: item.seo,
                    description: item.description,
                    hashtags: item.hashtags,
                    thumbnail: item.thumbnail,
                    titles: item.titles,
                  });
                }}
                className="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg border border-slate-700"
              >
                <div>
                  <div>{item.topic}</div>

                  <div className="text-xs text-gray-400">
                    {item.createdAt}
                  </div>
                </div>
              </button>
            ))}

          </div>

        </div>

<div className="grid md:grid-cols-5 gap-4 mb-6">

  <div>
    <label className="block mb-2 font-semibold">
      🌐 Language
    </label>

    <select
      value={language}
      onChange={(e) => setLanguage(e.target.value)}
      className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3"
    >
      <option>English</option>
      <option>Hindi</option>
      <option>Gujarati</option>
    </select>
  </div>

  <div>
    <label className="block mb-2 font-semibold">
      🎬 Platform
    </label>

    <select
      value={platform}
      onChange={(e) => setPlatform(e.target.value)}
      className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3"
    >
      <option>YouTube</option>
      <option>YouTube Shorts</option>
      <option>Instagram Reel</option>
      <option>Facebook</option>
      <option>LinkedIn</option>
    </select>
  </div>

  <div>
    <label className="block mb-2 font-semibold">
      🎭 Tone
    </label>

    <select
      value={tone}
      onChange={(e) => setTone(e.target.value)}
      className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3"
    >
      <option>Professional</option>
      <option>Funny</option>
      <option>Motivational</option>
      <option>Storytelling</option>
      <option>Educational</option>
    </select>
  </div>

  <div>
    <label className="block mb-2 font-semibold">
      ⏱ Script Length
    </label>

    <select
      value={length}
      onChange={(e) => setLength(e.target.value)}
      className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3"
    >
      <option>30 Seconds</option>
      <option>60 Seconds</option>
      <option>5 Minutes</option>
      <option>10 Minutes</option>
    </select>
  </div>

  <div>
    <label className="block mb-2 font-semibold">
      🖼️ Visual Style
    </label>

    <select
      value={visualStyle}
      onChange={(e) => setVisualStyle(e.target.value)}
      className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-sm font-bold text-emerald-400"
    >
      <option value="real">📸 Real Photography (Google 8K Real Photo)</option>
      <option value="animation">🎨 3D Animation & Cartoon</option>
    </select>
  </div>

</div>

        <TopicInput
          topic={topic}
          setTopic={setTopic}
          generate={generate}
          loading={loading}
        />

        {data && (
          
          <>
          <SummaryCard
               topic={topic}
               language={language}
               platform={platform}
               tone={tone}
               length={length}
               visualStyle={visualStyle}
              />


            <div className="flex flex-wrap gap-4 mt-6">
              <button
                onClick={generateFullVideo}
                disabled={videoLoading}
                className="bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 font-bold text-white px-6 py-3 rounded-xl shadow-lg transition-all transform hover:scale-105 flex items-center gap-2"
              >
                {videoLoading ? "🎥 Rendering AI Video..." : "🎥 Generate & Preview AI Video"}
              </button>



              <button
                onClick={generateThumbnailPrompt}
                className="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-xl"
              >
                🖼 Generate AI Prompt
              </button>

              <button
                onClick={downloadPDF}
                className="bg-red-600 hover:bg-red-700 px-6 py-3 rounded-xl"
              >
                📄 Download PDF
              </button>

              <button
                onClick={downloadDOCX}
                className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-xl"
              >
                📄 DOCX
              </button>

              <button
                onClick={copyAll}
                className="bg-green-600 hover:bg-green-700 px-6 py-3 rounded-xl"
              >
                📋 Copy All
              </button>

              <button
                onClick={downloadZIP}
                className="bg-yellow-600 hover:bg-yellow-700 px-6 py-3 rounded-xl"
              >
                📦 Download ZIP
              </button>

            </div>

            {/* Generated AI Video & SRT Captions Preview Card */}
            {generatedVideo && (
              <div className="bg-slate-800 border-2 border-red-500/40 rounded-2xl p-6 mt-8 shadow-2xl">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                    🎥 AI Moving Video Preview & Subtitles
                  </h2>
                  <button
                    onClick={unmuteAndPlayVideo}
                    className="bg-yellow-500 hover:bg-yellow-400 text-slate-950 font-extrabold text-sm px-4 py-2 rounded-xl flex items-center gap-2 shadow-lg transition transform hover:scale-105 active:scale-95"
                  >
                    🔊 Click to Unmute & Play Full Audio Sound
                  </button>
                </div>

                <div className="relative aspect-video w-full rounded-xl overflow-hidden bg-black border border-slate-700 shadow-inner mb-4">
                  <button
                    onClick={unmuteAndPlayVideo}
                    className="absolute top-3 left-3 z-20 bg-yellow-500 hover:bg-yellow-400 text-slate-950 font-extrabold text-sm px-4 py-2 rounded-xl flex items-center gap-2 shadow-2xl transition transform hover:scale-105 active:scale-95 border-2 border-yellow-300"
                  >
                    🔊 UNMUTE & PLAY FULL AUDIO SOUND
                  </button>
                  <video
                    ref={videoRef}
                    controls
                    playsInline
                    key={videoTimestamp}
                    className="w-full h-full object-contain"
                    src={`http://localhost:8000/media/videos/video.mp4?t=${videoTimestamp}`}
                    onPlay={(e) => {
                      e.currentTarget.muted = false;
                      e.currentTarget.volume = 1.0;
                    }}
                  >
                    <track
                      kind="subtitles"
                      src={`http://localhost:8000/media/videos/video.srt?t=${videoTimestamp}`}
                      srcLang="en"
                      label="English"
                      default
                    />
                    Your browser does not support HTML5 Video.
                  </video>
                </div>

                {/* Standalone Audio Voiceover Backup Player */}
                <div className="bg-slate-900/90 p-4 rounded-xl border border-yellow-500/40 mb-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-yellow-400 font-bold text-sm flex items-center gap-2">
                      🎙️ Standalone AI Voiceover Sound Bar (Listen MP3 directly):
                    </span>
                  </div>
                  <audio
                    controls
                    key={`audio-player-${videoTimestamp}`}
                    className="w-full rounded-lg"
                    src={`http://localhost:8000/media/audio/voice.mp3?t=${videoTimestamp}`}
                  >
                    Your browser does not support HTML5 Audio.
                  </audio>
                </div>

                <div className="flex flex-wrap gap-4 mt-5">
                  <a
                    href="http://localhost:8000/media/videos/video.mp4"
                    download="ai_generated_video.mp4"
                    className="bg-red-600 hover:bg-red-700 text-white font-semibold px-6 py-3 rounded-xl flex items-center gap-2 shadow"
                  >
                    📥 Download MP4 Video
                  </a>

                  <a
                    href="http://localhost:8000/media/audio/voice.mp3"
                    download="ai_voiceover.mp3"
                    className="bg-yellow-600 hover:bg-yellow-500 text-slate-950 font-bold px-6 py-3 rounded-xl flex items-center gap-2 shadow border border-yellow-400"
                  >
                    🎵 Download Voice MP3 Sound
                  </a>

                  <a
                    href="http://localhost:8000/media/videos/video.srt"
                    download="ai_subtitles.srt"
                    className="bg-slate-700 hover:bg-slate-600 text-white font-semibold px-6 py-3 rounded-xl flex items-center gap-2 border border-slate-600"
                  >

                    📝 Download SRT Subtitles (Toggleable)
                  </a>

                  <button
                    onClick={manualUploadYouTube}
                    disabled={uploadingYoutube}
                    className="bg-gradient-to-r from-red-600 to-red-800 hover:from-red-700 hover:to-red-900 text-white font-bold px-6 py-3 rounded-xl flex items-center gap-2 shadow-lg transition-transform hover:scale-105"
                  >
                    {uploadingYoutube ? "⏳ Uploading..." : "🚀 Upload to YouTube Now (Manual)"}
                  </button>
                </div>

                {generatedVideo.youtube_url && (
                  <div className="mt-4 p-4 bg-green-500/10 border border-green-500/30 rounded-xl text-green-400 font-semibold flex items-center justify-between">
                    <span>🎉 Successfully Uploaded to YouTube!</span>
                    <a
                      href={generatedVideo.youtube_url}
                      target="_blank"
                      rel="noreferrer"
                      className="underline font-bold hover:text-white"
                    >
                      🔗 Watch on YouTube
                    </a>
                  </div>
                )}
              </div>
            )}



            <div className="mt-8 space-y-8">
                          <ResultCard
                title="📜 Script"
                content={data.script}
              />

              <ResultCard
                title="🚀 SEO"
                content={data.seo}
              />

              <ResultCard
                title="📝 Description"
                content={data.description}
              />

              <ResultCard
                title="#️⃣ Hashtags"
                content={data.hashtags}
              />
              <ResultCard
                title="🎯 Viral Titles"
                content={data.titles}
              />
              <ResultCard
                title="🖼 Thumbnail Prompt"
                content={data.thumbnail}
              />

              {thumbnailPrompt && (
                <ResultCard
                  title="🎨 AI Image Prompt"
                  content={thumbnailPrompt}
                />
              )}

              {thumbnailImage && (
                <div className="bg-slate-800 rounded-xl p-6">

                  <h2 className="text-2xl font-bold mb-5">
                    🖼 AI Thumbnail Preview
                  </h2>

                  <img
                    src={thumbnailImage}
                    alt="AI Thumbnail"
                    className="w-full rounded-xl border border-slate-700"
                  />

                  <div className="flex gap-4 mt-5">

                    <a
                      href={thumbnailImage}
                      target="_blank"
                      rel="noreferrer"
                      className="bg-pink-600 hover:bg-pink-700 px-6 py-3 rounded-xl"
                    >
                      🔍 Open Full Image
                    </a>

                    <a
                      href={thumbnailImage}
                      download="thumbnail.png"
                      className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-xl"
                    >
                      📥 Download Image
                    </a>

                  </div>

                </div>
              )}

            </div>

          </>
        )}

      </div>
    </div>
  );
}

export default Home;