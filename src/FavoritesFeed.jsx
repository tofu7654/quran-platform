import React from "react";

function FavoritesFeed({ audioFiles, onLike, onFavorite, onBack }) {
  const favorites = audioFiles.filter((file) => file.favorite);

  return (
    <div>
      <button
        onClick={onBack}
        style={{
          marginBottom: "24px",
          background: "#0a66c2",
          color: "#fff",
          border: "none",
          borderRadius: "24px",
          padding: "8px 20px",
          fontWeight: 600,
          cursor: "pointer",
        }}
      >
        ← Back to Feed
      </button>
      <h2 style={{ textAlign: "center", color: "#222" }}>Your Favorites</h2>
      {favorites.length === 0 && (
        <div style={{ color: "#888", textAlign: "center", marginTop: "32px" }}>
          No favorites yet.
        </div>
      )}
      {favorites.map((file, idx) => (
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
            gap: "10px",
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
                border: "2px solid #e0e0e0",
              }}
            />
            <div style={{ flex: 1 }}>
              <strong style={{ fontSize: "1.1rem" }}>{file.name}</strong>
              <div style={{ fontSize: "0.95rem", color: "#666" }}>{file.location}</div>
            </div>
            <button
              onClick={() => onFavorite(file)}
              style={{
                background: "none",
                border: "none",
                color: file.favorite ? "#f9c846" : "#bbb",
                fontSize: "22px",
                cursor: "pointer",
                marginLeft: "8px",
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
              onClick={() => onLike(file)}
              style={{
                background: "none",
                border: "none",
                color: "#e63946",
                fontSize: "20px",
                cursor: "pointer",
                marginRight: "8px",
              }}
              aria-label="Like"
            >
              ❤️
            </button>
            <span style={{ fontWeight: 500 }}>
              {file.likes} {file.likes === 1 ? "Like" : "Likes"}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}

export default FavoritesFeed;