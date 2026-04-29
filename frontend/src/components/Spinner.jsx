function Spinner({ label = "Forging…" }) {
  return (
    <div className="spinner" role="status" aria-live="polite">
      <span className="spinner__ring" />
      {label}
    </div>
  );
}

export default Spinner;
