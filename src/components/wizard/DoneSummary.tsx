import { Button } from '../ui/Button';
import { Card } from '../ui/Card';

interface Props {
  keySlug: string | null;
  measurementIds: string[];
  onNew: () => void;
}

export function DoneSummary({ keySlug, measurementIds, onNew }: Props) {
  return (
    <Card title="Capture complete">
      <div className="space-y-4">
        <div className="text-3xl font-bold text-green-400">
          ✓ {measurementIds.length} measurements written
        </div>
        {keySlug && (
          <div className="text-sm text-gray-400">
            Stored under key:{' '}
            <code className="font-mono text-gray-200 bg-gray-900 px-2 py-0.5 rounded">
              {keySlug}
            </code>
          </div>
        )}
        <div className="flex items-center justify-end gap-3 pt-3 border-t border-gray-700">
          <Button onClick={onNew}>New capture</Button>
        </div>
      </div>
    </Card>
  );
}
