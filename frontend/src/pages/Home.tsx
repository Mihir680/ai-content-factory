import { useState } from "react";
import jsPDF from "jspdf";
import { Document, Packer, Paragraph, TextRun } from "docx";
import { saveAs } from "file-saver";
import toast from "react-hot-toast";
import api from "../services/api";

import Header from "../components/Header";
import TopicInput from "../components/TopicInput";
import ResultCard from "../components/ResultCard";

function Home() {
  const [topic, setTopic] = useState("");
  const [history, setHistory] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);

  const generate = async () => {
    if (!topic.trim()) {
      toast.error("Please enter a topic");
      return;
    }

    setLoading(true);

    try {
      const res = await api.post("/generate", {
        topic,
      });

      setData(res.data);
      setHistory((prev) => [topic, ...prev]);
    } catch (err: any) {
  console.error(err);

  console.log(err.response?.data);

  toast.error(
    err.response?.data?.detail ||
    err.response?.data ||
    err.message
  );
}finally {
      setLoading(false);
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
            children: [new TextRun({ text: "SCRIPT", bold: true })],
          }),
          new Paragraph(data.script),

          new Paragraph(" "),

          new Paragraph({
            children: [new TextRun({ text: "SEO", bold: true })],
          }),
          new Paragraph(data.seo),

          new Paragraph(" "),

          new Paragraph({
            children: [new TextRun({ text: "DESCRIPTION", bold: true })],
          }),
          new Paragraph(data.description),

          new Paragraph(" "),

          new Paragraph({
            children: [new TextRun({ text: "HASHTAGS", bold: true })],
          }),
          new Paragraph(data.hashtags),

          new Paragraph(" "),

          new Paragraph({
            children: [new TextRun({ text: "THUMBNAIL PROMPT", bold: true })],
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

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <div className="max-w-7xl mx-auto p-10">

        <Header />
        <div className="mt-8 mb-8">

  <h2 className="text-2xl font-bold mb-4">
    🕘 Recent Topics
  </h2>

  <div className="flex flex-wrap gap-3">

    {history.map((item, index) => (
      <button
        key={index}
        onClick={() => setTopic(item)}
        className="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg border border-slate-700"
      >
        {item}
      </button>
    ))}

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
            <div className="flex gap-4 mt-6">

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
                title="🖼 Thumbnail Prompt"
                content={data.thumbnail}
              />

            </div>
          </>
        )}

      </div>
    </div>
  );
}

export default Home;