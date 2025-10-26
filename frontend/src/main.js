import htm from 'https://unpkg.com/htm@3.1.0/dist/htm.module.js'
import React from 'https://unpkg.com/react@18/umd/react.development.js'
import ReactDOM from 'https://unpkg.com/react-dom@18/umd/react-dom.development.js'
const html = htm.bind(React.createElement)

function App(){
  const [tab, setTab] = React.useState('chat')
  const [token, setToken] = React.useState(localStorage.getItem('inderai_token')||'')
  return html`<div className="max-w-4xl mx-auto">
    <header className="mb-4">
      <h1 className="text-2xl font-bold">InderAI — Complete Demo</h1>
      <nav className="mt-2">
        <button className="mr-2" onClick=${()=>setTab('chat')}>Chat</button>
        <button className="mr-2" onClick=${()=>setTab('draft')}>Draft</button>
        <button className="mr-2" onClick=${()=>setTab('simulate')}>Simulator</button>
        <button className="mr-2" onClick=${()=>setTab('admin')}>Admin</button>
      </nav>
    </header>
    <main className="bg-white p-4 rounded shadow">
      ${tab === 'chat' ? html`<${Chat} token=${token} />` : null}
      ${tab === 'draft' ? html`<${Draft} token=${token} />` : null}
      ${tab === 'simulate' ? html`<${Simulator} />` : null}
      ${tab === 'admin' ? html`<${Admin} token=${token} setToken=${setToken} />` : null}
    </main>
  </div>`
}

function Chat({token}){
  const [msg,setMsg]=React.useState('mau saran pick hero yang nge-synergy');
  const [out,setOut]=React.useState('');
  const [history,setHistory]=React.useState(JSON.parse(localStorage.getItem('inderai_history')||'[]'))
  async function send(){
    setOut('loading...')
    const r = await fetch('/api/chat/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:'demo',message:msg})})
    const j = await r.json(); setOut(JSON.stringify(j,null,2))
    const h = [...history, {q:msg, a:j.response_text, t:new Date().toISOString()}]
    setHistory(h); localStorage.setItem('inderai_history', JSON.stringify(h))
  }
  return html`<div>
    <h2 className="text-xl font-semibold">Chat Coach</h2>
    <textarea className="w-full border p-2" rows=4 value=${msg} onInput=${e=>setMsg(e.target.value)}></textarea>
    <div className="mt-2"><button className="px-3 py-1 bg-blue-500 text-white rounded" onClick=${send}>Kirim</button></div>
    <pre className="mt-2 bg-gray-50 p-2">${out}</pre>
    <h3 className="mt-4">History</h3>
    <pre className="bg-gray-100 p-2">${JSON.stringify(history.slice(-10), null, 2)}</pre>
  </div>`
}

function Draft({token}){
  const [game,setGame]=React.useState('mlbb');
  const [avail,setAvail]=React.useState('Yu Zhong,Lesley,Valir');
  const [out,setOut]=React.useState('');
  async function ask(){
    const res = await fetch('/api/draft/suggest',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({game,available:avail.split(',').map(s=>s.trim())})})
    const j = await res.json(); setOut(JSON.stringify(j, null, 2))
  }
  return html`<div>
    <h2 className="text-xl font-semibold">Draft Tool</h2>
    <div className="mt-2">Game: <input className="border p-1" value=${game} onInput=${e=>setGame(e.target.value)}/></div>
    <div className="mt-2">Available: <input className="border p-1 w-full" value=${avail} onInput=${e=>setAvail(e.target.value)}/></div>
    <div className="mt-2"><button className="px-3 py-1 bg-green-500 text-white rounded" onClick=${ask}>Minta Saran</button></div>
    <pre className="mt-2 bg-gray-50 p-2">${out}</pre>
  </div>`
}

function Simulator(){
  const [out,setOut]=React.useState('')
  async function run(){
    const res = await fetch('/api/simulate/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({game:'mlbb',compA:['Yu Zhong','Lesley','Valir'],compB:['Lunox','Esmeralda','Gusion'],iterations:200})})
    const j = await res.json(); setOut(JSON.stringify(j,null,2))
  }
  return html`<div>
    <h2 className="text-xl font-semibold">Simulator</h2>
    <button className="px-3 py-1 bg-purple-500 text-white rounded" onClick=${run}>Run Simulation</button>
    <pre className="mt-2 bg-gray-50 p-2">${out}</pre>
  </div>`
}

function Admin({token,setToken}){
  const [modules,setModules]=React.useState([])
  const [u,setU]=React.useState(''); const [p,setP]=React.useState('')
  async function list(){
    const r = await fetch('/api/admin/list_modules'); const j = await r.json(); setModules(j.modules)
  }
  async function login(){
    const fd = new URLSearchParams(); fd.append('username', u); fd.append('password', p); fd.append('grant_type','password')
    const r = await fetch('/api/auth/token', {method:'POST', body: fd})
    if(r.ok){ const j = await r.json(); localStorage.setItem('inderai_token', j.access_token); setToken(j.access_token); alert('Logged in') } else { alert('Login failed') }
  }
  React.useEffect(()=>{list()},[])
  return html`<div>
    <h2 className="text-xl font-semibold">Admin</h2>
    <div className="mt-2">Installed modules: <pre>${JSON.stringify(modules,null,2)}</pre></div>
    <div className="mt-2">Login as admin: <input placeholder="username" value=${u} onInput=${e=>setU(e.target.value)}/> <input placeholder="password" type="password" value=${p} onInput=${e=>setP(e.target.value)}/> <button className="ml-2 px-2 py-1 bg-gray-700 text-white" onClick=${login}>Login</button></div>
    <div className="mt-2"><button className="px-3 py-1 bg-yellow-500 text-white rounded" onClick=${()=>fetch('/api/admin/rebuild_index',{headers:{'Authorization':'Bearer '+(localStorage.getItem('inderai_token')||'')}}).then(r=>r.json()).then(j=>alert(JSON.stringify(j)))}>Rebuild Index</button></div>
  </div>`
}

ReactDOM.render(html`<${App}/>`, document.getElementById('root'))
