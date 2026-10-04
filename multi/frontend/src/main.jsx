import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const MODELS = ['GPT', 'Gemini', 'Claude', 'Ollama'];

function App() {
  const [selected, setSelected] = useState(['GPT', 'Gemini']);
  const [prompt, setPrompt] = useState('');
  const [responses, setResponses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [chosen, setChosen] = useState(null);

  const toggle = (model) => {
    setSelected((current) => current.includes(model)
      ? current.filter((item) => item !== model)
      : [...current, model]);
  };

  const compare = async () => {
    if (!prompt.trim() || selected.length < 2) return;
    setLoading(true);
    setChosen(null);
    try {
      const result = await fetch('http://localhost:8000/api/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, models: selected })
      });
      const data = await result.json();
      setResponses(data.responses || []);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app">
      <section className="hero">
        <span className="eyebrow">AI MODEL ARENA · MVP</span>
        <h1>One task. Multiple AIs.<br /><span>Choose the best answer.</span></h1>
        <p>Run the same task across AI systems, compare their responses, and continue with the output you prefer.</p>
      </section>

      <section className="panel">
        <h2>1. Select AI models</h2>
        <div className="models">
          {MODELS.map((model) => (
            <button className={selected.includes(model) ? 'model selected' : 'model'} key={model} onClick={() => toggle(model)}>
              <span className="check">{selected.includes(model) ? '✓' : ''}</span>{model}
            </button>
          ))}
        </div>
      </section>

      <section className="panel">
        <h2>2. Give them the same task</h2>
        <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Enter your task or prompt..." />
        <button className="run" disabled={loading || selected.length < 2} onClick={compare}>
          {loading ? 'Running models…' : 'Compare responses →'}
        </button>
      </section>

      {responses.length > 0 && (
        <section className="results">
          <div className="results-head">
            <div><span className="eyebrow">RESULTS</span><h2>Compare the responses</h2></div>
            <span>{responses.length} models</span>
          </div>
          <div className="cards">
            {responses.map((response) => (
              <article className={chosen === response.model ? 'response chosen' : 'response'} key={response.model}>
                <div className="response-top"><h3>{response.model}</h3><small>{response.latency_ms} ms</small></div>
                <p>{response.error || response.output}</p>
                <button onClick={() => setChosen(response.model)} className="select">{chosen === response.model ? '✓ Selected' : 'Select this response'}</button>
              </article>
            ))}
          </div>
          {chosen && <div className="continue">Selected: <strong>{chosen}</strong><button onClick={() => alert('Continuation flow will be added in the next task.')}>Continue with this output →</button></div>}
        </section>
      )}
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);
