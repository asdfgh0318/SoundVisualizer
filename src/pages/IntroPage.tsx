import { Link } from 'react-router-dom';
import { Card } from '../components/ui/Card';
import { CREDITS, FUNDING, PROJECT } from '../content/projectInfo';

export function IntroPage() {
  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <header className="pt-4">
        <h1 className="text-3xl font-bold text-white">{PROJECT.name}</h1>
        <p className="text-base text-gray-300 mt-2">{PROJECT.tagline}</p>
        <div className="flex flex-wrap items-center gap-3 mt-4">
          <Link
            to="/setup"
            className="px-4 py-2 rounded-md text-sm font-medium bg-indigo-600 hover:bg-indigo-500 text-white transition-colors"
          >
            Start with Setup →
          </Link>
          <a
            href={PROJECT.githubUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 rounded-md text-sm font-medium border border-gray-600 text-gray-200 hover:bg-gray-700 transition-colors"
          >
            Source on GitHub ↗
          </a>
        </div>
      </header>

      <Card title="What it does">
        <div className="space-y-3 text-sm text-gray-300 leading-relaxed">
          {PROJECT.description.map((p, i) => <p key={i}>{p}</p>)}
        </div>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card title="Who it is for">
          <ul className="list-disc pl-5 space-y-2 text-sm text-gray-300">
            {PROJECT.audience.map((a, i) => <li key={i}>{a}</li>)}
          </ul>
        </Card>
        <Card title="How a session flows">
          <ol className="space-y-3 text-sm text-gray-300">
            {PROJECT.workflow.map((w, i) => (
              <li key={w.step} className="flex gap-3">
                <span className="shrink-0 w-6 h-6 rounded-full bg-indigo-600/30 border border-indigo-500/60 text-indigo-200 text-xs flex items-center justify-center font-mono">
                  {i + 1}
                </span>
                <div>
                  <Link to={`/${w.step.toLowerCase()}`} className="font-semibold text-gray-100 hover:text-indigo-300">
                    {w.step}
                  </Link>
                  <span className="text-gray-400"> — {w.text}</span>
                </div>
              </li>
            ))}
          </ol>
        </Card>
      </div>

      <Card title="Project information">
        <dl className="grid grid-cols-1 sm:grid-cols-[12rem_1fr] gap-x-6 gap-y-2 text-sm">
          <dt className="text-gray-500 uppercase tracking-wide text-xs pt-0.5">Institution</dt>
          <dd className="text-gray-200">{PROJECT.institution}</dd>
          <dt className="text-gray-500 uppercase tracking-wide text-xs pt-0.5">Funding programme</dt>
          <dd className="text-gray-200">{FUNDING.programme}</dd>
          <dt className="text-gray-500 uppercase tracking-wide text-xs pt-0.5">Project title</dt>
          <dd className="text-gray-200">{FUNDING.projectTitle}</dd>
          <dt className="text-gray-500 uppercase tracking-wide text-xs pt-0.5">Grant number</dt>
          <dd className="text-gray-200 font-mono">{FUNDING.grantNumber}</dd>
          <dt className="text-gray-500 uppercase tracking-wide text-xs pt-0.5">Beneficiary</dt>
          <dd className="text-gray-200">{FUNDING.beneficiary}</dd>
          <dt className="text-gray-500 uppercase tracking-wide text-xs pt-0.5">Source code</dt>
          <dd>
            <a href={PROJECT.githubUrl} target="_blank" rel="noopener noreferrer" className="text-indigo-300 hover:text-indigo-200 underline">
              {PROJECT.githubUrl.replace('https://', '')}
            </a>
          </dd>
        </dl>
        {FUNDING.note && <p className="text-xs text-amber-400/90 mt-4">{FUNDING.note}</p>}
      </Card>

      <Card title="Third-party code">
        <ul className="space-y-1.5 text-sm text-gray-300">
          {CREDITS.map((c) => (
            <li key={c.url}>
              {c.what}:{' '}
              <a href={c.url} target="_blank" rel="noopener noreferrer" className="text-indigo-300 hover:text-indigo-200 underline">
                {c.who}
              </a>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
}
