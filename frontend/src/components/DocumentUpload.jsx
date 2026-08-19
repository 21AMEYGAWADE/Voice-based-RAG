import { useState } from "react";

import axios from "axios";


const API_URL = "http://localhost:8000";


function DocumentUpload() {

  const [file, setFile] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [message, setMessage] =
    useState("");


  const uploadFile = async () => {

    if (!file) {

      alert("Please select a PDF.");

      return;

    }


    setLoading(true);

    setMessage("Uploading and processing...");


    try {

      const formData =
        new FormData();


      formData.append(
        "file",
        file
      );


      const response =
        await axios.post(
          `${API_URL}/api/documents/upload`,
          formData,
          {
            headers: {
              "Content-Type":
                "multipart/form-data"
            }
          }
        );


      const data =
        response.data.data;


      setMessage(
        `Uploaded ${data.filename} — ${data.chunks} chunks created.`
      );

    } catch (error) {

      console.error(error);

      setMessage(
        error.response?.data?.detail ||
        "Upload failed."
      );

    } finally {

      setLoading(false);

    }

  };


  return (

    <div>

      <input
        type="file"
        accept=".pdf"
        onChange={
          event =>
            setFile(
              event.target.files[0]
            )
        }
      />


      <button
        className="upload-button"
        onClick={uploadFile}
        disabled={loading}
      >

        {loading
          ? "Processing..."
          : "Upload PDF"
        }

      </button>


      {message && (

        <p className="upload-message">
          {message}
        </p>

      )}

    </div>

  );
}


export default DocumentUpload;