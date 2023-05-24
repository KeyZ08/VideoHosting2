const video_title = document.getElementById("video-title");
const video_description = document.getElementById("video-description");
const upload_btn = document.getElementById("upload_btn");
const preview = document.getElementById("preview");
const video_thumbnail = document.getElementById("video-thumbnail");
const video_delete = document.getElementById("video_delete");
const video_id = document.getElementById("id_video");

const progress = document.getElementById("progress");
const uploaded = document.getElementById("uploaded");
const result = document.getElementById("result");
const load_img = document.getElementById('spin');
const wait_message = document.getElementById('wait_message');
let MSize = ["B", "KB", "MB", "GB"];

video_delete.addEventListener("click", async () =>{
    let p = confirm("Вы уверены? Все данные будут безвозвратно удалены.")
    if (p){
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '../delete/');
        xhr.onload = () => {
            wait_message.style.display = "none"
            const response = JSON.parse(xhr.responseText);
            answerCheck(response, upload_btn);
            if (!response.error) {
                window.location.replace(response.result.next_url);
            } else {
                console.error(response.error.message);
            }
        }

        xhr.send(null)
    }
})


video_thumbnail.addEventListener("change", async ()=> {
    const file = video_thumbnail.files[0];
    const reader = new FileReader();

    reader.onloadend = function () {
        preview.src = reader.result;
    };

    if (file) {
        let fileAnswer = await fileValid(file).then(f => f.json());
        if (!fileAnswer.error) {
            reader.readAsDataURL(file);
        } else {
            preview.src = "";
        }
        answerCheck(fileAnswer, video_thumbnail);
    } else {
        preview.src = "#";
    }
})


///
async function fileValid(file){
  let fileData = {
      "jsonrpc": "2.0", "id": "0",
      "method": "check_file_valid",
      "params": {
          "file":{
          "name" : file.name,
          "size" : file.size,
          "target" : "video_preview_image"}
      }
  }
  return await window.fetch("/api/jsonrpc/", {
    method: 'POST',
    body: JSON.stringify(fileData)
  });
}

function answerCheck(answer, target){
    dataCheck();
  let el = document.querySelector(`.${target.id}_errorlist`);
  if (el !== null) el.remove();
  if (answer.error){
    let p = document.createElement('p');
    p.className = `${target.id}_errorlist`;
    target.parentElement.insertBefore(p, target.nextElementSibling);
    p.innerHTML = `${ answer.error.message }`;
  }
}
///

upload_btn.addEventListener("click", async ()=>{
    const formData = new FormData();
    formData.append("title", video_title.value);
    formData.append("description", video_description.value);
    formData.append("published", document.getElementById("published").checked);

    if (video_thumbnail.value !== ""){
        formData.append("preview", video_thumbnail.files[0]);
    }


    const xhr = new XMLHttpRequest();
    xhr.open('POST', "");

    xhr.onload = () => {
        load_img.style.display = "none";
        wait_message.style.display = "none"
        result.innerHTML = "";
        const response = JSON.parse(xhr.responseText);
        if (!response.error) {
            result.innerHTML = 'Изменения успешно сохранены';
            video_thumbnail.value = '';
        }
        answerCheck(response, upload_btn);
    };

    xhr.upload.onprogress = function(event) {
      progress.setAttribute('max', 100);
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
      progress.value = (size / sizeTotal * 100).toFixed(0)
    }

    xhr.onloadstart = function () {
        wait_message.style.display = "block";
        load_img.style.display = "flex";
        result.innerHTML = "";
    }

    if (dataCheck()) {
        console.log("send")
        xhr.send(formData);
    }
    else {
        console.log("notsend")
    }
})

function dataCheck(){
    let el = document.querySelectorAll('.exception');
    if (el.length > 0) {
        for (let i = el.length-1; i >= 0; i--) {
            el[i].remove();
        }
    }
    video_title.value = video_title.value.trim();
    let title = video_title.value;
    video_description.value = video_description.value.trim();
    let description = video_description.value

    if (title.length < 5) exception("Минимум 5 символов.", video_title);
    if (title.length > 100) exception("Максимум 100 символов.", video_title);
    if (description.length > 3000) exception("Максимум 3000 символов.", video_description);

    if (title.length < 5 || title.length > 100 || description.length > 3000)
    {
        console.log(false)
        return false;
    }
    else return true
}

function exception(message, target){
    let p = document.createElement('p');
    p.className = 'exception';
    target.parentElement.insertBefore(p, target.nextElementSibling);
    p.innerHTML = message;
}
