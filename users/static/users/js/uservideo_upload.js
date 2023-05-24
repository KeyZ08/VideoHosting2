upload_button = document.getElementById("upload-button")
video_input = document.getElementById("video-input")

const progress = document.getElementById("progress");
const uploaded = document.getElementById("uploaded");
const result = document.getElementById("result");
const load_img = document.getElementById('spin');
const wait_message = document.getElementById('wait_message');
let MSize = ["B", "KB", "MB", "GB"];

upload_button.addEventListener("click", async ()=>{
  if(!video_input.files[0]) {
    alert("Выбирите файл!")
    return;
  }
  let res = await video_upload_module.fileValid(video_input.files[0]).then(f => f.json())
    console.log(res)
  if(!res.error){
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'video_upload/');
    xhr.onload = () => {
        load_img.style.display = "none";
        wait_message.style.display = "none";
        result.innerHTML = "";
        const response = JSON.parse(xhr.responseText);
        if (!response.error) {
            window.location.replace(response.result.next_url);
            result.innerHTML = 'Файл успешно загружен';
        }
        video_upload_module.answerCheck(response, upload_button);
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

    xhr.onerror = function (){
      load_img.style.display = "none";
      wait_message.style.display = "none";
      result.innerHTML = "Похоже потеряна связь сервером, либо возникла непредвиденная ошибка:(";
    }

    xhr.send(video_input.files[0])
  }else {
    video_upload_module.answerCheck(res, upload_button)
  }
})

$(document).ready(function() {
  $('#video_create').click(function() {
    $('#upload-modal').fadeIn();
  });

  $('#upload-modal').click(function(event) {
    if (event.target == this) {
      $(this).fadeOut();
    }
  });
});

video_upload_module = {}

video_upload_module.answerCheck = function answerCheck(answer, target){
    let el = document.querySelector(`.errorlist`);
    if (el !== null) el.remove();
    if (answer.error){
      let ul = document.createElement('ul');
      ul.className = `errorlist`;
      let li = document.createElement('li');
      ul.append(li)
      target.parentElement.insertBefore(ul, target);
      li.innerHTML = `${ answer.error.message }`;
    }
  }

video_upload_module.fileValid = async function fileValid(file){
  let fileData = {
      "jsonrpc": "2.0", "id": "0",
      "method": "check_file_valid",
      "params": {
          "file":{
          "name" : file.name,
          "size" : file.size,
          "target" : "video"}
      }
  }
  return await window.fetch("../api/jsonrpc/", {
    method: 'POST',
    body: JSON.stringify(fileData)
  });
}
