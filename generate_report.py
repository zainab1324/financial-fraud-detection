import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Credit Card Fraud Detection Report</title>
<style>
  :root {
    --bg:       #f0f4f8;
    --surface:  #ffffff;
    --surface2: #f8fafc;
    --border:   #dde3ec;
    --blue:     #4c72b0;
    --blue-lt:  #e8eef7;
    --red:      #c44e52;
    --green:    #55a868;
    --text:     #1e293b;
    --muted:    #64748b;
    --mono:     'Courier New', 'Lucida Console', monospace;
    --sans:     'Trebuchet MS', 'Segoe UI', sans-serif;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--sans);
    font-size: 15px;
    line-height: 1.6;
    min-height: 100vh;
  }

  main { max-width: 1200px; margin: 0 auto; padding: 0 24px 80px; }

  header {
    padding: 64px 0 48px;
    text-align: center;
    position: relative;
  }

  header::after {
    content: '';
    display: block;
    width: 64px;
    height: 3px;
    background: var(--blue);
    border-radius: 2px;
    margin: 28px auto 0;
  }

  .tag {
    display: inline-block;
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .15em;
    text-transform: uppercase;
    color: var(--blue);
    background: var(--blue-lt);
    border-radius: 3px;
    padding: 4px 12px;
    margin-bottom: 18px;
    animation: fadeUp .5s ease both;
  }

  h1 {
    font-family: var(--mono);
    font-size: clamp(24px, 4vw, 40px);
    font-weight: 700;
    color: var(--text);
    line-height: 1.15;
    animation: fadeUp .5s .08s ease both;
  }

  h1 span { color: var(--blue); }

  .subtitle {
    margin-top: 12px;
    font-size: 14px;
    color: var(--muted);
    letter-spacing: .03em;
    animation: fadeUp .5s .16s ease both;
  }

  .section { margin-top: 60px; animation: fadeUp .4s ease both; }

  .section-label {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
  }

  .section-label::before {
    content: '';
    width: 4px; height: 18px;
    background: var(--blue);
    border-radius: 2px;
    flex-shrink: 0;
  }

  .section-label h2 {
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--blue);
    white-space: nowrap;
  }

  .section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  .stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px;
  }

  .stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 22px 18px;
    transition: box-shadow .2s, transform .2s;
  }

  .stat-card:hover {
    box-shadow: 0 4px 16px rgba(76,114,176,.12);
    transform: translateY(-2px);
  }

  .stat-label {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 8px;
  }

  .stat-value {
    font-family: var(--mono);
    font-size: 26px;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
  }

  .stat-value.blue  { color: var(--blue); }
  .stat-value.small { font-size: 18px; }
  .stat-sub { margin-top: 5px; font-size: 12px; color: var(--muted); }

  .eda-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }

  .eda-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    transition: box-shadow .2s, transform .2s;
  }

  .eda-card:hover {
    box-shadow: 0 4px 16px rgba(76,114,176,.1);
    transform: translateY(-2px);
  }

  .eda-card-label {
    padding: 10px 14px;
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--muted);
    background: var(--surface2);
    border-bottom: 1px solid var(--border);
  }

  .eda-card img { width: 100%; height: auto; display: block; }

  .model-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 22px; }

  .model-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,.06);
  }

  .model-header {
    padding: 22px 22px 18px;
    border-bottom: 1px solid var(--border);
    background: var(--surface2);
  }

  .model-name {
    font-family: var(--mono);
    font-size: 13px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: .03em;
  }

  .roc-label {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 14px;
    margin-bottom: 2px;
  }

  .roc-value {
    font-family: var(--mono);
    font-size: 40px;
    font-weight: 700;
    color: var(--blue);
    line-height: 1;
  }

  .model-body { padding: 22px; }

  .metrics-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin-bottom: 18px;
  }

  .metrics-table th {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--muted);
    padding: 7px 10px;
    text-align: left;
    border-bottom: 1px solid var(--border);
    background: var(--surface2);
  }

  .metrics-table td { padding: 9px 10px; border-bottom: 1px solid var(--border); }
  .metrics-table tr:last-child td { border-bottom: none; }
  .metrics-table tbody tr:hover { background: var(--blue-lt); }

  .class-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: var(--mono);
    font-size: 11px;
  }

  .dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
  .dot.green { background: var(--green); }
  .dot.red   { background: var(--red); }

  .metric-val { font-family: var(--mono); font-weight: 700; color: var(--text); }
  .metric-val.accent { color: var(--blue); }

  .model-img {
    width: 100%;
    height: auto;
    border-radius: 6px;
    border: 1px solid var(--border);
    display: block;
  }

  .conclusion-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--blue);
    border-radius: 8px;
    padding: 26px 30px;
  }

  .conclusion-card p { font-size: 15px; line-height: 1.8; max-width: 820px; color: var(--text); }
  .conclusion-card p + p { margin-top: 10px; }
  .highlight { color: var(--blue); font-weight: 600; }

  footer {
    margin-top: 72px;
    padding-top: 22px;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: var(--mono);
    font-size: 11px;
    color: var(--muted);
    letter-spacing: .05em;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .section:nth-child(1) { animation-delay: .05s; }
  .section:nth-child(2) { animation-delay: .1s; }
  .section:nth-child(3) { animation-delay: .15s; }
  .section:nth-child(4) { animation-delay: .2s; }

  @media (max-width: 720px) {
    .eda-grid, .model-grid { grid-template-columns: 1fr; }
    .stat-grid { grid-template-columns: 1fr 1fr; }
    .roc-value { font-size: 30px; }
    footer { flex-direction: column; gap: 8px; text-align: center; }
  }
</style>
</head>
<body>
<main>

  <header>
    <div class="tag">Financial Analytics Report</div>
    <h1>Credit Card <span>Fraud Detection</span></h1>
    <p class="subtitle">Anomaly Detection &nbsp;&middot;&nbsp; Autoencoder Neural Networks &amp; Isolation Forest &nbsp;&middot;&nbsp; Kaggle ULB Dataset</p>
  </header>

  <section class="section">
    <div class="section-label"><h2>Dataset Overview</h2></div>
    <div class="stat-grid">
      <div class="stat-card">
        <div class="stat-label">Total Transactions</div>
        <div class="stat-value">284,807</div>
        <div class="stat-sub">European cardholders, Sept 2013</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Features</div>
        <div class="stat-value blue">31</div>
        <div class="stat-sub">V1&ndash;V28 PCA &middot; Time &middot; Amount &middot; Class</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Legitimate Transactions</div>
        <div class="stat-value small">284,315</div>
        <div class="stat-sub" style="color:var(--green)">99.83% of dataset</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Fraudulent Transactions</div>
        <div class="stat-value small" style="color:var(--red)">492</div>
        <div class="stat-sub" style="color:var(--red)">0.17% &mdash; highly imbalanced</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Missing Values</div>
        <div class="stat-value blue">0</div>
        <div class="stat-sub">Clean dataset, no imputation needed</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Imbalance Handling</div>
        <div class="stat-value small">SMOTE</div>
        <div class="stat-sub">Synthetic Minority Oversampling</div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section-label"><h2>Exploratory Data Analysis</h2></div>
    <div class="eda-grid">
      <div class="eda-card">
        <div class="eda-card-label">Class Distribution</div>
        <img src="class_distribution.png" alt="Class Distribution">
      </div>
      <div class="eda-card">
        <div class="eda-card-label">Transaction Amount by Class</div>
        <img src="amount_distribution.png" alt="Amount Distribution">
      </div>
      <div class="eda-card">
        <div class="eda-card-label">Transaction Time by Class</div>
        <img src="time_distribution.png" alt="Time Distribution">
      </div>
      <div class="eda-card">
        <div class="eda-card-label">Feature Correlation Heatmap (V1&ndash;V10)</div>
        <img src="correlation_heatmap.png" alt="Correlation Heatmap">
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section-label"><h2>Model Results</h2></div>
    <div class="model-grid">

      <div class="model-card">
        <div class="model-header">
          <div class="model-name">Autoencoder Neural Network</div>
          <div class="roc-label">ROC AUC</div>
          <div class="roc-value">0.906</div>
        </div>
        <div class="model-body">
          <table class="metrics-table">
            <thead>
              <tr><th>Class</th><th>Precision</th><th>Recall</th><th>F1-Score</th></tr>
            </thead>
            <tbody>
              <tr>
                <td><span class="class-badge"><span class="dot green"></span>Legitimate</span></td>
                <td><span class="metric-val">0.87</span></td>
                <td><span class="metric-val">0.95</span></td>
                <td><span class="metric-val">0.91</span></td>
              </tr>
              <tr>
                <td><span class="class-badge"><span class="dot red"></span>Fraud</span></td>
                <td><span class="metric-val accent">0.95</span></td>
                <td><span class="metric-val">0.86</span></td>
                <td><span class="metric-val">0.90</span></td>
              </tr>
            </tbody>
          </table>
          <img src="Autoencoder_confusion_matrix.png" alt="Autoencoder Confusion Matrix" class="model-img">
        </div>
      </div>

      <div class="model-card">
        <div class="model-header">
          <div class="model-name">Isolation Forest</div>
          <div class="roc-label">ROC AUC</div>
          <div class="roc-value">0.883</div>
        </div>
        <div class="model-body">
          <table class="metrics-table">
            <thead>
              <tr><th>Class</th><th>Precision</th><th>Recall</th><th>F1-Score</th></tr>
            </thead>
            <tbody>
              <tr>
                <td><span class="class-badge"><span class="dot green"></span>Legitimate</span></td>
                <td><span class="metric-val">0.87</span></td>
                <td><span class="metric-val">0.90</span></td>
                <td><span class="metric-val">0.88</span></td>
              </tr>
              <tr>
                <td><span class="class-badge"><span class="dot red"></span>Fraud</span></td>
                <td><span class="metric-val">0.90</span></td>
                <td><span class="metric-val">0.87</span></td>
                <td><span class="metric-val">0.88</span></td>
              </tr>
            </tbody>
          </table>
          <img src="Isolation_Forest_confusion_matrix.png" alt="Isolation Forest Confusion Matrix" class="model-img">
        </div>
      </div>

    </div>
  </section>

  <section class="section">
    <div class="section-label"><h2>Conclusion</h2></div>
    <div class="conclusion-card">
      <p>
        Both models demonstrate strong performance on the highly imbalanced credit card fraud dataset after applying SMOTE oversampling.
        The <span class="highlight">Autoencoder Neural Network</span> edges out with a higher ROC AUC of <span class="highlight">0.906</span>
        and superior fraud precision of <span class="highlight">0.95</span>, meaning 95% of flagged transactions are genuine fraud &mdash;
        minimising false positives that create friction for legitimate customers.
      </p>
      <p>
        The <span class="highlight">Isolation Forest</span> performs competitively at ROC AUC <span class="highlight">0.883</span> with
        balanced precision and recall across both classes, making it a strong candidate where model interpretability is prioritised
        over marginal accuracy gains. Both models are suitable for production fraud detection pipelines.
      </p>
    </div>
  </section>

  <footer>
    <span>Credit Card Fraud Detection &nbsp;&middot;&nbsp; Kaggle ULB Dataset</span>
    <span>Python 3.10 &nbsp;&middot;&nbsp; TensorFlow 2.13 &nbsp;&middot;&nbsp; scikit-learn 1.3</span>
  </footer>

</main>
<script>
  document.querySelectorAll('.roc-value').forEach(el => {
    const target = parseFloat(el.textContent);
    const duration = 1000;
    const start = performance.now();
    const animate = now => {
      const progress = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      el.textContent = (target * ease).toFixed(3);
      if (progress < 1) requestAnimationFrame(animate);
      else el.textContent = target.toFixed(3);
    };
    setTimeout(() => requestAnimationFrame(animate), 300);
  });
</script>
</body>
</html>"""

with open('financial-fraud-detection/fraud_report.html', 'w') as f:
    f.write(html_content)

print("HTML report generated: financial-fraud-detection/fraud_report.html")
