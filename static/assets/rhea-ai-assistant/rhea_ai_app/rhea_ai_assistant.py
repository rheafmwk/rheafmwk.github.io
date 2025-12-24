#!/usr/bin/env python3
"""
rhea.framework AI Assistant
A local AI-powered assistant for team leadership knowledge.
"""

import os
import sys
import re
import webbrowser
import threading
import time
from pathlib import Path

# Configuration
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")
CHROMA_DB_PATH = os.environ.get("CHROMA_DB_PATH", "./chroma_db")
PORT = int(os.environ.get("PORT", 5050))

# Base URL for rhea.framework (can be local or remote)
RHEA_BASE_URL = os.environ.get("RHEA_BASE_URL", "https://rheafmwk.io")

def install_package(package):
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])

def ensure_dependencies():
    packages_to_check = [
        ('flask', 'flask'),
        ('chromadb', 'chromadb'),
        ('langchain_community', 'langchain-community'),
        ('langchain_core', 'langchain-core'),
        ('gpt4all', 'gpt4all'),
    ]
    missing = []
    for module_name, pip_name in packages_to_check:
        try:
            __import__(module_name)
        except ImportError:
            missing.append(pip_name)
    if missing:
        print(f"📦 Installing missing packages: {', '.join(missing)}")
        for pkg in missing:
            try:
                install_package(pkg)
                print(f"   ✅ {pkg}")
            except Exception as e:
                print(f"   ❌ Failed to install {pkg}: {e}")
                sys.exit(1)
        print()

ensure_dependencies()

from flask import Flask, render_template_string, request, jsonify
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

app = Flask(__name__)

vectorstore = None
rag_chain = None

# Mapping from doc_id prefixes to core flow pages
CORE_FLOW_MAPPING = {
    # PTI - Prototype Team Identity
    'V_': ('pti', 'Prototype Team Identity'),
    'T_': ('pti', 'Prototype Team Identity'),
    'I_': ('pti', 'Prototype Team Identity'),
    'CC_': ('pti', 'Prototype Team Identity'),
    'TB_': ('pti', 'Prototype Team Identity'),
    'RM_': ('pti', 'Prototype Team Identity'),
    
    # OFC - Organize for Complexity
    'TD_': ('ofc', 'Organize for Complexity'),
    'O_': ('ofc', 'Organize for Complexity'),
    'A_': ('ofc', 'Organize for Complexity'),
    
    # FTC - Facilitate Team Cohesion
    'C_': ('ftc', 'Facilitate Team Cohesion'),
    'CR_': ('ftc', 'Facilitate Team Cohesion'),
    'MC_': ('ftc', 'Facilitate Team Cohesion'),
    'PP_': ('ftc', 'Facilitate Team Cohesion'),
    
    # STE - Structure for Task Effectiveness
    'P_': ('ste', 'Structure Task Effectiveness'),
    'R_': ('ste', 'Structure Task Effectiveness'),
    'M_': ('ste', 'Structure Task Effectiveness'),
    'ID_': ('ste', 'Structure Task Effectiveness'),
    'WT_': ('ste', 'Structure Task Effectiveness'),
}

def get_core_flow_link(doc_id):
    """Get the core flow page link based on doc_id prefix."""
    if not doc_id:
        return None, None
    for prefix, (page, name) in CORE_FLOW_MAPPING.items():
        if doc_id.startswith(prefix):
            return f"{RHEA_BASE_URL}/{page}.html", name
    return None, None

def get_vectorstore():
    global vectorstore
    if vectorstore is None:
        db_path = Path(CHROMA_DB_PATH)
        if not db_path.exists():
            raise FileNotFoundError(f"ChromaDB not found at {CHROMA_DB_PATH}.")
        print(f"📚 Loading knowledge base...")
        vectorstore = Chroma(
            persist_directory=str(db_path),
            embedding_function=GPT4AllEmbeddings()
        )
        print("✅ Knowledge base loaded!")
    return vectorstore

def get_rag_chain():
    global rag_chain
    if rag_chain is None:
        print(f"🤖 Connecting to Ollama ({OLLAMA_MODEL})...")
        try:
            llm = Ollama(base_url=OLLAMA_BASE_URL, model=OLLAMA_MODEL)
            llm.invoke("test")
            print("✅ Connected!")
        except Exception as e:
            raise ConnectionError(f"Could not connect to Ollama: {e}")
        
        retriever = get_vectorstore().as_retriever(search_kwargs={"k": 4})
        
        template = """You are an expert assistant for the rhea.framework, focusing on team leadership in ICT projects.
Use the context to answer the question. Be concise and helpful. If you don't know, say so.

Context:
{context}

Question: {question}

Answer:"""

        prompt = PromptTemplate.from_template(template)
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        print("✅ Ready!")
    return rag_chain

def query_with_sources(question):
    vs = get_vectorstore()
    chain = get_rag_chain()
    answer = chain.invoke(question)
    docs = vs.similarity_search(question, k=4)
    return answer, docs

def format_sources(docs):
    sources = []
    seen = set()
    for doc in docs:
        source = doc.metadata.get("source", "")
        doc_id = source
        
        # Clean up title
        title = re.sub(r'^.*?_', '', source)
        if title.endswith('.txt'):
            title = title[:-4]
        title = title.replace("_", " ")
        
        # Get link to core flow page
        link, core_flow = get_core_flow_link(doc_id)
        
        if title not in seen:
            seen.add(title)
            sources.append({
                "title": title,
                "link": link,
                "coreFlow": core_flow
            })
    return sources

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>rhea.framework AI Assistant</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f8f9fa;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .container {
            max-width: 700px;
            width: 100%;
            margin: 0 auto;
            padding: 20px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        .header {
            text-align: center;
            padding: 40px 0 30px;
        }
        .header svg {
            width: 60px;
            height: 52px;
        }
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px 0;
        }
        .message {
            margin-bottom: 20px;
            line-height: 1.6;
        }
        .message.user {
            color: #495057;
        }
        .message.user::before {
            content: "You: ";
            font-weight: 600;
        }
        .message.assistant {
            color: #212529;
        }
        .sources {
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid #dee2e6;
        }
        .sources-label {
            font-size: 0.8rem;
            color: #6c757d;
            margin-bottom: 6px;
        }
        .source-link {
            display: inline-block;
            font-size: 0.85rem;
            color: #17a2b8;
            text-decoration: none;
            margin-right: 12px;
            margin-bottom: 4px;
            cursor: pointer;
        }
        .source-link:hover {
            text-decoration: underline;
        }
        .source-tag {
            font-size: 0.7rem;
            color: #6c757d;
        }
        .input-area {
            padding: 20px 0;
            border-top: 1px solid #dee2e6;
        }
        .input-wrapper {
            display: flex;
            gap: 8px;
            background: #fff;
            border: 1px solid #ced4da;
            border-radius: 24px;
            padding: 8px 8px 8px 20px;
        }
        .input-wrapper:focus-within {
            border-color: #17a2b8;
            box-shadow: 0 0 0 2px rgba(23, 162, 184, 0.15);
        }
        input[type="text"] {
            flex: 1;
            border: none;
            outline: none;
            font-size: 1rem;
            background: transparent;
        }
        button {
            width: 40px;
            height: 40px;
            border: none;
            border-radius: 50%;
            background: #212529;
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        button:hover {
            background: #343a40;
        }
        button:disabled {
            background: #adb5bd;
            cursor: not-allowed;
        }
        button svg {
            width: 18px;
            height: 18px;
        }
        .loading {
            color: #6c757d;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="883.7497 395 285 244.51282" width="285" height="244.51282">
              <g id="Canvas_1" fill-opacity="1" stroke-dasharray="none" stroke="none" stroke-opacity="1" fill="none">
                <g id="Canvas_1_Layer_1">
                  <g id="Graphic_56">
                    <path d="M 1110.996 637.5128 L 941.5027 637.5128 C 923.8296 637.5128 909.5027 623.1859 909.5027 605.5128 C 909.5027 599.8404 911.0105 594.26985 913.8718 589.3719 L 998.6174 444.29964 C 1007.5318 429.0395 1027.1291 423.89523 1042.3893 432.80963 C 1047.144 435.58716 1051.1016 439.54466 1053.8792 444.29936 L 1138.6268 589.3716 C 1147.5413 604.63166 1142.3972 624.2291 1127.1372 633.1436 C 1122.2391 636.0049 1116.6685 637.5128 1110.996 637.5128 Z" stroke="#464646" stroke-linecap="round" stroke-linejoin="round" stroke-width="4"/>
                  </g>
                  <g id="Graphic_55">
                    <circle cx="975.7497" cy="542" r="20.0000319580379" fill="#ffcb2c"/>
                  </g>
                  <g id="Graphic_54">
                    <circle cx="1078.7497" cy="542" r="20.0000319580379" fill="#d5003a"/>
                  </g>
                  <g id="Graphic_53">
                    <circle cx="1027.2497" cy="542" r="20.0000319580379" fill="#77007b"/>
                  </g>
                </g>
              </g>
            </svg>
        </div>
        
        <div class="messages" id="messages"></div>
        
        <div class="input-area">
            <form id="form" class="input-wrapper">
                <input type="text" id="input" placeholder="Ask about team leadership..." autocomplete="off">
                <button type="submit" id="submit">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 19V5M5 12l7-7 7 7"/>
                    </svg>
                </button>
            </form>
        </div>
    </div>

    <script>
        const form = document.getElementById('form');
        const input = document.getElementById('input');
        const messages = document.getElementById('messages');
        const submitBtn = document.getElementById('submit');

        function addMessage(content, type, sources) {
            const div = document.createElement('div');
            div.className = 'message ' + type;
            
            // Create text content
            const textSpan = document.createElement('span');
            textSpan.innerHTML = content.replace(/\\n/g, '<br>');
            div.appendChild(textSpan);
            
            // Add sources if available
            if (sources && sources.length > 0) {
                const sourcesDiv = document.createElement('div');
                sourcesDiv.className = 'sources';
                
                const label = document.createElement('div');
                label.className = 'sources-label';
                label.textContent = 'References:';
                sourcesDiv.appendChild(label);
                
                sources.forEach(function(s) {
                    if (s.link) {
                        const a = document.createElement('a');
                        a.className = 'source-link';
                        a.href = s.link;
                        a.target = '_blank';
                        a.rel = 'noopener noreferrer';
                        a.textContent = s.title;
                        if (s.coreFlow) {
                            const tag = document.createElement('span');
                            tag.className = 'source-tag';
                            tag.textContent = ' (' + s.coreFlow + ')';
                            a.appendChild(tag);
                        }
                        sourcesDiv.appendChild(a);
                    } else {
                        const span = document.createElement('span');
                        span.className = 'source-link';
                        span.textContent = s.title;
                        sourcesDiv.appendChild(span);
                    }
                });
                
                div.appendChild(sourcesDiv);
            }
            
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }

        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const q = input.value.trim();
            if (!q) return;
            
            addMessage(q, 'user', null);
            input.value = '';
            submitBtn.disabled = true;
            
            const loading = document.createElement('div');
            loading.className = 'message loading';
            loading.textContent = 'Thinking...';
            messages.appendChild(loading);
            
            try {
                const res = await fetch('/query', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query: q})
                });
                const data = await res.json();
                loading.remove();
                
                if (data.error) {
                    addMessage('Error: ' + data.error, 'assistant', null);
                } else {
                    addMessage(data.answer, 'assistant', data.sources);
                }
            } catch (err) {
                loading.remove();
                addMessage('Error connecting. Is Ollama running?', 'assistant', null);
            }
            
            submitBtn.disabled = false;
            input.focus();
        });

        input.focus();
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.json
        question = data.get('query', '').strip()
        if not question:
            return jsonify({"error": "Please provide a question"})
        answer, docs = query_with_sources(question)
        sources = format_sources(docs)
        return jsonify({"answer": answer, "sources": sources})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/health')
def health():
    try:
        get_vectorstore()
        get_rag_chain()
        return jsonify({"healthy": True})
    except Exception as e:
        return jsonify({"healthy": False, "message": str(e)})

def open_browser():
    time.sleep(1.5)
    webbrowser.open(f'http://localhost:{PORT}')

def main():
    print("\n" + "="*50)
    print("  rhea.framework AI Assistant")
    print("="*50)
    print(f"\n  http://localhost:{PORT}")
    print(f"  Model: {OLLAMA_MODEL}")
    print("\n" + "="*50 + "\n")
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == '__main__':
    main()
