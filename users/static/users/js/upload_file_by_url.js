uploadForm.addEventListener("submit", async function (event) {
  event.preventDefault();
  const file = event.target.elements.file.files[0];
  const presignedPost = await requestPresignedPost(file);
  console.log(presignedPost);
  uploadFile(file, presignedPost);
});

async function requestPresignedPost(file) {
  const name = file.name;
  const type = file.type;
  const size = file.size;
  const res = await window.fetch("http://127.0.0.1:8000/file_load/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name, type, size
    }),
  });
  return res.json();
}

function uploadFile(file, presignedPost) {
  const reader = new FileReader();
  reader.readAsArrayBuffer(file);
  reader.addEventListener('load', (e) => {
    console.log(e.target.result);
    upload(e.target.result, presignedPost);
  });
}

async function upload(file, presignedPost) {
  const res = await window.fetch(presignedPost.url, {
    method: "PUT",
    body: file,
  });
}