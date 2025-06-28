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
            likes: 0,
            favorite: false,
        }));
        setAudioFiles((prev) => [...prev, ...newFiles]);
    };

    const handleLike = (idx) => {
        setAudioFiles((prev) =>
            prev.map((file, i) =>
                i === idx ? { ...file, likes: file.likes + 1 } : file
            )
        );
    };

    const handleFavorite = (idx) => {
        setAudioFiles((prev) =>
            prev.map((file, i) =>
                i === idx ? { ...file, favorite: !file.favorite } : file
            )
        );
    };

    return (
        <div
            style={{
                minHeight: "100vh",
                background: "#f3f6f8", // LinkedIn-like background
                display: "flex",
                justifyContent: "center",
                alignItems: "flex-start",
                padding: "40px 0",
            }}
        >
            <div
                style={{
                    background: "#fff",
                    borderRadius: "12px",
                    boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
                    padding: "32px 0 0 0",
                    width: "100%",
                    maxWidth: "600px",
                    border: "1px solid #e0e0e0",
                }}
            >
                <h1 style={{
                    textAlign: "center",
                    marginBottom: "24px",
                    color: "#222",
                    fontWeight: 700,
                    fontSize: "2rem",
                    letterSpacing: "-1px"
                }}>
                    Audio Feed
                </h1>
                <div style={{ padding: "0 32px 24px 32px", borderBottom: "1px solid #e0e0e0", marginBottom: "24px" }}>
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
                            margin: "0 auto",
                            padding: "10px 28px",
                            background: "#0a66c2",
                            color: "#fff",
                            border: "none",
                            borderRadius: "24px",
                            fontSize: "16px",
                            fontWeight: 600,
                            cursor: "pointer",
                            boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
                            transition: "background 0.2s",
                        }}
                    >
                        + Upload Audio
                    </button>
                </div>
                <div style={{ padding: "0 32px 32px 32px" }}>
                    {audioFiles.map((file, idx) => (
                        <div
                            key={idx}
                            style={{
                                margin: "0 0 32px 0",
                                padding: "20px",
                                borderRadius: "12px",
                                background: "#fff",
                                border: "1px solid #e0e0e0",
                                boxShadow: "0 1px 4px rgba(0,0,0,0.04)",
                                color: "#222",
                                display: "flex",
                                flexDirection: "column",
                                gap: "10px"
                            }}
                        >
                            <div style={{ display: "flex", alignItems: "center", marginBottom: "8px" }}>
                                <img
                                    src={`https://ui-avatars.com/api/?name=${encodeURIComponent(file.name)}&background=0a66c2&color=fff&rounded=true&size=40`}
                                    alt="avatar"
                                    style={{
                                        width: "40px",
                                        height: "40px",
                                        borderRadius: "50%",
                                        marginRight: "12px",
                                        border: "2px solid #e0e0e0"
                                    }}
                                />
                                <strong style={{ fontSize: "1.1rem", flex: 1 }}>{file.name}</strong>
                                <button
                                    onClick={() => handleFavorite(idx)}
                                    style={{
                                        background: "none",
                                        border: "none",
                                        color: file.favorite ? "#f9c846" : "#bbb",
                                        fontSize: "22px",
                                        cursor: "pointer",
                                        marginLeft: "8px"
                                    }}
                                    aria-label="Favorite"
                                    title={file.favorite ? "Unfavorite" : "Favorite"}
                                >
                                    {file.favorite ? "★" : "☆"}
                                </button>
                            </div>
                            {file.type.startsWith("audio") ? (
                                <audio controls src={file.url} style={{ width: "100%" }} />
                            ) : (
                                <video controls width="100%" src={file.url} />
                            )}
                            <div style={{ marginTop: "8px", display: "flex", alignItems: "center" }}>
                                <button
                                    onClick={() => handleLike(idx)}
                                    style={{
                                        background: "none",
                                        border: "none",
                                        color: "#e63946",
                                        fontSize: "20px",
                                        cursor: "pointer",
                                        marginRight: "8px"
                                    }}
                                    aria-label="Like"
                                >
                                    ❤️
                                </button>
                                <span style={{ fontWeight: 500 }}>{file.likes} {file.likes === 1 ? "Like" : "Likes"}</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default AudioFeed;