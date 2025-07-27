// Language translation using LibreTranslate API
const langSelect = document.getElementById("languageSelect");

async function translatePage(language) {
    if (language === "en") return; // No translation needed

    const elements = document.querySelectorAll(".translate-text, .translate-text *");
    for (let el of elements) {
        if (el.innerText.trim().length > 0) {
            const translated = await translateText(el.innerText, language);
            el.innerText = translated;
        }
    }
}

async function translateText(text, targetLang) {
    if (targetLang === 'en') return text; // No need to translate
    try {
      const res = await fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=en|${targetLang}`);
      const data = await res.json();
      return data.responseData.translatedText || text;
    } catch (e) {
      console.error("Translation error:", e);
      return text;
    }
  }
  

langSelect.addEventListener("change", (e) => {
    translatePage(e.target.value);
});
