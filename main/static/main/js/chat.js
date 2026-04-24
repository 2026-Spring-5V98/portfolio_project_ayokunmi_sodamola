(function () {
  const launcher = document.getElementById("chat-launcher");
  const panel = document.getElementById("chat-panel");
  const closeBtn = document.getElementById("chat-close");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");
  const submitBtn = document.getElementById("chat-submit");
  const body = document.getElementById("chat-body");
  const suggestions = document.getElementById("chat-suggestions");

  if (!launcher || !panel) return;

  const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content || "";
  const chatUrl = panel.dataset.url;

  function open() {
    panel.setAttribute("aria-hidden", "false");
    launcher.style.display = "none";
    setTimeout(() => input.focus(), 100);
  }
  function close() {
    panel.setAttribute("aria-hidden", "true");
    launcher.style.display = "inline-flex";
  }

  launcher.addEventListener("click", open);
  closeBtn.addEventListener("click", close);

  function addMessage(text, role) {
    const div = document.createElement("div");
    div.className = `chat-msg ${role}`;
    div.textContent = text;
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
    return div;
  }

  function showTyping() {
    const el = document.createElement("div");
    el.className = "chat-typing";
    el.id = "chat-typing";
    el.innerHTML = "<span></span><span></span><span></span>";
    body.appendChild(el);
    body.scrollTop = body.scrollHeight;
    return el;
  }
  function hideTyping() {
    document.getElementById("chat-typing")?.remove();
  }

  async function send(message) {
    addMessage(message, "user");
    if (suggestions) suggestions.style.display = "none";
    input.value = "";
    input.disabled = true;
    submitBtn.disabled = true;
    showTyping();

    try {
      const res = await fetch(chatUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
        body: JSON.stringify({ message }),
      });
      const data = await res.json();
      hideTyping();
      if (!res.ok) {
        addMessage(data.error || "Something went wrong.", "error");
      } else {
        addMessage(data.reply, "bot");
      }
    } catch (err) {
      hideTyping();
      addMessage("Couldn't reach the server. Try again?", "error");
    } finally {
      input.disabled = false;
      submitBtn.disabled = false;
      input.focus();
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const msg = input.value.trim();
    if (msg) send(msg);
  });

  if (suggestions) {
    suggestions.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => send(btn.textContent));
    });
  }
})();
