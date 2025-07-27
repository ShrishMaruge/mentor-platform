const synth = window.speechSynthesis;
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-IN';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    const lang = document.getElementById('languageSelect')?.value || 'en';
    if (lang === 'hi') utterance.lang = 'hi-IN';
    else if (lang === 'mr') utterance.lang = 'mr-IN';
    else if (lang === 'bn') utterance.lang = 'bn-IN';
    else utterance.lang = 'en-US';
    speechSynthesis.speak(utterance);
  }
  

function startListening(callback) {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = document.getElementById("languageSelect").value || 'en-US';
    recognition.interimResults = false;
    recognition.onresult = (e) => callback(e.results[0][0].transcript);
    recognition.start();
  }
  