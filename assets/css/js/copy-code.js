document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("pre > code").forEach((codeBlock) => {
    const button = document.createElement("button");
    button.className = "copy-code-button";
    button.type = "button";
    button.innerText = "Copy";

    button.addEventListener("click", async () => {
      await navigator.clipboard.writeText(codeBlock.innerText);
      button.innerText = "Copied";
      setTimeout(() => (button.innerText = "Copy"), 1500);
    });

    const pre = codeBlock.parentNode;
    pre.style.position = "relative";
    pre.appendChild(button);
  });
});
