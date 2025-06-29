import React, { useState } from "react";
import AuthImagePattern from "./AuthImagePattern";

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
        onAuth(form.email);
    };

    return (
        <div
            style={{
                minHeight: "100vh",
                width: "100vw",
                background: "#f3f6f8",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
            }}
        >
            <div style={{
                display: "flex",
                background: "#fff",
                borderRadius: "16px",
                boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
                overflow: "hidden",
                minWidth: 640,
            }}>
                {/* Auth image/pattern section */}
                <div style={{
                    background: "#eaf3fc",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    width: 280,
                    minHeight: 400,
                }}>
                    <AuthImagePattern
                      title="Welcome Back!"
                      subtitle="Sign in to access your audio feed."
                      titleStyle={{ color: "#222" }} // Title color override
                    />
                </div>
                {/* Auth form section */}
                <form
                    onSubmit={handleSubmit}
                    style={{
                        background: "#fff",
                        borderRadius: "0 16px 16px 0",
                        padding: "32px",
                        minWidth: "320px",
                        display: "flex",
                        flexDirection: "column",
                        gap: "18px",
                        flex: 1,
                        justifyContent: "center",
                        alignItems: "center", // Center logo and title
                    }}
                >
                    {/* Logo at the top */}
                    <div
                        style={{
                            width: "100%",
                            height: "100px",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            marginBottom: "0",
                            overflow: "hidden",
                        }}
                    >
                        <img
                            src="/logo.png"
                            alt="Logo"
                            style={{
                                maxWidth: "90%",
                                maxHeight: "90px",
                                objectFit: "contain",
                                display: "block",
                            }}
                        />
                    </div>
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
                                background: "#c7cfd9",
                                color: "#222",
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
                            background: "#c7cfd9",
                            color: "#222",
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
                            background: "#c7cfd9",
                            color: "#222",
                        }}
                    />
                    {error && (
                        <div style={{ color: "#e63946", textAlign: "center" }}>{error}</div>
                    )}
                    <button
                        type="submit"
                        style={{
                            width: "100%",            // Make button stretch full width
                            padding: "10px 0",        // Keep vertical padding
                            background: "#1db954", // green
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
                                    style={{ color: "#1db954", cursor: "pointer" }} // green
                                    onClick={() => setIsLogin(false)}
                                >
                                    Sign Up
                                </span>
                            </>
                        ) : (
                            <>
                                Already have an account?{" "}
                                <span
                                    style={{ color: "#1db954", cursor: "pointer" }} // green
                                    onClick={() => setIsLogin(true)}
                                >
                                    Login
                                </span>
                            </>
                        )}
                    </div>
                </form>
            </div>
        </div>
    );
}

export default AuthPage;