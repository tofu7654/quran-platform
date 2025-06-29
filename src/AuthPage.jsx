import React, { useState } from "react";

function AuthPage({ onAuth }) {
    const [isLogin, setIsLogin] = useState(true);
    const [form, setForm] = useState({ email: "", password: "", name: "" });
    const [error, setError] = useState("");

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!form.email || !form.password || (!isLogin && !form.name)) {
            setError("Please fill all fields.");
            return;
        }
        setError("");
        // Simulate auth success
        onAuth(form.email);
    };

    return (
        <div
            style={{
                minHeight: "100vh",
                width: "100vw", // Add this line
                background: "#f3f6f8",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
            }}
        >
            <form
                onSubmit={handleSubmit}
                style={{
                    background: "#fff",
                    borderRadius: "12px",
                    boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
                    padding: "32px",
                    minWidth: "320px",
                    display: "flex",
                    flexDirection: "column",
                    gap: "18px",
                }}
            >
                <h2 style={{ textAlign: "center", color: "#222" }}>
                    {isLogin ? "Login" : "Sign Up"}
                </h2>
                {!isLogin && (
                    <input
                        type="text"
                        name="name"
                        placeholder="Name"
                        value={form.name}
                        onChange={handleChange}
                        style={{
                            padding: "10px",
                            borderRadius: "6px",
                            border: "1px solid #ccc",
                            fontSize: "16px",
                        }}
                    />
                )}
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={form.email}
                    onChange={handleChange}
                    style={{
                        padding: "10px",
                        borderRadius: "6px",
                        border: "1px solid #ccc",
                        fontSize: "16px",
                        background: "#c7cfd9", // Light gray background
                        color: "#222",         // Black text
                    }}
                />
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={form.password}
                    onChange={handleChange}
                    style={{
                        padding: "10px",
                        borderRadius: "6px",
                        border: "1px solid #ccc",
                        fontSize: "16px",
                        background: "#c7cfd9", // Light gray background
                        color: "#222",         // Black text
                    }}
                />
                {error && (
                    <div style={{ color: "#e63946", textAlign: "center" }}>{error}</div>
                )}
                <button
                    type="submit"
                    style={{
                        padding: "10px 0",
                        background: "#0a66c2",
                        color: "#fff",
                        border: "none",
                        borderRadius: "24px",
                        fontSize: "16px",
                        fontWeight: 600,
                        cursor: "pointer",
                        marginTop: "8px",
                    }}
                >
                    {isLogin ? "Login" : "Sign Up"}
                </button>
                <div style={{ textAlign: "center", marginTop: "8px" }}>
                    {isLogin ? (
                        <>
                            Don't have an account?{" "}
                            <span
                                style={{ color: "#0a66c2", cursor: "pointer" }}
                                onClick={() => setIsLogin(false)}
                            >
                                Sign Up
                            </span>
                        </>
                    ) : (
                        <>
                            Already have an account?{" "}
                            <span
                                style={{ color: "#0a66c2", cursor: "pointer" }}
                                onClick={() => setIsLogin(true)}
                            >
                                Login
                            </span>
                        </>
                    )}
                </div>
            </form>
        </div>
    );
}

export default AuthPage;