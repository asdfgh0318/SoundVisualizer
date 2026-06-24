import { useEffect, useState } from 'react';
import { api, ApiError } from '../../api/client';
import type { ResearchTreeNode, ResearchTreePhase, ResearchTreeRef } from '../../api/types';
import type { WizardForm } from '../../stores/wizardStore';

interface Props {
  form: WizardForm;
  onChange: (patch: Partial<WizardForm>) => void;
}

/** Derive a shroud-config shorthand from a node's geometry block.
 *  e.g. {airGapMm: 1, ductHeightMm: 50} -> "ag1-h50"; {material: "epp"} -> "epp".
 *  Empty if no recognized geometry. */
function shroudFromGeometry(g: ResearchTreeNode['geometry']): string {
  const parts: string[] = [];
  if (g.airGapMm != null) parts.push(`ag${g.airGapMm}`);
  if (g.ductHeightMm != null) parts.push(`h${g.ductHeightMm}`);
  if (g.rodCountTop != null || g.rodCountBottom != null) {
    parts.push(`r${g.rodCountTop ?? '?'}-${g.rodCountBottom ?? '?'}`);
  }
  if (parts.length === 0 && g.material) parts.push(g.material);
  return parts.join('-');
}

/** Picker that surfaces "active" research-tree nodes (not done) across every
 *  configured tree and, on pick, autofills the wizard's key fields from the
 *  node. The link is sent as `research_tree_node_id` so the backend pushes
 *  results back on success (routed to whichever tree owns the id). */
export function ResearchTreeNodePicker({ form, onChange }: Props) {
  const [phases, setPhases] = useState<ResearchTreePhase[]>([]);
  const [nodes, setNodes] = useState<ResearchTreeNode[]>([]);
  const [trees, setTrees] = useState<ResearchTreeRef[]>([]);
  const [enabled, setEnabled] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [refresh, setRefresh] = useState(0);

  useEffect(() => {
    let cancelled = false;
    api.listResearchTreeNodes().then(
      (r) => {
        if (cancelled) return;
        setEnabled(r.enabled);
        setTrees(r.trees);
        setPhases(r.phases);
        // Hide nodes that are already 'done' — researcher wants active work.
        setNodes(r.nodes.filter((n) => n.status !== 'done'));
      },
      (e: Error | ApiError) => !cancelled && setError(e.message),
    );
    return () => { cancelled = true; };
  }, [refresh]);

  // Re-fetch when the user returns to this tab — they likely just edited the
  // tree in the research-tree editor (other tab/window), so pick up changes.
  useEffect(() => {
    const onFocus = () => setRefresh((n) => n + 1);
    window.addEventListener('focus', onFocus);
    return () => window.removeEventListener('focus', onFocus);
  }, []);

  if (!enabled) {
    return (
      <div className="text-xs text-gray-500 italic">
        Research-tree integration is disabled. Add at least one{' '}
        <code className="font-mono text-gray-300">[[research_trees]]</code> entry with{' '}
        <code className="font-mono text-gray-300">enabled = true</code> in
        <code className="font-mono text-gray-300"> config.toml</code> to use it.
      </div>
    );
  }
  if (error) {
    return (
      <div className="text-xs text-amber-400 bg-amber-500/10 border border-amber-500/30 rounded p-2">
        Research-tree unreachable: {error}. The capture will run without a tree link.
      </div>
    );
  }

  const selected = form.research_tree_node_id
    ? nodes.find((n) => n.id === form.research_tree_node_id) ?? null
    : null;

  const onSelect = (nodeId: string) => {
    if (nodeId === '') {
      onChange({ research_tree_node_id: null });
      return;
    }
    const node = nodes.find((n) => n.id === nodeId);
    if (!node) return;
    // Autofill key fields from the node. Don't overwrite values the user
    // has already typed — only fill empty slots so re-picking a node
    // doesn't blow away their edits.
    const patch: Partial<WizardForm> = { research_tree_node_id: nodeId };
    if (!form.propeller.trim() && node.geometry.propellerInches != null) {
      patch.propeller = `${node.geometry.propellerInches}in`;
    }
    if (!form.shroud.trim()) {
      const sh = shroudFromGeometry(node.geometry);
      if (sh) patch.shroud = sh;
    }
    if (!form.notes.trim()) patch.notes = node.id;
    onChange(patch);
  };

  // Group nodes by tree → phase → node. Trees are ordered as configured;
  // phases inside each tree follow their server order.
  const groups = trees.flatMap((t) =>
    phases
      .filter((p) => p.treeKey === t.name)
      .map((p) => ({
        tree: t,
        phase: p,
        items: nodes.filter((n) => n.treeKey === t.name && n.phaseId === p.id),
      }))
      .filter((g) => g.items.length > 0),
  );
  // optgroup labels include the tree only when more than one tree is in play —
  // single-tree deployments stay visually identical to before.
  const showTreeInLabel = trees.length > 1;

  return (
    <div className="space-y-2">
      <label className="block">
        <span className="text-xs uppercase tracking-wide text-gray-400">
          Linked research-tree node{' '}
          <span className="normal-case text-gray-500 text-[10px]">(optional)</span>
          <button
            type="button"
            onClick={(e) => { e.preventDefault(); setRefresh((n) => n + 1); }}
            className="ml-2 normal-case text-indigo-400 hover:text-indigo-300 text-[10px]"
            title="Re-fetch nodes from the research tree"
          >
            ↻ refresh
          </button>
        </span>
        <select
          className="input w-full mt-1"
          value={form.research_tree_node_id ?? ''}
          onChange={(e) => onSelect(e.target.value)}
        >
          <option value="">— none —</option>
          {groups.map((g) => (
            <optgroup
              key={`${g.tree.name}:${g.phase.id}`}
              label={showTreeInLabel ? `${g.tree.name} — ${g.phase.title}` : g.phase.title}
            >
              {g.items.map((n) => (
                <option key={n.id} value={n.id}>
                  {n.title} {n.status !== 'planned' ? `(${n.status})` : ''}
                </option>
              ))}
            </optgroup>
          ))}
        </select>
      </label>
      {selected && (
        <div className="text-[11px] text-gray-400 bg-gray-900/40 border border-gray-700 rounded p-2 space-y-0.5">
          <div className="text-gray-300">
            <span className="font-mono">{selected.id}</span> · {selected.title}
            {showTreeInLabel && (
              <span className="ml-2 text-emerald-300/80">[{selected.treeKey}]</span>
            )}
          </div>
          {selected.description && (
            <div className="text-gray-500 line-clamp-2">{selected.description}</div>
          )}
          <div className="text-gray-500">
            On successful capture: Results URL is pushed back to this node and its
            status flips to <span className="text-amber-300">in-progress</span>.
          </div>
        </div>
      )}
    </div>
  );
}
