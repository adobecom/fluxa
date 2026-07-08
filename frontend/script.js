const form = document.getElementById("pipeline-form");
const tutorialUrlInput = document.getElementById("tutorialUrl");
const imageSlots = document.getElementById("imageSlots");
const addImageBtn = document.getElementById("addImageBtn");
const statusCard = document.getElementById("statusCard");
const statusMessage = document.getElementById("statusMessage");
const resultCard = document.getElementById("resultCard");
const resultContent = document.getElementById("resultContent");
const submitButton = document.getElementById("submitButton");

const baseApiUrl = window.FLUXA_API_BASE ?? "http://localhost:8000";
const MAX_SLOTS = 5;

const setStatus = (message) => {
  statusCard.hidden = false;
  statusMessage.textContent = message;
};

const resetResult = () => {
  resultCard.hidden = true;
  resultContent.innerHTML = "";
};

// -------------------------------------------------------------------------
// Image slots: slot 0 = base/subject, slot 1+ = placed images (in order).
// -------------------------------------------------------------------------

const slotLabel = (index) => {
  if (index === 0) return "Image 1 · Base (subject — cut out / edited)";
  return `Image ${index + 1} · Placed on top (backdrop / overlay)`;
};

const refreshSlots = () => {
  const slots = [...imageSlots.querySelectorAll(".image-slot")];
  slots.forEach((slot, index) => {
    slot.dataset.index = String(index);
    slot.querySelector(".slot-label").textContent = slotLabel(index);
    // The first slot cannot be removed.
    slot.querySelector(".remove-slot").hidden = index === 0;
  });
  addImageBtn.disabled = slots.length >= MAX_SLOTS;
};

const createSlot = ({ autoOpen = false } = {}) => {
  const slot = document.createElement("div");
  slot.className = "image-slot";

  const header = document.createElement("div");
  header.className = "slot-header";

  const label = document.createElement("span");
  label.className = "slot-label";
  header.appendChild(label);

  const removeBtn = document.createElement("button");
  removeBtn.type = "button";
  removeBtn.className = "remove-slot";
  removeBtn.textContent = "×";
  removeBtn.title = "Remove this image";
  removeBtn.addEventListener("click", () => {
    slot.remove();
    refreshSlots();
  });
  header.appendChild(removeBtn);
  slot.appendChild(header);

  const input = document.createElement("input");
  input.type = "file";
  input.accept = "image/*";
  input.className = "slot-input";
  slot.appendChild(input);

  const thumb = document.createElement("img");
  thumb.className = "slot-thumb";
  thumb.hidden = true;
  slot.appendChild(thumb);

  input.addEventListener("change", () => {
    const file = input.files?.[0];
    if (file) {
      thumb.src = URL.createObjectURL(file);
      thumb.hidden = false;
    } else {
      thumb.hidden = true;
    }
  });

  imageSlots.appendChild(slot);
  refreshSlots();
  // Open the file picker immediately when the user adds a new slot.
  if (autoOpen) input.click();
  return slot;
};

// Start with a single (base) slot.
createSlot();
addImageBtn.addEventListener("click", () => {
  if (imageSlots.querySelectorAll(".image-slot").length >= MAX_SLOTS) return;
  createSlot({ autoOpen: true });
});

// Collect the chosen files, in slot order, skipping empty slots.
const collectFiles = () => {
  const files = [];
  imageSlots.querySelectorAll(".slot-input").forEach((input) => {
    const file = input.files?.[0];
    if (file) files.push(file);
  });
  return files;
};

// -------------------------------------------------------------------------
// Result rendering with before/after toggle.
// -------------------------------------------------------------------------

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

// Object URL of the original (base) image, captured at submit time.
let originalImageUrl = null;

const handleResult = (payload) => {
  resultCard.hidden = false;
  resultContent.innerHTML = "";

  const gallery = document.createElement("div");
  gallery.className = "gallery";
  resultContent.appendChild(gallery);

  const { application, inline_render: inlineRender } = payload;

  const addPreview = (afterUrl, filename, beforeUrl) => {
    const wrapper = document.createElement("div");
    wrapper.className = "gallery-item";

    const img = document.createElement("img");
    img.src = afterUrl;
    img.alt = filename;
    img.className = "preview";
    wrapper.appendChild(img);

    if (beforeUrl) {
      let showingAfter = true;

      const badge = document.createElement("span");
      badge.className = "view-badge";
      badge.textContent = "After";
      wrapper.appendChild(badge);

      const toggle = document.createElement("button");
      toggle.type = "button";
      toggle.className = "toggle-btn";
      toggle.textContent = "Show Before";
      toggle.addEventListener("click", () => {
        showingAfter = !showingAfter;
        img.src = showingAfter ? afterUrl : beforeUrl;
        badge.textContent = showingAfter ? "After" : "Before";
        toggle.textContent = showingAfter ? "Show Before" : "Show After";
      });
      wrapper.appendChild(toggle);
    }

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
    addPreview(url, inlineRender.filename, originalImageUrl);
  } else if (application?.download_url) {
    const url = `${baseApiUrl}${application.download_url}`;
    const filename =
      application.output_path?.split("/").pop() ?? "rendered.psd";
    addPreview(url, filename, originalImageUrl);
  }
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const files = collectFiles();
  if (!files.length) {
    alert("Add at least the base image (Image 1).");
    return;
  }

  resetResult();
  setStatus("Uploading images…");
  submitButton.disabled = true;

  // Capture the base (first) image so we can toggle before/after.
  if (originalImageUrl) URL.revokeObjectURL(originalImageUrl);
  originalImageUrl = URL.createObjectURL(files[0]);

  try {
    const formData = new FormData();
    formData.append("tutorial_url", tutorialUrlInput.value.trim());
    formData.append("inline_render", "true");
    files.forEach((file) => formData.append("images", file, file.name));

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
