/** Editable text shown on the Intro page. Keep prose here, not in the page,
 *  so the project / funding details can be updated without touching layout. */

export const PROJECT = {
  name: 'SoundVisualizer',
  tagline: 'Drone-propeller noise directivity: capture, spectra, polar plots.',
  githubUrl: 'https://github.com/asdfgh0318/SoundVisualizer',
  institution: 'Politechnika Warszawska',
  /** One line per paragraph. */
  description: [
    'SoundVisualizer measures how loud a propeller is in every direction. Up to eleven miniDSP UMIK-2 microphones sit on a vertical arc around the test article while a Tyto Robotics 1585 thrust stand drives the motor through a programmed ESC-signal ramp and records thrust, torque, current, voltage and RPM.',
    'Every ramp step yields one acoustic measurement per microphone plus a performance record. The Results page turns them into per-microphone spectra, a sound-pressure-level polar over elevation, blade-passage tone levels separated from the tone-notched broadband, X/Y scatter of any two quantities, and psychoacoustic metrics (loudness, sharpness, roughness).',
  ],
  audience: [
    'Researchers characterising propeller, duct and shroud noise on a static rig.',
    'Engineers comparing propellers or shroud materials at matched thrust.',
    'Anyone who needs the acoustic and performance data of a propeller test saved side by side, in plain WAV and JSON files.',
  ],
  workflow: [
    { step: 'Setup', text: 'Assign each USB microphone to a serial and an elevation, upload its calibration file, and set the safety cutoffs on the stand.' },
    { step: 'Capture', text: 'Name the test article (motor, propeller, shroud, notes), edit the ESC-signal ramp, confirm the safety prompt, and let the stand and the microphones record every step.' },
    { step: 'Results', text: 'Pick a base, pick a ramp point, and read spectra, the elevation polar, tone and broadband levels, scatter plots and psychoacoustics. Overlay other bases to compare.' },
  ],
};

/** Grant / financing block. Fill in the real project title, agency and number;
 *  the Intro page renders whatever is here verbatim. */
export const FUNDING = {
  programme: 'Funding programme — to be completed',
  projectTitle: 'Project title — to be completed',
  grantNumber: 'Grant agreement no. — to be completed',
  beneficiary: 'Politechnika Warszawska',
  note: 'Funding details are placeholders until the grant information is entered in src/content/projectInfo.ts.',
};

export const CREDITS = [
  { what: 'Tyto Robotics MSP serial protocol and Norsonic NOR-145 control', who: 'Paweł Sadowski, ars_noise_measurement', url: 'https://git.swarozyn.pl/mtj/ars_noise_measurement.git' },
  { what: 'Psychoacoustic metrics', who: 'MOSQITO (Green Forge Coop, BSD)', url: 'https://github.com/Eomys/MoSQITo' },
];
