import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Route, Routes, useLocation } from "react-router-dom";

import AchievementToast from "./components/AchievementToast";
import HUD from "./components/HUD";
import StarField from "./components/StarField";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import { loadState } from "./services/gamification";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Lab", end: true },
  { to: "/", label: "Login", end: true },
  { to: "/register", label: "Forge" },
];

function App() {
  const [progress, setProgress] = useState(() => loadState());
  const [toasts, setToasts] = useState([]);
  const toastIdRef = useRef(0);
  const location = useLocation();

  const refreshProgress = useCallback(() => {
    setProgress(loadState());
  }, []);

  const pushToast = useCallback((toast) => {
    toastIdRef.current += 1;
    const id = toastIdRef.current;
    setToasts((current) => [...current, { id, ...toast }]);
    setTimeout(() => {
      setToasts((current) => current.filter((item) => item.id !== id));
    }, 4500);
  }, []);

  useEffect(() => {
    const sync = () => refreshProgress();
    window.addEventListener("storage", sync);
    return () => window.removeEventListener("storage", sync);
  }, [refreshProgress]);

  const isAuthRoute = location.pathname === "/" || location.pathname === "/register";

  const sharedDashboardProps = useMemo(
    () => ({
      progress,
      onProgressUpdate: refreshProgress,
      onToast: pushToast,
    }),
    [progress, refreshProgress, pushToast],
  );

  return (
    <>
      <StarField />
      {isAuthRoute ? (
        <main className="app-shell app-shell--auth">
          <Routes>
            <Route path="/" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
          </Routes>
        </main>
      ) : (
        <div className="app-shell">
          <HUD state={progress} navItems={NAV_ITEMS} />
          <main>
            <Routes>
              <Route path="/dashboard" element={<DashboardPage {...sharedDashboardProps} />} />
            </Routes>
          </main>
        </div>
      )}
      <AchievementToast toasts={toasts} />
    </>
  );
}

export default App;
