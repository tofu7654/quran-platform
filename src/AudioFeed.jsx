import React, { useState, useRef } from "react";

function AudioFeed() {
    const [audioFiles, setAudioFiles] = useState([]);
    const fileInputRef = useRef(null);

    const handleUpload = (event) => {
        const files = Array.from(event.target.files);
        const newFiles = files.map((file) => ({
            url: URL.createObjectURL(file),
            name: file.name,
            type: file.type,
        }));
        setAudioFiles((prev) => [...prev, ...newFiles]);
    };

    return (
        <div
            style={{
                minHeight: "100vh",
                display: "flex",
                justifyContent: "center",
                alignItems: "center", // changed from "flex-start" to "center"
                background: "#23272f",
            }}
        >
            <div
                style={{
                    background: "#2c2f36",
                    borderRadius: "12px",
                    boxShadow: "0 2px 16px rgba(0,0,0,0.18)",
                    padding: "32px 24px",
                    width: "100%",
                    maxWidth: "480px",
                }}
            >
                <h1 style={{ 
                    textAlign: "center", 
                    marginBottom: "24px",
                    color: "#fff"
                }}>
                    Audio Feed
                </h1>
                <input
                    type="file"
                    accept="audio/mp3, audio/mpeg, audio/mp4, audio/*, video/mp4"
                    multiple
                    onChange={handleUpload}
                    style={{ display: "none" }}
                    ref={fileInputRef}
                />
                <button
                    onClick={() => fileInputRef.current.click()}
                    style={{
                        display: "block",
                        margin: "0 auto 32px auto",
                        padding: "10px 24px",
                        background: "#007bff",
                        color: "#fff",
                        border: "none",
                        borderRadius: "6px",
                        fontSize: "16px",
                        cursor: "pointer",
                        boxShadow: "0 1px 4px rgba(0,0,0,0.12)",
                    }}
                >
                    Upload Audio
                </button>
                <div>
                    {audioFiles.map((file, idx) => (
                        <div
                            key={idx}
                            style={{
                                margin: "20px 0",
                                padding: "16px",
                                borderRadius: "8px",
                                background: "#23272f",
                                boxShadow: "0 1px 4px rgba(0,0,0,0.10)",
                                color: "#fff"
                            }}
                        >
                            <strong>{file.name}</strong>
                            <br />
                            {file.type.startsWith("audio") ? (
                                <audio controls src={file.url} style={{ width: "100%", background: "#23272f" }} />
                            ) : (
                                <video controls width="100%" src={file.url} style={{ background: "#23272f" }} />
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default AudioFeed;