const avatarBtnChange = document.getElementById('change-avatar-btn');
const avatarBtnReset = document.getElementById('reset-avatar-btn');
const avatarBtnSave = document.getElementById('save-avatar-btn');

const avatarImg = document.getElementById('avatar_img');
const message = document.getElementsByClassName('content-sec')[0];

let input;

avatarBtnChange.addEventListener('click', () => {
    input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    // Открыть диалог выбора файла
    input.addEventListener('change',  async () => {
         messageDelete();
        let fileAnswer = await fileValid(input.files[0]).then(f => f.json());
         if (!fileAnswer.error) {
             preview(input.files[0]);
         }
         else {
            answerCheck(fileAnswer, "");
         }
    });
    input.click();
});

avatarBtnReset.addEventListener('click', async ()=>{
    messageDelete();

    const xhr = new XMLHttpRequest();
    xhr.responseType = "json"
    xhr.open('POST', 'avatar_reset/');
    xhr.onload = () => {
        // Обновить аватар на странице при получении ответа от сервера
        const response = xhr.response
        answerCheck(response, "Аватар учтановлен по умолчанию.");
        if (!response.error) {
            avatarImg.src = response.result.url;
        } else {
            console.error(response.error.message);
        }
    };
    xhr.send(null);
});

avatarBtnSave.addEventListener('click', async ()=>{
    messageDelete();
    if(input.files[0]) {
        upload_to_server(input.files[0]);
    }
});

function answerCheck(answer, successMessage){
  if (answer.error){
    let ul = document.createElement('ul');
    ul.className = "errorlist";
    let li = document.createElement("li")
    message.insertBefore(ul, message.childNodes[0]);
    ul.append(li)
    li.innerHTML = `${ answer.error.message }`;
  }
  else{
    let ul = document.createElement('ul');
    ul.className = "success";
    let li = document.createElement("li")
    message.insertBefore(ul, message.childNodes[0]);
    ul.append(li)
    li.innerHTML = successMessage;
  }
}

async function fileValid(file){
  let fileData = {
      "jsonrpc": "2.0", "id": "0",
      "method": "check_file_valid",
      "params":{
          "file":{
          "name" : file.name,
          "size" : file.size,
          "target" : "avatar_image"}
      }
  }
  return await window.fetch("/api/jsonrpc/", {
    method: 'POST',
    body: JSON.stringify(fileData)
  });
}

function upload_to_server(file){
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'avatar_upload/');
    xhr.onload = () => {
        // Обновить аватар на странице при получении ответа от сервера
        const response = JSON.parse(xhr.responseText);
        answerCheck(response, "Файл успешно сохранен.");
        if (!response.error) {
            avatarImg.src = response.result.url;
        } else {
            console.error(response.error.message);
        }
    };
    xhr.send(file);
}

function preview(file){
    // Создаем объект FileReader для загрузки файла
    const reader = new FileReader();

    // Назначаем обработчик событий для загрузки файла
    reader.addEventListener('load', function() {
      // Отображаем загруженное изображение на странице
      avatarImg.src = reader.result;
    });

    // Загружаем файл
    reader.readAsDataURL(file);
}

function messageDelete(){
    let el = document.querySelector('.errorlist');
    if (el !== null) el.remove();
    el = document.querySelector('.success');
    if (el !== null) el.remove();
}