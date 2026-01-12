import { useState } from 'react';
import axios from 'axios';
import { Send, Github, Loader2, Database } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

// Connect to the backend using the variable we set in .env
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';

interface Message {
  role: 'user' | 'bot';
  content: string;
}

function App() {
  // State for the Ingestion UI
  const [repoUrl, setRepoUrl] = useState('');
  const [ingesting, setIngesting] = useState(false);
  const [ingestStatus, setIngestStatus] = useState('');

  // State for the Chat UI
  const [query, setQuery] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: 'bot', content: 'Repo loaded. Ask me anything about the code!' }
  ]);

  // 1. Function to handle Ingestion
  const handleIngest = async () => {
    if (!repoUrl) return;
    setIngesting(true);
    setIngestStatus('Cloning and indexing...');
    
    try {
      await axios.post(`${API_URL}/ingest`, { repo_url: repoUrl });
      setIngestStatus('Ingestion started! Give it 10-20 seconds to finish.');
    } catch (error) {
      console.error(error);
      setIngestStatus('Error ingesting repo. Check console.');
    } finally {
      setIngesting(false);
    }
  };

  // 2. Function to handle Chat
  const handleChat = async () => {
    if (!query.trim()) return;
    
    // Add user message immediately
    const newMessages: Message[] = [...messages, { role: 'user', content: query }];
    setMessages(newMessages);
    setQuery('');
    setChatLoading(true);

    try {
      // Send question to backend
      const res = await axios.post(`${API_URL}/chat`, { query });
      
      // Add bot response
      setMessages([...newMessages, { role: 'bot', content: res.data.response }]);
    } catch (error) {
      setMessages([...newMessages, { role: 'bot', content: "Error: Couldn't reach the AI." }]);
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-900 text-slate-100 font-sans">
      
      {/* --- Header / Ingestion Area --- */}
      <div className="p-6 border-b border-slate-700 bg-slate-800 shadow-md">
        <h1 className="text-2xl font-bold mb-4 flex items-center gap-2">
          <Database className="text-blue-400" /> Repo Runner
        </h1>
        
        <div className="flex gap-4 max-w-3xl">
          <input 
            type="text" 
            placeholder="https://github.com/username/repo"
            className="flex-1 px-4 py-2 rounded-lg bg-slate-900 border border-slate-600 focus:border-blue-400 focus:outline-none"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
          />
          <button 
            onClick={handleIngest}
            disabled={ingesting}
            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 px-6 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors"
          >
            {ingesting ? <Loader2 className="animate-spin" /> : <Github size={20} />}
            {ingesting ? 'Processing...' : 'Ingest Repo'}
          </button>
        </div>
        {ingestStatus && <p className="mt-2 text-sm text-green-400">{ingestStatus}</p>}
      </div>

      {/* --- Chat Area --- */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-3xl p-4 rounded-xl shadow-sm ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-100 border border-slate-600'}`}>
              <ReactMarkdown className="prose prose-invert max-w-none">
                {msg.content}
              </ReactMarkdown>
            </div>
          </div>
        ))}
        {chatLoading && (
           <div className="flex justify-start">
             <div className="bg-slate-700 p-4 rounded-xl border border-slate-600 flex items-center gap-2">
               <Loader2 className="animate-spin text-blue-400" size={18} /> Thinking...
             </div>
           </div>
        )}
      </div>

      {/* --- Input Area --- */}
      <div className="p-6 border-t border-slate-700 bg-slate-800">
        <div className="max-w-4xl mx-auto flex gap-4">
          <input 
            type="text" 
            placeholder="Ask a question about the codebase..."
            className="flex-1 px-4 py-3 rounded-lg bg-slate-900 border border-slate-600 focus:border-blue-400 focus:outline-none"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleChat()}
          />
          <button 
            onClick={handleChat}
            disabled={chatLoading}
            className="bg-green-600 hover:bg-green-500 disabled:opacity-50 px-6 rounded-lg transition-colors"
          >
            <Send size={20} />
          </button>
        </div>
      </div>

    </div>
  );
}

export default App;