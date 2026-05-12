import { Button } from '../ui/Button';
import { Card } from '../ui/Card';

interface Props {
  keySlug: string | null;
  topIds: string[];
  bottomIds: string[];
  onNew: () => void;
}

export function DoneSummary({ keySlug, topIds, bottomIds, onNew }: Props) {
  const total = topIds.length + bottomIds.length;
  return (
    <Card title="Capture complete">
      <div className="space-y-4">
        <div className="text-3xl font-bold text-green-400">✓ {total} measurements written</div>
        {keySlug && (
          <div className="text-sm text-gray-400">
            Stored under key:{' '}
            <code className="font-mono text-gray-200 bg-gray-900 px-2 py-0.5 rounded">
              {keySlug}
            </code>
          </div>
        )}
        <div className="grid grid-cols-2 gap-4 pt-2 border-t border-gray-700">
          <Stat label="Top half" count={topIds.length} />
          <Stat label="Bottom half" count={bottomIds.length} />
        </div>
        <div className="flex items-center justify-end gap-3 pt-3 border-t border-gray-700">
          <Button onClick={onNew}>New capture</Button>
        </div>
      </div>
    </Card>
  );
}

function Stat({ label, count }: { label: string; count: number }) {
  return (
    <div>
      <div className="text-xs uppercase tracking-wide text-gray-500">{label}</div>
      <div className="text-2xl text-gray-100 mt-0.5 font-mono">{count}</div>
    </div>
  );
}
