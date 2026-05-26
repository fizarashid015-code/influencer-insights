document.getElementById('analyzeBtn').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  document.getElementById('results').innerHTML = '<p>Scraping comments...</p>';
  
  const [{result: comments}] = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      const els = document.querySelectorAll('#content-text');
      return Array.from(els).map(el => el.innerText).filter(t => t.trim()).slice(0, 100);
    }
  });

  if (!comments || !comments.length) {
    document.getElementById('results').innerHTML = '<p>❌ No comments found! Scroll down on YouTube to load comments first, then try again.</p>';
    return;
  }

  document.getElementById('results').innerHTML = `<p>Found ${comments.length} comments. Analyzing...</p>`;

  try {
    const response = await fetch('https://influencer-insights.onrender.com/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comments })
    });
    const data = await response.json();
    document.getElementById('results').innerHTML = `
      <div class="stat positive">✅ Positive: ${data.positive}</div>
      <div class="stat negative">❌ Negative: ${data.negative}</div>
      <div class="stat neutral">😐 Neutral: ${data.neutral}</div>
      <p>Total: ${data.total}</p>
    `;
  } catch (err) {
    document.getElementById('results').innerHTML = '<p>❌ API error. Make sure https://influencer-insights.onrender.com is running!</p>';
  }
});