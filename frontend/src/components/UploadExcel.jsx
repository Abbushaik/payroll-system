import { useState, useRef } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000";

export default function UploadExcel({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef();

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped && dropped.name.endsWith(".xlsx")) {
      setFile(dropped);
      setError("");
    } else {
      setError("Only .xlsx files are supported!");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select an Excel file first!");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
    try {
      setLoading(true);
      setError("");
      const res = await axios.post(`${API}/upload-excel`, formData);
      onUploadSuccess(res.data.employees);
    } catch (err) {
      setError("Failed to upload file. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto m-6">
      <div className="bg-white rounded-2xl shadow-lg p-8">
        {/* Step Label */}
        <div className="flex items-center gap-3 mb-6">
          <span className="bg-violet-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm">
            1
          </span>
          <h2 className="text-xl font-bold text-gray-700">
            Upload Employee Excel File
          </h2>
        </div>

        {/* Drag & Drop Zone */}
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          onClick={() => inputRef.current.click()}
          className={`border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all duration-300 ${
            dragging
              ? "border-violet-500 bg-violet-50 scale-105"
              : file
                ? "border-green-400 bg-green-50"
                : "border-purple-300 bg-purple-50 hover:border-violet-400 hover:bg-violet-50"
          }`}
        >
          <div className="text-5xl mb-3">
            {file ? "✅" : dragging ? "📂" : "📊"}
          </div>
          <p className="text-gray-600 font-medium">
            {file ? file.name : "Drag & Drop your Excel file here"}
          </p>
          <p className="text-gray-400 text-sm mt-1">
            {file ? "File ready to upload!" : "or click to browse — .xlsx only"}
          </p>
          <input
            ref={inputRef}
            type="file"
            accept=".xlsx"
            className="hidden"
            onChange={(e) => {
              setFile(e.target.files[0]);
              setError("");
            }}
          />
        </div>

        {error && (
          <p className="text-red-500 text-sm mt-3 flex items-center gap-1">
            ⚠️ {error}
          </p>
        )}

        <button
          onClick={handleUpload}
          disabled={loading || !file}
          className="mt-6 bg-gradient-to-r from-violet-600 to-indigo-600 text-white px-8 py-3 rounded-xl font-semibold hover:opacity-90 disabled:opacity-40 transition-all duration-200 shadow-md"
        >
          {loading ? "⏳ Uploading..." : "🚀 Upload & Process Excel"}
        </button>
      </div>
    </div>
  );
}
