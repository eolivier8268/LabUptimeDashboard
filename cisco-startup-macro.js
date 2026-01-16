// Ensures the homepage dashboard is displayed when the Cisco starts up
// Go to https://BOARD-IP/web-macros
// Copy this macro in and make sure to save

import xapi from 'xapi';

// CONFIGURATION
const TARGET_URL = 'http://10.200.1.3:3000/';
const WAKE_DELAY_MS = 750; // let network initialize

function openWebPage() {
  console.log('Firing WebView Display command...');
  xapi.Command.UserInterface.WebView.Display({
    Url: TARGET_URL,
    Title: 'Uptime Display',
    Mode: 'Fullscreen', // Options: 'Fullscreen,' 'Modal' (popup) or 'Panel' (sidebar)
  })
  .then(() => console.log('WebView command sent successfully.'))
  .catch((e) => console.error('Failed to open WebView: ' + e.message));
}

xapi.Status.Standby.State.on((state) => {
  // 'Off' = Device is fully awake
  // 'HalfWake' = Device detected presence
  if (state === 'Off' || state === 'HalfWake') {
    console.log(`Device Woke up (State: ${state}). Waiting ${WAKE_DELAY_MS}ms...`);
    setTimeout(openWebPage, WAKE_DELAY_MS);
  }
});
