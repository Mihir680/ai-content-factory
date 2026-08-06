import toast from "react-hot-toast";

type Props = {
  title: string;
  content: string;
};

function ResultCard({ title, content }: Props) {
  const copyContent = () => {
    navigator.clipboard.writeText(content);
    toast.success("Copied Successfully!");
  };

  // Statistics
  const words = content.trim().split(/\s+/).filter(Boolean).length;
  const characters = content.length;
  const readingTime = Math.max(1, Math.ceil(words / 200));
  const speakingTime = Math.max(1, Math.ceil(words / 130));

  return (
    <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">

      <div className="flex justify-between items-center mb-4">

        <h2 className="text-2xl font-bold">
          {title}
        </h2>

        <button
          onClick={copyContent}
          className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg"
        >
          📋 Copy
        </button>

      </div>

      {/* Content Statistics */}
      <div className="flex flex-wrap gap-5 text-sm text-gray-400 mb-5">

        <span>📝 {words} Words</span>

        <span>🔤 {characters} Characters</span>

        <span>📖 {readingTime} min Read</span>

        <span>🎤 {speakingTime} min Speak</span>

      </div>

      <pre className="whitespace-pre-wrap text-gray-200">
        {content}
      </pre>

    </div>
  );
}

export default ResultCard;