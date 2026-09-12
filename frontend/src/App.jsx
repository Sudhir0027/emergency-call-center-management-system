import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import EmergencyCalls from "./pages/EmergencyCalls";
import CallDetails from "./pages/CallDetails";
import Responders from "./pages/Responders";
import Queue from "./pages/Queue";
import History from "./pages/History";

function Protected(){
  const {user,loading}=useAuth();
  const loc=useLocation();
  if(loading)return <div className="min-h-screen grid place-items-center">Loading...</div>;
  if(!user)return <Navigate to="/login" state={{from:loc}} replace/>;
  return <div className="min-h-screen flex"><Sidebar/><main className="flex-1 min-w-0"><Navbar/><div className="p-4 md:p-6"><Routes>
    <Route path="/" element={<Dashboard/>}/><Route path="/calls" element={<EmergencyCalls/>}/><Route path="/calls/:id" element={<CallDetails/>}/><Route path="/queue" element={<Queue/>}/><Route path="/responders" element={<Responders/>}/><Route path="/history" element={<History/>}/>
  </Routes></div></main></div>
}
export default function App(){return <AuthProvider><Routes><Route path="/login" element={<Login/>}/><Route path="/*" element={<Protected/>}/></Routes></AuthProvider>}
