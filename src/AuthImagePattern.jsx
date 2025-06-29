import React from "react";

const pulseKeyframes = `
@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}
`;

function AuthImagePattern({ title, subtitle }) {
  return (
    <div
      style={{
        background: "#eaf3fc",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "32px",
        minHeight: 400,
        width: 280,
        flexDirection: "column",
      }}
    >
      <style>{pulseKeyframes}</style>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "12px",
          marginBottom: "32px",
        }}
      >
        {[...Array(9)].map((_, i) => (
          <div
            key={i}
            style={{
              aspectRatio: "1 / 1",
              borderRadius: "16px",
              background: "rgba(10,102,194,0.10)",
              animation: i % 2 === 0 ? "pulse 1.5s infinite" : undefined,
            }}
          />
        ))}
      </div>
      <h2 style={{ color: "#222", fontSize: "1.5rem", fontWeight: 700, marginBottom: "16px", textAlign: "center" }}>
        {title}
      </h2>
      <p style={{ color: "#666", textAlign: "center" }}>{subtitle}</p>
    </div>
  );
}

export default AuthImagePattern;