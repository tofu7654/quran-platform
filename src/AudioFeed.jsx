import React, { useState, useRef } from "react";
import FavoritesFeed from "./FavoritesFeed";

function AudioFeed({ user, onSignOut }) {
    const [audioFiles, setAudioFiles] = useState([]);
    const [likedIndexes, setLikedIndexes] = useState([]); // Track liked posts
    const [showModal, setShowModal] = useState(false);
    const [form, setForm] = useState({ name: "", location: "", file: null });
    const [dragActive, setDragActive] = useState(false);
    const [showFavorites, setShowFavorites] = useState(false);
    const fileInputRef = useRef(null);

    const handleModalOpen = () => setShowModal(true);
    const handleModalClose = () => {
        setShowModal(false);
        setForm({ name: "", location: "", file: null });
        setDragActive(false);
    };

    const handleFormChange = (e) => {
        const { name, value } = e.target;
        setForm((prev) => ({ ...prev, [name]: value }));
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) setForm((prev) => ({ ...prev, file }));
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setDragActive(false);
        const file = e.dataTransfer.files[0];
        if (file) setForm((prev) => ({ ...prev, file }));
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setDragActive(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setDragActive(false);
    };

    const handleUpload = (e) => {
        e.preventDefault();
        if (!form.name || !form.location || !form.file) return;
        const file = form.file;
        const newFile = {
            url: URL.createObjectURL(file),
            name: form.name,
            location: form.location,
            type: file.type,
            likes: 0,
            favorite: false,
        };
        setAudioFiles((prev) => [...prev, newFile]);
        handleModalClose();
    };

    const handleLike = (idx) => {
        if (likedIndexes.includes(idx)) return; // Prevent multiple likes
        setAudioFiles((prev) =>
            prev.map((file, i) =>
                i === idx ? { ...file, likes: file.likes + 1 } : file
            )
        );
        setLikedIndexes((prev) => [...prev, idx]);
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
                width: "100vw",
                background: "#f3f6f8",
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
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "0 32px" }}>
                    <div style={{
                        width: "240px",      // Increased width
                        height: "120px",     // Increased height
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "flex-start",
                    }}>
                        <img
                            src="/logo.png"
                            alt="Logo"
                            style={{
                                maxWidth: "220px",   // Increased max width
                                maxHeight: "110px",  // Increased max height
                                objectFit: "contain",
                                display: "block",
                            }}
                        />
                    </div>
                    <button
                        onClick={onSignOut}
                        style={{
                            padding: "8px 18px",
                            background: "#fff",
                            color: "#1db954", // green
                            border: "1px solid #1db954", // green
                            borderRadius: "24px",
                            fontSize: "15px",
                            fontWeight: 600,
                            cursor: "pointer",
                            marginLeft: "12px",
                            boxShadow: "0 1px 4px rgba(0,0,0,0.03)",
                            transition: "background 0.2s",
                        }}
                    >
                        Sign Out
                    </button>
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "0 32px 24px 32px", borderBottom: "1px solid #e0e0e0", marginBottom: "24px" }}>
                    <button
                        onClick={handleModalOpen}
                        style={{
                            padding: "10px 28px",
                            background: "#1db954", // green
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
                    <button
                        onClick={() => setShowFavorites(true)}
                        style={{
                            padding: "10px 20px",
                            background: "#fff",
                            color: "#1db954", // green
                            border: "1px solid #1db954", // green
                            borderRadius: "24px",
                            fontSize: "16px",
                            fontWeight: 600,
                            cursor: "pointer",
                            marginLeft: "12px",
                            boxShadow: "0 1px 4px rgba(0,0,0,0.03)",
                            transition: "background 0.2s",
                        }}
                    >
                        ★ Favorites
                    </button>
                </div>
                {/* Modal */}
                {showModal && (
                    <div style={{
                        position: "fixed",
                        top: 0, left: 0, right: 0, bottom: 0,
                        background: "rgba(0,0,0,0.3)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        zIndex: 1000
                    }}>
                        <form
                            onSubmit={handleUpload}
                            style={{
                                background: "#fff",
                                borderRadius: "12px",
                                padding: "32px",
                                minWidth: "320px",
                                boxShadow: "0 4px 24px rgba(0,0,0,0.15)",
                                display: "flex",
                                flexDirection: "column",
                                gap: "18px",
                                position: "relative"
                            }}
                            onDrop={handleDrop}
                            onDragOver={handleDragOver}
                            onDragLeave={handleDragLeave}
                        >
                            <button
                                type="button"
                                onClick={handleModalClose}
                                style={{
                                    position: "absolute",
                                    top: "12px",
                                    right: "16px",
                                    background: "none",
                                    border: "none",
                                    fontSize: "22px",
                                    color: "#888",
                                    cursor: "pointer"
                                }}
                                aria-label="Close"
                            >×</button>
                            <h2 style={{ margin: 0, color: "#222", fontWeight: 600 }}>Upload Quran Recording</h2>
                            <input
                                type="text"
                                name="name"
                                placeholder="Name"
                                value={form.name}
                                onChange={handleFormChange}
                                required
                                style={{
                                    padding: "10px",
                                    borderRadius: "6px",
                                    border: "1px solid #ccc",
                                    fontSize: "16px"
                                }}
                            />
                            <input
                                type="text"
                                name="location"
                                placeholder="Location"
                                value={form.location}
                                onChange={handleFormChange}
                                required
                                style={{
                                    padding: "10px",
                                    borderRadius: "6px",
                                    border: "1px solid #ccc",
                                    fontSize: "16px"
                                }}
                            />
                            <div
                                style={{
                                    border: dragActive ? "2px dashed #1db954" : "2px dashed #bbb",
                                    borderRadius: "8px",
                                    padding: "24px",
                                    textAlign: "center",
                                    background: dragActive ? "#eafbe7" : "#fafbfc", // light green background when active
                                    color: "#222",
                                    cursor: "pointer",
                                    transition: "border 0.2s, background 0.2s"
                                }}
                                onClick={() => fileInputRef.current.click()}
                                onDragOver={handleDragOver}
                                onDragLeave={handleDragLeave}
                                onDrop={handleDrop}
                            >
                                {form.file ? (
                                    <span>{form.file.name}</span>
                                ) : (
                                    <span>
                                        Drag &amp; drop Quran audio here, or <span style={{ color: "#1db954", textDecoration: "underline" }}>browse</span>
                                    </span>
                                )}
                                <input
                                    type="file"
                                    accept="audio/mp3, audio/mpeg, audio/mp4, audio/*, video/mp4"
                                    style={{ display: "none" }}
                                    ref={fileInputRef}
                                    onChange={handleFileChange}
                                />
                            </div>
                            <button
                                type="submit"
                                disabled={!form.name || !form.location || !form.file}
                                style={{
                                    padding: "10px 0",
                                    background: (!form.name || !form.location || !form.file) ? "#bbb" : "#1db954", // green
                                    color: "#fff",
                                    border: "none",
                                    borderRadius: "24px",
                                    fontSize: "16px",
                                    fontWeight: 600,
                                    cursor: (!form.name || !form.location || !form.file) ? "not-allowed" : "pointer",
                                    marginTop: "8px"
                                }}
                            >
                                Upload
                            </button>
                        </form>
                    </div>
                )}
                {showFavorites ? (
                    <FavoritesFeed
                        audioFiles={audioFiles}
                        onLike={(file) => handleLike(audioFiles.indexOf(file))}
                        onFavorite={(file) => handleFavorite(audioFiles.indexOf(file))}
                        onBack={() => setShowFavorites(false)}
                    />
                ) : (
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
                                    <div style={{ flex: 1 }}>
                                        <strong style={{ fontSize: "1.1rem" }}>{file.name}</strong>
                                        <div style={{ fontSize: "0.95rem", color: "#666" }}>{file.location}</div>
                                    </div>
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
                )}
            </div>
        </div>
    );
}

export default AudioFeed;