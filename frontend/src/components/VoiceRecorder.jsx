import { useRef, useState } from "react";

import axios from "axios";


const API_URL = "http://localhost:8000";


function VoiceRecorder({
  setQuestion,
  setAnswer,
  setSources,
  setAudioUrl
}) {

  const mediaRecorderRef = useRef(null);

  const audioChunksRef = useRef([]);


  const [recording, setRecording] =
    useState(false);


  const [loading, setLoading] =
    useState(false);


  const startRecording = async () => {

    try {

      const stream =
        await navigator.mediaDevices.getUserMedia({
          audio: true
        });


      const mediaRecorder =
        new MediaRecorder(stream);


      mediaRecorderRef.current =
        mediaRecorder;


      audioChunksRef.current = [];


      mediaRecorder.ondataavailable =
        (event) => {

          if (event.data.size > 0) {

            audioChunksRef.current.push(
              event.data
            );

          }

        };


      mediaRecorder.onstop =
        async () => {

          const audioBlob =
            new Blob(
              audioChunksRef.current,
              {
                type: "audio/webm"
              }
            );


          await sendAudio(
            audioBlob
          );


          stream
            .getTracks()
            .forEach(
              track => track.stop()
            );

        };


      mediaRecorder.start();

      setRecording(true);

    } catch (error) {

      console.error(error);

      alert(
        "Microphone permission is required."
      );

    }

  };


  const stopRecording = () => {

    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state !== "inactive"
    ) {

      mediaRecorderRef.current.stop();

      setRecording(false);

    }

  };


  const sendAudio = async (
    audioBlob
  ) => {

    setLoading(true);

    setAnswer("");

    setSources([]);

    setAudioUrl("");


    try {

      const formData =
        new FormData();


      formData.append(
        "file",
        audioBlob,
        "question.webm"
      );


      const response =
        await axios.post(
          `${API_URL}/api/voice/ask`,
          formData,
          {
            headers: {
              "Content-Type":
                "multipart/form-data"
            }
          }
        );


      setQuestion(
        response.data.question
      );


      setAnswer(
        response.data.answer
      );


      setSources(
        response.data.sources
      );


      setAudioUrl(
        `${API_URL}${response.data.audio_url}`
      );

    } catch (error) {

      console.error(error);

      alert(
        error.response?.data?.detail ||
        "Something went wrong."
      );

    } finally {

      setLoading(false);

    }

  };


  return (

    <div className="voice-recorder">

      <button
        className={
          recording
            ? "record-button recording"
            : "record-button"
        }
        onClick={
          recording
            ? stopRecording
            : startRecording
        }
        disabled={loading}
      >

        {loading
          ? "⏳ Processing..."
          : recording
            ? "⏹ Stop Recording"
            : "🎤 Start Speaking"
        }

      </button>


      <p>

        {recording
          ? "Listening..."
          : loading
            ? "Searching documents and generating answer..."
            : "Click and speak your question"
        }

      </p>

    </div>

  );
}


export default VoiceRecorder;