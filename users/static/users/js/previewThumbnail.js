function previewThumbnail(event) {
    const preview = document.getElementById("preview");
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onloadend = function () {
        preview.src = reader.result;
    };

    if (file) {
        reader.readAsDataURL(file);
    } else {
        preview.src = "#";
    }
}
