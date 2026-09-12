import { createContext, useContext, useEffect, useState } from "react";
import api from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem("user") || "null"));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!localStorage.getItem("token")) return setLoading(false);
    api.get("/auth/me").then(r => {
      setUser(r.data); localStorage.setItem("user", JSON.stringify(r.data));
    }).catch(() => {}).finally(() => setLoading(false));
  }, []);

  const login = async (username, password) => {
    const { data } = await api.post("/auth/login", { username, password });
    localStorage.setItem("token", data.access_token);
    const me = await api.get("/auth/me");
    setUser(me.data); localStorage.setItem("user", JSON.stringify(me.data));
  };
  const logout = () => {
    localStorage.clear(); setUser(null);
  };
  return <AuthContext.Provider value={{ user, loading, login, logout }}>{children}</AuthContext.Provider>;
}
export const useAuth = () => useContext(AuthContext);
