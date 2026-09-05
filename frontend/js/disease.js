requireAuth();

const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const previewWrap = document.getElementById("previewWrap");
const previewImg = document.getElementById("previewImg");
const analyzeBtn = document.getElementById("analyzeBtn");
const uploadError = document.getElementById("uploadError");

let selectedFile = null;

dropzone.addEventListener("click", () => fileInput.click());
dropzone.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") { e.preventDefault(); fileInput.click(); }
});

dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("dragover");
});
dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.classList.remove("dragover");
  if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
});

fileInput.addEventListener("change", () => {
  if (fileInput.files.length) handleFile(fileInput.files[0]);
});

function handleFile(file) {
  uploadError.textContent = "";

  const allowed = ["image/jpeg", "image/png", "image/webp", "image/jpg"];
  if (!allowed.includes(file.type)) {
    uploadError.textContent = "Please upload a JPEG, PNG, or WEBP image.";
    return;
  }
  if (file.size > 8 * 1024 * 1024) {
    uploadError.textContent = "Image is too large. Maximum size is 8MB.";
    return;
  }

  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    previewWrap.classList.add("visible");
  };
  reader.readAsDataURL(file);

  analyzeBtn.disabled = false;

  // Reset any previous result while a new image is staged
  document.getElementById("resultEmpty").style.display = "flex";
  document.getElementById("resultContent").style.display = "none";
}

analyzeBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  document.getElementById("resultEmpty").style.display = "none";
  document.getElementById("resultContent").style.display = "none";
  document.getElementById("resultLoading").style.display = "flex";
  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";

  // Simulated processing delay so the loading state is visible (demo mode)
  await new Promise((resolve) => setTimeout(resolve, 1400));

  const result = await detectDisease(selectedFile);

  document.getElementById("resultLoading").style.display = "none";
  analyzeBtn.disabled = false;
  analyzeBtn.textContent = "Analyze Image";

  if (!result.ok || !result.data) {
    document.getElementById("resultEmpty").style.display = "flex";
    uploadError.textContent = friendlyErrorMessage(result);
    return;
  }

  const d = result.data;

  document.getElementById("diseaseLabel").textContent = d.disease;
  document.getElementById("confidenceValue").textContent = `${d.confidence}% confidence`;
  document.getElementById("confidenceBar").style.width = `${d.confidence}%`;
  document.getElementById("symptomsText").textContent = d.symptoms;
  document.getElementById("treatmentText").textContent = d.treatment;
  document.getElementById("preventionText").textContent = d.prevention;

  document.getElementById("resultContent").style.display = "block";
});
