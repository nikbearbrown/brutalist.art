import {useEffect, useState} from 'react';
import {continueRender, delayRender, staticFile} from 'remotion';

/**
 * useLato — load the bundled Lato (NEU brand typeface) per component, the same
 * pattern LogoMotion uses for Montserrat: per-component (never module scope —
 * Root.tsx imports 600+ compositions), continue-on-failure so a missing file
 * degrades to the system sans instead of hanging the render. Every NEU/SEIS
 * scene calls this once; without it Chrome silently substitutes Helvetica,
 * which NU brand law forbids.
 */
const LATO_FILES: [number, string][] = [
  [400, 'fonts/Lato-Regular.ttf'],
  [700, 'fonts/Lato-Bold.ttf'],
];

export const useLato = () => {
  const [handle] = useState(() => delayRender('NEU: Lato'));
  useEffect(() => {
    let live = true;
    Promise.all(
      LATO_FILES.map(([weight, file]) =>
        new FontFace('Lato', `url(${staticFile(file)}) format('truetype')`, {weight: String(weight)})
          .load()
          .then((f) => {
            (document.fonts as unknown as {add: (f: FontFace) => void}).add(f);
          }),
      ),
    )
      .catch(() => undefined)
      .then(() => {
        if (live) continueRender(handle);
      });
    return () => {
      live = false;
    };
  }, [handle]);
};
