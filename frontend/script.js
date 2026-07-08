const form = document.getElementById("pipeline-form");
const tutorialUrlInput = document.getElementById("tutorialUrl");
const imageInput = document.getElementById("imageInput");
const inlineRenderInput = document.getElementById("inlineRender");
const statusCard = document.getElementById("statusCard");
const statusMessage = document.getElementById("statusMessage");
const resultCard = document.getElementById("resultCard");
const resultContent = document.getElementById("resultContent");
const submitButton = document.getElementById("submitButton");
const dropzone = document.getElementById("dropzone");
const dropzonePrompt = document.getElementById("dropzonePrompt");
const dropzonePreview = document.getElementById("dropzonePreview");
const fileList = document.getElementById("fileList");

const baseApiUrl = window.FLUXA_API_BASE ?? "http://0.0.0.0:8000";

let dropzonePreviewUrl = null;

const renderFileList = (files) => {
  fileList.innerHTML = "";

  if (dropzonePreviewUrl) {
    URL.revokeObjectURL(dropzonePreviewUrl);
    dropzonePreviewUrl = null;
  }

  if (!files.length) {
    fileList.hidden = true;
    dropzonePreview.hidden = true;
    dropzonePrompt.hidden = false;
    dropzone.classList.remove("has-preview");
    return;
  }

  dropzonePreviewUrl = URL.createObjectURL(files[0]);
  dropzonePreview.src = dropzonePreviewUrl;
  dropzonePreview.hidden = false;
  dropzonePrompt.hidden = true;
  dropzone.classList.add("has-preview");

  if (files.length > 1) {
    fileList.hidden = false;
    Array.from(files).forEach((file) => {
      const chip = document.createElement("span");
      chip.className = "file-chip";

      const name = document.createElement("span");
      name.textContent = file.name;
      chip.appendChild(name);

      fileList.appendChild(chip);
    });
  } else {
    fileList.hidden = true;
  }
};

const setFiles = (files) => {
  const dataTransfer = new DataTransfer();
  Array.from(files)
    .filter((file) => file.type.startsWith("image/"))
    .forEach((file) => dataTransfer.items.add(file));
  imageInput.files = dataTransfer.files;
  renderFileList(imageInput.files);
};

dropzone.addEventListener("click", () => imageInput.click());
dropzone.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    imageInput.click();
  }
});

imageInput.addEventListener("change", () => renderFileList(imageInput.files));

["dragenter", "dragover"].forEach((eventName) => {
  dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.add("dragover");
  });
});

["dragleave", "drop"].forEach((eventName) => {
  dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.remove("dragover");
  });
});

dropzone.addEventListener("drop", (event) => {
  const { files } = event.dataTransfer;
  if (files?.length) {
    setFiles(files);
  }
});

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
