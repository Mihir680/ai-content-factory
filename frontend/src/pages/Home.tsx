import { useState, useEffect } from "react";
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

            {history.map((item, index) => (
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

<div className="grid md:grid-cols-4 gap-4 mb-6">

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
              />

            <div className="flex flex-wrap gap-4 mt-6">

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