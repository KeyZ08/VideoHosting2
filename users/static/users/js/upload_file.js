const progress = document.getElementById("progress");
const uploaded = document.getElementById("uploaded");
const result = document.getElementById("result");
const load_img = document.getElementById('spin');
const wait_message = document.getElementById('wait_message');
let MSize = ["B", "KB", "MB", "GB"];
let task_id;
let task_progress = 0;
let file_progress = 0;
let nullCountProgress = 0;

uploadForm.addEventListener("submit", async function (event) {
  event.preventDefault();
  const file = event.target.elements.file.files[0];
  let fileAnswer = await fileValid(file).then(f => f.json());

  let el = document.querySelector('.alertStatusError');
    if (el !== null) el.remove();
    el = document.querySelector('.alertStatusOk');
    if (el !== null) el.remove();

  if (fileAnswer.status === "ok") {
    await upload_to_server();
  }
  else {
    answerCheck(fileAnswer);
  }
});

async function upload_to_server() {
    progress.setAttribute('max', 100);
  let ajax = new XMLHttpRequest();
  ajax.upload.onprogress = function(event) {
      let level = 0;
      let sizeTotal = event.total
      while (sizeTotal > 1024.0 && level <= MSize.length - 1){
        sizeTotal /= 1024.0;
        level += 1;
      }
      sizeTotal = sizeTotal.toFixed(1);
      let size = event.loaded;
      let l = level;
      while (l > 0){
        size /= 1024.0;
        l -= 1;
      }
      size = size.toFixed(1);
      uploaded.innerHTML = 'Загружено ' + size + ' из ' + sizeTotal + MSize[level];
      file_progress = (size / sizeTotal * 100).toFixed(0)
      progress.value = (file_progress / 2 + task_progress / 2).toFixed(0);
  }

  ajax.onloadstart = function () {
    wait_message.style.display = "block";
    load_img.style.display = "block";
    result.innerHTML = "";
  }

  ajax.onload = ajax.onerror = function() {
    if (this.status === 200) {
        wait_message.style.display = "none";
        result.innerHTML = 'Файл успешно загружен';
    } else {
        wait_message.style.display = "none";
        load_img.style.display = "none";
        result.innerHTML = 'Не удалось загрузить файл';
    }

    console.log(ajax.responseText);
    answerCheck(JSON.parse(ajax.responseText));
    load_img.style.display = "none";
    result.innerHTML = "";
  }
  let formData = new FormData(uploadForm);
  task_id = uuidv4();
  formData.append("task_id", task_id)

  ajax.open("POST", "", true);
  await ajax.send(formData);
  await updateProgress(task_id)
  return ajax.responseText;
}

async function updateProgress (task_id) {
    let fileData = {
    "method": "check_progress",
    "task_id": task_id
  }
    let res = await fetch("../api/", {
        method: 'POST',
        body: JSON.stringify(fileData)}
    ).then(response => response.json())

    if (res["progress"] < 100 && res["progress"] >= task_progress && nullCountProgress < 20) {
        setTimeout(updateProgress, 5000, "../api/");
    }
    task_progress = res["progress"];
    if (task_progress === 0) nullCountProgress +=1;
    progress.value = (file_progress / 2 + task_progress / 2).toFixed(0);
}

function answerCheck(answer){
  if (answer.status === "ok"){
    let div = document.createElement('div');
    div.className = "alertStatusOk";
    div.innerHTML = "<strong>Файл успешно сохранен.</strong>";
    uploadForm.before(div);
  }
  else {
    let div = document.createElement('div');
    div.className = "alertStatusError";
    div.innerHTML = `<strong>${ answer.error }</strong>`;
    uploadForm.before(div);
  }
}

async function fileValid(file){
  let fileData = {
    "method": "check_file_valid",
    "file":{
      "name" : file.name,
      "size" : file.size,
      "type" : file.type
    }
  }
  return await window.fetch("../api/", {
    method: 'POST',
    body: JSON.stringify(fileData)
  });
}

function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        let r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}