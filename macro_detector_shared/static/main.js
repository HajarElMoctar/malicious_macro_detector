document.addEventListener("DOMContentLoaded", function () {
  const dropZone = document.getElementById("drop-zone");
  const chatBox = document.getElementById("chat-box");
  const chatInput = document.getElementById("chat-input");
  const sendBtn = document.getElementById("send-btn");
  const resultsSection = document.getElementById("results");
  const loadingSpinner = document.getElementById("loading-spinner");
  const suggestionsBox = document.getElementById("suggestions");

  let reportId = null;

  // Checkbox validation: Ensure one is always selected
  const staticCheckbox = document.getElementById("static");
  const dynamicCheckbox = document.getElementById("dynamic");

  function ensureAtLeastOneChecked(event) {
    if (!staticCheckbox.checked && !dynamicCheckbox.checked) {
      event.preventDefault();
      alert("At least one analysis type must be selected.");
      event.target.checked = true;
    }
  }

  staticCheckbox.addEventListener("change", ensureAtLeastOneChecked);
  dynamicCheckbox.addEventListener("change", ensureAtLeastOneChecked);

  // Drag-and-drop styling
  dropZone.addEventListener("dragover", e => {
    e.preventDefault();
    dropZone.style.borderColor = "#198754";
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.style.borderColor = "#0d6efd";
  });

  dropZone.addEventListener("drop", e => {
    e.preventDefault();
    dropZone.style.borderColor = "#0d6efd";
    const file = e.dataTransfer.files[0];
    handleFileUpload(file);
  });

  function handleFileUpload(file) {
    if (!/\.(doc|docm)$/i.test(file.name)) {
      alert("Only .doc and .docm files are allowed (must be macro-capable).");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const analysisTypes = [];
    if (staticCheckbox.checked) analysisTypes.push("static");
    if (dynamicCheckbox.checked) analysisTypes.push("dynamic");
    formData.append("analysisType", analysisTypes.join(","));

    loadingSpinner.classList.remove("d-none");

    fetch("/upload", {
      method: "POST",
      body: formData,
    })
    .then(res => res.json())
    .then(data => {
      loadingSpinner.classList.add("d-none");

      if (data.error) {
        alert(data.error);
        return;
      }

      reportId = data.reportId;

      // 🔄 Clear previous chat and suggestions
      chatBox.innerHTML = "";
      suggestionsBox.innerHTML = "";

      const displayScore = score => score === "N/A" ? "N/A" : `${score}/100`;
      document.getElementById("static-threat-score").innerText = displayScore(data.staticThreatScore);
      document.getElementById("dynamic-threat-score").innerText = displayScore(data.dynamicThreatScore);

      document.getElementById("summary").innerText = data.summary;
      document.getElementById("download-report").href = `/export-report/${reportId}`;
      resultsSection.classList.remove("d-none");

      appendChat("assistant", "✅ Report has been generated. You can ask follow-up questions.");
      showSuggestions();
      resultsSection.scrollIntoView({ behavior: "smooth" });
    })
    .catch(err => {
      loadingSpinner.classList.add("d-none");
      alert("Something went wrong while analyzing the document.");
      console.error(err);
    });
  }

  sendBtn.addEventListener("click", () => {
    const message = chatInput.value.trim();
    if (!message || !reportId) return;

    appendChat("user", message);
    chatInput.value = "";
    sendBtn.disabled = true;

    fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message, reportId })
    })
    .then(res => res.json())
    .then(data => {
      appendChat("assistant", data.reply);
    })
    .catch(err => {
      appendChat("assistant", "⚠️ Sorry, something went wrong.");
      console.error(err);
    })
    .finally(() => {
      sendBtn.disabled = false;
    });
  });

  function appendChat(role, message) {
    const div = document.createElement("div");
    div.classList.add("chat-msg", "p-2", "mb-2", "rounded", "shadow-sm");

    const escaped = message
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\n/g, "<br>");

    const isCode = message.includes("Sub ") || message.includes("Shell") || message.includes("MsgBox");

    const bubble = isCode
      ? `<pre class="m-0" style="white-space: pre-wrap;"><code>${escaped}</code></pre>`
      : `<div>${escaped}</div>`;

    if (role === "user") {
      div.classList.add("bg-primary", "text-white", "align-self-end");
      div.innerHTML = `<strong>You:</strong><br>${bubble}`;
    } else {
      div.classList.add("bg-light", "border", "align-self-start");
      div.innerHTML = `<strong>AI:</strong><br>${bubble}`;
    }

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function showSuggestions() {
    suggestionsBox.innerHTML = `
      <p class="fw-bold mt-3 mb-2">💡 Suggested Questions:</p>
      <ul class="list-unstyled">
        <li><button class="btn btn-sm btn-outline-primary mb-1">Is this macro considered dangerous?</button></li>
        <li><button class="btn btn-sm btn-outline-primary mb-1">What kind of payload does it use?</button></li>
        <li><button class="btn btn-sm btn-outline-primary mb-1">Can you explain how this macro works?</button></li>
        <li><button class="btn btn-sm btn-outline-primary mb-1">How can I remove this macro?</button></li>
      </ul>
    `;

    suggestionsBox.querySelectorAll("button").forEach(button => {
      button.addEventListener("click", () => {
        chatInput.value = button.innerText;
        sendBtn.click();
      });
    });
  }
});
