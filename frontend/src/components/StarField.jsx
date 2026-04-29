import { useMemo } from "react";

const STAR_COUNT = 80;

function StarField() {
  const stars = useMemo(
    () =>
      Array.from({ length: STAR_COUNT }, (_, index) => ({
        id: index,
        top: Math.random() * 100,
        left: Math.random() * 100,
        delay: Math.random() * 4,
        size: Math.random() < 0.85 ? 2 : 3,
      })),
    [],
  );

  return (
    <div className="starfield" aria-hidden="true">
      {stars.map((star) => (
        <span
          key={star.id}
          className="star"
          style={{
            top: `${star.top}%`,
            left: `${star.left}%`,
            width: `${star.size}px`,
            height: `${star.size}px`,
            "--delay": `${star.delay}s`,
          }}
        />
      ))}
    </div>
  );
}

export default StarField;
