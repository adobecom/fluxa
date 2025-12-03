const form = document.getElementById("pipeline-form");
const tutorialUrlInput = document.getElementById("tutorialUrl");
const imageInput = document.getElementById("imageInput");
const inlineRenderInput = document.getElementById("inlineRender");
const statusCard = document.getElementById("statusCard");
const statusMessage = document.getElementById("statusMessage");
const resultCard = document.getElementById("resultCard");
const resultContent = document.getElementById("resultContent");
const submitButton = document.getElementById("submitButton");

const baseApiUrl = window.FLUXA_API_BASE ?? "http://0.0.0.0:8000";

const setStatus = (message) => {
  statusCard.hidden = false;
  statusMessage.textContent = message;
};

const resetResult = () => {
  resultCard.hidden = true;
  resultContent.innerHTML = "";
};

const base64ToBlob = (base64, mime) => {
  const byteCharacters = atob(base64);
  const byteArrays = [];
  for (let offset = 0; offset < byteCharacters.length; offset += 512) {
    const slice = byteCharacters.slice(offset, offset + 512);
    const byteNumbers = new Array(slice.length);
    for (let i = 0; i < slice.length; i += 1) {
      byteNumbers[i] = slice.charCodeAt(i);
    }
    byteArrays.push(new Uint8Array(byteNumbers));
  }
  return new Blob(byteArrays, { type: mime });
};

const handleResult = (payload) => {
  resultCard.hidden = false;
  resultContent.innerHTML = "";

  const gallery = document.createElement("div");
  gallery.className = "gallery";
  resultContent.appendChild(gallery);

  const { application, inline_render: inlineRender } = payload;

  const addPreview = (url, filename) => {
    const wrapper = document.createElement("div");
    wrapper.className = "gallery-item";

    const img = document.createElement("img");
    img.src = url;
    img.alt = filename;
    img.className = "preview";
    wrapper.appendChild(img);

    const linkRow = document.createElement("div");
    linkRow.className = "links";
    wrapper.appendChild(linkRow);
    gallery.appendChild(wrapper);
  };

  if (inlineRender) {
    const blob = base64ToBlob(
      inlineRender.base64_data,
      inlineRender.content_type,
    );
    const url = URL.createObjectURL(blob);
    addPreview(url, inlineRender.filename);
  } else if (application?.download_url) {
    const url = `${baseApiUrl}${application.download_url}`;
    const filename =
      application.output_path?.split("/").pop() ?? "rendered.psd";
    addPreview(url, filename);
  }
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const files = imageInput.files;
  if (!files.length) {
    alert("Select at least one image.");
    return;
  }

  resetResult();
  setStatus("Uploading images…");
  submitButton.disabled = true;

  try {
    const formData = new FormData();
    formData.append("tutorial_url", tutorialUrlInput.value.trim());
    formData.append("inline_render", "true");
    Array.from(files).forEach((file) =>
      formData.append("images", file, file.name),
    );

    const response = await fetch(`${baseApiUrl}/apply`, {
      method: "POST",
      body: formData,
    });
    debugger

    if (!response.ok) {
      throw new Error(`Pipeline failed. Status: ${response.status}`);
    }

    setStatus("Processing complete.");
    const payload = await response.json();
    handleResult(payload);
  } catch (error) {
    console.error(error);
    setStatus(`Error: ${error.message}`);
  } finally {
    submitButton.disabled = false;
  }
});
