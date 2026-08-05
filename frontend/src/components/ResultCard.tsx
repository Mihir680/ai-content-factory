import toast from "react-hot-toast";
import ReactMarkdown from "react-markdown";

type Props = {
  title: string;
  content: string;
};

function ResultCard({ title, content }: Props) {
  const copy = () => {
    navigator.clipboard.writeText(content);
    toast.success("Copied Successfully!");
  };

  const downloadTXT = () => {
    const blob = new Blob([content], {
      type: "text/plain;charset=utf-8",
    });

    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = `${title.replace(/[^a-zA-Z0-9]/g, "")}.txt`;
    a.click();

    window.URL.revokeObjectURL(url);

    toast.success("Downloaded Successfully!");
  };

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6 shadow-lg">

      <div className="flex justify-between items-center mb-5">

        <h2 className="text-2xl font-bold text-white">
          {title}
        </h2>

        <div className="flex gap-3">

          <button
            onClick={copy}
            className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg transition"
          >
            📋 Copy
          </button>

          <button
            onClick={downloadTXT}
            className="bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-lg transition"
          >
            ⬇ TXT
          </button>

        </div>

      </div>

      <div className="prose prose-invert max-w-none break-words">
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>

    </div>
  );
}

export default ResultCard;