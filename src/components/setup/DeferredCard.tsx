export function DeferredCard({ title, reason }: { title: string; reason: string }) {
  return (
    <section className="bg-gray-800/40 border border-dashed border-gray-700 rounded-lg p-5 text-gray-500">
      <div className="flex items-center gap-3">
        <span className="text-xs uppercase tracking-wide text-amber-500/80 border border-amber-500/40 rounded px-2 py-0.5">
          Deferred
        </span>
        <h2 className="text-sm font-semibold uppercase tracking-wide text-gray-400">
          {title}
        </h2>
      </div>
      <p className="text-sm text-gray-500 mt-2">{reason}</p>
    </section>
  );
}
