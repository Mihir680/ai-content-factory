type Props = {
  topic: string;
  language: string;
  platform: string;
  tone: string;
  length: string;
};

function SummaryCard({
  topic,
  language,
  platform,
  tone,
  length,
}: Props) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">

      <h2 className="text-2xl font-bold mb-5">
        📊 Content Summary
      </h2>

      <div className="grid md:grid-cols-2 gap-4">

        <p><strong>Topic:</strong> {topic}</p>

        <p><strong>Language:</strong> {language}</p>

        <p><strong>Platform:</strong> {platform}</p>

        <p><strong>Tone:</strong> {tone}</p>

        <p><strong>Length:</strong> {length}</p>

      </div>

    </div>
  );
}

export default SummaryCard;