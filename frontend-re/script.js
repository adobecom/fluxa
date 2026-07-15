document.addEventListener('keydown', (event) => {
  if (event.key !== 'F') return;
  (async () => {
    try {
      await document.body.requestFullscreen();
    } catch (e) {
      console.warn('Unable to go full screen', e);
    }
  })();
});

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
const restartButton = document.getElementById("restartButton");

const baseApiUrl = window.FLUXA_API_BASE ?? "http://0.0.0.0:8000";

const mockApply = new URLSearchParams(window.location.search).has("mock");

const MOCK_PREVIEW_BASE64 =
  "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR42mNg+M/A8AEABQAB86WmQQAAAABJRU5ErkJggg==";

const mockApplyResponse = () =>
  new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        pipeline_id: "mock-pipeline-id",
        application: {
          job_id: "mock-job-id",
          output_path: "/tmp/mock/rendered.psd",
          download_url: "/download/mock-job-id",
          preview_path: "/tmp/mock/rendered.png",
        },
        inline_render: {
          filename: "rendered.png",
          content_type: "image/png",
          base64_data: MOCK_PREVIEW_BASE64,
        },
      });
    }, 1200);
  });

let dropzonePreviewUrls = [];

const renderFileList = (files) => {
  dropzonePreviewUrls.forEach((url) => URL.revokeObjectURL(url));
  dropzonePreviewUrls = [];
  dropzonePreview.innerHTML = "";

  if (!files.length) {
    dropzonePreview.hidden = true;
    dropzonePrompt.hidden = false;
    dropzone.classList.remove("has-preview");
    return;
  }

  dropzonePreviewUrls = Array.from(files).map((file) =>
    URL.createObjectURL(file),
  );
  dropzonePreviewUrls.forEach((url, index) => {
    const tile = document.createElement("img");
    tile.className = "dropzone-preview-tile";
    tile.src = url;
    tile.alt = files[index].name;
    dropzonePreview.appendChild(tile);
  });
  dropzonePreview.hidden = false;
  dropzonePrompt.hidden = true;
  dropzone.classList.add("has-preview");
};

const MAX_IMAGES = 2;

const setFiles = (files) => {
  const dataTransfer = new DataTransfer();
  Array.from(files)
    .filter((file) => file.type.startsWith("image/"))
    .slice(0, MAX_IMAGES)
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

imageInput.addEventListener("change", () => {
  if (imageInput.files.length > MAX_IMAGES) {
    setFiles(imageInput.files);
  } else {
    renderFileList(imageInput.files);
  }
});

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

const handleResult = (payload, beforeUrl) => {
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

    if (beforeUrl) {
      const EYE_ICON =
        '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7Z"/><circle cx="12" cy="12" r="3"/></svg>';
      const EYE_OFF_ICON =
        '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.9 4.24A10.94 10.94 0 0 1 12 4c7 0 11 7 11 7a17.5 17.5 0 0 1-3.22 4.06M6.61 6.61C3.9 8.32 2 12 2 12s4 7 11 7a10.9 10.9 0 0 0 5.39-1.61M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="m1 1 22 22"/></svg>';

      const toggleButton = document.createElement("button");
      toggleButton.type = "button";
      toggleButton.className = "before-toggle";
      toggleButton.innerHTML = EYE_ICON;
      toggleButton.setAttribute("aria-label", "Show before image");
      toggleButton.title = "Show before image";

      let showingBefore = false;
      toggleButton.addEventListener("click", () => {
        showingBefore = !showingBefore;
        img.src = showingBefore ? beforeUrl : url;
        toggleButton.innerHTML = showingBefore ? EYE_OFF_ICON : EYE_ICON;
        const label = showingBefore ? "Show after image" : "Show before image";
        toggleButton.setAttribute("aria-label", label);
        toggleButton.title = label;
      });

      wrapper.appendChild(toggleButton);
    }

    const linkRow = document.createElement("div");
    linkRow.className = "links";
    wrapper.appendChild(linkRow);
    gallery.appendChild(wrapper);

    if (application?.download_url) {
      const psdFilename =
        application.output_path?.split("/").pop() ?? "rendered.psd";
      const downloadLink = document.createElement("a");
      downloadLink.className = "pill";
      downloadLink.href = `${baseApiUrl}${application.download_url}`;
      downloadLink.download = psdFilename;
      downloadLink.textContent = "Download PSD";
      linkRow.appendChild(downloadLink);
    }
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

// ---- Styled input dialog (replaces window.prompt) ----
const inputDialog = document.getElementById("inputDialog");
const dialogTitle = document.getElementById("dialogTitle");
const dialogDesc = document.getElementById("dialogDesc");
const dialogInput = document.getElementById("dialogInput");
const dialogCancel = document.getElementById("dialogCancel");
const dialogConfirm = document.getElementById("dialogConfirm");

// Show a modal asking for one value. Resolves to the trimmed string, or null if
// the user cancels (Esc / Cancel / backdrop click). Requires a non-empty value.
const showInputDialog = ({
  title,
  description = "",
  placeholder = "",
  defaultValue = "",
  confirmLabel = "Continue",
}) =>
  new Promise((resolve) => {
    dialogTitle.textContent = title;
    dialogDesc.textContent = description;
    dialogDesc.hidden = !description;
    dialogInput.value = defaultValue;
    dialogInput.placeholder = placeholder;
    dialogConfirm.textContent = confirmLabel;
    inputDialog.hidden = false;
    requestAnimationFrame(() => {
      dialogInput.focus();
      dialogInput.select();
    });

    const cleanup = () => {
      inputDialog.hidden = true;
      dialogConfirm.removeEventListener("click", onConfirm);
      dialogCancel.removeEventListener("click", onCancel);
      dialogInput.removeEventListener("keydown", onKey);
      inputDialog.removeEventListener("mousedown", onBackdrop);
    };
    const finish = (value) => {
      cleanup();
      resolve(value);
    };
    const onConfirm = () => {
      const value = dialogInput.value.trim();
      if (!value) {
        dialogInput.focus();
        return; // require a value
      }
      finish(value);
    };
    const onCancel = () => finish(null);
    const onKey = (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        onConfirm();
      } else if (event.key === "Escape") {
        event.preventDefault();
        onCancel();
      }
    };
    const onBackdrop = (event) => {
      if (event.target === inputDialog) onCancel();
    };

    dialogConfirm.addEventListener("click", onConfirm);
    dialogCancel.addEventListener("click", onCancel);
    dialogInput.addEventListener("keydown", onKey);
    inputDialog.addEventListener("mousedown", onBackdrop);
  });

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const files = imageInput.files;
  if (!files.length || files.length > MAX_IMAGES) {
    alert(`Select 1 or ${MAX_IMAGES} images.`);
    return;
  }

  resetResult();
  setStatus("Uploading images…");
  submitButton.disabled = true;

  try {
    const buildFormData = (extra = {}) => {
      const fd = new FormData();
      fd.append("tutorial_url", tutorialUrlInput.value.trim());
      fd.append("inline_render", "true");
      Array.from(files).forEach((file) => fd.append("images", file, file.name));
      if (extra.glowTarget) fd.append("glow_target", extra.glowTarget);
      if (extra.textContent) fd.append("text_content", extra.textContent);
      return fd;
    };

    const callApply = async (extra = {}) => {
      if (mockApply) return await mockApplyResponse();
      const response = await fetch(`${baseApiUrl}/apply`, {
        method: "POST",
        body: buildFormData(extra),
      });
      if (!response.ok) {
        throw new Error(`Pipeline failed. Status: ${response.status}`);
      }
      return await response.json();
    };

    let payload = await callApply();

    // Glow tutorials: the backend asks which object should glow, then we resubmit.
    if (payload && payload.status === "needs_glow_target") {
      const target = await showInputDialog({
        title: "Which object should glow?",
        description: "This looks like a glow tutorial. Name the object to make glow.",
        placeholder: "e.g. peanut",
        defaultValue: payload.suggested_object || "",
        confirmLabel: "Glow it",
      });
      if (!target) {
        setStatus("Cancelled — no object chosen to glow.");
        submitButton.disabled = false;
        return;
      }
      setStatus(`Making “${target}” glow…`);
      payload = await callApply({ glowTarget: target });
    }

    // Text-embed tutorials: the backend asks for the word to embed, then resubmit.
    if (payload && payload.status === "needs_text") {
      const text = await showInputDialog({
        title: "What text to embed?",
        description:
          "This is a text-behind-subject effect. Enter the word or text to place behind the subject.",
        placeholder: "e.g. DREAM",
        confirmLabel: "Embed text",
      });
      if (!text) {
        setStatus("Cancelled — no text provided.");
        submitButton.disabled = false;
        return;
      }
      setStatus(`Embedding “${text}” behind the subject…`);
      payload = await callApply({ textContent: text });
    }

    // Double-exposure: needs two images (subject + texture). Ask the user to add one.
    if (payload && payload.status === "needs_second_image") {
      alert(payload.message);
      setStatus("Add a second image (subject + texture) and try again.");
      submitButton.disabled = false;
      return;
    }

    setStatus("Processing complete.");
    const beforeUrl = URL.createObjectURL(files[0]);
    handleResult(payload, beforeUrl);
    form.hidden = true;
    statusCard.hidden = true;
  } catch (error) {
    console.error(error);
    setStatus(`Error: ${error.message}`);
  } finally {
    submitButton.disabled = false;
  }
});

restartButton.addEventListener("click", () => {
  form.reset();
  setFiles([]);
  resetResult();
  statusCard.hidden = true;
  form.hidden = false;
});
