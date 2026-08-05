import { BeatLoader } from "react-spinners";

type Props = {
  topic: string;
  setTopic: (value: string) => void;
  generate: () => void;
  loading: boolean;
};

function TopicInput({
  topic,
  setTopic,
  generate,
  loading,
}: Props) {
  return (
    <div className="space-y-5">

      <textarea
        rows={5}
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && e.ctrlKey) {
            generate();
          }
        }}
        placeholder="Example: AI will replace Software Engineers in 2026"
        className="w-full rounded-2xl bg-slate-800 border border-slate-700 p-5 text-white outline-none focus:border-blue-500 resize-none text-lg"
      />

      <div className="flex justify-between items-center">

        <span className="text-slate-400 text-sm">
          {topic.length} Characters
        </span>

        <button
          onClick={generate}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 transition px-8 py-3 rounded-xl font-semibold flex items-center gap-3"
        >
          {loading ? (
            <>
              <BeatLoader
                color="#fff"
                size={8}
              />
              Generating...
            </>
          ) : (
            <>🚀 Generate</>
          )}
        </button>

      </div>

      <p className="text-slate-500 text-sm">
        💡 Tip: Press <b>Ctrl + Enter</b> to generate instantly.
      </p>

    </div>
  );
}

export default TopicInput;