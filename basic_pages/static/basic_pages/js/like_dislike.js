const likeButton = document.getElementById('like-button');
const dislikeButton = document.getElementById('dislike-button');
const likeCount = document.getElementById('like-count');
const dislikeCount = document.getElementById('dislike-count');
const id_video = document.getElementById('id_video').textContent;


dislikeButton.addEventListener('click', async () => {
   await Request("dislike");
})

likeButton.addEventListener('click', async () => {
  await Request("like");
});

function SetValues(request){
  if (request.liked)
    likeButton.classList.add('liked');
  else likeButton.classList.remove('liked');
  if (request.disliked)
    dislikeButton.classList.add('liked');
  else dislikeButton.classList.remove('liked');
  likeCount.textContent = request.likes_count
  dislikeCount.textContent = request.dislikes_count
  console.log(request)
}

function Request(like_or_dislike){
  const xhr = new XMLHttpRequest();
  xhr.open('POST', `${like_or_dislike}/`);
  xhr.responseType = 'json';
  xhr.onload = () => {
      const response = xhr.response.result;
      if (response.status === "ok")
        SetValues(response)
      else alert(response.error)
  };
  xhr.onerror = () => console.error(xhr.statusText);

  xhr.send(null);
}

