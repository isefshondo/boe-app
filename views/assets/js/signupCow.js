const signupCowForm = document.querySelector("#signupCowForm");

signupCowForm.addEventListener('submit', (e) => {
  e.preventDefault();

  const formData = new FormData(signupCowForm);

  fetch('http://127.0.0.1:5000/signupCow/646e262baf4d3a798c8fc944', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    console.log(data, "Vai lá ver se enviou");
  })
  .catch(error => {
    console.log(error);
  })
});


// Display results to Sign Up

function displayData(tempIdCow, results) {
  const showPercentage = document.querySelector('#displayChances');
  const showIdCow = document.querySelector('#idCow');
  
  showPercentage.textContent = results + "%";
  showIdCow.value = tempIdCow;
}

fetch('http://127.0.0.1:5000/signupCow/646e262baf4d3a798c8fc944', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(responseData => {
  const results = responseData.results;
  const tempIdCow = responseData.tempIdCow;

  displayData(tempIdCow, results);

  console.log(responseData)
})
.catch(error => {
  console.log(error)
})