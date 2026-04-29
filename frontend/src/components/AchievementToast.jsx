function AchievementToast({ toasts = [] }) {
  if (!toasts.length) return null;

  return (
    <div className="toast-stack" aria-live="polite" aria-atomic="true">
      {toasts.map((toast) => (
        <div className="toast" key={toast.id} role="status">
          <div className="toast__icon" aria-hidden="true">
            {toast.icon}
          </div>
          <div>
            <div className="toast__head">{toast.head}</div>
            <div className="toast__title">{toast.title}</div>
            {toast.description && <div className="toast__desc">{toast.description}</div>}
          </div>
        </div>
      ))}
    </div>
  );
}

export default AchievementToast;
