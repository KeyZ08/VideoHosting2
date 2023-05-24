const btnDeleteComment = document.querySelectorAll('.btn-delete-comment');

btnDeleteComment.forEach(btn => {
    btn.addEventListener('click', async (e) => {
        const commentId = e.target.dataset.commentId;
        let res = await fetch(`delete-comment/${commentId}/`, {method: "POST"})
            .then(response => response.json())
        if (res.deleted) {
            console.log(`comment-${commentId}`)
            const commentElem = document.getElementById(`comment-${commentId}`);
            commentElem.remove();
        }
        else{
            console.error("Ошибка")
        }
    });
});