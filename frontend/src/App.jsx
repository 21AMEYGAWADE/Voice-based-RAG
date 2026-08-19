import { useState } from "react";

import VoiceRecorder from "./components/VoiceRecorder";

import DocumentUpload from "./components/DocumentUpload";

import "./App.css";


function App() {

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [sources, setSources] = useState([]);

  const [audioUrl, setAudioUrl] = useState("");

  return (

    <div className="app">

      <header className="header">

        <h1>🎙️ Voice RAG</h1>

        <p>
          Ask questions about your documents using your voice.
        </p>

      </header>


      <main className="container">

        <section className="card">

          <h2>📄 Upload Knowledge</h2>

          <DocumentUpload />

        </section>


        <section className="card voice-card">

          <h2>🎤 Ask a Question</h2>

          <VoiceRecorder
            setQuestion={setQuestion}
            setAnswer={setAnswer}
            setSources={setSources}
            setAudioUrl={setAudioUrl}
          />

        </section>


        {question && (

          <section className="card">

            <h3>You asked:</h3>

            <p>{question}</p>

          </section>

        )}


        {answer && (

          <section className="card answer">

            <h2>🤖 AI Answer</h2>

            <p>{answer}</p>


            {sources.length > 0 && (

              <div className="sources">

                <h3>📚 Sources</h3>

                <ul>

                  {sources.map(
                    (source, index) => (

                      <li key={index}>
                        {source}
                      </li>

                    )
                  )}

                </ul>

              </div>

            )}


            {audioUrl && (

              <audio
                controls
                autoPlay
                src={audioUrl}
              />

            )}

          </section>

        )}

      </main>

    </div>

  );
}


export default App;