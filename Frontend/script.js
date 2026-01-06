const BASE_URL = "http://127.0.0.1:8000/api";

async function uploadResume() {
  const file = document.getElementById("resumeFile").files[0];
  if (!file) return alert("Please select a PDF resume");

  const formData = new FormData();
  formData.append("resume", file);

  const res = await fetch(`${BASE_URL}/upload_resume/`, {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  document.getElementById("resumeText").value = data.resume_text;
}

function showSelectedFile() {
  const input = document.getElementById("resumeFile");
  const fileLabel = document.getElementById("fileLabel");
  const fileName = document.getElementById("fileName");

  if (input.files.length > 0) {
    const file = input.files[0];

    fileLabel.textContent = "✅ File Selected";
    fileName.textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
  } else {
    fileLabel.textContent = "📁 Choose PDF File";
    fileName.textContent = "";
  }
}


async function compareResume() {
  const resumeText = document.getElementById("resumeText").value;
  const jobDesc = document.getElementById("jobDesc").value;

  if (!resumeText || !jobDesc) {
    return alert("Both fields are required");
  }

  const res = await fetch(`${BASE_URL}/compare_resume/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobDesc
    })
  });

  const data = await res.json();

  const percent = data.match_percentage.toFixed(2);
  document.getElementById("progressBar").style.width = percent + "%";
  document.getElementById("resultText").innerText =
    `Resume matches ${percent}% with the Job Description`;
}
