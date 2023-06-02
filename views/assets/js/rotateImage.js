const formRotate = document.querySelector("#rotateImage");

formRotate.addEventListener('submit', (e) => {
  e.preventDefault();

  const formImage = new FormData(formRotate);

  fetch('http://127.0.0.1:5000/rotateImage', {
    method: 'POST',
    body: formImage
  })
  .then(response => response.json())
  .then(responseData => {
    const displayImage = document.querySelector("#imageRotated");

    displayImage.src = `data:image/png;base64,${responseData.imgRotated}`;
  })
  .catch(error => {
    console.log(error)
  })
})